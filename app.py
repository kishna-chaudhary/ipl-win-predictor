import streamlit as st
import pandas as pd

from predictor import CITIES, TEAMS, predict_win_probability


st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="wide")

CSS = """
<style>
body { background: #f2f7fb; }
.app-header { background: linear-gradient(90deg,#0b3b73,#1f4c99); padding: 16px; border-radius: 8px; color: #fff; }
.app-title { margin: 0; font-weight: 700; font-size: 20px; }
.card { background: #fff; border-radius: 12px; padding: 18px; box-shadow: 0 12px 30px rgba(11,38,71,0.06); }
.muted { color: #6b7686; font-size: 13px; }
.field-canvas { width:100%; height:260px; border-radius:10px; background: linear-gradient(180deg,#eaf5ff,#ffffff); display:flex; align-items:center; justify-content:center; }
.predict-btn > button { background: linear-gradient(90deg,#1565c0,#1e88e5); color: white; border-radius: 999px; padding: 10px 16px; font-weight:700; }
.result-card { border-radius: 12px; padding: 14px; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

st.markdown('<div class="app-header"><div style="display:flex;justify-content:space-between;align-items:center"><div><h1 class="app-title">🏏 IPL Win Predictor</h1><div class="muted">Adjust match parameters and instantly visualize win probability.</div></div></div></div>', unsafe_allow_html=True)

left, center, right = st.columns([1.2, 1.6, 1.0], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Match Details")
    batting_team = st.selectbox("Batting Team", TEAMS, index=0)
    bowling_team = st.selectbox("Bowling Team", TEAMS, index=1)
    city = st.selectbox("City", CITIES, index=2)
    st.markdown("<hr/>", unsafe_allow_html=True)
    with st.expander("Prediction Result", expanded=False):
        st.write("Adjust sliders on the right and press Predict to see results.")
    st.markdown('</div>', unsafe_allow_html=True)

with center:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Field State")
    # Prefer a provided field-layout image if available, otherwise show SVG placeholder
    import os
    img_path = "field_layout.png"
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True, caption="Ground layout")
    else:
        # Simple illustrative SVG field (fallback)
        svg_field = """
        <svg width='100%' height='220' viewBox='0 0 600 220' xmlns='http://www.w3.org/2000/svg'>
            <rect x='0' y='0' width='600' height='220' rx='12' fill='#eef9ff' stroke='#d7ecff' />
            <rect x='270' y='50' width='60' height='120' rx='6' fill='#ffffff' stroke='#cfe7ff' />
            <circle cx='300' cy='110' r='6' fill='#ff6b35' />
        </svg>
        """
        st.markdown(f'<div class="field-canvas">{svg_field}</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    if st.button("Predict Win Probability", key="predict_button"):
        # gather inputs from right column session state
        inputs = {
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "city": city,
            "current_runs": int(st.session_state.get("current_runs", 0)),
            "overs_completed": float(st.session_state.get("overs_completed", 0.0)),
            "total_overs": int(st.session_state.get("total_overs", 20)),
            "wickets": int(st.session_state.get("wickets", 0)),
            "target_runs": int(st.session_state.get("target_runs", 0)),
        }

        prob = predict_win_probability(inputs)
        batting_pct = prob * 100
        bowling_pct = 100 - batting_pct

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:32px;font-weight:800;color:#08345a'>{batting_pct:.0f}%</div>", unsafe_allow_html=True)
        st.progress(prob)

        # simple bar chart using pandas + streamlit (avoids Altair compatibility issues)
        data = [
            {"team": batting_team, "prob": batting_pct},
            {"team": bowling_team, "prob": bowling_pct},
        ]
        df = pd.DataFrame(data).set_index('team')
        teams = df.index.tolist()
        probs = df['prob'].tolist()
        colors = ['#ff6b35', '#2563eb']
        # render HTML/CSS horizontal bars to avoid external chart libs
        bars_html = "<div style='display:flex;flex-direction:column;gap:8px;'>"
        for i, team in enumerate(teams):
            p = probs[i]
            color = colors[i] if i < len(colors) else '#888'
            bars_html += f"<div style='display:flex;align-items:center;gap:12px'><div style='width:110px;font-weight:700;color:#08345a'>{team}</div><div style='flex:1;background:#e9f2ff;border-radius:10px;height:18px;'><div style='width:{p}%;background:{color};height:100%;border-radius:10px;'></div></div><div style='width:48px;text-align:right;font-weight:700;color:#08345a'>{p:.0f}%</div></div>"
        bars_html += "</div>"
        st.markdown(bars_html, unsafe_allow_html=True)

        if prob >= 0.6:
            st.success("The batting team is looking strong in this situation.")
        elif prob <= 0.4:
            st.warning("The bowling side is currently favored.")
        else:
            st.info("This match is finely balanced and could swing either way.")

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Live Match State")
    current_runs = st.slider("Current Runs", min_value=0, max_value=400, value=120, step=1, key="current_runs")
    overs_completed = st.slider("Overs Completed", min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="overs_completed")
    total_overs = st.select_slider("Total Overs", options=[10, 20, 50], value=20, key="total_overs")
    wickets = st.slider("Wickets Down", min_value=0, max_value=10, value=2, step=1, key="wickets")
    target_runs = st.number_input("Target Runs", min_value=1, max_value=500, value=180, step=1, key="target_runs")

    runs_needed = max(int(target_runs - current_runs), 0)
    balls_left = max(int((int(total_overs) - overs_completed) * 6), 0)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.text(f"Runs Req: {runs_needed}   |   Balls Left: {balls_left}   |   Wickets: {wickets}")
    st.caption('Use sliders to adjust the live match state. Press Predict to compute win probability.')
    st.markdown('</div>', unsafe_allow_html=True)
