"""
Custom Quant Screener
======================
Pulls fundamental + market data from Yahoo Finance (via yfinance) and runs it
through a 6-formula pipeline that scores stocks, with a bias toward
small/mid-cap companies carrying low debt and strong free cash flow.

Install requirements:
    pip install yfinance pandas numpy

Run:
    python stock_screener.py

Edit the CONFIG block below to change your ticker universe and assumptions.
"""

import math
import numpy as np
import pandas as pd

# ============================================================
# CONFIG — tune these to your taste
# ============================================================

# Full S&P MidCap 400 constituent list (pulled from Wikipedia, current as of this build).
# This IS the standard mid-cap universe -- combined with the $2B-$10B size overlay below,
# it naturally narrows toward your target band without you having to hand-pick names.
# Note: index composition changes periodically (S&P adds/removes names as caps shift),
# so re-pull this list occasionally if you want it fully current.
# Combined S&P 500 (large-cap) + S&P 400 (mid-cap) universe, 903 unique tickers.
# Pulled from Wikipedia; broadened at the user's request for maximum coverage.
# Formula 6's size overlay still steers rankings toward the $6B goldilocks zone,
# so large-caps aren't excluded, just naturally down-weighted unless they're a
# great fit on debt/FCF grounds too.
TICKERS = [
    "A", "AA", "AAL", "AAON", "AAPL", "ABBV", "ABNB", "ABT",
    "ACGL", "ACI", "ACM", "ACN", "ADBE", "ADC", "ADI", "ADM",
    "ADP", "ADSK", "AEE", "AEIS", "AEP", "AES", "AFG", "AFL",
    "AGCO", "AHR", "AIG", "AIT", "AIZ", "AJG", "AKAM", "ALB",
    "ALGM", "ALGN", "ALK", "ALL", "ALLE", "ALLY", "ALV", "AM",
    "AMAT", "AMCR", "AMD", "AME", "AMG", "AMGN", "AMH", "AMKR",
    "AMP", "AMT", "AMZN", "AN", "ANET", "ANF", "AON", "AOS",
    "APA", "APD", "APG", "APH", "APO", "APP", "APPF", "APTV",
    "AR", "ARE", "ARES", "ARMK", "ARW", "ARWR", "ASB", "ASH",
    "ATI", "ATO", "ATR", "AVAV", "AVB", "AVGO", "AVNT", "AVT",
    "AVTR", "AVY", "AWK", "AXON", "AXP", "AXTA", "AYI", "AZO",
    "BA", "BAC", "BAH", "BALL", "BAX", "BBWI", "BBY", "BC",
    "BCO", "BDC", "BDX", "BEN", "BF-B", "BG", "BHF", "BIIB",
    "BILL", "BIO", "BJ", "BKH", "BKNG", "BKR", "BLD", "BLDR",
    "BLK", "BLKB", "BMRN", "BMY", "BNY", "BR", "BRBR", "BRK-B",
    "BRKR", "BRO", "BROS", "BRX", "BSX", "BSY", "BURL", "BWA",
    "BWXT", "BX", "BXP", "BYD", "C", "CACI", "CAG", "CAH",
    "CAR", "CARR", "CART", "CASY", "CAT", "CAVA", "CB", "CBOE",
    "CBRE", "CBSH", "CBT", "CCI", "CCK", "CCL", "CDNS", "CDP",
    "CDW", "CEG", "CELH", "CF", "CFG", "CFR", "CG", "CGNX",
    "CHD", "CHDN", "CHE", "CHH", "CHRD", "CHRW", "CHTR", "CHWY",
    "CI", "CIEN", "CINF", "CL", "CLF", "CLH", "CLX", "CMC",
    "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNH", "CNM",
    "CNO", "CNP", "CNX", "CNXC", "COF", "COHR", "COIN", "COKE",
    "COLB", "COLM", "COO", "COP", "COR", "COST", "COTY", "CPAY",
    "CPB", "CPRI", "CPRT", "CPT", "CR", "CRBG", "CRH", "CRL",
    "CRM", "CROX", "CRS", "CRUS", "CRWD", "CSCO", "CSGP", "CSL",
    "CSX", "CTAS", "CTRE", "CTSH", "CTVA", "CUBE", "CUZ", "CVLT",
    "CVNA", "CVS", "CVX", "CW", "CXT", "CYTK", "D", "DAL",
    "DAR", "DASH", "DBX", "DCI", "DD", "DDOG", "DE", "DECK",
    "DELL", "DG", "DGX", "DHI", "DHR", "DINO", "DIS", "DKS",
    "DLB", "DLR", "DLTR", "DOC", "DOCN", "DOCS", "DOCU", "DOV",
    "DOW", "DPZ", "DRI", "DT", "DTE", "DTM", "DUK", "DUOL",
    "DVA", "DVN", "DXCM", "DY", "EA", "EBAY", "ECL", "ED",
    "EEFT", "EFX", "EG", "EGP", "EHC", "EIX", "EL", "ELAN",
    "ELF", "ELS", "ELV", "EME", "EMR", "ENS", "ENSG", "ENTG",
    "EOG", "EPAM", "EPR", "EQH", "EQIX", "EQR", "EQT", "ERIE",
    "ES", "ESAB", "ESNT", "ESS", "ETN", "ETR", "EVR", "EVRG",
    "EW", "EWBC", "EXC", "EXE", "EXEL", "EXLS", "EXP", "EXPD",
    "EXPE", "EXPO", "EXR", "F", "FAF", "FANG", "FAST", "FBIN",
    "FCFS", "FCN", "FCX", "FDS", "FDX", "FE", "FFIN", "FFIV",
    "FHI", "FHN", "FICO", "FIS", "FISV", "FITB", "FIVE", "FIX",
    "FLEX", "FLG", "FLO", "FLR", "FLS", "FN", "FNB", "FND",
    "FNF", "FOUR", "FOX", "FOXA", "FR", "FRT", "FSLR", "FTI",
    "FTNT", "FTV", "G", "GAP", "GATX", "GBCI", "GD", "GDDY",
    "GE", "GEF", "GEHC", "GEN", "GEV", "GGG", "GHC", "GILD",
    "GIS", "GL", "GLPI", "GLW", "GM", "GME", "GMED", "GNRC",
    "GNTX", "GOOG", "GOOGL", "GPC", "GPK", "GPN", "GRMN", "GS",
    "GT", "GTLS", "GWRE", "GWW", "GXO", "H", "HAE", "HAL",
    "HALO", "HAS", "HBAN", "HCA", "HD", "HGV", "HIG", "HII",
    "HIMS", "HL", "HLI", "HLNE", "HLT", "HOG", "HOMB", "HON",
    "HOOD", "HPE", "HPQ", "HQY", "HR", "HRB", "HRL", "HSIC",
    "HST", "HSY", "HUBB", "HUM", "HWC", "HWM", "HXL", "IBKR",
    "IBM", "IBOC", "ICE", "IDA", "IDCC", "IDXX", "IEX", "IFF",
    "ILMN", "INCY", "INGR", "INTC", "INTU", "INVH", "IP", "IPGP",
    "IQV", "IR", "IRM", "IRT", "ISRG", "IT", "ITT", "ITW",
    "IVZ", "J", "JAZZ", "JBHT", "JBL", "JCI", "JEF", "JHG",
    "JKHY", "JLL", "JNJ", "JPM", "KBH", "KBR", "KD", "KDP",
    "KEX", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC", "KMB",
    "KMI", "KNF", "KNSL", "KNX", "KO", "KR", "KRC", "KRG",
    "KTOS", "KVUE", "L", "LAD", "LAMR", "LDOS", "LEA", "LECO",
    "LEN", "LFUS", "LH", "LHX", "LII", "LIN", "LITE", "LIVN",
    "LLY", "LMT", "LNT", "LNTH", "LOPE", "LOW", "LPX", "LRCX",
    "LSCC", "LSTR", "LULU", "LUV", "LVS", "LYB", "LYV", "M",
    "MA", "MAA", "MANH", "MAR", "MAS", "MASI", "MAT", "MCD",
    "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MEDP", "MET", "META",
    "MGM", "MIDD", "MKC", "MKSI", "MLI", "MLM", "MMC", "MMM",
    "MMS", "MNST", "MO", "MOG-A", "MORN", "MOS", "MP", "MPC",
    "MPWR", "MRK", "MRNA", "MS", "MSA", "MSCI", "MSFT", "MSI",
    "MSM", "MTB", "MTD", "MTDR", "MTG", "MTN", "MTSI", "MTZ",
    "MU", "MUR", "MUSA", "MZTI", "NBIX", "NCLH", "NDAQ", "NDSN",
    "NEE", "NEM", "NEU", "NFG", "NFLX", "NI", "NJR", "NKE",
    "NLY", "NNN", "NOC", "NOV", "NOVT", "NOW", "NRG", "NSA",
    "NSC", "NTAP", "NTNX", "NTRS", "NUE", "NVDA", "NVR", "NVST",
    "NVT", "NWE", "NWS", "NWSA", "NXPI", "NXST", "NXT", "NYT",
    "O", "OC", "ODFL", "OGE", "OGS", "OHI", "OKE", "OKTA",
    "OLED", "OLLI", "OLN", "OMC", "ON", "ONB", "ONTO", "OPCH",
    "ORA", "ORCL", "ORI", "ORLY", "OSK", "OTIS", "OVV", "OXY",
    "OZK", "PAG", "PANW", "PATH", "PAYX", "PB", "PBF", "PCAR",
    "PCG", "PCTY", "PEG", "PEGA", "PEN", "PEP", "PFE", "PFG",
    "PFGC", "PG", "PGR", "PH", "PHM", "PII", "PINS", "PK",
    "PKG", "PLD", "PLNT", "PLTR", "PM", "PNC", "PNFP", "PNR",
    "PNW", "PODD", "POOL", "POR", "POST", "PPC", "PPG", "PPL",
    "PR", "PRI", "PRU", "PSA", "PSKY", "PSN", "PSTG", "PSX",
    "PTC", "PVH", "PWR", "PYPL", "Q", "QCOM", "QLYS", "R",
    "RBA", "RBC", "RCL", "REG", "REGN", "REXR", "RF", "RGA",
    "RGEN", "RGLD", "RH", "RJF", "RL", "RLI", "RMBS", "RMD",
    "RNR", "ROIV", "ROK", "ROL", "ROP", "ROST", "RPM", "RRC",
    "RRX", "RS", "RSG", "RTX", "RVTY", "RYAN", "RYN", "SAIA",
    "SAIC", "SAM", "SARO", "SATS", "SBAC", "SBRA", "SBUX", "SCHW",
    "SCI", "SEIC", "SF", "SFM", "SGI", "SHC", "SHW", "SIGI",
    "SITM", "SJM", "SLAB", "SLB", "SLGN", "SLM", "SMCI", "SMG",
    "SNA", "SNDK", "SNPS", "SNX", "SO", "SOLS", "SOLV", "SON",
    "SPG", "SPGI", "SPXC", "SR", "SRE", "SSB", "SSD", "ST",
    "STAG", "STE", "STLD", "STRL", "STT", "STWD", "STX", "STZ",
    "SW", "SWK", "SWKS", "SWX", "SYF", "SYK", "SYNA", "SYY",
    "T", "TAP", "TCBI", "TDG", "TDY", "TECH", "TEL", "TER",
    "TEX", "TFC", "TGT", "THC", "THG", "THO", "TJX", "TKO",
    "TKR", "TLN", "TMHC", "TMO", "TMUS", "TNL", "TOL", "TPL",
    "TPR", "TREX", "TRGP", "TRMB", "TROW", "TRU", "TRV", "TSCO",
    "TSLA", "TSN", "TT", "TTC", "TTD", "TTEK", "TTMI", "TTWO",
    "TWLO", "TXN", "TXNM", "TXRH", "TXT", "TYL", "UAL", "UBER",
    "UBSI", "UDR", "UFPI", "UGI", "UHS", "ULS", "ULTA", "UMBF",
    "UNH", "UNM", "UNP", "UPS", "URI", "USB", "USFD", "UTHR",
    "V", "VAL", "VC", "VEEV", "VFC", "VICI", "VICR", "VLO",
    "VLTO", "VLY", "VMC", "VMI", "VNO", "VNOM", "VNT", "VOYA",
    "VRSK", "VRSN", "VRT", "VRTX", "VST", "VTR", "VTRS", "VVV",
    "VZ", "WAB", "WAL", "WAT", "WBD", "WBS", "WCC", "WDAY",
    "WDC", "WEC", "WELL", "WEX", "WFC", "WFRD", "WH", "WHR",
    "WING", "WLK", "WM", "WMB", "WMG", "WMS", "WMT", "WPC",
    "WRB", "WSM", "WSO", "WST", "WTFC", "WTRG", "WTS", "WTW",
    "WWD", "WY", "WYNN", "XEL", "XOM", "XPO", "XRAY", "XYL",
    "XYZ", "YETI", "YUM", "ZBH", "ZBRA", "ZION", "ZTS",
]

