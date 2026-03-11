"""
dashboard.py — Energy Trading Dashboard
Bloomberg terminal stil v2
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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap');

* { font-family: 'IBM Plex Mono', monospace !important; }
html, body, [class*="css"] { background-color: #000 !important; color: #ddd; }
.stApp { background-color: #000 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* TOP BAR */
.top-bar {
    background: #0d0d0d;
    border-bottom: 2px solid #ff5500;
    padding: 5px 14px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.top-title { color: #fff; font-size: 15px; font-weight: 700; letter-spacing: 0.1em; }
.top-sub { color: #ff5500; font-size: 10px; letter-spacing: 0.15em; margin-left: 4px; }
.top-time { margin-left: auto; color: #aaa; font-size: 11px; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #0d0d0d !important;
    border-bottom: 1px solid #222 !important;
    gap: 0 !important;
    padding: 0 12px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #666 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 8px 16px !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #ff5500 !important;
    border-bottom: 2px solid #ff5500 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 12px !important; background: #000 !important; }

/* SECTION HEADER */
.sec-hdr {
    background: #ff5500;
    color: #000;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 6px;
    margin-top: 10px;
}

/* COMMODITY CELL */
.cell {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    border-top: 2px solid #ff5500;
    padding: 8px 10px;
    height: 80px;
}
.cell-lbl { color: #ff5500; font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 3px; }
.cell-val { font-size: 24px; font-weight: 700; color: #fff; line-height: 1.1; }
.cell-sub { font-size: 9px; color: #555; margin-top: 3px; }

/* SPREAD CELL */
.scell {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    border-left: 4px solid #333;
    padding: 8px 10px;
    height: 90px;
}
.scell-pos { border-left-color: #00ff44 !important; }
.scell-neg { border-left-color: #ff2222 !important; }
.scell-lbl { color: #666; font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 2px; }
.scell-val-pos { font-size: 26px; font-weight: 700; color: #00ff44; }
.scell-val-neg { font-size: 26px; font-weight: 700; color: #ff2222; }
.scell-status-pos { font-size: 9px; color: #00ff44; letter-spacing: 0.08em; }
.scell-status-neg { font-size: 9px; color: #ff2222; letter-spacing: 0.08em; }
.scell-sub { font-size: 9px; color: #444; margin-top: 3px; }

/* WEATHER */
.wcell {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    border-top: 2px solid #333;
    padding: 10px 12px;
}
.wcell-date { color: #ff5500; font-size: 10px; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 4px; }
.wcell-temp { font-size: 36px; font-weight: 700; color: #fff; line-height: 1; }
.wcell-sub  { font-size: 10px; color: #666; margin-top: 4px; line-height: 1.6; }
.badge-bull { background: #002211; color: #00ff44; border: 1px solid #00ff4433; padding: 2px 6px; font-size: 9px; letter-spacing: 0.08em; margin-right: 3px; }
.badge-bear { background: #220000; color: #ff2222; border: 1px solid #ff222233; padding: 2px 6px; font-size: 9px; margin-right: 3px; }
.badge-neut { background: #111100; color: #ff5500; border: 1px solid #ff550033; padding: 2px 6px; font-size: 9px; margin-right: 3px; }

/* BRIEFING */
.brief-row {
    background: #060606;
    border-left: 3px solid #ff5500;
    border-bottom: 1px solid #111;
    padding: 6px 10px;
    margin-bottom: 2px;
    font-size: 11px;
    color: #bbb;
    line-height: 1.5;
}

/* SPREAD DETAIL */
.detail-box {
    background: #060606;
    border: 1px solid #1e1e1e;
    padding: 14px;
    margin-bottom: 8px;
}
.detail-title { color: #ff5500; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 8px; }
.detail-row { display: flex; justify-content: space-between; padding: 3px 0; border-bottom: 1px solid #111; font-size: 11px; }
.detail-key { color: #666; }
.detail-val { color: #fff; font-weight: 600; }
.detail-val-pos { color: #00ff44; font-weight: 700; }
.detail-val-neg { color: #ff2222; font-weight: 700; }

/* BUTTON */
.stButton button {
    background: #0d0d0d !important;
    border: 1px solid #ff5500 !important;
    color: #ff5500 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    padding: 3px 12px !important;
    border-radius: 0 !important;
}

div[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── TOKENS ────────────────────────────────────────────────────────────────────
OILPRICE_TOKEN = "ee7f1e4afc476e3d40279cceb5676293f2c6b30a62cdd24ea5b9592a0e03f5c6"
AGSI_KEY       = "b26cf657bcbcd971d16eded061017e6d"
ENTSO_TOKEN    = "0e72f85a-2620-4a36-b812-c4cbfa17b4ec"

GAS_EFF=0.50; GAS_EM=0.37
COAL_EFF=0.40; COAL_EM=0.83
EUR_USD=1.08; COAL_DIV=8.14

# ── FETCH ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_commodities():
    out = {}
    for name, code in [("TTF","DUTCH_TTF_EUR"),("EUA","EU_CARBON_EUR"),("COAL","COAL_USD")]:
        try:
            r = requests.get("https://api.oilpriceapi.com/v1/prices/latest",
                params={"by_code": code},
                headers={"Authorization": "Token " + OILPRICE_TOKEN}, timeout=10)
            d = r.json()
            out[name] = d["data"]["price"] if d.get("status") == "success" else None
        except: out[name] = None
    return out

@st.cache_data(ttl=300)
def fetch_storage():
    for params in [{"type":"aggregated","size":2}, {"size":2}]:
        try:
            r = requests.get("https://agsi.gie.eu/api", params=params,
                headers={"x-key": AGSI_KEY}, timeout=10)
            entries = r.json().get("data", [])
            if not entries: continue
            e = entries[0]
            fill = float(e.get("full", 0) or 0)
            prev = float(entries[1].get("full", 0) or 0) if len(entries) > 1 else fill
            return {"fill": fill, "date": e.get("gasDayStart",""), "trend": fill-prev}
        except: continue
    return None

@st.cache_data(ttl=300)
def fetch_power():
    try:
        from entsoe import EntsoePandasClient
        import pandas as pd
        client = EntsoePandasClient(api_key=ENTSO_TOKEN)
        yesterday = pd.Timestamp(datetime.now().date() - timedelta(days=1), tz='UTC')
        today = pd.Timestamp(datetime.now().date(), tz='UTC')
        prices = client.query_day_ahead_prices('10YSI-ELES-----O', start=yesterday, end=today)
        all_v = prices.values.tolist()
        peak_v = prices.between_time('09:00','19:00').values.tolist()
        hours = [(prices.index[i].hour, float(prices.values[i])) for i in range(len(prices))]
        return {"country":"SI","base":sum(all_v)/len(all_v),"peak":sum(peak_v)/len(peak_v),
                "min":min(all_v),"max":max(all_v),"source":"ENTSO-E","hours":hours}
    except: pass
    try:
        yesterday = datetime.now() - timedelta(days=1)
        ts = int(yesterday.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()*1000)
        r = requests.get(f"https://www.smard.de/app/chart_data/4169/DE/4169_DE_quarterhour_{ts}.json", timeout=10)
        series = r.json().get("series",[])
        hourly = {}
        for i,(ts_ms,v) in enumerate(series):
            if v is not None:
                h = i//4
                if h not in hourly: hourly[h] = []
                hourly[h].append(v/10)
        hours = [(h, sum(vals)/len(vals)) for h,vals in sorted(hourly.items())]
        all_v = [v for _,v in hours]
        peak_v = [v for h,v in hours if 9<=h<20]
        return {"country":"DE*","base":sum(all_v)/len(all_v),"peak":sum(peak_v)/len(peak_v),
                "min":min(all_v),"max":max(all_v),"source":"SMARD","hours":hours}
    except: return None

@st.cache_data(ttl=600)
def fetch_weather():
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude":46.0569,"longitude":14.5058,
            "hourly":"temperature_2m,windspeed_10m,shortwave_radiation",
            "forecast_days":3,"timezone":"Europe/Ljubljana"}, timeout=10)
        h = r.json().get("hourly",{})
        times = h.get("time",[])
        return [{"time":times[i],
            "temp": h["temperature_2m"][i]     if i<len(h.get("temperature_2m",[])) else None,
            "wind": h["windspeed_10m"][i]       if i<len(h.get("windspeed_10m",[])) else None,
            "solar":h["shortwave_radiation"][i] if i<len(h.get("shortwave_radiation",[])) else None,
        } for i in range(len(times))]
    except: return []

def day_avg(data, date_str):
    dan = [h for h in data if h["time"].startswith(date_str)]
    if not dan: return None
    temps  = [h["temp"]  for h in dan if h["temp"]  is not None]
    winds  = [h["wind"]  for h in dan if h["wind"]  is not None]
    solars = [h["solar"] for h in dan if h["solar"] is not None]
    peak_t = [h["temp"]  for h in dan if h["temp"] is not None and 9<=int(h["time"][11:13])<20]
    return {"avg":sum(temps)/len(temps) if temps else None,
            "peak_t":sum(peak_t)/len(peak_t) if peak_t else None,
            "min":min(temps) if temps else None,"max":max(temps) if temps else None,
            "wind":sum(winds)/len(winds) if winds else None,
            "solar":sum(solars)/len(solars) if solars else None,
            "hours_temp": [(int(h["time"][11:13]), h["temp"]) for h in dan if h["temp"] is not None],
            "hours_solar": [(int(h["time"][11:13]), h["solar"]) for h in dan if h["solar"] is not None]}

def coal_eur(usd): return (usd/EUR_USD)/COAL_DIV
def css(p,ttf,eua): return p - ttf/GAS_EFF - eua*GAS_EM
def cds(p,coal_usd,eua): return p - coal_eur(coal_usd)/COAL_EFF - eua*COAL_EM

# ── FETCH ALL ─────────────────────────────────────────────────────────────────
with st.spinner(""):
    comm    = fetch_commodities()
    storage = fetch_storage()
    power   = fetch_power()
    weather = fetch_weather()

ttf  = comm.get("TTF")
eua  = comm.get("EUA")
coal = comm.get("COAL")
now  = datetime.now()

# ── TOP BAR ───────────────────────────────────────────────────────────────────
col_hdr, col_btn = st.columns([9,1])
with col_hdr:
    entso_status = "SI ●" if power and power.get("source")=="ENTSO-E" else "DE* ●"
    st.markdown(f"""<div class="top-bar">
        <span class="top-title">⚡ ENERGY TRADING DASHBOARD</span>
        <span class="top-sub">GEN-I · SLOVENIJA · SHORT-TERM POWER</span>
        <span style="margin-left:auto;color:#555;font-size:10px">
            ENTSO-E: {'<span style="color:#00ff44">ACTIVE</span>' if power and power.get("source")=="ENTSO-E" else '<span style="color:#666">PENDING</span>'}
            &nbsp;|&nbsp; {now.strftime('%a %d %b %Y')}
            &nbsp;|&nbsp; <span style="color:#ff5500">{now.strftime('%H:%M')}</span>
        </span>
    </div>""", unsafe_allow_html=True)
with col_btn:
    if st.button("↺ REFRESH"):
        st.cache_data.clear(); st.rerun()

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["OVERVIEW", "SPREADS & MARGINS", "FORECAST"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    # COMMODITIES
    st.markdown('<div class="sec-hdr">Commodities &amp; Fundamentals</div>', unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6 = st.columns(6)

    def cell(col, label, value, sub=""):
        with col:
            st.markdown(f"""<div class="cell">
                <div class="cell-lbl">{label}</div>
                <div class="cell-val">{value}</div>
                <div class="cell-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    cell(c1,"TTF GAS EUR/MWh", f"€{ttf:.2f}" if ttf else "n/a", "Dutch TTF front month")
    cell(c2,"EUA CO₂ EUR/t",   f"€{eua:.2f}" if eua else "n/a", "EU carbon allowance")
    cell(c3,"COAL ARA USD/t",  f"${coal:.1f}" if coal else "n/a", f"= €{coal_eur(coal):.1f}/MWh th." if coal else "")
    cell(c4,"POWER BASE EUR/MWh", f"€{power['base']:.1f}" if power else "n/a",
         f"{power['country']} · {power['source']}" if power else "")
    cell(c5,"POWER PEAK EUR/MWh", f"€{power['peak']:.1f}" if power else "n/a", "09:00–20:00h")
    if storage:
        t = storage['trend']
        cell(c6,"EU GAS STORAGE", f"{storage['fill']:.1f}%",
             f"{'▲' if t>=0 else '▼'} {abs(t):.2f}% · {storage['date']}")
    else:
        cell(c6,"EU GAS STORAGE","n/a","")

    # SPREADS SUMMARY
    st.markdown('<div class="sec-hdr">Clean Spreads</div>', unsafe_allow_html=True)
    if ttf and eua and coal and power:
        bp = power["base"]; pp = power.get("peak") or bp
        ce = coal_eur(coal)
        srmc_g = ttf/GAS_EFF + eua*GAS_EM
        srmc_c = ce/COAL_EFF + eua*COAL_EM
        css_b = css(bp,ttf,eua); css_p = css(pp,ttf,eua)
        cds_b = cds(bp,coal,eua); cds_p = cds(pp,coal,eua)
        winner = "GAS" if srmc_g < srmc_c else "COAL"
        wcol = "#00ff44" if winner=="GAS" else "#ff5500"
        diff = abs(srmc_g - srmc_c)

        s1,s2,s3,s4,s5,s6 = st.columns(6)
        def scell(col, label, val, sub=""):
            pos = val >= 0
            cls = "scell-pos" if pos else "scell-neg"
            vcls = "scell-val-pos" if pos else "scell-val-neg"
            scls = "scell-status-pos" if pos else "scell-status-neg"
            sign = "+" if pos else ""
            status = "IN THE MONEY ●" if pos else "OUT OF MONEY ●"
            with col:
                st.markdown(f"""<div class="scell {cls}">
                    <div class="scell-lbl">{label}</div>
                    <div class="{vcls}">{sign}{val:.1f}</div>
                    <div class="{scls}">{status}</div>
                    <div class="scell-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        scell(s1,"CSS · BASE  gas 50%", css_b, f"€{bp:.1f} − €{srmc_g:.1f}")
        scell(s2,"CSS · PEAK  gas 50%", css_p, f"€{pp:.1f} − €{srmc_g:.1f}")
        scell(s3,"CDS · BASE  coal 40%", cds_b, f"€{bp:.1f} − €{srmc_c:.1f}")
        scell(s4,"CDS · PEAK  coal 40%", cds_p, f"€{pp:.1f} − €{srmc_c:.1f}")
        with s5:
            st.markdown(f"""<div class="scell" style="border-left:4px solid {wcol}">
                <div class="scell-lbl">MARGINAL FUEL</div>
                <div style="font-size:26px;font-weight:700;color:{wcol}">{winner}</div>
                <div class="scell-sub">Gas €{srmc_g:.1f} · Coal €{srmc_c:.1f}</div>
            </div>""", unsafe_allow_html=True)
        with s6:
            st.markdown(f"""<div class="scell" style="border-left:4px solid #ff5500">
                <div class="scell-lbl">FUEL SWITCH GAP</div>
                <div style="font-size:26px;font-weight:700;color:#ff5500">€{diff:.1f}</div>
                <div class="scell-sub">TTF ↓ €{diff*GAS_EFF:.1f} za switch</div>
            </div>""", unsafe_allow_html=True)

    # INTRADAY GRAF + BRIEFING
    st.markdown('<div class="sec-hdr">Intraday Power Price &amp; Morning Briefing</div>', unsafe_allow_html=True)
    col_chart, col_brief = st.columns([3,2])

    with col_chart:
        if power and power.get("hours"):
            import streamlit as _st
            try:
                import pandas as pd
                hours_data = power["hours"]
                df = pd.DataFrame(hours_data, columns=["Ura","EUR/MWh"])
                df["Ura"] = df["Ura"].apply(lambda x: f"{x:02d}:00")
                df["Barva"] = df["EUR/MWh"].apply(lambda v: "#00ff44" if v >= (sum([x[1] for x in hours_data])/len(hours_data)) else "#ff2222")

                import altair as alt
                chart = alt.Chart(df).mark_bar(size=18).encode(
                    x=alt.X("Ura:O", axis=alt.Axis(labelColor="#666", tickColor="#333",
                            domainColor="#333", labelFontSize=10, labelFont="IBM Plex Mono",
                            title=None)),
                    y=alt.Y("EUR/MWh:Q", axis=alt.Axis(labelColor="#666", tickColor="#333",
                            domainColor="#333", labelFontSize=10, labelFont="IBM Plex Mono",
                            gridColor="#111", title="EUR/MWh")),
                    color=alt.Color("Barva:N", scale=None, legend=None),
                    tooltip=["Ura","EUR/MWh"]
                ).properties(
                    background="#0a0a0a", height=200,
                    title=alt.TitleParams(
                        text=f"Intraday DA Price · {power['country']} · {power['source']}",
                        color="#ff5500", fontSize=10, font="IBM Plex Mono"
                    )
                ).configure_view(stroke="#1e1e1e").configure_axis(
                    labelColor="#666", titleColor="#666"
                )
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                st.markdown(f'<div style="color:#555;font-size:10px;padding:20px">Graf ni na voljo: {e}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#555;font-size:10px;padding:20px">Ni podatkov za graf</div>', unsafe_allow_html=True)

    with col_brief:
        lines = []
        if storage:
            f = storage["fill"]
            if f < 40: lines.append(f"🔴 GAS STORAGE {f:.1f}% — {f-45:.1f}% pod sezonsko normo. Bullish TTF.")
            else: lines.append(f"🟢 GAS STORAGE {f:.1f}% — nad sezonsko normo. Bearish TTF.")
        if ttf and eua and coal and power:
            bp = power["base"]
            srmc_g = ttf/GAS_EFF + eua*GAS_EM
            srmc_c = coal_eur(coal)/COAL_EFF + eua*COAL_EM
            winner2 = "COAL" if srmc_c < srmc_g else "GAS"
            diff2 = abs(srmc_g-srmc_c)
            lines.append(f"⚡ MARGINAL: {winner2} · gap €{diff2:.1f}/MWh")
            lines.append(f"📊 EUA €{eua:.1f}/t · coal {COAL_EM/GAS_EM:.1f}x bolj izpostavljen kot gas")
            if bp < 30: lines.append(f"🟢 POWER €{bp:.1f} · renewables dominirajo")
            elif bp < 80: lines.append(f"🟡 POWER €{bp:.1f} · normalen trg")
            else: lines.append(f"🔴 POWER €{bp:.1f} · supply crunch!")
        jutri = str((now+timedelta(days=1)).date())
        d_j = day_avg(weather, jutri)
        if d_j and d_j["avg"]:
            t = d_j["avg"]
            if t < 15: lines.append(f"🌡 JUTRI {t:.1f}°C · ogrevanje · demand +{(15-t)*1.5:.0f}%")
            else: lines.append(f"🌡 JUTRI {t:.1f}°C · normalen demand")
        brief_html = "".join([f'<div class="brief-row">{l}</div>' for l in lines])
        st.markdown(f'<div style="padding-top:4px"><div style="color:#ff5500;font-size:9px;letter-spacing:0.15em;font-weight:700;margin-bottom:6px">MORNING BRIEFING</div>{brief_html}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SPREADS & MARGINS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    if not (ttf and eua and coal and power):
        st.markdown('<div style="color:#555;padding:20px">Ni dovolj podatkov.</div>', unsafe_allow_html=True)
    else:
        bp = power["base"]; pp = power.get("peak") or bp
        ce = coal_eur(coal)
        srmc_g = ttf/GAS_EFF + eua*GAS_EM
        srmc_c = ce/COAL_EFF + eua*COAL_EM
        css_b = css(bp,ttf,eua); css_p = css(pp,ttf,eua)
        cds_b = cds(bp,coal,eua); cds_p = cds(pp,coal,eua)
        diff = abs(srmc_g-srmc_c)
        winner = "GAS" if srmc_g < srmc_c else "COAL"

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="sec-hdr">Clean Spark Spread — Gas CCGT</div>', unsafe_allow_html=True)
            css_b_cls = "detail-val-pos" if css_b>=0 else "detail-val-neg"
            css_p_cls = "detail-val-pos" if css_p>=0 else "detail-val-neg"
            st.markdown(f"""<div class="detail-box">
                <div class="detail-title">CSS = Power − (TTF / η) − (EUA × 0.37)</div>
                <div class="detail-row"><span class="detail-key">TTF</span><span class="detail-val">€{ttf:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Efficiency (η)</span><span class="detail-val">{GAS_EFF*100:.0f}%</span></div>
                <div class="detail-row"><span class="detail-key">Fuel cost</span><span class="detail-val">€{ttf/GAS_EFF:.2f}/MWh &nbsp; (TTF ÷ {GAS_EFF})</span></div>
                <div class="detail-row"><span class="detail-key">EUA emission factor</span><span class="detail-val">{GAS_EM} tCO₂/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Carbon cost</span><span class="detail-val">€{eua*GAS_EM:.2f}/MWh &nbsp; (EUA × {GAS_EM})</span></div>
                <div class="detail-row"><span class="detail-key">SRMC gas</span><span class="detail-val">€{srmc_g:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Power base</span><span class="detail-val">€{bp:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Power peak</span><span class="detail-val">€{pp:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">CSS BASE</span><span class="{css_b_cls}">{'+' if css_b>=0 else ''}€{css_b:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">CSS PEAK</span><span class="{css_p_cls}">{'+' if css_p>=0 else ''}€{css_p:.2f}/MWh</span></div>
            </div>""", unsafe_allow_html=True)

            # EUA sensitivity
            st.markdown('<div class="sec-hdr">EUA Sensitivity</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="detail-box">
                <div class="detail-title">Vpliv +€10 EUA na SRMC</div>
                <div class="detail-row"><span class="detail-key">Gas SRMC</span><span class="detail-val">+€{10*GAS_EM:.1f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Coal SRMC</span><span class="detail-val">+€{10*COAL_EM:.1f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Coal je</span><span class="detail-val-neg">{COAL_EM/GAS_EM:.1f}x bolj izpostavljen</span></div>
                <div class="detail-row"><span class="detail-key">Višji EUA → bullish za</span><span class="detail-val-pos">FUEL SWITCH v GAS</span></div>
            </div>""", unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="sec-hdr">Clean Dark Spread — Coal</div>', unsafe_allow_html=True)
            cds_b_cls = "detail-val-pos" if cds_b>=0 else "detail-val-neg"
            cds_p_cls = "detail-val-pos" if cds_p>=0 else "detail-val-neg"
            st.markdown(f"""<div class="detail-box">
                <div class="detail-title">CDS = Power − (Coal€ / η) − (EUA × 0.83)</div>
                <div class="detail-row"><span class="detail-key">Coal ARA</span><span class="detail-val">${coal:.2f}/t</span></div>
                <div class="detail-row"><span class="detail-key">EUR/USD</span><span class="detail-val">{EUR_USD}</span></div>
                <div class="detail-row"><span class="detail-key">Coal thermal</span><span class="detail-val">€{ce:.2f}/MWh &nbsp; (${coal:.0f} ÷ {EUR_USD} ÷ {COAL_DIV})</span></div>
                <div class="detail-row"><span class="detail-key">Efficiency (η)</span><span class="detail-val">{COAL_EFF*100:.0f}%</span></div>
                <div class="detail-row"><span class="detail-key">Fuel cost</span><span class="detail-val">€{ce/COAL_EFF:.2f}/MWh &nbsp; (Coal ÷ {COAL_EFF})</span></div>
                <div class="detail-row"><span class="detail-key">EUA emission factor</span><span class="detail-val">{COAL_EM} tCO₂/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Carbon cost</span><span class="detail-val">€{eua*COAL_EM:.2f}/MWh &nbsp; (EUA × {COAL_EM})</span></div>
                <div class="detail-row"><span class="detail-key">SRMC coal</span><span class="detail-val">€{srmc_c:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">CDS BASE</span><span class="{cds_b_cls}">{'+' if cds_b>=0 else ''}€{cds_b:.2f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">CDS PEAK</span><span class="{cds_p_cls}">{'+' if cds_p>=0 else ''}€{cds_p:.2f}/MWh</span></div>
            </div>""", unsafe_allow_html=True)

            # Fuel switch
            st.markdown('<div class="sec-hdr">Fuel Switch Analysis</div>', unsafe_allow_html=True)
            ttf_switch = ttf - diff*GAS_EFF
            eua_switch = eua - diff/(COAL_EM-GAS_EM)
            st.markdown(f"""<div class="detail-box">
                <div class="detail-title">Kdaj se Gas splača bolj kot Coal?</div>
                <div class="detail-row"><span class="detail-key">Trenutni gap</span><span class="detail-val">€{diff:.1f}/MWh &nbsp; ({winner} je cenejši)</span></div>
                <div class="detail-row"><span class="detail-key">TTF mora pasti na</span><span class="detail-val">€{ttf_switch:.1f}/MWh &nbsp; (−€{diff*GAS_EFF:.1f})</span></div>
                <div class="detail-row"><span class="detail-key">ALI EUA mora pasti na</span><span class="detail-val">€{eua_switch:.1f}/t &nbsp; (−€{diff/(COAL_EM-GAS_EM):.1f})</span></div>
                <div class="detail-row"><span class="detail-key">Gas SRMC zdaj</span><span class="detail-val">€{srmc_g:.1f}/MWh</span></div>
                <div class="detail-row"><span class="detail-key">Coal SRMC zdaj</span><span class="detail-val">€{srmc_c:.1f}/MWh</span></div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FORECAST
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-hdr">3-Day Weather Forecast — Ljubljana</div>', unsafe_allow_html=True)

    today_s   = str(now.date())
    jutri_s   = str((now+timedelta(days=1)).date())
    pojutri_s = str((now+timedelta(days=2)).date())

    for label, dat in [("DANES", today_s), ("JUTRI", jutri_s), ("POJUTRI", pojutri_s)]:
        d = day_avg(weather, dat)
        if not d: continue

        temp = d["avg"]; wind = d["wind"]; solar = d["solar"]

        if temp and temp < 15:
            delta = (15-temp)*1.5
            demand_s = f"+{delta:.0f}% vs baza"
            demand_col = "#00ff44"
            demand_lbl = "▲ VISOKA PORABA — ogrevanje aktivno"
        elif temp and temp > 22:
            delta = (temp-22)*0.8
            demand_s = f"+{delta:.0f}% vs baza"
            demand_col = "#00ff44"
            demand_lbl = "▲ POVIŠANA PORABA — hlajenje aktivno"
        else:
            demand_s = "normalna"
            demand_col = "#666"
            demand_lbl = "◆ NORMALNA PORABA"

        wind_sig = "▼ BEARISH — veter pritiska na cene" if wind and wind > 20 else "◆ minimalen vpliv"
        solar_sig = "▼ BEARISH — solar cannibalization 10-15h" if solar and solar > 150 else "◆ minimalen vpliv"

        col_info, col_detail = st.columns([1,3])

        with col_info:
            st.markdown(f"""<div class="wcell" style="margin-bottom:8px">
                <div class="wcell-date">{label} · {dat}</div>
                <div class="wcell-temp">{temp:.1f}°C</div>
                <div class="wcell-sub">min {d['min']:.1f}° &nbsp; max {d['max']:.1f}°<br>
                peak {d['peak_t']:.1f}°C (9–20h)<br>
                💨 {wind:.0f} km/h<br>
                ☀️  {solar:.0f} W/m²</div>
                <div style="margin-top:8px;color:{demand_col};font-size:10px;font-weight:700">{demand_lbl}</div>
                <div style="color:{demand_col};font-size:10px">Demand: {demand_s}</div>
            </div>""", unsafe_allow_html=True)

        with col_detail:
            st.markdown(f"""<div class="detail-box" style="margin-bottom:8px">
                <div class="detail-row">
                    <span class="detail-key">Temperatura (avg)</span>
                    <span class="detail-val">{temp:.1f}°C</span>
                </div>
                <div class="detail-row">
                    <span class="detail-key">HDD (heating degree days)</span>
                    <span class="detail-val">{max(0,18-temp):.1f} &nbsp; (ref 18°C)</span>
                </div>
                <div class="detail-row">
                    <span class="detail-key">Ocenjena poraba SI</span>
                    <span style="color:{demand_col};font-weight:700">~{int(1400*(1+(delta/100 if temp<15 or temp>22 else 0)))} MW &nbsp; ({demand_s})</span>
                </div>
                <div class="detail-row">
                    <span class="detail-key">Veter signal</span>
                    <span class="detail-val">{wind:.0f} km/h · {wind_sig}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-key">Solar signal</span>
                    <span class="detail-val">{solar:.0f} W/m² · {solar_sig}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-key">Skupen price signal</span>
                    <span style="color:{'#00ff44' if temp<15 and (not wind or wind<20) else '#ff2222' if wind and wind>30 else '#ff5500'};font-weight:700">
                        {'🔴 BULLISH — hladno, malo renewables' if temp<15 and (not wind or wind<20) and (not solar or solar<150)
                         else '🟡 MEŠAN SIGNAL' if temp<15
                         else '🟢 BEARISH — toplo ali visok delež renewables'}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)

    # Hourly temperature chart za jutri
    st.markdown('<div class="sec-hdr">Hourly Temperature Profile — Jutri</div>', unsafe_allow_html=True)
    d_jutri = day_avg(weather, jutri_s)
    if d_jutri and d_jutri.get("hours_temp"):
        try:
            import pandas as pd, altair as alt
            df_t = pd.DataFrame(d_jutri["hours_temp"], columns=["Ura","°C"])
            df_t["Ura"] = df_t["Ura"].apply(lambda x: f"{x:02d}:00")
            chart_t = alt.Chart(df_t).mark_line(color="#ff5500", strokeWidth=2).encode(
                x=alt.X("Ura:O", axis=alt.Axis(labelColor="#666", labelFont="IBM Plex Mono",
                        labelFontSize=10, title=None, domainColor="#333")),
                y=alt.Y("°C:Q", axis=alt.Axis(labelColor="#666", labelFont="IBM Plex Mono",
                        labelFontSize=10, gridColor="#111", title="°C")),
                tooltip=["Ura","°C"]
            ).mark_area(
                line={"color":"#ff5500","strokeWidth":2},
                color=alt.Gradient(gradient="linear", stops=[
                    alt.GradientStop(color="#ff550033", offset=0),
                    alt.GradientStop(color="#ff550000", offset=1)
                ], x1=1, x2=1, y1=1, y2=0)
            ).properties(background="#0a0a0a", height=150).configure_view(stroke="#1e1e1e")
            st.altair_chart(chart_t, use_container_width=True)
        except: pass

# FOOTER
st.markdown(f"""<div style="border-top:1px solid #111;padding:4px 14px;
    font-size:9px;color:#333;display:flex;justify-content:space-between;background:#050505">
    <span>DATA: oilpriceapi.com · AGSI+ GIE · SMARD.de · Open-Meteo · ENTSO-E Transparency</span>
    <span>POWER SOURCE: {power['country'] + ' · ' + power['source'] if power else 'n/a'}</span>
    <span>UPDATED: {now.strftime('%H:%M:%S')}</span>
</div>""", unsafe_allow_html=True)
