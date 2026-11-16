import random

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Room Energy Waste Detector",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --orange: #d66b2e;
        --orange-dark: #ad4d1e;
        --orange-soft: #f9e8d9;
        --ink: #33261e;
        --muted: #76665a;
        --line: #f0dfcf;
        --paper: #fff9f3;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 92% 0%, rgba(251, 191, 131, .2), transparent 34rem),
            var(--paper);
        color: var(--ink);
    }

    .stApp header[data-testid="stHeader"] {
        background: rgba(255, 249, 243, .82);
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff2e5 0%, #fff8f1 100%);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] label {
        color: var(--ink);
    }

    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: -.025em;
    }

    [data-testid="stMarkdownContainer"] h4 {
        color: var(--orange-dark) !important;
        font-size: .82rem;
        font-weight: 750;
        letter-spacing: .11em;
        text-transform: uppercase;
    }

    .creator-badge {
        display: inline-flex;
        align-items: center;
        gap: .55rem;
        margin: .55rem 0 .25rem;
        padding: .5rem .85rem;
        border: 1px solid rgba(173, 77, 30, .2);
        border-radius: 999px;
        background: linear-gradient(135deg, #fff4e9, #ffffff);
        box-shadow: 0 5px 14px rgba(104, 67, 37, .08), inset 0 1px 0 white;
        color: var(--muted);
        font-size: .83rem;
        animation: card-enter .55s cubic-bezier(.2, .75, .25, 1) both;
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .creator-badge:hover {
        transform: translateY(-2px) scale(1.015);
        box-shadow: 0 9px 20px rgba(104, 67, 37, .13), inset 0 1px 0 white;
    }

    .creator-badge strong {
        color: var(--orange-dark);
        font-size: .96rem;
        letter-spacing: .015em;
    }

    [data-testid="stMetric"] {
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        padding: 1.15rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(255, 255, 255, .98), rgba(255, 247, 238, .94));
        box-shadow: 0 10px 24px rgba(104, 67, 37, .08), inset 0 1px 0 rgba(255, 255, 255, .95);
        animation: card-enter .55s cubic-bezier(.2, .75, .25, 1) both;
        transition: transform .24s ease, box-shadow .24s ease, border-color .24s ease;
    }

    [data-testid="stMetric"]::before {
        position: absolute;
        top: 0;
        left: 1.25rem;
        right: 1.25rem;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(214, 107, 46, .42), transparent);
        content: "";
    }

    [data-testid="stMetric"]:hover {
        transform: perspective(900px) rotateX(1deg) translateY(-4px);
        border-color: rgba(214, 107, 46, .35);
        box-shadow: 0 18px 34px rgba(104, 67, 37, .13), inset 0 1px 0 white;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--orange-dark);
        font-weight: 750;
    }

    [data-testid="stTabs"] [role="tablist"] {
        gap: .4rem;
        border-bottom: 1px solid var(--line);
    }

    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 12px 12px 0 0;
        color: var(--muted);
        font-weight: 650;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--orange-dark);
        border-bottom-color: var(--orange);
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 2.7rem;
        border: 1px solid #bd5925;
        border-radius: 12px;
        background: linear-gradient(145deg, #df7838, #c45b26);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 0 #9e451b, 0 9px 18px rgba(173, 77, 30, .2), inset 0 1px 0 rgba(255, 255, 255, .28);
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        border-color: var(--orange-dark);
        color: white;
        filter: brightness(1.03);
        transform: translateY(-2px);
        box-shadow: 0 6px 0 #9e451b, 0 13px 24px rgba(173, 77, 30, .25), inset 0 1px 0 rgba(255, 255, 255, .3);
    }

    .stButton > button:active,
    [data-testid="stFormSubmitButton"] > button:active {
        transform: translateY(2px);
        box-shadow: 0 1px 0 #9e451b, 0 4px 10px rgba(173, 77, 30, .16);
    }

    .stButton > button:focus-visible,
    [data-testid="stFormSubmitButton"] > button:focus-visible {
        outline: 3px solid rgba(232, 121, 50, .35);
        outline-offset: 2px;
    }

    input, textarea, [data-baseweb="select"] > div {
        border-radius: 10px !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background-color: var(--orange);
        border-color: var(--orange);
    }

    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    hr {
        border-color: var(--line);
    }

    @keyframes card-enter {
        from {
            opacity: 0;
            transform: translateY(12px) scale(.985);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: .01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Core logic (same rule as the ideathon code)
#   if occupancy > threshold  -> efficient, waste = 0
#   else                      -> waste = power * (1 - occupancy/100)
# ----------------------------------------------------------------------------
DEFAULT_ROOMS = pd.DataFrame(
    {
        "Room": ["Seminar Hall", "CSE Lab", "Room 102", "Library", "Auditorium"],
        "Power (kW)": [20.0, 11.0, 8.0, 14.0, 30.0],
    }
)

COLORS = {"Wasting": "#d66b2e", "Efficient": "#31916f"}


def analyse(rooms: pd.DataFrame, occ: dict, threshold: int, tariff: float) -> pd.DataFrame:
    rows = []
    for _, r in rooms.iterrows():
        name, kw = r["Room"], float(r["Power (kW)"])
        p = int(occ.get(name, 0))
        waste = 0.0 if p > threshold else kw * (1 - p / 100)
        rows.append(
            {
                "room": name,
                "power": kw,
                "occupancy": p,
                "waste_kw": round(waste, 1),
                "cost_hr": round(waste * tariff),
                "status": "Wasting" if p <= threshold else "Efficient",
            }
        )
    return pd.DataFrame(rows)


def random_occ(rooms: pd.DataFrame) -> dict:
    return {name: random.randint(0, 100) for name in rooms["Room"]}


def show_results(df: pd.DataFrame, threshold: int, tariff: float, hours: int):
    total_kw = df["waste_kw"].sum()
    total_hr = total_kw * tariff
    flagged = int((df["status"] == "Wasting").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rooms flagged", f"{flagged} / {len(df)}")
    c2.metric("Power wasted", f"{total_kw:.1f} kW")
    c3.metric("Cost per hour", f"₹ {total_hr:,.0f}")
    c4.metric(f"Per day ({hours} hrs)", f"₹ {total_hr * hours:,.0f}")
    st.caption(f"Roughly ₹ {total_hr * hours * 30:,.0f} per month if this pattern continues.")

    left, right = st.columns([3, 2])

    with left:
        st.subheader("Crowd % vs the threshold")
        bars = (
            alt.Chart(df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("room:N", sort=None, title=None),
                y=alt.Y("occupancy:Q", title="Occupancy %", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color(
                    "status:N",
                    scale=alt.Scale(domain=list(COLORS), range=list(COLORS.values())),
                    legend=alt.Legend(title=None, orient="bottom"),
                ),
                tooltip=["room", "occupancy", "power", "waste_kw", "cost_hr", "status"],
            )
        )
        rule = (
            alt.Chart(pd.DataFrame({"t": [threshold]}))
            .mark_rule(strokeDash=[6, 4], color="#888", size=2)
            .encode(y="t:Q")
        )
        st.altair_chart(bars + rule, width="stretch")
        st.caption(f"Dashed line = {threshold}% rule. Rooms at or below it with power ON are wasting energy.")

    with right:
        st.subheader("Room report")
        view = df.rename(
            columns={
                "room": "Room",
                "power": "Power (kW)",
                "occupancy": "Crowd %",
                "waste_kw": "Waste (kW)",
                "cost_hr": "Rs/hr",
                "status": "Status",
            }
        )
        st.dataframe(view, hide_index=True, width="stretch")

    wasting = df[df["status"] == "Wasting"].sort_values("cost_hr", ascending=False)
    if wasting.empty:
        st.success("All rooms are used efficiently right now. No action needed.")
    else:
        st.subheader("Suggested actions")
        for _, r in wasting.iterrows():
            st.warning(
                f"**{r['room']}** is only {r['occupancy']}% full but can draw {r['power']:.0f} kW. "
                f"Switch off AC/lights to save about **{r['waste_kw']} kW (₹ {r['cost_hr']}/hr)**."
            )


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ Settings")
    threshold = st.slider("Occupancy threshold (%)", 5, 60, 30, help="Rooms at or below this are flagged.")
    tariff = st.number_input("Electricity cost (₹ per kWh)", 1.0, 30.0, 7.0, 0.5)
    hours = st.number_input("Hours used per day", 1, 24, 8)
    st.divider()
    mode = st.radio(
        "Crowd data source",
        ["Manual sliders", "Random snapshot", "Live simulation"],
        help="Manual: you set the crowd. Random: one random run (like the Python code). Live: refreshes every few seconds.",
    )
    st.divider()
    st.caption("Edit rooms and their power in the 'Rooms' tab.")

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    "<h4 style='margin:0;color:#1f3864'>BGS College of Engineering and Technology · Dept. of CSE</h4>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='creator-badge'><span>Project by</span><strong>Raghunandan</strong><span>· CSE, BGSCET</span></div>",
    unsafe_allow_html=True,
)
st.title("Smart Room Energy Waste Detector")
st.write("Finds rooms where AC and lights run at full power while almost nobody is inside, and shows the waste in kW and ₹.")

if "rooms" not in st.session_state:
    st.session_state.rooms = DEFAULT_ROOMS.copy()
if "snap" not in st.session_state:
    st.session_state.snap = random_occ(DEFAULT_ROOMS)
if "history" not in st.session_state:
    st.session_state.history = []

tab_demo, tab_rooms, tab_code, tab_about = st.tabs(["📊 Live Demo", "🏫 Rooms", "💻 Code", "ℹ️ About"])

# ----------------------------------------------------------------------------
# Rooms tab (edited first so the demo uses the latest values)
# ----------------------------------------------------------------------------
with tab_rooms:
    st.write("Add, remove or edit rooms. Power (kW) is the load of AC + lights when ON.")
    edited = st.data_editor(
        st.session_state.rooms,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        column_config={
            "Power (kW)": st.column_config.NumberColumn(min_value=0.1, max_value=500.0, step=0.5),
        },
    )
    edited = edited.dropna(subset=["Room", "Power (kW)"])
    edited = edited[edited["Room"].astype(str).str.strip() != ""].drop_duplicates("Room")
    st.session_state.rooms = edited.reset_index(drop=True)

rooms = st.session_state.rooms

# ----------------------------------------------------------------------------
# Demo tab
# ----------------------------------------------------------------------------
with tab_demo:
    if rooms.empty:
        st.warning("Add at least one room in the Rooms tab.")
    elif mode == "Manual sliders":
        st.subheader("Set the crowd in each room")
        cols = st.columns(min(len(rooms), 3))
        occ = {}
        for i, name in enumerate(rooms["Room"]):
            with cols[i % len(cols)]:
                occ[name] = st.slider(f"{name} – crowd %", 0, 100, 10 if i == 0 else 60, key=f"m_{name}")
        st.divider()
        show_results(analyse(rooms, occ, threshold, tariff), threshold, tariff, hours)

    elif mode == "Random snapshot":
        if st.button("🎲 Generate new random crowd", type="primary"):
            st.session_state.snap = random_occ(rooms)
        for name in rooms["Room"]:
            st.session_state.snap.setdefault(name, random.randint(0, 100))
        st.divider()
        show_results(analyse(rooms, st.session_state.snap, threshold, tariff), threshold, tariff, hours)

    else:  # Live simulation
        c1, c2, c3 = st.columns([1, 1, 2])
        running = c1.toggle("Running", value=True)
        interval = c2.selectbox("Refresh every", [2, 3, 5], format_func=lambda s: f"{s} sec")
        if c3.button("Clear history"):
            st.session_state.history = []

        @st.fragment(run_every=interval if running else None)
        def live():
            if running:
                st.session_state.snap = random_occ(rooms)
            df = analyse(rooms, st.session_state.snap, threshold, tariff)
            if running:
                hist = st.session_state.history
                hist.append(
                    {"step": len(hist) + 1, "Waste (kW)": df["waste_kw"].sum(), "Rs/hr": df["cost_hr"].sum()}
                )
                st.session_state.history = hist[-30:]
            show_results(df, threshold, tariff, hours)
            if st.session_state.history:
                st.subheader("Waste over time steps")
                h = pd.DataFrame(st.session_state.history).set_index("step")
                st.line_chart(h[["Waste (kW)"]])

        live()

# ----------------------------------------------------------------------------
# Code tab
# ----------------------------------------------------------------------------
with tab_code:
    st.write("The original ideathon logic that powers this app:")
    st.code(
        '''import random
for name, kw in {"Seminar Hall": 20, "CSE Lab": 11, "Room 102": 8}.items():
    p = random.randint(0, 100)   # % occupancy
    w = 0 if p > 30 else kw * (1 - p / 100)
    print(name, p, round(w, 1), "kW", round(w * 7), "Rs/hr")''',
        language="python",
    )
    st.write("Worked example: CSE Lab uses 11 kW but is only 10% full → waste = 11 × 0.90 = 9.9 kW ≈ ₹ 69/hr.")

# ----------------------------------------------------------------------------
# About tab
# ----------------------------------------------------------------------------
with tab_about:
    st.markdown(
        """
**Problem:** Rooms keep AC and lights ON at full power even when almost empty, so electricity and money are wasted and nobody sees how much.

**Solution:** A Python simulation compares each room's power (kW) with its crowd %. Empty room with AC/lights ON = 100% waste. Under 30% full = high waste. Above 30% full = efficient.

**AI technique:** Rule-based decision logic with a 30% occupancy threshold.

**Python concepts:** `random`, dictionary, `for` loop, `if/else`, `print` and `round` (plus Streamlit, pandas, Altair for the web app).

**Workflow:** Room power + crowd % → 30% rule → waste in kW and ₹/hr → repeat every time step.

**Future scope:** Replace random numbers with IoT sensors or OpenCV cameras and show real live data on this dashboard.
"""
    )

st.divider()
st.caption("Built by RAGHUNANDAN · CSE, BGSCET · Ideathon Project")