# --- Macro / market assumptions (used if not fetchable) ---
DEFAULT_RISK_FREE = 0.043       # fallback risk-free rate (10Y UST), decimal
DEFAULT_VIX = 16.0               # fallback VIX level
ERP = 0.045                      # equity risk premium, decimal (Damodaran-style estimate; set your own)
G_MACRO = 0.02                   # macro growth floor, decimal

# --- Formula 1: cost of equity ---
LAMBDA_S = 0.03                  # max extra premium for very small caps
TAU_S = 4.0                      # decay scale (in $B of market cap)
M_SIZE_FLOOR = 4.0                # size-premium starts phasing in below this market cap ($B)

# --- Formula 4: cross-sectional blend weights ---
W1 = 0.7                         # weight on ATSV z-score
W2 = 0.3                         # weight on industry percentile rank

# --- Formula 5: debt-decay + VIX-relative risk ---
TD = 4.0                         # years of FCF tolerated to cover net debt
VIX_MEAN = 19.5                  # long-run average VIX, used to gauge "is VIX elevated right now"
VIX_STD = 7.5                    # typical VIX swing size
VIX_Z_CAP = 2.5                  # cap how much a VIX spike can tighten the liquidity gate
GATE_SHARPNESS = 6.0             # how close final_score's smooth-min gate is to a true min()

