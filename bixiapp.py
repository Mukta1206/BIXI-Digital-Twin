import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from geopy.distance import geodesic
import time

st.set_page_config(page_title="BIXI Digital Twin", layout="wide")

# =========================
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>

/* =========================
🌈 BACKGROUND (SOFT GRADIENT)
========================= */
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #e4ecf7);
    font-family: 'Inter', sans-serif;
}

/* =========================
🧊 GLASS CARD (PREMIUM)
========================= */
.block {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(14px);
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: all 0.25s ease-in-out;
    border: 1px solid rgba(255,255,255,0.4);
}

.block:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 14px 40px rgba(0,0,0,0.12);
}

/* =========================
📌 SECTION TITLES
========================= */
.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 18px;
    color: #1e293b;
}

/* =========================
🚲 MAIN TITLE
========================= */
.big-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 10px;
    color: #0f172a;
}

.sub-title {
    text-align: center;
    font-size: 16px;
    color: #64748b;
    margin-bottom: 30px;
}

/* =========================
📊 KPI CARDS (MODERN)
========================= */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff, #f1f5f9);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    transition: 0.2s;
}

[data-testid="metric-container"]:hover {
    transform: scale(1.03);
}

/* =========================
🎯 BUTTONS (GRADIENT STYLE)
========================= */
.stButton button {
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 600;
    padding: 8px 16px;
    border: none;
    transition: all 0.2s ease;
}

.stButton button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: scale(1.05);
}

/* =========================
💬 CHAT UI
========================= */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 14px;
    background: rgba(255,255,255,0.7);
    margin-bottom: 10px;
}

/* =========================
📦 SELECTBOX & INPUT
========================= */
div[data-baseweb="select"] {
    border-radius: 12px;
}

/* =========================
📊 PLOT CONTAINER
========================= */
.js-plotly-plot {
    border-radius: 12px;
}

/* =========================
⚡ ALERTS (SOFT COLORS)
========================= */
.stAlert {
    border-radius: 12px;
}

/* =========================
📍 LOCATION / INFO BOXES
========================= */
.stInfo, .stSuccess, .stWarning {
    border-radius: 12px;
}

/* =========================
🧭 TABS (VERY IMPORTANT UPGRADE)
========================= */
button[data-baseweb="tab"] {
    font-weight: 600;
    font-size: 15px;
    padding: 10px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)



# =========================
# 🎯 TITLE
# =========================

st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
    <div>
        <div class="big-title">BIXI Center</div>
        <div style="color:#9ca3af; font-size:14px;">
            Real-time Smart Mobility System
        </div>
    </div>
    <div style="background:#111827; padding:10px 15px; border-radius:10px;">
        🟢 Live System
    </div>
</div>
""", unsafe_allow_html=True)
# =========================
# 📡 LOAD DATA
# =========================
@st.cache_data(ttl=10)
def load_data():
    status = requests.get("https://gbfs.velobixi.com/gbfs/en/station_status.json").json()
    info = requests.get("https://gbfs.velobixi.com/gbfs/en/station_information.json").json()

    df1 = pd.DataFrame(status["data"]["stations"])
    df2 = pd.DataFrame(info["data"]["stations"])

    df = pd.merge(df1, df2, on="station_id")

    df = df.rename(columns={
        "num_bikes_available": "Bikes",
        "num_docks_available": "Docks",
        "name": "Station",
        "lat": "Latitude",
        "lon": "Longitude"
    })

    df["Stockout"] = (df["Bikes"] == 0).astype(int)
    df["Overflow"] = (df["Docks"] == 0).astype(int)

    return df

df = load_data()
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 System KPIs</div>', unsafe_allow_html=True)

# =========================
# KPI CARDS
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("⚠️ Stockout", int(df["Stockout"].sum()))
col2.metric("🚫 Full", int(df["Overflow"].sum()))
col3.metric("🚲 Bikes", int(df["Bikes"].sum()))
col4.metric("🅿️ Docks", int(df["Docks"].sum()))

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INTERACTIVE KPI ANALYSIS
# =========================
st.markdown("### 🔍 KPI Analysis")

selected_kpi = st.selectbox(
    "Select KPI to visualize:",
    ["Stockout", "Overflow", "Bikes", "Docks"]
)

fig = px.bar(
    df.sort_values(selected_kpi, ascending=False).head(10),
    x="Station",
    y=selected_kpi,
    color=selected_kpi,
    title=f"Top 10 Stations by {selected_kpi}"
)

fig.update_layout(title_x=0.5)
st.plotly_chart(fig, use_container_width=True)


# 📈 CHART + MAP
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 System Overview</div>', unsafe_allow_html=True)

colA, colB = st.columns([2,1])

fig = px.bar(df.head(10), x="Station", y="Bikes", color="Bikes")

map_fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    size="Bikes",
    color="Bikes",
    hover_name="Station",
    zoom=11
)
map_fig.update_layout(mapbox_style="open-street-map")

colA.plotly_chart(fig, use_container_width=True)
colB.plotly_chart(map_fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🔮 PREDICTION
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title"> Stockout Risk</div>', unsafe_allow_html=True)

df["risk"] = 1/(df["Bikes"]+1)
risk_df = df.sort_values("risk", ascending=False).head(5)

for _, row in risk_df.iterrows():
    st.error(f"{row['Station']} | Bikes: {row['Bikes']}")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🔁 REBALANCING SYSTEM (GAMIFIED)
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔁 Smart Rebalancing</div>', unsafe_allow_html=True)

# INIT STATE
if "points" not in st.session_state:
    st.session_state.points = 0

if "reward_unlocked" not in st.session_state:
    st.session_state.reward_unlocked = False

low = df[df["Bikes"] <= 2]
high = df[df["Bikes"] >= 10]

plans = []

for i in range(min(len(low), len(high))):
    plans.append(f"{high.iloc[i]['Station']} ➝ {low.iloc[i]['Station']}")

if plans:
    selected = st.selectbox("Choose rebalancing action:", plans)

    if st.button("🚚 Execute Rebalancing"):
        st.session_state.points += 100
        st.success("✅ Rebalancing completed! +100 points")

        # 🎯 CHECK REWARD
        if st.session_state.points >= 500 and not st.session_state.reward_unlocked:
            st.session_state.reward_unlocked = True

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🏆 REWARDS SYSTEM (PREMIUM EXPERIENCE)
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏆 Rewards</div>', unsafe_allow_html=True)

points = st.session_state.points
progress = points % 500

# 🎯 PROGRESS BAR
st.progress(progress / 500)

col1, col2 = st.columns(2)
col1.metric("Total Points", points)
col2.metric("Points to Reward", 500 - progress if progress != 0 else 0)

# 🎁 REWARD EXPERIENCE
if st.session_state.reward_unlocked:

    st.balloons()

    st.success("""
