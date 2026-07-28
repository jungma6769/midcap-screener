"""
Backtest: does the formula stack actually separate future bankruptcies
from future compounders, using their REAL financials from before the
outcome was known?

Data sources / notes on accuracy:
  - Bankrupt-company figures are sourced from contemporaneous reporting
    (10-Ks, CNBC, Forbes, CNN, Motley Fool -- see comments per company)
    at a snapshot roughly 1-2 years BEFORE the actual Chapter 11 filing.
  - Successful-company figures are order-of-magnitude estimates from
    financial history at a point when each company was still mid-cap,
    reconstructed from memory rather than pulled filing-by-filing --
    treat these as directionally correct, not audit-grade.
  - This is a sanity check on the formula's LOGIC (does it penalize the
    right things), not a rigorous historical backtest with point-in-time
    consensus estimates for g, beta, VIX, etc. Macro inputs (VIX, risk-free
    rate) are held at reasonable historical averages for simplicity.

Run:
    python backtest.py
"""

import math

# Reuse the exact same formula implementations as the live screener
from stock_screener import (
    formula1_cost_of_equity, formula2_growth_governor, formula3_atsv,
    formula4_factor_score, formula5_final_score, formula6_quality_size_overlay,
    combine_final_and_quality,
    ERP, G_MACRO, T_D,
)
import numpy as np

RF = 0.025      # long-run-ish average risk-free rate across these snapshots
VIX = 20.0      # long-run-ish average VIX

TARGET_MARKET_CAP_B = 6.0
SIZE_SIGMA = 0.8
MAX_DEBT_TO_EQUITY = 0.8
MIN_FCF_YIELD = 0.025

# ============================================================
# CASE DATA
# ============================================================
# fields: market_cap_b, ev_b, beta, total_debt_b, total_cash_b, fcf_b,
#         revenue_b, op_margin, revenue_growth, capex_b, depr_b, debt_to_equity

CASES = {
    # ---------------- WENT BANKRUPT ----------------
    "Sears Holdings (2016, ~2yr pre-Ch.11 Oct'18)": dict(
        group="bankrupt",
        market_cap_b=2.8, ev_b=6.3, beta=1.9,
        total_debt_b=3.5, total_cash_b=0.25,
        fcf_b=-1.5,                      # Moody's-cited operating cash flow loss
        revenue_b=22.1, op_margin=-0.03, revenue_growth=-0.10,
        capex_b=0.25, depr_b=0.45,       # under-investing while still depreciating
        debt_to_equity=3.5,              # equity was near zero/negative -> treat as very high
    ),
    "J.C. Penney (2018, ~1.5yr pre-Ch.11 May'20)": dict(
        group="bankrupt",
        market_cap_b=0.9, ev_b=4.9, beta=2.1,
        total_debt_b=4.0, total_cash_b=0.55,
        fcf_b=-0.10,
        revenue_b=11.66, op_margin=0.02, revenue_growth=-0.02,
        capex_b=0.30, depr_b=0.42,
        debt_to_equity=2.2,
    ),
    "Bed Bath & Beyond (mid-2022, ~9mo pre-Ch.11 Apr'23)": dict(
        group="bankrupt",
        market_cap_b=1.5, ev_b=4.3, beta=2.0,
        total_debt_b=3.5, total_cash_b=0.30,
        fcf_b=-1.30,                     # ~$325M/quarter burn annualized
        revenue_b=7.9, op_margin=-0.05, revenue_growth=-0.25,
        capex_b=0.15, depr_b=0.20,
        debt_to_equity=3.0,              # negative equity in filing -> treat as very high
    ),

    # ---------------- WENT ON TO COMPOUND ----------------
    "AAON (2015, was mid-cap)": dict(
        group="compounder",
        market_cap_b=1.8, ev_b=1.8, beta=1.0,
        total_debt_b=0.0, total_cash_b=0.04,
        fcf_b=0.06,
        revenue_b=0.40, op_margin=0.14, revenue_growth=0.07,
        capex_b=0.04, depr_b=0.02,
        debt_to_equity=0.0,
    ),
    "Copart (2012, was mid-cap)": dict(
        group="compounder",
        market_cap_b=3.0, ev_b=3.3, beta=0.9,
        total_debt_b=0.35, total_cash_b=0.05,
        fcf_b=0.15,
        revenue_b=0.80, op_margin=0.30, revenue_growth=0.10,
        capex_b=0.12, depr_b=0.06,
        debt_to_equity=0.15,
    ),
    "Old Dominion Freight Line (2012, was mid-cap)": dict(
        group="compounder",
        market_cap_b=3.1, ev_b=3.3, beta=1.1,
        total_debt_b=0.20, total_cash_b=0.02,
        fcf_b=0.09,
        revenue_b=1.82, op_margin=0.12, revenue_growth=0.15,
        capex_b=0.25, depr_b=0.11,
        debt_to_equity=0.10,
    ),
    "Monster Beverage (2010, was mid-cap)": dict(
        group="compounder",
        market_cap_b=3.2, ev_b=3.0, beta=1.0,
        total_debt_b=0.0, total_cash_b=0.30,
        fcf_b=0.16,
        revenue_b=1.30, op_margin=0.20, revenue_growth=0.20,
        capex_b=0.02, depr_b=0.01,
        debt_to_equity=0.0,
    ),
}