# --- Formula 6: quality/size overlay ---
# M_TARGET overridden to 6.0 to match your stated $6B goldilocks zone (the formula file's
# own default was 3.0 -- flagging that in case it wasn't intentional).
M_TARGET = 6.0
SIGMA = 0.9                      # width of tolerance around M_TARGET, in log-$B space
DTE_TARGET = 0.30                # "sweet spot" debt/equity -- not just a ceiling anymore
DTE_SIGMA = 0.30                 # width of tolerance around DTE_TARGET
MAX_DTE = 0.80                   # hard-ish ceiling: leverage above this gets penalized regardless
MIN_CASH_CONVERSION = 0.15       # floor on F / softplus(O): how much operating income becomes real FCF
CASH_CONVERSION_STEEPNESS = 8.0  # how sharply that floor bites

# Kept for backwards compatibility with any old code/URLs still using the previous names.
TARGET_MARKET_CAP_B = M_TARGET
SIZE_SIGMA = SIGMA
MAX_DEBT_TO_EQUITY = MAX_DTE

# ============================================================
# DATA FETCHING
# ============================================================

def get_macro_inputs():
    """Fetch risk-free rate (10Y UST via ^TNX) and VIX from Yahoo."""
    import yfinance as yf
    rf, vix = DEFAULT_RISK_FREE, DEFAULT_VIX
    try:
        tnx = yf.Ticker("^TNX").history(period="5d")["Close"].dropna()
        if len(tnx):
            rf = float(tnx.iloc[-1]) / 100.0  # ^TNX quotes yield*10 (e.g. 43.0 => 4.30%)
    except Exception:
        pass
    try:
        vix_hist = yf.Ticker("^VIX").history(period="5d")["Close"].dropna()
        if len(vix_hist):
            vix = float(vix_hist.iloc[-1])
    except Exception:
        pass
    return rf, vix


