"""
Local backend API for the Mid-Cap Quality Screen dashboard.

Wraps stock_screener.run_screen() and serves it as JSON so the HTML
dashboard can fetch real numbers instead of the sample dataset.

Install:
    pip install flask yfinance pandas numpy

Run:
    python app.py

Then open midcap-screener.html in your browser (it looks for this API
at http://localhost:5001/api/screen and falls back to sample data if
the server isn't running).

Endpoints:
    GET /api/screen                 -> full 400-ticker S&P MidCap 400 screen
    GET /api/screen?tickers=A,B,C   -> screen just the tickers you list
    GET /api/screen?target=6&max_dte=0.8&min_fcf_yield=0.025
                                     -> override the Formula 6 overlay params
"""

from flask import Flask, jsonify, request
import stock_screener as sc
import time
import os

app = Flask(__name__)

CACHE_TTL_SECONDS = 900  # 15 minutes -- repeated clicks within this window reuse fetched data
_cache = {}  # {tuple(sorted(tickers)): (timestamp, df)}

# Render sets this env var automatically on their platform. Free-tier instances
# have limited RAM, and scanning all ~900 tickers at once was crashing the
# server (502 Bad Gateway) -- so on Render specifically, default to a smaller,
# curated subset unless the caller explicitly asks for specific tickers.
# Running app.py on your own computer always gets the full universe.
IS_RENDER = os.environ.get("RENDER") == "true"
DEFAULT_TICKERS = sc.TICKERS[:120] if IS_RENDER else sc.TICKERS
DEFAULT_WORKERS = 3 if IS_RENDER else 6


@app.after_request
def add_cors_headers(resp):
    # Minimal manual CORS so the dashboard (opened as a local file or
    # served from a different port) can call this API without extra deps.
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/api/screen", methods=["GET", "OPTIONS"])
def screen():
    if request.method == "OPTIONS":
        return "", 204

    tickers_param = request.args.get("tickers")
    tickers = [t.strip().upper() for t in tickers_param.split(",")] if tickers_param else DEFAULT_TICKERS

    # Allow the dashboard sliders to override the Formula 6 overlay live
    target = float(request.args.get("target", sc.TARGET_MARKET_CAP_B))
    sigma = float(request.args.get("sigma", sc.SIZE_SIGMA))
    max_dte = float(request.args.get("max_dte", sc.MAX_DEBT_TO_EQUITY))
    min_fcf_yield = float(request.args.get("min_fcf_yield", sc.MIN_FCF_YIELD))

    cache_key = tuple(sorted(tickers))
    cached = _cache.get(cache_key)
    if cached and (time.time() - cached[0]) < CACHE_TTL_SECONDS:
        df = cached[1].copy()
        print(f"[cache hit] serving {len(tickers)} tickers from cache "
              f"({int(time.time() - cached[0])}s old)")
    else:
        df = sc.run_screen(tickers, max_workers=DEFAULT_WORKERS)
        if not df.empty:
            _cache[cache_key] = (time.time(), df.copy())

    if df.empty:
        return jsonify({"error": "No data returned for given tickers", "rows": []}), 200

    # Recompute Formula 6 + combined score with the request's overlay params
    # (run_screen already applied the module defaults; this reapplies with overrides)
    overlay = df.apply(
        lambda row: sc.formula6_quality_size_overlay(
            row["market_cap_b"], row["debt_to_equity"], row["fcf_yield"],
            target, sigma, max_dte, min_fcf_yield
        ), axis=1, result_type="expand"
    )
    overlay.columns = ["quality_overlay", "size_score", "debt_score", "fcf_score"]
    for col in overlay.columns:
        df[col] = overlay[col]
    df["combined_score"] = df.apply(
        lambda row: sc.combine_final_and_quality(row["final_score"], row["quality_overlay"]), axis=1
    )
    df = df.sort_values("combined_score", ascending=False)

    return jsonify({
        "params": {"target": target, "sigma": sigma, "max_dte": max_dte, "min_fcf_yield": min_fcf_yield},
        "count": len(df),
        "rows": df.to_dict(orient="records"),
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    print(f"Mid-Cap Screen API running on port {port}")
    print(f"Try: http://localhost:{port}/api/screen?tickers=AAON,MLI,UFPI")
    app.run(host="0.0.0.0", port=port, debug=False)