def run_case(name, c):
    r = formula1_cost_of_equity(RF, c["beta"], ERP, c["ev_b"], c["market_cap_b"], VIX)
    g = formula2_growth_governor(c["revenue_growth"], r, G_MACRO,
                                  c["capex_b"], c["depr_b"], c["op_margin"])
    atsv = formula3_atsv(c["fcf_b"], c["market_cap_b"], r, g)
    net_debt = max(0.0, c["total_debt_b"] - c["total_cash_b"])
    fcf_yield = c["fcf_b"] / c["market_cap_b"]
    return {"name": name, "group": c["group"], "r": r, "g": g, "atsv": atsv,
            "net_debt_b": net_debt, "fcf_yield": fcf_yield, **c}


def main():
    rows = [run_case(name, c) for name, c in CASES.items()]

    atsv_vals = np.array([row["atsv"] for row in rows])
    factor_scores = formula4_factor_score(atsv_vals, np.full(len(rows), 0.5))  # neutral industry PR at this sample size

    for row, fscore in zip(rows, factor_scores):
        row["factor_score"] = fscore
        row["final_score"] = formula5_final_score(
            fscore, row["total_cash_b"], row["fcf_b"], VIX, row["op_margin"], row["net_debt_b"], T_D
        )
        overlay, size_s, debt_s, fcf_s = formula6_quality_size_overlay(
            row["market_cap_b"], row["debt_to_equity"], row["fcf_yield"],
            TARGET_MARKET_CAP_B, SIZE_SIGMA, MAX_DEBT_TO_EQUITY, MIN_FCF_YIELD
        )
        row["size_score"] = size_s
        row["debt_score"] = debt_s
        row["fcf_score"] = fcf_s
        row["quality_overlay"] = overlay
        row["combined_score"] = combine_final_and_quality(row["final_score"], overlay)

    rows.sort(key=lambda x: x["combined_score"], reverse=True)

    print(f"{'Company':46} {'Group':11} {'D/E':>6} {'FCFyld':>8} {'R':>7} {'G':>7} "
          f"{'ATSV':>7} {'Final':>8} {'DebtScr':>8} {'FCFScr':>7} {'SizeScr':>8} {'Combined':>10}")
    print("-" * 148)
    for row in rows:
        print(f"{row['name']:46} {row['group']:11} {row['debt_to_equity']:6.2f} "
              f"{row['fcf_yield']*100:7.1f}% {row['r']*100:6.1f}% {row['g']*100:6.1f}% "
              f"{row['atsv']:7.2f} {row['final_score']:8.4f} {row['debt_score']:8.3f} "
              f"{row['fcf_score']:7.3f} {row['size_score']:8.3f} {row['combined_score']:10.4f}")

    bankrupt_scores = [r["combined_score"] for r in rows if r["group"] == "bankrupt"]
    compounder_scores = [r["combined_score"] for r in rows if r["group"] == "compounder"]
    print("\n--- Summary ---")
    print(f"Bankrupt group   combined_score:  mean={np.mean(bankrupt_scores):.4f}  "
          f"min={min(bankrupt_scores):.4f}  max={max(bankrupt_scores):.4f}")
    print(f"Compounder group combined_score:  mean={np.mean(compounder_scores):.4f}  "
          f"min={min(compounder_scores):.4f}  max={max(compounder_scores):.4f}")
    separation = min(compounder_scores) - max(bankrupt_scores)
    print(f"Separation (min compounder - max bankrupt): {separation:.4f} "
          f"{'(clean separation)' if separation > 0 else '(OVERLAP -- see notes below)'}")


if __name__ == "__main__":
    main()