def fetch_fundamentals(ticker, retries=2):
    """Pull the raw fields we need for one ticker. Returns dict or None on failure.

    Retries on transient errors (Yahoo rate-limiting / "Invalid Crumb" auth hiccups),
    which show up under concurrent load -- a short pause and retry usually clears them.
    """
    import time
    import yfinance as yf

    info = None
    for attempt in range(retries + 1):
        try:
            t = yf.Ticker(ticker)
            info = t.info
            if info and info.get("marketCap") is not None:
                break
        except Exception:
            pass
        if attempt < retries:
            time.sleep(1.5 * (attempt + 1))  # brief backoff before retrying
    if not info or info.get("marketCap") is None:
        return None

    def g(key, default=None):
        v = info.get(key, default)
        return v if v is not None else default

    market_cap = g("marketCap")
    enterprise_value = g("enterpriseValue", market_cap)
    beta = g("beta", 1.0)
    total_debt = g("totalDebt", 0.0)
    total_cash = g("totalCash", 0.0)
    fcf = g("freeCashflow")
    op_cf = g("operatingCashflow")
    revenue = g("totalRevenue")
    revenue_growth = g("revenueGrowth", G_MACRO)
    op_margin = g("operatingMargins", 0.1)
    debt_to_equity = g("debtToEquity")  # Yahoo reports this as a percent (e.g. 45.2 => 0.452)
    industry = g("industry", "Unknown")
    sector = g("sector", "Unknown")

    if fcf is None and op_cf is not None:
        # crude capex estimate if freeCashflow missing: assume ~15% of op cash flow as capex
        fcf = op_cf * 0.85

    if fcf is None or market_cap is None:
        return None

    capex_est = (op_cf - fcf) if (op_cf is not None and fcf is not None) else abs(fcf) * 0.15
    depr_est = capex_est * 0.7  # rough proxy when depreciation isn't directly exposed

    return {
        "ticker": ticker,
        "industry": industry,
        "sector": sector,
        "market_cap_b": market_cap / 1e9,
        "enterprise_value_b": (enterprise_value or market_cap) / 1e9,
        "beta": beta,
        "total_debt_b": (total_debt or 0.0) / 1e9,
        "total_cash_b": (total_cash or 0.0) / 1e9,
        "fcf_b": fcf / 1e9,
        "revenue_b": (revenue or 0.0) / 1e9,
        "op_margin": op_margin if op_margin is not None else 0.1,
        "revenue_growth": revenue_growth if revenue_growth is not None else G_MACRO,
        "capex_b": capex_est / 1e9 if capex_est else 0.0,
        "depr_b": depr_est / 1e9 if depr_est else 0.0,
        "debt_to_equity": (debt_to_equity / 100.0) if debt_to_equity else 0.0,
    }


