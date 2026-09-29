"""
KrishiSmriti Streamlit Application
Deployment entrypoint for Streamlit Community Cloud (share.streamlit.io).
"""
import base64
import os
from datetime import date
import streamlit as st

import main
from agronomy import PROBLEMS
from languages import LANGUAGES, local_pest, local_product

# Configure Page
st.set_page_config(
    page_title="KrishiSmriti — Farm Memory Operating System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to match KrishiSmriti brand aesthetic
st.markdown("""
<style>
    :root {
        --primary-color: #1f6b3a;
        --background-color: #f7f9f6;
    }
    .main {
        background-color: #f8faf7;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1f6b3a, #154d29);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #278548, #1a5e33);
        color: white;
    }
    .metric-box {
        background: white;
        border: 1px solid #e1e8e2;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .metric-val {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 2px;
    }
    .metric-lbl {
        font-size: 12px;
        color: #556250;
        font-weight: 600;
    }
    .motto-banner {
        background: linear-gradient(135deg, #fdf8eb 0%, #fffbf2 100%);
        border-left: 5px solid #d49c1b;
        border-radius: 0 14px 14px 0;
        padding: 14px 18px;
        margin-bottom: 18px;
        color: #453303;
    }
    .sub-en {
        font-size: 12px;
        color: #4a5c4e;
        font-style: italic;
        margin-top: 2px;
    }
    .guard-box {
        background: #fdf2f2;
        border-left: 5px solid #b3261e;
        border-radius: 0 12px 12px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #4d1411;
    }
    .proven-box {
        background: #eef7f0;
        border-left: 5px solid #1f6b3a;
        border-radius: 0 12px 12px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #10381e;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("static/icon.svg", width=64)
    st.title("KrishiSmriti")
    st.caption("Farm Memory Operating System · Powered by Hindsight")
    
    st.markdown("---")
    
    # 1. Plot Selection
    plots = main.mem.plots()
    plot_options = {p["id"]: f"{p['farmer']} · {p['village']} ({p['crop']})" for p in plots}
    selected_pid = st.selectbox(
        "Select Demo Farmer / Plot",
        options=list(plot_options.keys()),
        format_func=lambda x: plot_options[x]
    )
    current_plot = main.mem.plot(selected_pid)
    
    # 2. Language Selection
    lang_codes = list(LANGUAGES.keys())
    selected_lang = st.selectbox(
        "Choose Language / భాష / भाषा",
        options=lang_codes,
        format_func=lambda c: f"{LANGUAGES[c]['native']} ({LANGUAGES[c]['name']})",
        index=0 if current_plot.get("lang") == "te" else lang_codes.index(current_plot.get("lang", "en"))
    )

    st.markdown("---")
    
    # Whitepaper PDF Download
    pdf_path = os.path.join(os.path.dirname(__file__), "docs", "KrishiSmriti_Motto_and_Impact.pdf")
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📑 Download Whitepaper (PDF)",
            data=pdf_bytes,
            file_name="KrishiSmriti_Motto_and_Impact.pdf",
            mime="application/pdf"
        )
        
    st.link_button("🌐 Open Full Mobile UI (Local)", "http://localhost:8000")
    st.link_button("⭐ GitHub Repository", "https://github.com/jeshwanth1368/krishismriti")
    st.link_button("🧠 Vectorize Hindsight", "https://github.com/vectorize-io/hindsight")

# ----------------- MAIN DASHBOARD -----------------
home_data = main.home(selected_pid, selected_lang)
plot = home_data["plot"]
stage = home_data["stage"]
weather = home_data["weather"]
ledger = home_data["ledger"]
alerts = home_data["alerts"]

# Header Banner
st.markdown(f"## {home_data['greeting']} 🙏")
if selected_lang != "en" and home_data.get("greeting_en"):
    st.markdown(f"<div class='sub-en'>({home_data['greeting_en']})</div>", unsafe_allow_html=True)
st.caption(f"🌾 **{plot['crop']}** · 📍 {plot['village']}, {plot['district']} · 📐 {plot['area_acres']} acres")

# Motto & Mission Box
st.markdown("""
<div class="motto-banner">
    <b>🌾 Core Mission:</b> <i>"Every farm plot deserves its own medical chart. Stop repeating what already failed; double down on what truly works."</i>
    <br><span style="font-size:11.5px;color:#6b500a">Powered by <b>Hindsight</b> agent memory to prevent chemical resistance and wasted farmer expenditure.</span>
</div>
""", unsafe_allow_html=True)

# ----------------- AUDIO BRIEF -----------------
st.markdown("### 🔊 Today's Audio Briefing")
brief_sentences = [home_data["greeting"] + "."]
if alerts:
    brief_sentences.append(alerts[0]["text"])
if stage:
    brief_sentences.append(f"{stage['stage']}. {stage['tasks'][0]}.")
if weather:
    brief_sentences.append(weather["advice"])
brief_native = " ".join(brief_sentences)

brief_en_sentences = [home_data.get("greeting_en", "Hello") + "."]
if alerts:
    brief_en_sentences.append(alerts[0].get("text_en", alerts[0]["text"]))
if stage:
    t_en = (stage.get("tasks_en") and stage["tasks_en"][0]) or stage["tasks"][0]
    brief_en_sentences.append(f"{stage.get('stage_en', stage['stage'])}. {t_en}.")
if weather:
    brief_en_sentences.append(weather.get("advice_en", weather["advice"]))
brief_en = " ".join(brief_en_sentences)

col_audio, col_txt = st.columns([1, 2])
with col_audio:
    if st.button("🎙️ Generate & Play Native Audio"):
        with st.spinner("Generating native voice..."):
            audio_b64 = main.voice.speak(brief_native, selected_lang)
            if audio_b64:
                st.audio(base64.b64decode(audio_b64), format="audio/mp3")
with col_txt:
    st.markdown(f"**Spoken ({LANGUAGES[selected_lang]['name']}):** {brief_native}")
    if selected_lang != "en":
        st.markdown(f"<div class='sub-en'><b>English Subtitle:</b> {brief_en}</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------- 4 FINANCIAL & CLINICAL METRICS -----------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-val" style="color:#1f6b3a">₹{ledger['saved_by_memory']:,}</div>
        <div class="metric-lbl">💰 Saved by Memory Guard</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-val" style="color:#b3261e">₹{ledger['wasted_on_failures']:,}</div>
        <div class="metric-lbl">⛔ Wasted on Failed Sprays</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-val" style="color:#1f5f99">₹{ledger['total_spent']:,}</div>
        <div class="metric-lbl">📊 Total Plot Investment</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    das_val = stage['das'] if stage else "-"
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-val" style="color:#8a5a00">Day {das_val}</div>
        <div class="metric-lbl">🌱 Days After Sowing</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- 2 COLUMN LAYOUT: ADVICE & ALERTS -----------------
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
    st.markdown("### 🧠 Ask Crop Doctor & Test Resistance Guard")
    default_try = {
        "PLOT-14": "Dealer is giving me thiamethoxam for whitefly. Is it ok?",
        "PLOT-41": "Sheath blight again on paddy. Can I use carbendazim?",
        "PLOT-9": "Whitefly is increasing. Can I spray acetamiprid?",
        "PLOT-22": "धान में तना छेदक फिर से आ गया है, क्या करूं?"
    }
    user_q = st.text_input(
        "Ask a problem or pesticide recommendation:",
        value=default_try.get(selected_pid, "What should I spray for whitefly?"),
        key="query_input"
    )
    
    if st.button("🧪 Ask KrishiSmriti (Recall from Hindsight)"):
        with st.spinner("Recalling plot memory & checking resistance guard..."):
            ans = main.run_ask(plot, user_q, selected_lang)
            advice = ans["advice"]
            warnings = ans["warnings"]
            
            # Show Warnings
            if warnings:
                for w in warnings:
                    st.markdown(f"""
                    <div class="guard-box">
                        <b>⛔ RESISTANCE GUARD ALERT: Blocked '{w['product'].upper()}'</b><br>
                        {w['reason']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show Advice
            st.markdown(f"""
            <div class="proven-box">
                <b>🌾 Recommended Action:</b><br>
                {advice.get('speak', '')}
            </div>
            """, unsafe_allow_html=True)
            
            if selected_lang != "en" and advice.get("english_summary"):
                st.markdown(f"<div class='sub-en'><b>English Translation:</b> {advice['english_summary']}</div>", unsafe_allow_html=True)
                
            # Audio player for response
            if ans.get("audio_b64"):
                st.audio(base64.b64decode(ans["audio_b64"]), format="audio/mp3")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 7-Day Follow-up Verification
    st.markdown("### 🔔 7-Day Outcome Verification (Closed-Loop)")
    due_fu = main.mem.due_followups(selected_pid)
    if due_fu:
        f = due_fu[0]
        st.info(f"**Follow-up Question:** {f.get('event', {}).get('product', '')} was sprayed {f.get('event', {}).get('date', '')}. Did it work?")
        fc1, fc2, fc3 = st.columns(3)
        if fc1.button("👍 Worked"):
            main.mem.close_followup(f["id"], "worked", days_healthy=21)
            st.success("Saved: marked as proven remedy in Hindsight bank!")
            st.rerun()
        if fc2.button("🤏 Partial"):
            main.mem.close_followup(f["id"], "partial", days_healthy=7)
            st.warning("Saved: marked as partial.")
            st.rerun()
        if fc3.button("👎 Failed"):
            main.mem.close_followup(f["id"], "failed")
            st.error("Saved: permanently blocked from future recommendations!")
            st.rerun()
    else:
        st.caption("No pending spray verifications due today for this plot.")

with col_right:
    # Weather & Spray Window
    st.markdown("### 🌦️ Spray Window & Weather")
    if weather:
        w_icon = "✅ Safe to Spray" if weather["ok_to_spray"] else "⛔ Hold Spraying"
        st.markdown(f"**Status:** {w_icon}")
        st.write(f"💬 {weather['advice']}")
        if selected_lang != "en":
            st.markdown(f"<div class='sub-en'>📝 {weather['advice_en']}</div>", unsafe_allow_html=True)
        st.caption(f"🌧️ Rain Chance: {weather['max_rain_prob']}% · 💨 Wind: {weather['max_wind_kmh']} km/h · 🌡️ Temp: {weather['max_temp_c']}°C · 💧 Humidity: {weather['avg_humidity']}%")
    else:
        st.caption("Weather data unavailable.")

    # Growth Stage
    if stage:
        st.markdown("### 🌿 Crop Stage & Seasonal Tasks")
        st.progress(stage["progress"] / 100.0)
        st.markdown(f"**Stage:** {stage['icon']} {stage['stage']}")
        if selected_lang != "en" and stage.get("stage_en"):
            st.markdown(f"<div class='sub-en'>{stage['stage_en']}</div>", unsafe_allow_html=True)
        st.markdown("**Tasks To Do Now:**")
        for i, t in enumerate(stage["tasks"]):
            t_sub = stage.get("tasks_en", [])[i] if (selected_lang != "en" and stage.get("tasks_en")) else ""
            st.markdown(f"• **{t}**" + (f"<div class='sub-en'>↳ {t_sub}</div>" if t_sub else ""), unsafe_allow_html=True)

st.markdown("---")

# ----------------- TIMELINE & PLOT MEDICAL CHART -----------------
st.markdown("### 📋 Plot Medical Chart & Event Timeline")
events = main.mem.events(selected_pid)
if events:
    timeline_rows = []
    for e in events[::-1]:
        outcome_badge = {"worked": "✅ Worked", "failed": "⛔ Failed", "pending": "⏳ Pending"}.get(e.get("outcome"), "-")
        timeline_rows.append({
            "Date": e.get("date"),
            "Type": e.get("type", "").capitalize(),
            "Product / Treatment": local_product(e.get("product") or "-", selected_lang),
            "Target Pest / Disease": local_pest(e.get("target") or "-", selected_lang),
            "Cost": f"₹{e.get('cost', 0):,}" if e.get("cost") else "-",
            "Clinical Outcome": outcome_badge
        })
    st.dataframe(timeline_rows, use_container_width=True)
else:
    st.caption("No events recorded yet.")

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("KrishiSmriti — Long-Term Farm Memory Operating System · Powered by Vectorize Hindsight")
