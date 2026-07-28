<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mid-Cap Quality Screen</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#12151a;
    --panel:#1b1f26;
    --panel-2:#20252d;
    --border:#2a2f38;
    --text:#e7e4dc;
    --muted:#8a8f98;
    --gold:#c9a227;
    --gold-dim:#8f7419;
    --green:#4f9d69;
    --red:#c1483e;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;}
  ::selection{background:var(--gold-dim);color:#fff;}

  /* ---------- ticker tape ---------- */
  .tape-wrap{border-bottom:1px solid var(--border);background:#0e1116;overflow:hidden;white-space:nowrap;}
  .tape{display:inline-block;padding:8px 0;animation:scroll 38s linear infinite;font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.02em;}
  .tape span{margin:0 22px;color:var(--muted);}
  .tape b{color:var(--text);font-weight:600;}
  .up{color:var(--green);}
  .down{color:var(--red);}
  @keyframes scroll{from{transform:translateX(0);}to{transform:translateX(-50%);}}

  /* ---------- header ---------- */
  header{padding:36px 32px 20px;max-width:1180px;margin:0 auto;}
  .eyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 10px;}
  h1{font-family:'Fraunces',serif;font-weight:600;font-size:38px;line-height:1.05;margin:0 0 10px;letter-spacing:-.01em;}
  h1 em{font-style:italic;color:var(--gold);}
  .sub{color:var(--muted);font-size:14.5px;max-width:620px;line-height:1.55;margin:0 0 22px;}
  .macro-row{display:flex;gap:10px;flex-wrap:wrap;}
  .macro-chip{border:1px solid var(--border);background:var(--panel);border-radius:6px;padding:8px 12px;font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted);}
  .macro-chip b{color:var(--text);font-weight:600;}

  /* ---------- layout ---------- */
  main{max-width:1180px;margin:0 auto;padding:0 32px 60px;display:grid;grid-template-columns:260px 1fr;gap:24px;}
  @media (max-width:860px){main{grid-template-columns:1fr;}}

  .panel{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:20px;}
  .panel h2{font-family:'Fraunces',serif;font-size:16px;font-weight:600;margin:0 0 4px;}
  .panel .hint{font-size:12px;color:var(--muted);margin:0 0 18px;line-height:1.5;}

  .ctrl{margin-bottom:20px;}
  .ctrl label{display:flex;justify-content:space-between;font-size:12.5px;color:var(--text);margin-bottom:8px;}
  .ctrl label .val{font-family:'IBM Plex Mono',monospace;color:var(--gold);}
  input[type=range]{-webkit-appearance:none;width:100%;height:3px;background:var(--border);border-radius:2px;outline:none;}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:var(--gold);cursor:pointer;border:2px solid #0e1116;}
  input[type=range]::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:var(--gold);cursor:pointer;border:2px solid #0e1116;}

  .preset-row{display:flex;gap:6px;margin-bottom:22px;}
  .preset-btn{flex:1;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.03em;text-transform:uppercase;padding:7px 4px;border-radius:5px;border:1px solid var(--border);background:var(--panel-2);color:var(--muted);cursor:pointer;transition:.15s;}
  .preset-btn:hover{color:var(--text);border-color:var(--gold-dim);}
  .preset-btn.active{background:var(--gold-dim);color:#fff;border-color:var(--gold-dim);}

  .divider{height:1px;background:var(--border);margin:20px 0;}
  .weight-note{font-size:11.5px;color:var(--muted);line-height:1.5;}
  .weight-note code{font-family:'IBM Plex Mono',monospace;color:var(--gold);}

  .data-source{display:flex;gap:10px;align-items:flex-start;margin-bottom:6px;}
  .ds-dot{width:9px;height:9px;border-radius:50%;margin-top:4px;flex:none;}
  .ds-sample{background:var(--gold-dim);}
  .ds-live{background:var(--green);box-shadow:0 0 6px var(--green);}
  .ds-error{background:var(--red);}
  .ds-loading{background:var(--gold);animation:pulse 1s ease-in-out infinite;}
  @keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
  .ds-text{display:flex;flex-direction:column;gap:6px;font-size:12.5px;}
  #loadLiveBtn{align-self:flex-start;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.02em;background:transparent;border:1px solid var(--gold-dim);color:var(--gold);padding:5px 10px;border-radius:5px;cursor:pointer;transition:.15s;}
  #loadLiveBtn:hover{background:var(--gold-dim);color:#fff;}
  #loadLiveBtn:disabled{opacity:.5;cursor:default;}
  .hint code{font-family:'IBM Plex Mono',monospace;color:var(--gold);background:#0e1116;padding:1px 5px;border-radius:3px;}

  /* ---------- table ---------- */
  .table-wrap{background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;}
  .table-head{display:flex;justify-content:space-between;align-items:center;padding:16px 18px;border-bottom:1px solid var(--border);}
  .table-head h2{font-family:'Fraunces',serif;font-size:16px;font-weight:600;margin:0;}
  .count-badge{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--muted);}
  .scroll-x{overflow-x:auto;}
  table{width:100%;border-collapse:collapse;font-family:'IBM Plex Mono',monospace;font-size:12.5px;min-width:900px;}
  thead th{text-align:right;padding:10px 12px;color:var(--muted);font-weight:500;font-size:11px;letter-spacing:.03em;text-transform:uppercase;cursor:pointer;user-select:none;border-bottom:1px solid var(--border);white-space:nowrap;}
  thead th:hover{color:var(--gold);}
  thead th.left,tbody td.left{text-align:left;}
  thead th.active-sort{color:var(--gold);}
  tbody td{padding:9px 12px;text-align:right;border-bottom:1px solid #22262e;white-space:nowrap;}
  tbody tr:hover{background:var(--panel-2);}
  .rank{color:var(--muted);}
  .tk{font-weight:600;color:var(--text);font-family:'IBM Plex Mono',monospace;}
  .nm{color:var(--muted);font-size:11px;display:block;font-family:'Inter',sans-serif;}
  .bar-cell{display:flex;align-items:center;justify-content:flex-end;gap:8px;}
  .bar-track{width:52px;height:5px;background:#2a2f38;border-radius:3px;overflow:hidden;}
  .bar-fill{height:100%;background:linear-gradient(90deg,var(--gold-dim),var(--gold));}
  .pos{color:var(--green);}
  .neg{color:var(--red);}

  .search-row{display:flex;gap:10px;padding:0 18px 14px;}
  #searchBox{flex:1;background:#0e1116;border:1px solid var(--border);border-radius:6px;padding:9px 12px;color:var(--text);font-family:'IBM Plex Mono',monospace;font-size:12.5px;outline:none;}
  #searchBox:focus{border-color:var(--gold-dim);}
  #searchBox::placeholder{color:#565b64;}
  #trackedToggle{flex:none;font-family:'IBM Plex Mono',monospace;font-size:11.5px;background:transparent;border:1px solid var(--border);color:var(--muted);padding:8px 12px;border-radius:6px;cursor:pointer;transition:.15s;white-space:nowrap;}
  #trackedToggle:hover{border-color:var(--gold-dim);color:var(--text);}
  #trackedToggle.active{background:var(--gold-dim);color:#fff;border-color:var(--gold-dim);}
  .search-status{padding:0 18px 10px;font-size:11.5px;font-family:'IBM Plex Mono',monospace;min-height:14px;}
  .search-status.loading{color:var(--gold);}
  .search-status.success{color:var(--green);}
  .search-status.error{color:var(--red);}

  .star-cell{padding-right:0 !important;}
  .star-btn{background:none;border:none;color:var(--muted);font-size:15px;cursor:pointer;padding:0;line-height:1;}
  .star-btn.starred{color:var(--gold);}
  .star-btn:hover{color:var(--gold);}
  .remove-btn{font-size:13px;}
  .remove-btn:hover{color:var(--red) !important;}
  tr.tracked-row{background:rgba(201,162,39,0.06);box-shadow:inset 3px 0 0 var(--gold-dim);}
  tr.tracked-row:hover{background:rgba(201,162,39,0.1);}

  footer{max-width:1180px;margin:0 auto;padding:0 32px 50px;color:var(--muted);font-size:12px;line-height:1.6;}
  footer b{color:var(--text);}
</style>
</head>
<body>

  <div class="tape-wrap">
    <div class="tape" id="tape"></div>
  </div>

  <header>
    <p class="eyebrow" id="eyebrowText">Empty watchlist &middot; add your first stock below</p>
    <h1>My mid-cap <em>watchlist</em></h1>
    <p class="sub">Formulas 1&ndash;6 recomputing in your browser as you move the sliders. Add the stocks you actually own or follow — nothing is bulk-scanned, so this stays fast and light on requests.</p>
    <div class="macro-row">
      <div class="macro-chip">Risk-free (10Y) &nbsp;<b>4.30%</b></div>
      <div class="macro-chip">VIX &nbsp;<b>16.0</b></div>
      <div class="macro-chip">ERP &nbsp;<b>4.50%</b></div>
      <div class="macro-chip">Tracking &nbsp;<b id="uniCount">0</b> stocks</div>
    </div>
  </header>

  <main>
    <div class="panel">
      <h2>Screen controls</h2>
      <p class="hint">Tune the size &amp; quality overlay (Formula 6). Rankings update instantly.</p>

      <div class="data-source" id="dataSourceBox">
        <div class="ds-dot ds-loading" id="dsDot"></div>
        <div class="ds-text">
          <span id="dsLabel">Checking backend…</span>
          <button id="refreshAllBtn" type="button">Refresh all tracked</button>
        </div>
      </div>
      <p class="hint" id="dsHint">This list starts empty. Add a stock using the search box on the right — only what you add gets fetched, nothing scanned in bulk.</p>

      <div class="divider"></div>

      <div class="preset-row">
        <button class="preset-btn" data-preset="strict">Strict</button>
        <button class="preset-btn active" data-preset="moderate">Moderate</button>
        <button class="preset-btn" data-preset="lenient">Lenient</button>
      </div>

      <div class="ctrl">
        <label>Target market cap <span class="val" id="capVal">$6.0B</span></label>
        <input type="range" id="capSlider" min="1" max="14" step="0.5" value="6">
      </div>
      <div class="ctrl">
        <label>Max debt / equity <span class="val" id="dteVal">0.80</span></label>
        <input type="range" id="dteSlider" min="0.1" max="2" step="0.05" value="0.8">
      </div>
      <div class="ctrl">
        <label>Min cash conversion <span class="val" id="fcfVal">15%</span></label>
        <input type="range" id="fcfSlider" min="-20" max="60" step="1" value="15">
      </div>

      <div class="divider"></div>
      <p class="weight-note">
        <code>combined_score</code> = Final Score (Formulas 1&ndash;5) &times; Quality Overlay (size fit &times; debt sweet-spot &times; cash-conversion quality). Click any column header to sort.
      </p>
    </div>

    <div class="table-wrap">
      <div class="table-head">
        <h2>My tracked stocks</h2>
        <span class="count-badge" id="resultCount">0 tracked</span>
      </div>
      <div class="search-row">
        <input type="text" id="searchBox" placeholder="Type a ticker (e.g. AAPL) and press Enter to add it…" autocomplete="off">
      </div>
      <div class="search-status" id="searchStatus"></div>
      <div class="scroll-x">
        <table>
          <thead>
            <tr>
              <th class="left" style="width:26px;"></th>
              <th class="left" data-key="rank">#</th>
              <th class="left" data-key="ticker">Ticker</th>
              <th data-key="market_cap_b">Mkt Cap</th>
              <th data-key="debt_to_equity">D/E</th>
              <th data-key="fcf_yield">FCF Yld</th>
              <th data-key="r">R</th>
              <th data-key="g">G</th>
              <th data-key="atsv">ATSV</th>
              <th data-key="final_score">Final</th>
              <th data-key="quality_overlay">Quality</th>
              <th data-key="combined_score">Combined</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </div>
  </main>

  <footer>
    <p><b>How this works:</b> your list starts empty and only grows when you add a ticker — nothing gets bulk-scanned in the background. Each addition is a single, lightweight request to Yahoo Finance via your backend, which keeps this fast and far less likely to trip any rate limiting. Your list is saved in this browser, so it'll still be here next time you visit this site (on this device/browser).</p>
  </footer>

<script>
// Points at the live Render backend. If you ever go back to testing on your
// own computer only, change this back to "http://localhost:5001".
const API_BASE = "https://midcap-screener-92ec.onrender.com";

const STORAGE_KEY = "midcap_watchlist_tickers_v2";

// ---------------- watchlist persistence ----------------
// Only the ticker symbols are saved -- all scoring/formula math now happens
// server-side (stock_screener.py is the single source of truth), so on
// reload we just re-ask the backend to (re)compute everything fresh.
function loadSavedTickers(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  }catch(err){
    console.warn("Couldn't read saved watchlist:", err);
    return [];
  }
}
function saveTickers(){
  try{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DATASET.map(c => c.ticker)));
  }catch(err){
    console.warn("Couldn't save watchlist:", err);
  }
}

