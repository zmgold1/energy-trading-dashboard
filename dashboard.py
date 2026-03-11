"""
dashboard.py — Energy Trading Dashboard
EchoFi-inspired dark trading UI
Poženi: streamlit run dashboard.py
"""

import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Energy Trading Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

* { font-family: 'DM Sans', sans-serif !important; box-sizing: border-box; }
code, .mono { font-family: 'DM Mono', monospace !important; }
html, body, [class*="css"] { background-color: #0d0f14 !important; color: #e2e8f0; margin:0; padding:0; }
.stApp { background-color: #0d0f14 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* NAV */
.nav {
    background: #111318;
    border-bottom: 1px solid #1e2330;
    padding: 0 24px;
    height: 52px;
    display: flex;
    align-items: center;
    gap: 32px;
}
.nav-logo { color: #fff; font-size: 16px; font-weight: 700; letter-spacing: -0.02em; display:flex; align-items:center; gap:8px; }
.nav-logo span { color: #4ecdc4; }
.nav-item { color: #64748b; font-size: 13px; font-weight: 500; cursor: pointer; padding: 4px 0; }
.nav-item-active { color: #e2e8f0; font-size: 13px; font-weight: 600; border-bottom: 2px solid #4ecdc4; padding: 4px 0; }
.nav-right { margin-left: auto; display:flex; align-items:center; gap:12px; }
.nav-time { color: #64748b; font-size: 12px; font-family: 'DM Mono', monospace !important; }
.nav-badge { background: #4ecdc415; border: 1px solid #4ecdc430; color: #4ecdc4; font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 500; }

/* STATS BAR */
.stats-bar {
    background: #111318;
    border-bottom: 1px solid #1e2330;
    padding: 10px 24px;
    display: flex;
    gap: 32px;
    align-items: center;
    overflow-x: auto;
}
.stat-item { display: flex; flex-direction: column; gap: 2px; min-width: fit-content; }
.stat-label { color: #64748b; font-size: 10px; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; }
.stat-value { color: #f1f5f9; font-size: 15px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.stat-pos { color: #4ecdc4 !important; }
.stat-neg { color: #fc5c7d !important; }
.stat-divider { width: 1px; height: 32px; background: #1e2330; }

/* MAIN CONTENT */
.main-wrap { padding: 20px 24px; }

/* CHART CARD */
.chart-card {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.chart-title { color: #f1f5f9; font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.chart-sub { color: #64748b; font-size: 12px; margin-bottom: 16px; }

/* PANEL CARD */
.panel-card {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 12px;
    padding: 16px;
    height: 100%;
}
.panel-title { color: #94a3b8; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center; }
.panel-date { color: #475569; font-size: 10px; }

/* SPREAD ROW */
.spread-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #1e2330;
}
.spread-row:last-child { border-bottom: none; }
.spread-name { color: #94a3b8; font-size: 12px; }
.spread-val-pos { color: #4ecdc4; font-size: 14px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.spread-val-neg { color: #fc5c7d; font-size: 14px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.spread-badge-pos { background: #4ecdc415; color: #4ecdc4; border-radius: 4px; padding: 2px 6px; font-size: 10px; font-weight: 600; }
.spread-badge-neg { background: #fc5c7d15; color: #fc5c7d; border-radius: 4px; padding: 2px 6px; font-size: 10px; font-weight: 600; }

/* BIG NUMBER */
.big-num { font-size: 32px; font-weight: 700; font-family: 'DM Mono', monospace !important; color: #f1f5f9; line-height:1; margin: 8px 0 4px 0; }
.big-sub { font-size: 12px; color: #64748b; }

/* WEATHER ROW */
.wx-row { display:flex; justify-content:space-between; align-items:center; padding: 6px 0; border-bottom: 1px solid #1e2330; }
.wx-row:last-child { border-bottom:none; }
.wx-date { color: #94a3b8; font-size: 12px; font-weight: 500; min-width: 80px; }
.wx-temp { color: #f1f5f9; font-size: 14px; font-weight: 600; font-family: 'DM Mono', monospace !important; min-width: 70px; text-align: right; }
.wx-badge-bull { background: #4ecdc415; color: #4ecdc4; border-radius: 4px; padding: 2px 6px; font-size: 10px; }
.wx-badge-bear { background: #fc5c7d15; color: #fc5c7d; border-radius: 4px; padding: 2px 6px; font-size: 10px; }
.wx-badge-neut { background: #64748b20; color: #64748b; border-radius: 4px; padding: 2px 6px; font-size: 10px; }

/* PROGRESS BAR */
.prog-wrap { background: #1e2330; border-radius: 4px; height: 6px; margin: 8px 0; }
.prog-fill { height: 6px; border-radius: 4px; background: linear-gradient(90deg, #4ecdc4, #44b5ad); }

/* BRIEFING */
.brief-item { padding: 8px 0; border-bottom: 1px solid #1e2330; font-size: 12px; color: #94a3b8; display:flex; gap:8px; align-items:flex-start; }
.brief-item:last-child { border-bottom: none; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1e2330 !important; gap:0 !important; padding: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #64748b !important; font-size: 13px !important; font-weight: 500 !important; padding: 10px 20px !important; border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important; }
.stTabs [aria-selected="true"] { color: #4ecdc4 !important; border-bottom: 2px solid #4ecdc4 !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; background: transparent !important; }

/* BUTTON */
.stButton button { background: #4ecdc415 !important; border: 1px solid #4ecdc430 !important; color: #4ecdc4 !important; font-size: 12px !important; font-weight: 600 !important; padding: 6px 16px !important; border-radius: 8px !important; }
div[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── TOKENS ────────────────────────────────────────────────────────────────────
OILPRICE_TOKEN = "ee7f1e4afc476e3d40279cceb5676293f2c6b30a62cdd24ea5b9592a0e03f5c6"
AGSI_KEY       = "b26cf657bcbcd971d16eded061017e6d"
ENTSO_TOKEN    = "0e72f85a-2620-4a36-b812-c4cbfa17b4ec"
GAS_EFF=0.50; GAS_EM=0.37; COAL_EFF=0.40; COAL_EM=0.83; EUR_USD=1.08; COAL_DIV=8.14

# ── FETCH ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_all_countries():
    from xml.etree import ElementTree as ET
    from collections import defaultdict

    COUNTRIES = {
        "SI": "10YSI-ELES-----O",
        "AT": "10YAT-APG------L",
        "FR": "10YFR-RTE------C",
        "CH": "10YCH-SWISSGRIDZ",
        "CZ": "10YCZ-CEPS-----N",
        "RS": "10YCS-SERBIATSOV",
        "SK": "10YSK-SEPS-----K",
        "PL": "10YPL-AREA-----S",
        "NL": "10YNL----------L",
        "BE": "10YBE----------2",
        "GR": "10YGR-HTSO-----Y",
        "BG": "10YCA-BULGARIA-R",
        "HR": "10YHR-HEP------M",
    }

    now = datetime.utcnow()
    if now.hour >= 12:
        ps = now.strftime("%Y%m%d0000")
        pe = (now + timedelta(days=1)).strftime("%Y%m%d0000")
    else:
        ps = (now - timedelta(days=1)).strftime("%Y%m%d0000")
        pe = now.strftime("%Y%m%d0000")

    results = []
    for name, eic in COUNTRIES.items():
        try:
            r = requests.get("https://web-api.tp.entsoe.eu/api", params={
                "securityToken": ENTSO_TOKEN,
                "documentType": "A44",
                "in_Domain": eic, "out_Domain": eic,
                "periodStart": ps, "periodEnd": pe,
            }, timeout=12)
            root = ET.fromstring(r.text)
            ns = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}
            raw = [(int(pt.find("ns:position",ns).text)-1, float(pt.find("ns:price.amount",ns).text))
                   for pt in root.findall(".//ns:Point",ns) if pt.find("ns:price.amount",ns) is not None]
            if raw:
                hv = defaultdict(list)
                for h,v in raw: hv[h%24].append(v)
                prices = sorted([(h, sum(vs)/len(vs)) for h,vs in hv.items()])
                all_v = [v for _,v in prices]
                peak_v = [v for h,v in prices if 9<=h<20]
                results.append({
                    "country": name, "base": sum(all_v)/len(all_v),
                    "peak": sum(peak_v)/len(peak_v) if peak_v else None,
                    "min": min(all_v), "max": max(all_v), "hours": prices
                })
        except: pass

    # DE iz SMARD
    try:
        yesterday = datetime.now() - timedelta(days=1)
        ts = int(yesterday.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()*1000)
        r = requests.get(f"https://www.smard.de/app/chart_data/4169/DE/4169_DE_quarterhour_{ts}.json", timeout=10)
        series = r.json().get("series",[])
        hourly = {}
        for i,(ts_ms,v) in enumerate(series):
            if v is not None:
                h=i//4
                if h not in hourly: hourly[h]=[]
                hourly[h].append(v/10)
        hours = [(h, sum(vs)/len(vs)) for h,vs in sorted(hourly.items())]
        all_v = [v for _,v in hours]
        peak_v = [v for h,v in hours if 9<=h<20]
        results.append({"country":"DE","base":sum(all_v)/len(all_v),
                        "peak":sum(peak_v)/len(peak_v) if peak_v else None,
                        "min":min(all_v),"max":max(all_v),"hours":hours})
    except: pass

    return sorted(results, key=lambda x: x["base"])

@st.cache_data(ttl=300)
def fetch_generation():
    from xml.etree import ElementTree as ET
    from collections import defaultdict

    PSR_NAMES = {
        "B01": ("Biomasa",       "#6b7280", ""),
        "B02": ("Lignit",        "#92400e", ""),
        "B03": ("Premog",        "#78350f", ""),
        "B04": ("Plin",          "#f59e0b", ""),
        "B05": ("Nafta",         "#b45309", ""),
        "B06": ("Geotermalna",   "#10b981", ""),
        "B09": ("Hidro DAM",     "#3b82f6", ""),
        "B10": ("Hidro črpalna", "#6366f1", ""),
        "B11": ("Hidro pretočna","#2563eb", ""),
        "B12": ("Tide",          "#0891b2", ""),
        "B13": ("Jedrska",       "#8b5cf6", ""),
        "B14": ("Jedrska",       "#8b5cf6", ""),
        "B15": ("Ostalo",        "#6b7280", ""),
        "B16": ("Solar",         "#fbbf24", ""),
        "B17": ("Odpadki",       "#64748b", ""),
        "B18": ("Veter offshore","#4ecdc4", ""),
        "B19": ("Veter onshore", "#4ecdc4", ""),
        "B20": ("Ostalo",        "#6b7280", ""),
    }

    # Ključni viri za hourly graf
    HOURLY_SOURCES = {"B14":"Jedrska","B11":"Hidro pretočna","B16":"Solar","B04":"Plin","B02":"Lignit"}
    HOURLY_COLORS  = {"B14":"#8b5cf6","B11":"#2563eb","B16":"#fbbf24","B04":"#f59e0b","B02":"#92400e"}

    now = datetime.utcnow()
    ps = now.strftime("%Y%m%d0000")
    pe = (now + timedelta(days=1)).strftime("%Y%m%d0000")

    try:
        r = requests.get("https://web-api.tp.entsoe.eu/api", params={
            "securityToken": ENTSO_TOKEN,
            "documentType": "A75",
            "processType": "A16",
            "in_Domain": "10YSI-ELES-----O",
            "periodStart": ps, "periodEnd": pe,
        }, timeout=15)
        root = ET.fromstring(r.text)
        ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}

        sources = {}
        hourly = defaultdict(lambda: defaultdict(list))  # source → position → [vals]

        for ts in root.findall(".//ns:TimeSeries", ns):
            psr = ts.find(".//ns:psrType", ns)
            points = ts.findall(".//ns:Point", ns)
            if psr is None or not points: continue
            code = psr.text
            vals = []
            for p in points:
                qty = p.find("ns:quantity", ns)
                pos = p.find("ns:position", ns)
                if qty is not None and pos is not None:
                    vals.append(float(qty.text))
                    # Shrani hourly za ključne vire
                    if code in HOURLY_SOURCES:
                        hourly[code][int(pos.text)].append(float(qty.text))
            if not vals: continue
            avg = sum(vals)/len(vals)
            if avg < 1: continue
            name, color, icon = PSR_NAMES.get(code, (code, "#6b7280", ""))
            if name in sources:
                sources[name]["mw"] += avg
            else:
                sources[name] = {"mw": avg, "color": color, "icon": icon, "code": code}

        # Pripravi hourly DataFrame podatke
        hourly_rows = []
        for code, pos_vals in hourly.items():
            name = HOURLY_SOURCES[code]
            color = HOURLY_COLORS[code]
            for pos, vals in sorted(pos_vals.items()):
                hourly_rows.append({
                    "Pozicija": pos,
                    "Vir": name,
                    "MW": sum(vals)/len(vals),
                    "Color": color
                })

        return sorted(sources.items(), key=lambda x: x[1]["mw"], reverse=True), hourly_rows
    except:
        return [], []

@st.cache_data(ttl=300)
def fetch_commodities():
    out = {}
    for name, code in [("TTF","DUTCH_TTF_EUR"),("EUA","EU_CARBON_EUR"),("COAL","COAL_USD")]:
        try:
            r = requests.get("https://api.oilpriceapi.com/v1/prices/latest",
                params={"by_code":code}, headers={"Authorization":"Token "+OILPRICE_TOKEN}, timeout=10)
            d = r.json()
            out[name] = d["data"]["price"] if d.get("status")=="success" else None
        except: out[name] = None
    return out

@st.cache_data(ttl=3600)
def fetch_storage():
    # GIE javni CSV download
    try:
        r = requests.get("https://agsi.gie.eu/api/data/eu", params={"size": 2}, 
                        headers={"x-key": AGSI_KEY}, timeout=10)
        data = r.json().get("data", [])
        if data:
            e = data[0]
            fill = float(e.get("full", 0) or 0)
            prev = float(data[1].get("full", 0) or 0) if len(data) > 1 else fill
            return {"fill": fill, "date": e.get("gasDayStart", ""), "trend": fill - prev}
    except: pass
    # Fallback — direktni CSV
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        r = requests.get(
            f"https://agsi.gie.eu/api/data/eu?from={week_ago}&to={today}&size=3",
            headers={"x-key": AGSI_KEY}, timeout=10)
        data = r.json().get("data", [])
        if data:
            e = data[0]
            fill = float(e.get("full", 0) or 0)
            prev = float(data[1].get("full", 0) or 0) if len(data) > 1 else fill
            return {"fill": fill, "date": e.get("gasDayStart", ""), "trend": fill - prev}
    except: pass
    return None

@st.cache_data(ttl=300)
def fetch_power():
    from xml.etree import ElementTree as ET
    from collections import defaultdict

    now = datetime.now()
    # ENTSO-E objavi jutri cene ob ~13:00
    # Pred 13h: pokaži danes (že objavljene), po 13h: pokaži jutri
    if now.hour >= 13:
        target_start = now
        target_end   = now + timedelta(days=1)
        label_date   = now.strftime("%Y-%m-%d")
    else:
        target_start = now - timedelta(days=1)
        target_end   = now
        label_date   = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        r = requests.get("https://web-api.tp.entsoe.eu/api", params={
            "securityToken": ENTSO_TOKEN,
            "documentType":  "A44",
            "in_Domain":     "10YSI-ELES-----O",
            "out_Domain":    "10YSI-ELES-----O",
            "periodStart":   target_start.strftime("%Y%m%d0000"),
            "periodEnd":     target_end.strftime("%Y%m%d0000"),
        }, timeout=15)
        root = ET.fromstring(r.text)
        ns = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}
        raw = []
        for pt in root.findall(".//ns:Point", ns):
            val = pt.find("ns:price.amount", ns)
            pos = pt.find("ns:position", ns)
            if val is not None:
                raw.append(((int(pos.text)-1) % 24, float(val.text)))
        if raw:
            hour_vals = defaultdict(list)
            for h,v in raw: hour_vals[h].append(v)
            prices = sorted([(h, sum(vs)/len(vs)) for h,vs in hour_vals.items()])
            all_v  = [v for _,v in prices]
            peak_v = [v for h,v in prices if 9<=h<20]
            return {"country":"SI", "source":"ENTSO-E", "date": label_date,
                    "base": sum(all_v)/len(all_v),
                    "peak": sum(peak_v)/len(peak_v) if peak_v else sum(all_v)/len(all_v),
                    "min": min(all_v), "max": max(all_v), "hours": prices}
    except: pass
    # DE fallback iz SMARD
    try:
        yesterday=datetime.now()-timedelta(days=1)
        ts=int(yesterday.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()*1000)
        r=requests.get(f"https://www.smard.de/app/chart_data/4169/DE/4169_DE_quarterhour_{ts}.json",timeout=10)
        series=r.json().get("series",[])
        hourly={}
        for i,(ts_ms,v) in enumerate(series):
            if v is not None:
                h=i//4
                if h not in hourly: hourly[h]=[]
                hourly[h].append(v/10)
        hours=[(h,sum(vals)/len(vals)) for h,vals in sorted(hourly.items())]
        all_v=[v for _,v in hours]; peak_v=[v for h,v in hours if 9<=h<20]
        return {"country":"DE","base":sum(all_v)/len(all_v),"peak":sum(peak_v)/len(peak_v),
                "min":min(all_v),"max":max(all_v),"source":"SMARD","hours":hours,
                "date": yesterday.strftime("%Y-%m-%d")}
    except: return None

@st.cache_data(ttl=600)
def fetch_weather():
    try:
        r=requests.get("https://api.open-meteo.com/v1/forecast",params={
            "latitude":46.0569,"longitude":14.5058,
            "hourly":"temperature_2m,windspeed_10m,shortwave_radiation",
            "forecast_days":3,"timezone":"Europe/Ljubljana"},timeout=10)
        h=r.json().get("hourly",{}); times=h.get("time",[])
        return [{"time":times[i],
            "temp":h["temperature_2m"][i] if i<len(h.get("temperature_2m",[])) else None,
            "wind":h["windspeed_10m"][i] if i<len(h.get("windspeed_10m",[])) else None,
            "solar":h["shortwave_radiation"][i] if i<len(h.get("shortwave_radiation",[])) else None,
        } for i in range(len(times))]
    except: return []

def day_avg(data,date_str):
    dan=[h for h in data if h["time"].startswith(date_str)]
    if not dan: return None
    temps=[h["temp"] for h in dan if h["temp"] is not None]
    winds=[h["wind"] for h in dan if h["wind"] is not None]
    solars=[h["solar"] for h in dan if h["solar"] is not None]
    peak_t=[h["temp"] for h in dan if h["temp"] is not None and 9<=int(h["time"][11:13])<20]
    return {"avg":sum(temps)/len(temps) if temps else None,
            "peak_t":sum(peak_t)/len(peak_t) if peak_t else None,
            "min":min(temps) if temps else None,"max":max(temps) if temps else None,
            "wind":sum(winds)/len(winds) if winds else None,
            "solar":sum(solars)/len(solars) if solars else None}

def coal_eur(usd): return (usd/EUR_USD)/COAL_DIV
def css(p,ttf,eua): return p-ttf/GAS_EFF-eua*GAS_EM
def cds(p,c,eua): return p-coal_eur(c)/COAL_EFF-eua*COAL_EM

# ── FETCH ALL ─────────────────────────────────────────────────────────────────
with st.spinner(""):
    comm=fetch_commodities(); storage=fetch_storage()
    power=fetch_power(); weather=fetch_weather()

ttf=comm.get("TTF"); eua=comm.get("EUA"); coal=comm.get("COAL"); now=datetime.now()

# ── NAV ───────────────────────────────────────────────────────────────────────
col_nav, col_refresh = st.columns([10,1])
with col_nav:
    entso_ok = power and power.get("source")=="ENTSO-E"
    st.markdown(f"""<div class="nav">
        <div class="nav-logo"><span>Energy</span>&nbsp;Trading Dashboard</div>
        <span class="nav-item-active">Overview</span>
        <span class="nav-item">Spreads</span>
        <span class="nav-item">Forecast</span>
        <span class="nav-item">Storage</span>
        <div class="nav-right">
            <span class="nav-time">{now.strftime('%a %d %b %Y · %H:%M')}</span>
            <span class="nav-badge">{'SI · LIVE' if entso_ok else 'DE · FALLBACK'}</span>
        </div>
    </div>""", unsafe_allow_html=True)
with col_refresh:
    st.markdown('<div style="padding-top:8px">', unsafe_allow_html=True)
    if st.button("↺ Refresh"): st.cache_data.clear(); st.rerun()

# ── STATS BAR ─────────────────────────────────────────────────────────────────
ttf_s  = f"€{ttf:.2f}"   if ttf  else "—"
eua_s  = f"€{eua:.2f}"   if eua  else "—"
coal_s = f"${coal:.1f}"  if coal else "—"
coal_e = f"€{coal_eur(coal):.1f}" if coal else "—"
base_s = f"€{power['base']:.2f}" if power else "—"
peak_s = f"€{power['peak']:.2f}" if power else "—"
stor_s = f"{storage['fill']:.1f}%" if storage else "—"

srmc_g = ttf/GAS_EFF+eua*GAS_EM if ttf and eua else None
srmc_c = coal_eur(coal)/COAL_EFF+eua*COAL_EM if coal and eua else None
margin_fuel = "GAS" if srmc_g and srmc_c and srmc_g<srmc_c else "COAL" if srmc_c else "—"

st.markdown(f"""<div class="stats-bar">
    <div class="stat-item"><div class="stat-label">TTF Gas</div><div class="stat-value">{ttf_s}</div></div>
    <div class="stat-divider"></div>
    <div class="stat-item"><div class="stat-label">EUA CO₂</div><div class="stat-value">{eua_s}</div></div>
    <div class="stat-divider"></div>
    <div class="stat-item"><div class="stat-label">Coal ARA</div><div class="stat-value">{coal_s} <span style="color:#64748b;font-size:11px">= {coal_e}/MWh</span></div></div>
    <div class="stat-divider"></div>
    <div class="stat-item"><div class="stat-label">Power Base · {power['country'] if power else '—'}</div><div class="stat-value stat-{'pos' if power and power['base']>50 else 'neg' if power and power['base']<20 else 'value'}">{base_s}</div></div>
    <div class="stat-item"><div class="stat-label">Power Peak</div><div class="stat-value">{peak_s}</div></div>
    <div class="stat-divider"></div>
    <div class="stat-item"><div class="stat-label">EU Storage</div><div class="stat-value {'stat-neg' if storage and storage['fill']<40 else 'stat-pos'}">{stor_s}</div></div>
    <div class="stat-divider"></div>
    <div class="stat-item"><div class="stat-label">Marginal Fuel</div><div class="stat-value" style="color:#4ecdc4">{margin_fuel}</div></div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Spreads & Margins", "Forecast", "Arbitrage", "Generation"])

# ════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    # CHART + RIGHT PANELS
    col_chart, col_right = st.columns([2, 1])

    with col_chart:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        src = power['country']+' · '+power['source'] if power else 'n/a'
        st.markdown(f'<div class="chart-title">Intraday Power Price <span style="color:#64748b;font-weight:400;font-size:12px">· {src} · {(datetime.now()-timedelta(days=1)).strftime("%d %b %Y")}</span></div>', unsafe_allow_html=True)

        if power and power.get("hours"):
            try:
                import pandas as pd, altair as alt
                hours_data=power["hours"]
                avg_p=sum(v for _,v in hours_data)/len(hours_data)
                df=pd.DataFrame(hours_data,columns=["Hour","EUR/MWh"])
                df["Label"]=df["Hour"].apply(lambda x:f"{x:02d}:00")
                df["Color"]=df["EUR/MWh"].apply(lambda v:"#4ecdc4" if v>=avg_p else "#fc5c7d")
                df["Above"]=df["EUR/MWh"].apply(lambda v:"Above avg" if v>=avg_p else "Below avg")

                bars=alt.Chart(df).mark_bar(cornerRadiusTopLeft=3,cornerRadiusTopRight=3,size=22).encode(
                    x=alt.X("Label:O",sort=None,axis=alt.Axis(labelColor="#475569",tickColor="#1e2330",
                            domainColor="#1e2330",labelFontSize=11,labelFont="DM Mono",title=None,labelAngle=0)),
                    y=alt.Y("EUR/MWh:Q",axis=alt.Axis(labelColor="#475569",gridColor="#1e2330",
                            domainColor="#1e2330",labelFontSize=11,labelFont="DM Mono",title="EUR/MWh",titleColor="#475569")),
                    color=alt.Color("Color:N",scale=None,legend=None),
                    tooltip=[alt.Tooltip("Label:O",title="Ura"),alt.Tooltip("EUR/MWh:Q",format=".2f")]
                ).properties(height=220)

                rule=alt.Chart(pd.DataFrame({"avg":[avg_p]})).mark_rule(
                    color="#ffffff",strokeDash=[4,4],strokeWidth=1,opacity=0.3
                ).encode(y="avg:Q")

                st.altair_chart((bars+rule).properties(background="#111318").configure_view(stroke=None), use_container_width=True)
                st.markdown(f'<div style="font-size:11px;color:#64748b;margin-top:-8px">Povprečje: <span style="color:#94a3b8;font-weight:600">€{avg_p:.2f}/MWh</span> &nbsp;·&nbsp; Min: <span style="color:#fc5c7d">€{power["min"]:.2f}</span> &nbsp;·&nbsp; Max: <span style="color:#4ecdc4">€{power["max"]:.2f}</span></div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div style="color:#fc5c7d;font-size:11px;padding:20px 0">{str(e)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#475569;font-size:12px;padding:40px 0;text-align:center">Ni podatkov za graf</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # GAS STORAGE
        st.markdown('<div class="panel-card" style="margin-bottom:12px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">EU Gas Storage <span class="panel-date">AGSI+</span></div>', unsafe_allow_html=True)
        if storage:
            f=storage["fill"]; t=storage["trend"]
            col={"#4ecdc4" if f>=50 else "#f59e0b" if f>=30 else "#fc5c7d"}
            fill_color="#4ecdc4" if f>=50 else "#f59e0b" if f>=30 else "#fc5c7d"
            signal="Bearish TTF" if f>=50 else "Neutral" if f>=40 else "Bullish TTF"
            sig_col="#fc5c7d" if f<40 else "#64748b" if f<50 else "#4ecdc4"
            st.markdown(f"""
            <div class="big-num" style="color:{fill_color}">{f:.1f}%</div>
            <div class="big-sub">{storage['date']} &nbsp;
                <span style="color:{'#4ecdc4' if t>=0 else '#fc5c7d'}">{'▲' if t>=0 else '▼'} {abs(t):.2f}%</span>
            </div>
            <div class="prog-wrap"><div class="prog-fill" style="width:{min(f,100):.0f}%;background:{fill_color}40;border:1px solid {fill_color}60"></div></div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#475569"><span>0%</span><span>Sezona: 45%</span><span>100%</span></div>
            <div style="margin-top:10px;font-size:11px;font-weight:600;color:{sig_col}">{'🔴' if f<40 else '🟡' if f<50 else '🟢'} {signal}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#475569;font-size:12px">Ni podatkov</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # MORNING BRIEFING
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Morning Briefing</div>', unsafe_allow_html=True)
        briefs=[]
        if storage:
            f=storage["fill"]
            briefs.append(("🔴" if f<40 else "🟢", f"Storage {f:.1f}% — {'bearish' if f>=50 else 'bullish'} za TTF"))
        if srmc_g and srmc_c and power:
            diff=abs(srmc_g-srmc_c)
            briefs.append(("⚡", f"Marginal: {margin_fuel} · gap €{diff:.1f}/MWh"))
            bp=power["base"]
            briefs.append(("📊", f"Power €{bp:.1f} · {'renewables dom.' if bp<30 else 'normalen trg' if bp<80 else 'supply crunch!'}"))
        jutri_s=str((now+timedelta(days=1)).date())
        dj=day_avg(weather,jutri_s)
        if dj and dj["avg"]:
            t=dj["avg"]
            briefs.append(("🌡", f"Jutri {t:.1f}°C · demand {'+' if t<15 else '='}{(15-t)*1.5:.0f}% vs baza" if t<15 else f"Jutri {t:.1f}°C · normalen demand"))

        brief_html="".join([f'<div class="brief-item"><span>{ico}</span><span>{txt}</span></div>' for ico,txt in briefs])
        st.markdown(brief_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # BOTTOM ROW — spreads + weather
    col_s1, col_s2, col_wx = st.columns(3)

    if ttf and eua and coal and power:
        bp=power["base"]; pp=power.get("peak") or bp
        srmc_g2 = ttf/GAS_EFF + eua*GAS_EM
        srmc_c2 = coal_eur(coal)/COAL_EFF + eua*COAL_EM
        css_b=css(bp,ttf,eua); css_p=css(pp,ttf,eua)
        cds_b=cds(bp,coal,eua); cds_p=cds(pp,coal,eua)

        def s_row(name, val):
            pos=val>=0
            vcls="spread-val-pos" if pos else "spread-val-neg"
            bcls="spread-badge-pos" if pos else "spread-badge-neg"
            badge="IN ●" if pos else "OUT ●"
            sign="+" if pos else ""
            return f'<div class="spread-row"><span class="spread-name">{name}</span><div style="display:flex;align-items:center;gap:8px"><span class="{vcls}">{sign}{val:.1f}</span><span class="{bcls}">{badge}</span></div></div>'

        with col_s1:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Clean Spark Spread <span class="panel-date">Gas 50%</span></div>
                {s_row("CSS · Base", css_b)}
                {s_row("CSS · Peak", css_p)}
                <div style="margin-top:10px;font-size:11px;color:#64748b">SRMC Gas: <span style="color:#94a3b8;font-weight:600">€{srmc_g2:.1f}/MWh</span></div>
            </div>""", unsafe_allow_html=True)

        with col_s2:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Clean Dark Spread <span class="panel-date">Coal 40%</span></div>
                {s_row("CDS · Base", cds_b)}
                {s_row("CDS · Peak", cds_p)}
                <div style="margin-top:10px;font-size:11px;color:#64748b">SRMC Coal: <span style="color:#94a3b8;font-weight:600">€{srmc_c2:.1f}/MWh</span></div>
            </div>""", unsafe_allow_html=True)
    else:
        with col_s1:
            st.markdown('<div class="panel-card"><div style="color:#475569;font-size:12px">Ni podatkov</div></div>', unsafe_allow_html=True)
        with col_s2:
            st.markdown('<div class="panel-card"><div style="color:#475569;font-size:12px">Ni podatkov</div></div>', unsafe_allow_html=True)

    with col_wx:
        today_s=str(now.date()); jutri_s2=str((now+timedelta(days=1)).date()); poj_s=str((now+timedelta(days=2)).date())
        wx_rows=""
        for label, dat in [("Danes",today_s),("Jutri",jutri_s2),("Pojutri",poj_s)]:
            d=day_avg(weather,dat)
            if not d: continue
            t=d["avg"]; w=d["wind"]; s=d["solar"]
            if t and t<15:
                badge=f'<span class="wx-badge-bull">▲ +{(15-t)*1.5:.0f}%</span>'
            elif t and t>22:
                badge=f'<span class="wx-badge-bull">▲ +{(t-22)*0.8:.0f}%</span>'
            else:
                badge='<span class="wx-badge-neut">Normal</span>'
            if w and w>20: badge+=f' <span class="wx-badge-bear">Wind</span>'
            if s and s>150: badge+=f' <span class="wx-badge-bear">Solar</span>'
            wx_rows+=f'''<div class="wx-row">
                <span class="wx-date" style="width:70px">{label}<br><span style="color:#475569;font-size:10px">{dat}</span></span>
                <span style="width:70px;text-align:right;color:#f1f5f9;font-size:14px;font-weight:600;font-family:DM Mono,monospace">{t:.1f}°C</span>
                <span style="flex:1;text-align:right">{badge}</span>
            </div>'''

        st.markdown(f"""<div class="panel-card">
            <div class="panel-title">Weather · Ljubljana <span class="panel-date">Open-Meteo</span></div>
            {wx_rows}
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2 — SPREADS
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    if not (ttf and eua and coal and power):
        st.markdown('<div style="color:#475569;padding:20px">Ni dovolj podatkov.</div>', unsafe_allow_html=True)
    else:
        bp=power["base"]; pp=power.get("peak") or bp
        ce=coal_eur(coal); diff=abs(srmc_g-srmc_c)
        css_b=css(bp,ttf,eua); css_p=css(pp,ttf,eua)
        cds_b=cds(bp,coal,eua); cds_p=cds(pp,coal,eua)
        ttf_switch=ttf-diff*GAS_EFF; eua_switch=eua-diff/(COAL_EM-GAS_EM)

        ca,cb,cc = st.columns(3)

        def detail_row(k,v,color="#94a3b8"):
            return f'<div class="spread-row"><span style="color:#475569;font-size:12px">{k}</span><span style="color:{color};font-size:13px;font-weight:600;font-family:DM Mono,monospace">{v}</span></div>'

        with ca:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Clean Spark Spread</div>
                <div style="font-size:11px;color:#475569;margin-bottom:12px">CSS = Power − (TTF ÷ η) − (EUA × 0.37)</div>
                {detail_row("TTF", f"€{ttf:.2f}/MWh")}
                {detail_row("Efficiency η", "50%")}
                {detail_row("Fuel cost", f"€{ttf/GAS_EFF:.2f}/MWh")}
                {detail_row("Carbon cost", f"€{eua*GAS_EM:.2f}/MWh")}
                {detail_row("SRMC Gas", f"€{srmc_g:.2f}/MWh")}
                {detail_row("CSS Base", f"{'+' if css_b>=0 else ''}€{css_b:.2f}", '#4ecdc4' if css_b>=0 else '#fc5c7d')}
                {detail_row("CSS Peak", f"{'+' if css_p>=0 else ''}€{css_p:.2f}", '#4ecdc4' if css_p>=0 else '#fc5c7d')}
            </div>""", unsafe_allow_html=True)

        with cb:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Clean Dark Spread</div>
                <div style="font-size:11px;color:#475569;margin-bottom:12px">CDS = Power − (Coal ÷ η) − (EUA × 0.83)</div>
                {detail_row("Coal ARA", f"${coal:.1f}/t")}
                {detail_row("Coal thermal", f"€{ce:.2f}/MWh")}
                {detail_row("Efficiency η", "40%")}
                {detail_row("Fuel cost", f"€{ce/COAL_EFF:.2f}/MWh")}
                {detail_row("Carbon cost", f"€{eua*COAL_EM:.2f}/MWh")}
                {detail_row("SRMC Coal", f"€{srmc_c:.2f}/MWh")}
                {detail_row("CDS Base", f"{'+' if cds_b>=0 else ''}€{cds_b:.2f}", '#4ecdc4' if cds_b>=0 else '#fc5c7d')}
                {detail_row("CDS Peak", f"{'+' if cds_p>=0 else ''}€{cds_p:.2f}", '#4ecdc4' if cds_p>=0 else '#fc5c7d')}
            </div>""", unsafe_allow_html=True)

        with cc:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Fuel Switch Analysis</div>
                {detail_row("Marginal fuel", margin_fuel, '#4ecdc4')}
                {detail_row("Gap", f"€{diff:.1f}/MWh")}
                {detail_row("TTF switch level", f"€{ttf_switch:.1f}/MWh")}
                {detail_row("EUA switch level", f"€{eua_switch:.1f}/t")}
                <div style="height:16px"></div>
                <div class="panel-title">EUA Sensitivity</div>
                {detail_row("+€10 EUA → Gas", f"+€{10*GAS_EM:.1f}/MWh")}
                {detail_row("+€10 EUA → Coal", f"+€{10*COAL_EM:.1f}/MWh")}
                {detail_row("Coal exposure", f"{COAL_EM/GAS_EM:.1f}x višja", '#fc5c7d')}
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 3 — FORECAST
# ════════════════════════════════════════════
with tab3:
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    today_s=str(now.date()); jutri_s3=str((now+timedelta(days=1)).date()); poj_s3=str((now+timedelta(days=2)).date())

    for label,dat in [("Danes",today_s),("Jutri",jutri_s3),("Pojutri",poj_s3)]:
        d=day_avg(weather,dat)
        if not d: continue
        t=d["avg"]; w=d["wind"]; s=d["solar"]

        if t and t<15: delta=(15-t)*1.5; dsig=f"+{delta:.0f}% demand"; dlbl="Ogrevanje aktivno"; dcol="#4ecdc4"
        elif t and t>22: delta=(t-22)*0.8; dsig=f"+{delta:.0f}% demand"; dlbl="Hlajenje aktivno"; dcol="#4ecdc4"
        else: delta=0; dsig="Normalna poraba"; dlbl="Komfortna temperatura"; dcol="#64748b"

        w_sig="Bearish — veter pritiska" if w and w>20 else "Minimalen vpliv"
        s_sig="Bearish — solar cannibalization 10–15h" if s and s>150 else "Minimalen vpliv"
        overall = "🔴 BULLISH" if t<15 and (not w or w<20) and (not s or s<150) else "🟡 MEŠAN" if t<15 else "🟢 BEARISH/NEVTRALEN"
        o_col = "#fc5c7d" if "BULLISH" in overall else "#f59e0b" if "MEŠAN" in overall else "#4ecdc4"

        c1f,c2f,c3f,c4f = st.columns(4)
        with c1f:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">{label} <span class="panel-date">{dat}</span></div>
                <div class="big-num">{t:.1f}°C</div>
                <div class="big-sub">min {d['min']:.1f}° · max {d['max']:.1f}°<br>peak {d['peak_t']:.1f}°C (9–20h)</div>
                <div style="margin-top:8px;font-size:11px;font-weight:600;color:{dcol}">{dlbl}</div>
                <div style="font-size:11px;color:#64748b">{dsig}</div>
            </div>""", unsafe_allow_html=True)
        with c2f:
            mw=int(1400*(1+delta/100))
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Demand Signal</div>
                <div class="big-num" style="color:{dcol}">{mw} MW</div>
                <div class="big-sub">Ocena SI (baza: 1400 MW)</div>
                <div style="margin-top:8px">
                    <div class="prog-wrap"><div class="prog-fill" style="width:{min(mw/1400*50+50,100):.0f}%;background:{dcol}40;border:1px solid {dcol}60"></div></div>
                </div>
                <div style="font-size:11px;color:#64748b;margin-top:4px">HDD: {max(0,18-t):.1f} · CDD: {max(0,t-18):.1f}</div>
            </div>""", unsafe_allow_html=True)
        with c3f:
            w_val = f"{w:.0f}" if w else "0"
            w_col = '#fc5c7d' if w and w>20 else '#64748b'
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Wind Signal</div>
                <div class="big-num" style="color:{w_col}">{w_val} km/h</div>
                <div class="big-sub">Povprečna hitrost</div>
                <div style="margin-top:8px;font-size:11px;color:{w_col}">{w_sig}</div>
            </div>""", unsafe_allow_html=True)
        with c4f:
            s_val = f"{s:.0f}" if s else "0"
            s_col = '#fc5c7d' if s and s>150 else '#64748b'
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Solar Signal</div>
                <div class="big-num" style="color:{s_col}">{s_val} W/m²</div>
                <div class="big-sub">Povprečno sevanje</div>
                <div style="margin-top:8px;font-size:11px;color:{s_col}">{s_sig}</div>
                <div style="margin-top:8px;font-size:12px;font-weight:700;color:{o_col}">{overall}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 4 — ARBITRAGE
# ════════════════════════════════════════════
with tab4:
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    with st.spinner("Fetching evropske cene..."):
        all_countries = fetch_all_countries()

    if not all_countries:
        st.markdown('<div style="color:#475569;padding:20px">Ni podatkov.</div>', unsafe_allow_html=True)
    else:
        si = next((c for c in all_countries if c["country"]=="SI"), None)
        si_base = si["base"] if si else None

        # BAR CHART
        st.markdown('<div class="panel-card" style="margin-bottom:16px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Day-Ahead Cene · Evropa <span class="panel-date">od najcenejše do najdražje</span></div>', unsafe_allow_html=True)
        try:
            import pandas as pd, altair as alt
            df = pd.DataFrame([{"Država": c["country"], "EUR": round(c["base"],2)} for c in all_countries])
            df["Color"] = df["Država"].apply(lambda v: "#4ecdc4" if v=="SI" else "#334155")
            bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4,cornerRadiusTopRight=4,size=40).encode(
                x=alt.X("Država:O",sort=None,axis=alt.Axis(labelColor="#94a3b8",tickColor="#1e2330",
                        domainColor="#1e2330",labelFontSize=13,labelFont="DM Mono",title=None)),
                y=alt.Y("EUR:Q",axis=alt.Axis(labelColor="#475569",gridColor="#1e2330",
                        domainColor="#1e2330",labelFontSize=11,labelFont="DM Mono",title="€/MWh",titleColor="#475569")),
                color=alt.Color("Color:N",scale=None,legend=None),
                tooltip=[alt.Tooltip("Država:O"),alt.Tooltip("EUR:Q",format=".2f",title="€/MWh")]
            ).properties(height=220)
            text = bars.mark_text(dy=-10,color="#94a3b8",fontSize=12,font="DM Mono").encode(
                text=alt.Text("EUR:Q",format=".0f"))
            st.altair_chart((bars+text).properties(background="#111318").configure_view(stroke=None),use_container_width=True)
            st.markdown('<div style="font-size:11px;color:#64748b;margin-top:-8px">🟢 Teal = Slovenija</div>',unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div style="color:#fc5c7d;font-size:11px">{e}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

        # SPREADI + RANKING
        col_arb1, col_arb2 = st.columns([3,2])

        with col_arb1:
            st.markdown('<div class="panel-card">',unsafe_allow_html=True)
            st.markdown('<div class="panel-title">SI Arbitraža Spreadi <span class="panel-date">pozitiven = SI dražji</span></div>',unsafe_allow_html=True)
            if si_base:
                for c in sorted(all_countries, key=lambda x: x["base"], reverse=True):
                    if c["country"]=="SI": continue
                    spread = si_base - c["base"]
                    color = "#fc5c7d" if spread>0 else "#4ecdc4"
                    sign = "+" if spread>0 else ""
                    tip = f"Kupuj {c['country']}, prodaj SI" if spread>0 else f"Kupuj SI, prodaj {c['country']}"
                    tip_col = "#fc5c7d20" if spread>0 else "#4ecdc420"
                    tip_tcol = "#fc5c7d" if spread>0 else "#4ecdc4"
                    st.markdown(f"""<div class="spread-row">
                        <span style="color:#94a3b8;font-size:13px;font-weight:700;width:35px;display:inline-block">{c['country']}</span>
                        <span style="color:#475569;font-size:12px;flex:1;font-family:DM Mono,monospace">€{c['base']:.1f}</span>
                        <span style="color:{color};font-size:15px;font-weight:700;font-family:DM Mono,monospace;width:75px;text-align:right">{sign}{spread:.1f}</span>
                        <span style="background:{tip_col};color:{tip_tcol};border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600;margin-left:10px">{tip}</span>
                    </div>""",unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:10px;font-size:11px;color:#64748b">SI referenca: <span style="color:#4ecdc4;font-weight:600">€{si_base:.2f}/MWh</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        with col_arb2:
            st.markdown('<div class="panel-card">',unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Ranking · Najcenejša → Najdražja</div>',unsafe_allow_html=True)
            for i,c in enumerate(all_countries):
                is_si = c["country"]=="SI"
                col = "#4ecdc4" if is_si else "#f59e0b" if i==0 else "#94a3b8"
                bg = "background:#4ecdc412;border-radius:6px;padding:0 4px;" if is_si else ""
                pk = f"€{c['peak']:.0f}pk" if c.get('peak') else ""
                st.markdown(f"""<div class="spread-row" style="{bg}">
                    <span style="color:#334155;font-size:11px;width:22px">#{i+1}</span>
                    <span style="color:{col};font-size:13px;font-weight:700;width:32px">{c['country']}</span>
                    <span style="color:#f1f5f9;font-size:14px;font-weight:600;font-family:DM Mono,monospace;flex:1;text-align:right">€{c['base']:.1f}</span>
                    <span style="color:#475569;font-size:10px;margin-left:8px;font-family:DM Mono,monospace">{pk}</span>
                </div>""",unsafe_allow_html=True)
            if len(all_countries)>=2:
                cheap=all_countries[0]; pricey=all_countries[-1]
                max_arb=pricey["base"]-cheap["base"]
                st.markdown(f"""<div style="margin-top:12px;padding:10px;background:#4ecdc412;border:1px solid #4ecdc430;border-radius:8px">
                    <div style="font-size:10px;color:#64748b;font-weight:600;letter-spacing:0.06em;text-transform:uppercase">Max arbitraža danes</div>
                    <div style="font-size:22px;font-weight:700;color:#4ecdc4;font-family:DM Mono,monospace;margin-top:2px">€{max_arb:.1f}/MWh</div>
                    <div style="font-size:11px;color:#64748b;margin-top:2px">{cheap['country']} €{cheap['base']:.0f} → {pricey['country']} €{pricey['base']:.0f}</div>
                </div>""",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 5 — GENERATION MIX
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    with st.spinner("Fetching SI generation data..."):
        gen_data, hourly_rows = fetch_generation()

    if not gen_data:
        st.markdown('<div style="color:#475569;padding:20px">Ni podatkov.</div>', unsafe_allow_html=True)
    else:
        total_mw = sum(v["mw"] for _,v in gen_data)
        renewable = sum(v["mw"] for _,v in gen_data if v["code"] in ["B16","B18","B19","B11","B09","B10","B06"])
        nuclear   = sum(v["mw"] for _,v in gen_data if v["code"] in ["B13","B14"])
        fossil    = sum(v["mw"] for _,v in gen_data if v["code"] in ["B02","B03","B04","B05"])

        col_g1, col_g2, col_g3 = st.columns(3)

        with col_g1:
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">Skupna Produkcija · SI <span class="panel-date">ENTSO-E</span></div>
                <div class="big-num">{total_mw:.0f} <span style="font-size:18px;color:#64748b">MW</span></div>
                <div class="big-sub">Danes · {now.strftime('%d %b %Y')}</div>
                <div style="height:12px"></div>
                <div class="spread-row"><span style="color:#4ecdc4;font-size:12px">Obnovljivi</span><span style="color:#4ecdc4;font-weight:700;font-family:DM Mono,monospace">{renewable:.0f} MW · {renewable/total_mw*100:.0f}%</span></div>
                <div class="spread-row"><span style="color:#8b5cf6;font-size:12px">Jedrska</span><span style="color:#8b5cf6;font-weight:700;font-family:DM Mono,monospace">{nuclear:.0f} MW · {nuclear/total_mw*100:.0f}%</span></div>
                <div class="spread-row"><span style="color:#f59e0b;font-size:12px">Fosilna</span><span style="color:#f59e0b;font-weight:700;font-family:DM Mono,monospace">{fossil:.0f} MW · {fossil/total_mw*100:.0f}%</span></div>
            </div>""", unsafe_allow_html=True)

        with col_g2:
            co2_factors = {"B02":1.0,"B03":0.9,"B04":0.4,"B05":0.65,"B14":0.02,"B13":0.02,
                          "B16":0.04,"B19":0.01,"B18":0.01,"B11":0.01,"B10":0.01,"B01":0.23}
            co2_total = sum(v["mw"] * co2_factors.get(v["code"],0.1) for _,v in gen_data)
            co2_intensity = co2_total / total_mw if total_mw else 0
            co2_col = "#4ecdc4" if co2_intensity<0.2 else "#f59e0b" if co2_intensity<0.4 else "#fc5c7d"
            co2_label = "Nizka 🟢" if co2_intensity<0.2 else "Srednja 🟡" if co2_intensity<0.4 else "Visoka 🔴"
            st.markdown(f"""<div class="panel-card">
                <div class="panel-title">CO₂ Intenzivnost</div>
                <div class="big-num" style="color:{co2_col}">{co2_intensity*1000:.0f}</div>
                <div class="big-sub">gCO₂/kWh · {co2_label}</div>
                <div style="margin-top:10px">
                    <div class="prog-wrap"><div class="prog-fill" style="width:{min(co2_intensity/0.6*100,100):.0f}%;background:{co2_col}40;border:1px solid {co2_col}60"></div></div>
                </div>
                <div style="font-size:11px;color:#64748b;margin-top:8px">EU avg ~300 gCO₂/kWh · SI danes {co2_label}</div>
            </div>""", unsafe_allow_html=True)

        with col_g3:
            solar_mw  = next((v["mw"] for _,v in gen_data if v["code"]=="B16"), 0)
            wind_mw   = sum(v["mw"] for _,v in gen_data if v["code"] in ["B18","B19"])
            hydro_mw  = sum(v["mw"] for _,v in gen_data if v["code"] in ["B09","B10","B11"])
            signals = []
            if solar_mw>200: signals.append(("Solar",  f"{solar_mw:.0f} MW", "bearish — tlači peak", "#fc5c7d"))
            else:            signals.append(("Solar",  f"{solar_mw:.0f} MW", "bullish", "#4ecdc4"))
            if wind_mw>100:  signals.append(("Veter",  f"{wind_mw:.0f} MW", "bearish", "#fc5c7d"))
            else:            signals.append(("Veter",  f"{wind_mw:.0f} MW", "bullish", "#4ecdc4"))
            signals.append(("Krško",  f"{nuclear:.0f} MW", "online" if nuclear>600 else "redukcija!", "#8b5cf6" if nuclear>600 else "#fc5c7d"))
            signals.append(("Hidro",  f"{hydro_mw:.0f} MW", "visoko" if hydro_mw>400 else "nizko" if hydro_mw<200 else "normalno", "#3b82f6"))
            rows = "".join([f'<div class="spread-row"><span style="color:#94a3b8;font-size:12px;flex:1">{il}</span><span style="color:{c};font-size:12px;font-weight:600;font-family:DM Mono,monospace">{mw}</span><span style="color:#475569;font-size:10px;margin-left:8px">{sig}</span></div>' for il,mw,sig,c in signals])
            st.markdown(f'<div class="panel-card"><div class="panel-title">Trading Signal iz Gen Mix</div>{rows}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        # BAR CHART
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Produkcija po Virih · MW</div>', unsafe_allow_html=True)
        try:
            import pandas as pd, altair as alt
            df = pd.DataFrame([{"Vir": f"{v['icon']} {name}", "MW": round(v['mw'],0), "Color": v['color']} for name,v in gen_data]).sort_values("MW",ascending=False)
            bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4,cornerRadiusTopRight=4,size=38).encode(
                x=alt.X("Vir:O",sort=None,axis=alt.Axis(labelColor="#94a3b8",tickColor="#1e2330",domainColor="#1e2330",labelFontSize=12,title=None)),
                y=alt.Y("MW:Q",axis=alt.Axis(labelColor="#475569",gridColor="#1e2330",domainColor="#1e2330",labelFontSize=11,labelFont="DM Mono",title="MW",titleColor="#475569")),
                color=alt.Color("Color:N",scale=None,legend=None),
                tooltip=[alt.Tooltip("Vir:O"),alt.Tooltip("MW:Q",format=".0f")]
            ).properties(height=220)
            text = bars.mark_text(dy=-10,color="#94a3b8",fontSize=12,font="DM Mono").encode(text=alt.Text("MW:Q",format=".0f"))
            st.altair_chart((bars+text).properties(background="#111318").configure_view(stroke=None),use_container_width=True)
        except Exception as e:
            st.markdown(f'<div style="color:#fc5c7d;font-size:11px">{e}</div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # HOURLY CHART
        if hourly_rows:
            st.markdown('<div class="panel-card" style="margin-top:12px">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Produkcija po Urah · MW <span class="panel-date">Jedrska · Hidro · Solar · Plin · Lignit</span></div>', unsafe_allow_html=True)
            try:
                import pandas as pd, altair as alt
                df_h = pd.DataFrame(hourly_rows)
                df_h["Label"] = df_h["Pozicija"].apply(lambda x: f"{x:02d}h")

                domain = ["Jedrska","Hidro pretočna","Solar","Plin","Lignit"]
                range_ = ["#8b5cf6","#2563eb","#fbbf24","#f59e0b","#92400e"]

                chart = alt.Chart(df_h).mark_line(strokeWidth=2, point=alt.OverlayMarkDef(size=40)).encode(
                    x=alt.X("Label:O", sort=None, axis=alt.Axis(labelColor="#94a3b8", tickColor="#1e2330",
                            domainColor="#1e2330", labelFontSize=11, labelFont="DM Mono", title=None)),
                    y=alt.Y("MW:Q", axis=alt.Axis(labelColor="#475569", gridColor="#1e2330",
                            domainColor="#1e2330", labelFontSize=11, labelFont="DM Mono", title="MW", titleColor="#475569")),
                    color=alt.Color("Vir:N", scale=alt.Scale(domain=domain, range=range_),
                                   legend=alt.Legend(orient="bottom", labelColor="#94a3b8", titleColor="#64748b",
                                                    labelFontSize=11, symbolSize=80, padding=10)),
                    tooltip=[alt.Tooltip("Label:O", title="Pozicija"), alt.Tooltip("Vir:N"), alt.Tooltip("MW:Q", format=".0f")]
                ).properties(height=220, background="#111318")

                st.altair_chart(chart.configure_view(stroke=None), use_container_width=True)
            except Exception as e:
                st.markdown(f'<div style="color:#fc5c7d;font-size:11px">{e}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # DETAJLNA TABELA
        st.markdown('<div class="panel-card" style="margin-top:12px">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Detajli po Virih</div>', unsafe_allow_html=True)
        for name,v in gen_data:
            pct = v["mw"]/total_mw*100
            st.markdown(f"""<div style="padding:6px 0;border-bottom:1px solid #1e2330">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="color:#94a3b8;font-size:13px">{v['icon']} {name}</span>
                    <span style="color:#f1f5f9;font-size:13px;font-weight:600;font-family:DM Mono,monospace">{v['mw']:.0f} MW &nbsp;<span style="color:#475569;font-size:11px">{pct:.1f}%</span></span>
                </div>
                <div style="background:#1e2330;border-radius:3px;height:4px">
                    <div style="width:{pct:.0f}%;height:4px;border-radius:3px;background:{v['color']}"></div>
                </div>
            </div>""",unsafe_allow_html=True)
        st.markdown(f'<div style="margin-top:10px;font-size:11px;color:#64748b">Skupaj: <span style="color:#f1f5f9;font-weight:600">{total_mw:.0f} MW</span></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)





st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown(f"""<div style="border-top:1px solid #1e2330;padding:8px 24px;font-size:10px;
    color:#334155;display:flex;justify-content:space-between;background:#0d0f14">
    <span>Data: oilpriceapi.com · AGSI+ GIE · SMARD.de · Open-Meteo · ENTSO-E</span>
    <span>Power: {power['country']+' · '+power['source'] if power else 'n/a'}</span>
    <span>Updated: {now.strftime('%H:%M:%S')}</span>
</div>""", unsafe_allow_html=True)