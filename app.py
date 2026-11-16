import random

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Room Energy Waste Detector",
    page_icon="⚡",
    layout="wide",
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

COLORS = {"Wasting": "#e74c3c", "Efficient": "#2ecc71"}


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
            st.error(
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