let DATASET = [];          // scored rows, straight from the backend -- no client-side formula math
let sortKey = "combined_score", sortDesc = true;
let searchQuery = "";

function mapRow(r){
  return {
    ticker: r.ticker,
    name: r.industry || r.sector || r.ticker,
    sector: r.sector || "",
    market_cap_b: r.market_cap_b,
    debt_to_equity: r.debt_to_equity,
    fcf_yield: r.fcf_yield,
    r: r.r,
    g: r.g,
    atsv: r.atsv,
    final_score: r.final_score,
    quality_overlay: r.quality_overlay,
    combined_score: r.combined_score,
  };
}

function sliderParams(){
  const p = new URLSearchParams();
  p.set("target", document.getElementById("capSlider").value);
  p.set("max_dte", document.getElementById("dteSlider").value);
  p.set("min_cash_conversion", (parseFloat(document.getElementById("fcfSlider").value)/100).toString());
  return p;
}

// Single function for talking to the backend: given a list of tickers, ask it
// to fetch (or reuse cached) fundamentals AND apply the current slider settings,
// returning fully-scored rows. Used for adding, refreshing, AND slider changes.
async function fetchScoredRows(tickers){
  const params = sliderParams();
  params.set("tickers", tickers.join(","));
  const res = await fetch(`${API_BASE}/api/screen?${params.toString()}`);
  if(!res.ok) throw new Error("HTTP " + res.status);
  const json = await res.json();
  if(!json.rows || !json.rows.length) throw new Error("No data returned");
  return json.rows.map(mapRow);
}