# ============================================================
# FORMULAS
# ============================================================

def _sp(x):
    if x > 0:
        return x + math.log1p(math.exp(-x))
    return math.log1p(math.exp(x))


def softplus_leaky(x):
    """ln(1+e^x) + 0.1*ln(1+e^-x) — smooth, always-positive normalizer used in G and Final Score.
    (Numerically stable version -- avoids overflow for large |x| that math.exp(x) alone would hit.)
    """
    return _sp(x) + 0.1 * _sp(-x)


def probit(p, eps=1e-4):
    """Inverse standard normal CDF (Acklam's approximation). Turns a percentile rank
    into a z-score so it combines cleanly with ATSV's z-score in factor_score."""
    p = min(max(p, eps), 1 - eps)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low, p_high = 0.02425, 1 - 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= p_high:
        q = p - 0.5
        r = q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def smooth_min(values, k=GATE_SHARPNESS):
    """Soft version of min() -- approaches true min() as k grows. Used in final_score
    so the weakest of (liquidity, margin, debt) gates dominates without the gates
    all multiplying together and compounding unrelated weaknesses."""
    m = min(values)
    return m - (1.0 / k) * math.log(sum(math.exp(-k * (v - m)) for v in values))


def formula1_cost_of_equity(rf, beta, erp, ev, m, vix,
                             lambda_s=LAMBDA_S, tau_s=TAU_S, m_size_floor=M_SIZE_FLOOR):
    size_term = lambda_s * (1 - math.exp(-max(0.0, (m - m_size_floor) / tau_s)))
    vol_term = (1 - 1 / (1 + math.exp(ev / m))) * (beta * vix / 100)
    return rf + beta * erp + vol_term + size_term


def formula2_growth_governor(g, r, g_macro, capex, depr, op_margin):
    reinvest_rate = (capex - depr) / softplus_leaky(op_margin)
    return min(g, r - 0.01, max(g_macro, reinvest_rate))


def formula3_atsv(f, m, r, g):
    """
    Valuation signal: FCF yield (f/m) scaled by growth and discounted by distance
    between growth and required return. f/m is used HERE as the valuation driver --
    this is the only place f/m should appear (see formula6_overlay_score, which used
    to duplicate this exact ratio -- see its docstring for the fix).
    """
    denom = math.sqrt((r - g) ** 2 + 0.0004)
    return (f / m) * (math.tanh(f / m) * max(0.0, g) + 1 / (1 + math.exp(-f))) * (1 / denom)