🎉 **Reward Unlocked!** 🎉  

🚲 You earned **30 minutes of FREE BIXI ride time!**


""")

    # 🔄 RESET BUTTON (OPTIONAL FOR DEMO)
    if st.button("🔄 Redeem & Reset Points"):
        st.session_state.points = 0
        st.session_state.reward_unlocked = False
        st.success("Points reset. Start earning again!")

else:
    st.info("💡 Earn 500 points to unlock a FREE 30-minute ride!")

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 📍 LOCATION
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📍 Your Location</div>', unsafe_allow_html=True)

lat = st.number_input("Latitude", value=45.495)
lon = st.number_input("Longitude", value=-73.578)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 🤖 A+ AI CHATBOT (FINAL)
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🤖 BIXI AI Assistant</div>', unsafe_allow_html=True)

import time

# INIT CHAT MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT
user_input = st.chat_input("Ask: find bike / return / stockout / best station")

# =========================
# 🧠 HELPER FUNCTIONS
# =========================

def get_best(user_loc, mode):
    results = []

    for _, r in df.iterrows():
        try:
            dist = geodesic(user_loc, (r["Latitude"], r["Longitude"])).meters
        except:
            continue

        if mode == "bike" and r["Bikes"] > 2:
            results.append((dist, r))

        elif mode == "dock" and r["Docks"] > 2:
            results.append((dist, r))

    return sorted(results, key=lambda x: x[0])[:3]


def get_risk_stations():
    df_copy = df.copy()
    df_copy["risk"] = 1 / (df_copy["Bikes"] + 1)
    return df_copy.sort_values("risk", ascending=False).head(5)


# =========================
# 💬 HANDLE USER INPUT
# =========================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    user_loc = (lat, lon)
    text = user_input.lower()

    reply = ""

    try:
        # 🚲 BIKE SEARCH
        if "bike" in text or "find" in text:
            best = get_best(user_loc, "bike")

            if best:
                reply = "🚲 **Best nearby bike stations:**\n\n"
                for d, r in best:
                    reply += f"• **{r['Station']}** — {int(d)}m — {r['Bikes']} bikes\n"
            else:
                reply = "❌ No bikes available nearby."

        # 🔁 RETURN
        elif "return" in text or "dock" in text:
            best = get_best(user_loc, "dock")

            if best:
                reply = "🔁 **Best stations to return your bike:**\n\n"
                for d, r in best:
                    reply += f"• **{r['Station']}** — {int(d)}m — {r['Docks']} docks\n"
            else:
                reply = "❌ No docking stations nearby."

        # ⚠️ STOCKOUT LIST
        elif "stockout" in text:
            stock = df[df["Bikes"] == 0]["Station"].head(5)
            reply = "⚠️ **Stations with no bikes:**\n\n"
            reply += "\n".join(stock) if len(stock) > 0 else "None currently"

        # ⚠️ FULL STATIONS
        elif "full" in text or "overflow" in text:
            full = df[df["Docks"] == 0]["Station"].head(5)
            reply = "⚠️ **Stations with no docks:**\n\n"
            reply += "\n".join(full) if len(full) > 0 else "None currently"

        # 🔮 PREDICTIVE ALERTS ⭐
        elif "predict" in text or "risk" in text or "alert" in text:
            risk_df = get_risk_stations()

            reply = "🔮 **High Risk (Likely Stockout Soon):**\n\n"

            for _, r in risk_df.iterrows():
                reply += f"🚨 **{r['Station']}** — {r['Bikes']} bikes left\n"

            reply += "\n💡 Consider avoiding these stations."

        # 🤖 DEFAULT SMART RESPONSE
        else:
            reply = """💬 **Try asking:**
- Where can I find a bike?
- Where can I return my bike?
- Show stockout stations
- Predict high-risk stations
"""

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # SAVE RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # DISPLAY RESPONSE WITH THINKING EFFECT
    with st.chat_message("assistant"):
        with st.spinner("Analyzing real-time data..."):
            time.sleep(0.5)
            st.markdown(reply)

st.markdown('</div>', unsafe_allow_html=True)