function debounce(fn, wait){
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

// ---------------- rendering (pure display logic -- no formula math here) ----------------
function refreshLabelsAndSort(){
  document.getElementById("capVal").textContent = "$" + parseFloat(document.getElementById("capSlider").value).toFixed(1) + "B";
  document.getElementById("dteVal").textContent = parseFloat(document.getElementById("dteSlider").value).toFixed(2);
  document.getElementById("fcfVal").textContent = parseFloat(document.getElementById("fcfSlider").value).toFixed(1) + "%";
  document.getElementById("uniCount").textContent = DATASET.length;
  document.getElementById("eyebrowText").textContent = DATASET.length
    ? `Tracking ${DATASET.length} stock${DATASET.length===1?'':'s'}`
    : "Empty watchlist · add your first stock below";

  const sorted = [...DATASET].sort((a,b)=> sortDesc ? (b[sortKey]??0)-(a[sortKey]??0) : (a[sortKey]??0)-(b[sortKey]??0));
  sorted.forEach((row,i)=>{ row.rank = i+1; });

  updateTape(sorted);

  let filtered = sorted;
  if(searchQuery){
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(r => r.ticker.toLowerCase().includes(q) || (r.name||"").toLowerCase().includes(q));
  }
  render(filtered);
}

function updateTape(sorted){
  const wrap = document.querySelector(".tape-wrap");
  const tapeEl = document.getElementById("tape");
  if(!DATASET.length){ wrap.style.display = "none"; return; }
  wrap.style.display = "";
  const items = sorted.map(c=>{
    const delta = (c.combined_score*100).toFixed(1);
    const cls = c.combined_score>=0 ? "up" : "down";
    const sign = c.combined_score>=0 ? "+" : "";
    return `<span><b>${c.ticker}</b> $${c.market_cap_b.toFixed(1)}B <span class="${cls}">${sign}${delta}</span></span>`;
  }).join("");
  tapeEl.innerHTML = items + items;
}

function render(rows){
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = "";

  if(!DATASET.length){
    tbody.innerHTML = `<tr><td colspan="12" style="text-align:center;color:var(--muted);padding:32px 24px;">Your watchlist is empty. Type a ticker above (like <span style="color:var(--gold);">AAPL</span> or <span style="color:var(--gold);">MLI</span>) and press Enter to add it.</td></tr>`;
    document.getElementById("resultCount").textContent = "0 tracked";
    return;
  }
  if(!rows.length){
    tbody.innerHTML = `<tr><td colspan="12" style="text-align:center;color:var(--muted);padding:24px;">No matches for that search.</td></tr>`;
    document.getElementById("resultCount").textContent = `0 of ${DATASET.length} shown`;
    return;
  }

  const maxCombined = Math.max(...rows.map(r=>Math.abs(r.combined_score)), 0.001);

  rows.forEach(row=>{
    const tr = document.createElement("tr");
    const barPct = Math.max(2, Math.min(100, (Math.abs(row.combined_score)/maxCombined)*100));
    tr.innerHTML = `
      <td class="left star-cell"><button class="star-btn remove-btn" data-ticker="${row.ticker}" title="Remove from watchlist">✕</button></td>
      <td class="left rank">${row.rank}</td>
      <td class="left"><span class="tk">${row.ticker}</span><span class="nm">${row.name}</span></td>
      <td>$${row.market_cap_b.toFixed(1)}B</td>
      <td>${row.debt_to_equity.toFixed(2)}</td>
      <td>${(row.fcf_yield*100).toFixed(1)}%</td>
      <td>${(row.r*100).toFixed(1)}%</td>
      <td>${(row.g*100).toFixed(1)}%</td>
      <td>${row.atsv.toFixed(2)}</td>
      <td class="${row.final_score>=0?'pos':'neg'}">${row.final_score.toFixed(3)}</td>
      <td>${row.quality_overlay.toFixed(2)}</td>
      <td>
        <div class="bar-cell">
          <span class="${row.combined_score>=0?'pos':'neg'}">${row.combined_score.toFixed(3)}</span>
          <div class="bar-track"><div class="bar-fill" style="width:${barPct}%"></div></div>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });

  tbody.querySelectorAll(".remove-btn").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const tk = btn.getAttribute("data-ticker");
      DATASET = DATASET.filter(c => c.ticker !== tk);
      saveTickers();
      refreshLabelsAndSort();
    });
  });

  document.getElementById("resultCount").textContent =
    rows.length === DATASET.length ? `${DATASET.length} tracked` : `${rows.length} of ${DATASET.length} shown`;
}

// ---------------- controls ----------------
document.querySelectorAll("th[data-key]").forEach(th=>{
  th.addEventListener("click", ()=>{
    const key = th.getAttribute("data-key");
    if(key==="rank") return;
    if(sortKey===key){ sortDesc = !sortDesc; } else { sortKey=key; sortDesc=true; }
    document.querySelectorAll("th").forEach(h=>h.classList.remove("active-sort"));
    th.classList.add("active-sort");
    refreshLabelsAndSort();
  });
});

document.querySelectorAll(".preset-btn").forEach(btn=>{
  btn.addEventListener("click", ()=>{
    document.querySelectorAll(".preset-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    const presets = { strict:{dte:0.5,fcf:30}, moderate:{dte:0.8,fcf:15}, lenient:{dte:1.3,fcf:0} };
    const p = presets[btn.getAttribute("data-preset")];
    document.getElementById("dteSlider").value = p.dte;
    document.getElementById("fcfSlider").value = p.fcf;
    onSliderChange();
  });
});

const debouncedRecompute = debounce(recomputeFromBackend, 450);
function onSliderChange(){
  refreshLabelsAndSort();  // instant label update, using last-known scores
  debouncedRecompute();     // then ask the backend for the real recompute, debounced
}
document.getElementById("capSlider").addEventListener("input", onSliderChange);
document.getElementById("dteSlider").addEventListener("input", onSliderChange);
document.getElementById("fcfSlider").addEventListener("input", onSliderChange);

document.getElementById("searchBox").addEventListener("input", (e)=>{
  searchQuery = e.target.value.trim();
  refreshLabelsAndSort();
});

document.getElementById("searchBox").addEventListener("keydown", async (e)=>{
  if(e.key !== "Enter") return;
  const q = searchQuery.trim().toUpperCase();
  if(!q) return;
  const exists = DATASET.some(c => c.ticker.toUpperCase() === q);
  if(exists){
    document.getElementById("searchStatus").textContent = `${q} is already on your list.`;
    document.getElementById("searchStatus").className = "search-status";
    return;
  }
  await addTicker(q);
});

// ---------------- backend calls ----------------
function setStatus(state, label){
  document.getElementById("dsDot").className = "ds-dot ds-" + state;
  document.getElementById("dsLabel").textContent = label;
}

async function checkBackendHealth(){
  try{
    const res = await fetch(`${API_BASE}/api/health`);
    if(!res.ok) throw new Error("HTTP " + res.status);
    setStatus("live", "Backend online");
  }catch(err){
    setStatus("error", "Backend offline — adding stocks won't work right now");
  }
}

async function recomputeFromBackend(){
  // Re-scores the CURRENT watchlist against the current slider settings.
  // Cheap: the backend reuses its cache for fundamentals it already has,
  // it's only re-running Formula 6 + the combine step, not re-fetching Yahoo.
  if(!DATASET.length) return;
  try{
    const rows = await fetchScoredRows(DATASET.map(c=>c.ticker));
    DATASET = rows;
    refreshLabelsAndSort();
  }catch(err){
    console.error("Recompute failed:", err);
    // Leave the last-known scores on screen rather than clearing the table.
  }
}

async function addTicker(ticker){
  const statusEl = document.getElementById("searchStatus");
  statusEl.textContent = `Looking up ${ticker} from Yahoo Finance…`;
  statusEl.className = "search-status loading";
  try{
    const rows = await fetchScoredRows([ticker]);
    const newRow = rows[0];
    DATASET = DATASET.filter(c => c.ticker !== newRow.ticker);
    DATASET.push(newRow);
    saveTickers();

    statusEl.textContent = `Added ${ticker} to your watchlist.`;
    statusEl.className = "search-status success";
    document.getElementById("searchBox").value = "";
    searchQuery = "";
    refreshLabelsAndSort();
  }catch(err){
    statusEl.textContent = `Couldn't find "${ticker}" — double-check the ticker symbol, or the backend may be temporarily unavailable.`;
    statusEl.className = "search-status error";
    console.error(err);
  }
}

async function refreshAllTracked(){
  if(!DATASET.length){
    document.getElementById("searchStatus").textContent = "Nothing to refresh yet — add a stock first.";
    document.getElementById("searchStatus").className = "search-status";
    return;
  }
  const btn = document.getElementById("refreshAllBtn");
  btn.disabled = true;
  const statusEl = document.getElementById("searchStatus");
  statusEl.textContent = `Refreshing ${DATASET.length} tracked stock${DATASET.length===1?'':'s'}…`;
  statusEl.className = "search-status loading";
  try{
    DATASET = await fetchScoredRows(DATASET.map(c=>c.ticker));
    saveTickers();
    statusEl.textContent = `Refreshed ${DATASET.length} stock${DATASET.length===1?'':'s'} with the latest data.`;
    statusEl.className = "search-status success";
    refreshLabelsAndSort();
  }catch(err){
    statusEl.textContent = "Couldn't refresh right now — try again in a moment.";
    statusEl.className = "search-status error";
    console.error(err);
  }finally{
    btn.disabled = false;
  }
}
document.getElementById("refreshAllBtn").addEventListener("click", refreshAllTracked);

// ---------------- init ----------------
async function init(){
  checkBackendHealth();
  const savedTickers = loadSavedTickers();
  if(savedTickers.length){
    document.getElementById("searchStatus").textContent = `Loading your ${savedTickers.length} saved stock${savedTickers.length===1?'':'s'}…`;
    document.getElementById("searchStatus").className = "search-status loading";
    try{
      DATASET = await fetchScoredRows(savedTickers);
      document.getElementById("searchStatus").textContent = "";
      document.getElementById("searchStatus").className = "search-status";
    }catch(err){
      document.getElementById("searchStatus").textContent = "Couldn't reload your saved watchlist — the backend may be waking up (free tier sleeps when idle). Try refreshing in a minute.";
      document.getElementById("searchStatus").className = "search-status error";
    }
  }
  refreshLabelsAndSort();
}
init();
</script>
</body>
</html>