def formula4_factor_score(atsv_val, atsv_universe, pr_industry, w1=W1, w2=W2):
    med = np.median(atsv_universe)
    mad = np.median(np.abs(np.array(atsv_universe) - med)) or 1e-6
    z_atsv = (atsv_val - med) / (1.4826 * mad)  # 1.4826 makes MAD comparable to std-dev for normal data
    z_industry = probit(pr_industry)
    raw = w1 * z_atsv + w2 * z_industry
    return max(-3.0, min(3.0, raw))


def formula5_final_score(factor, cash, f, vix, op_margin, d_adj, t_d=TD):
    vix_z = max(-VIX_Z_CAP, min(VIX_Z_CAP, (vix - VIX_MEAN) / VIX_STD))
    risk_multiplier = 1.0 + 0.5 * max(0.0, vix_z)  # elevated VIX tightens the liquidity gate

    denom = softplus_leaky(op_margin)
    liquidity_gate = 1 / (1 + math.exp(-((cash / abs(f)) / risk_multiplier - 1.5)))
    margin_gate = 1 / (1 + math.exp(2 * (f / denom + 0.5)))
    debt_decay = math.exp(-max(0.0, (d_adj / denom) / t_d))

    gate = smooth_min([liquidity_gate, margin_gate, debt_decay])
    return factor * gate


def formula6_overlay_score(m, d_e, op_margin, f,
                            target=M_TARGET, sigma=SIGMA,
                            dte_target=DTE_TARGET, dte_sigma=DTE_SIGMA, max_dte=MAX_DTE,
                            min_cash_conversion=MIN_CASH_CONVERSION,
                            steepness=CASH_CONVERSION_STEEPNESS):
    """
    FIX (collinearity): this gate used to reuse f/m (FCF yield) -- the exact same
    ratio already driving formula3_atsv's magnitude. That meant a single number
    (FCF yield) was influencing Factor AND Overlay through two different nonlinear
    paths, silently correlating them and giving that one input more effective
    weight than w1/w2 implied.

    Replaced with cash-conversion ratio f/softplus(op_margin): what fraction of
    operating income actually becomes free cash flow. This captures a DIFFERENT
    thing (earnings quality -- how much profit is "real" cash, not accrual) rather
    than re-measuring valuation cheapness. Market cap (m) no longer appears in this
    gate at all beyond the explicit size_fit term below -- it's the only place m
    drives the Overlay score.

    Also adds a debt "sweet spot" (gaussian centered on dte_target) on top of the
    previous hard ceiling (max_dte), so moderate, healthy leverage doesn't score
    identically to zero debt.
    """
    size_fit = math.exp(-((math.log(m) - math.log(target)) ** 2) / (2 * sigma ** 2))
    debt_sweet_spot = math.exp(-((d_e - dte_target) ** 2) / (2 * dte_sigma ** 2))
    debt_ceiling = 1 / (1 + math.exp(4 * (d_e - max_dte)))

    cash_conversion = f / softplus_leaky(op_margin)
    quality_gate = 1 / (1 + math.exp(-steepness * (cash_conversion - min_cash_conversion)))

    overlay = size_fit * debt_sweet_spot * debt_ceiling * quality_gate
    return overlay, size_fit, debt_sweet_spot * debt_ceiling, quality_gate


def combine_final_and_quality(final_score, quality_overlay):
    """
    Combine Formula 5's final_score with Formula 6's quality overlay into the
    ranking number everyone actually looks at.

    BUG FOUND VIA BACKTEST: a straight final_score * quality_overlay crushes bad
    companies toward zero instead of leaving them clearly negative. quality_overlay
    is always in [0, 1] -- so when it's near 0 (heavy debt, thin FCF, wrong size),
    multiplying ANY final_score by it shrinks the magnitude toward zero regardless
    of sign. A company with a badly negative final_score (deteriorating cash flow,
    high risk) gets multiplied by ~0 and ends up looking almost neutral instead of
    clearly bad. Confirmed in backtest.py: Sears, J.C. Penney, and Bed Bath & Beyond
    (all real pre-bankruptcy cases) scored ~0.0000 instead of clearly negative.

    FIX: when final_score is already negative, a poor quality overlay should make
    it WORSE, not erase it. Symmetric around quality_overlay = 1 (no change either way):
        final_score >= 0:  combined = final_score * quality_overlay        (shrinks 0..1x)
        final_score <  0:  combined = final_score * (2 - quality_overlay)  (amplifies 1..2x)
    """
    if final_score >= 0:
        return final_score * quality_overlay
    return final_score * (2 - quality_overlay)


