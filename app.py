import streamlit as st

from predictor import CITIES, TEAMS, predict_win_probability

st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(7, 30, 61, 0.95), rgba(31, 60, 136, 0.95));
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 18px 45px rgba(0,0,0,0.25);
        animation: slideInDown 0.7s ease-out;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        color: #fff7e6;
    }
    .hero-subtitle {
        color: #dbe9ff;
        margin-top: 0.35rem;
        font-size: 1rem;
    }
    .panel-card {
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 1rem 1rem 0.6rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        animation: slideInLeft 0.8s ease-out;
    }
    .result-card {
        margin-top: 1rem;
        background: linear-gradient(135deg, rgba(255,107,53,0.95), rgba(255, 165, 0, 0.9));
        border-radius: 20px;
        padding: 1rem 1.2rem;
        box-shadow: 0 14px 30px rgba(0,0,0,0.2);
        color: white;
        animation: slideInRight 0.8s ease-out;
    }
    .prob-badge {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .stButton > button {
        border-radius: 999px;
        background: linear-gradient(90deg, #ff6b35, #ff9f1c);
        color: white;
        border: none;
        padding: 0.55rem 1rem;
        font-weight: 700;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(255,107,53,0.25);
    }
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        border-radius: 12px;
    }
    @keyframes slideInDown {
        from { transform: translateY(-14px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-16px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInRight {
        from { transform: translateX(16px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🏏 IPL Win Predictor</div>
        <div class="hero-subtitle">Slide through a live match scenario and get a quick, intuitive win probability.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("prediction_form"):
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox("Batting Team", TEAMS, index=0)
        bowling_team = st.selectbox("Bowling Team", TEAMS, index=1)
        city = st.selectbox("City", CITIES, index=3)

    with col2:
        current_runs = st.number_input("Current Runs", min_value=0, max_value=300, value=120, step=1)
        overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
        wickets = st.number_input("Wickets", min_value=0, max_value=9, value=2, step=1)
        target_runs = st.number_input("Target Runs", min_value=1, max_value=400, value=180, step=1)

    submitted = st.form_submit_button("Predict Win Probability", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    inputs = {
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "city": city,
        "current_runs": int(current_runs),
        "overs_completed": float(overs_completed),
        "wickets": int(wickets),
        "target_runs": int(target_runs),
    }

    probability = predict_win_probability(inputs)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f"<div class='prob-badge'>{probability * 100:.1f}%</div>", unsafe_allow_html=True)
    st.progress(probability)
    st.caption("Predicted win chance for the batting side")

    if probability >= 0.6:
        st.success("The batting team is looking strong in this situation.")
    elif probability <= 0.4:
        st.warning("The bowling side is currently favored.")
    else:
        st.info("This match is finely balanced and could swing either way.")

    st.caption("This demo uses a lightweight match-style model for quick, interactive predictions.")
    st.markdown('</div>', unsafe_allow_html=True)