# ============================================================
# CALIBRATION FRAMEWORK
# These turn W1/W2 and GATE_SHARPNESS from fixed guesses into values fitted on
# real data. They require a historical panel:
#   panel = [{"z_atsv": ..., "z_industry": ..., "fwd_return": ...}, ...]
# where fwd_return is a stock's ACTUAL forward return (e.g. next-quarter total
# return) observed AFTER the scoring date -- real market data you'd need to
# supply; nothing here can fabricate it. Not wired into run_screen() yet --
# call these manually once you have real panel data to fit against.
# ============================================================

def _ols_2var(x1, x2, y):
    """Closed-form least squares: y ~ b0 + b1*x1 + b2*x2. No numpy needed."""
    n = len(y)
    mean_x1, mean_x2, mean_y = sum(x1)/n, sum(x2)/n, sum(y)/n
    s11 = sum((a-mean_x1)**2 for a in x1)
    s22 = sum((a-mean_x2)**2 for a in x2)
    s12 = sum((x1[i]-mean_x1)*(x2[i]-mean_x2) for i in range(n))
    s1y = sum((x1[i]-mean_x1)*(y[i]-mean_y) for i in range(n))
    s2y = sum((x2[i]-mean_x2)*(y[i]-mean_y) for i in range(n))
    det = s11*s22 - s12**2
    if abs(det) < 1e-12:
        return 0.5, 0.5  # degenerate/collinear inputs, fall back to equal weight
    b1 = (s1y*s22 - s2y*s12) / det
    b2 = (s2y*s11 - s1y*s12) / det
    return b1, b2


def calibrate_factor_weights(panel):
    """Fits W1, W2 via OLS of forward return on [z_atsv, z_industry], normalized
    so |W1|+|W2| == 1 (keeps Factor on the same -3..3 clip scale). Requires a
    real historical panel -- see module docstring above."""
    import statistics
    z_atsv = [row["z_atsv"] for row in panel]
    z_ind = [row["z_industry"] for row in panel]
    fwd = [row["fwd_return"] for row in panel]
    b1, b2 = _ols_2var(z_atsv, z_ind, fwd)
    total = abs(b1) + abs(b2)
    if total < 1e-9:
        return W1, W2  # no signal found, keep defaults rather than divide by ~0
    return b1/total, b2/total


def _spearman_ic(scores, fwd_returns):
    """Rank correlation between scores and forward returns (Information Coefficient)."""
    n = len(scores)
    rank_s = {v: r for r, v in enumerate(sorted(range(n), key=lambda i: scores[i]))}
    rank_f = {v: r for r, v in enumerate(sorted(range(n), key=lambda i: fwd_returns[i]))}
    rs = [rank_s[i] for i in range(n)]
    rf = [rank_f[i] for i in range(n)]
    mean_rs, mean_rf = sum(rs)/n, sum(rf)/n
    cov = sum((rs[i]-mean_rs)*(rf[i]-mean_rf) for i in range(n))
    std_s = math.sqrt(sum((r-mean_rs)**2 for r in rs))
    std_f = math.sqrt(sum((r-mean_rf)**2 for r in rf))
    if std_s < 1e-9 or std_f < 1e-9:
        return 0.0
    return cov / (std_s * std_f)


def calibrate_gate_sharpness(panel_with_gates, fwd_returns, k_grid=None):
    """
    panel_with_gates: list of [liquidity_gate, margin_gate, debt_decay] triples
    (pre-smooth_min, per stock-period), aligned with fwd_returns. Grid-searches k,
    picks the k with the best Information Coefficient against REAL forward returns.
    Requires real historical data.
    """
    if k_grid is None:
        k_grid = [1, 2, 4, 6, 8, 12, 20, 40]
    best_k, best_ic = GATE_SHARPNESS, -2.0
    for k in k_grid:
        proxy_scores = [smooth_min(gates, k=k) for gates in panel_with_gates]
        ic = _spearman_ic(proxy_scores, fwd_returns)
        if ic > best_ic:
            best_ic, best_k = ic, k
    return best_k, best_ic


# ============================================================
# PIPELINE
# ============================================================

def run_screen(tickers=TICKERS, max_workers=6):
    """
    max_workers controls how many tickers are fetched from Yahoo simultaneously.
    Higher = faster, but too high risks Yahoo's anti-bot rate limiting kicking in
    ("Invalid Crumb" / 401 errors). 6 is a gentler default after seeing that happen
    at 15; if you still see lots of skips, drop it further (e.g. 3).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    rf, vix = get_macro_inputs()
    print(f"Risk-free rate: {rf:.3%}   VIX: {vix:.1f}\n")

    # Warm-up: one single-threaded request first to establish Yahoo's session/crumb
    # before opening multiple threads against it -- doing this concurrently from the
    # first request onward is what was triggering "Invalid Crumb" errors.
    if tickers:
        fetch_fundamentals(tickers[0])
        time.sleep(0.5)

    fetched = {}
    completed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_ticker = {pool.submit(fetch_fundamentals, tk): tk for tk in tickers}
        for future in as_completed(future_to_ticker):
            tk = future_to_ticker[future]
            completed += 1
            if completed % 50 == 0 or completed == len(tickers):
                print(f"  ...fetched {completed}/{len(tickers)}")
            try:
                data = future.result()
            except Exception:
                data = None
            if data is not None:
                fetched[tk] = data

    rows = []
    # Preserve the original ticker order in the output for readability
    for tk in tickers:
        data = fetched.get(tk)
        if data is None:
            continue

        r = formula1_cost_of_equity(rf, data["beta"], ERP,
                                     data["enterprise_value_b"], data["market_cap_b"], vix)
        g = formula2_growth_governor(data["revenue_growth"], r, G_MACRO,
                                      data["capex_b"], data["depr_b"], data["op_margin"])
        atsv = formula3_atsv(data["fcf_b"], data["market_cap_b"], r, g)

        net_debt = max(0.0, data["total_debt_b"] - data["total_cash_b"])
        fcf_yield = data["fcf_b"] / data["market_cap_b"] if data["market_cap_b"] else 0.0

        rows.append({**data, "r": r, "g": g, "atsv": atsv,
                     "net_debt_b": net_debt, "fcf_yield": fcf_yield, "vix": vix})

    if not rows:
        print("No tickers returned usable data.")
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Formula 4 needs cross-sectional stats + an industry percentile rank.
    # (formula4_factor_score is now per-row, not vectorized, so this loops via .apply)
    df["pr_industry"] = df.groupby("industry")["atsv"].rank(pct=True).fillna(0.5)
    atsv_universe = df["atsv"].tolist()
    df["factor_score"] = df.apply(
        lambda row: formula4_factor_score(row["atsv"], atsv_universe, row["pr_industry"]), axis=1
    )

    # Formula 5 (smooth-min gate combiner + VIX-relative liquidity requirement)
    df["final_score"] = df.apply(
        lambda row: formula5_final_score(
            row["factor_score"], row["total_cash_b"], row["fcf_b"],
            row["vix"], row["op_margin"], row["net_debt_b"]
        ), axis=1
    )

    # Formula 6 -- quality/size overlay (debt sweet-spot + cash-conversion gate,
    # no longer FCF-yield, to avoid double-counting with Formula 3's ATSV)
    overlay = df.apply(
        lambda row: formula6_overlay_score(
            row["market_cap_b"], row["debt_to_equity"], row["op_margin"], row["fcf_b"]
        ), axis=1, result_type="expand"
    )
    overlay.columns = ["quality_overlay", "size_score", "debt_score", "cash_conversion_score"]
    df = pd.concat([df, overlay], axis=1)
    df["cash_conversion"] = df.apply(lambda row: row["fcf_b"] / softplus_leaky(row["op_margin"]), axis=1)

    # Combined score: final allocation score reweighted by the quality overlay
    df["combined_score"] = df.apply(
        lambda row: combine_final_and_quality(row["final_score"], row["quality_overlay"]), axis=1
    )

    df = df.sort_values("combined_score", ascending=False)
    return df


DISPLAY_COLS = [
    "ticker", "industry", "market_cap_b", "debt_to_equity", "fcf_yield",
    "r", "g", "atsv", "factor_score", "final_score",
    "quality_overlay", "combined_score",
]


if __name__ == "__main__":
    result = run_screen()
    if not result.empty:
        pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
        print(result[DISPLAY_COLS].to_string(index=False))
        result.to_csv("screen_results.csv", index=False)
        print("\nFull results (all columns) written to screen_results.csv")
