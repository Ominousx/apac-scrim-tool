import streamlit as st
import pandas as pd
import os
import base64

# --- Page config ---
st.set_page_config(page_title="APAC Scrim Recommendation Tool", layout="wide")

# --- CSS Styling ---
def local_css():
    st.markdown("""
        <style>
            body {
                background-color: #0e0e0e;
                color: #ffffff;
                font-family: 'Inter', sans-serif;
            }
            .block-container {
                padding-top: 2rem;
            }
            .title {
                font-size: 2.5rem;
                font-weight: bold;
                color: #f5f5f5;
                margin-bottom: 0.5rem;
            }
            .subtitle {
                color: #888;
                font-size: 1.1rem;
                margin-bottom: 2rem;
            }
            .team-box {
                background-color: #1c1c1e;
                border: 1px solid #333;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            .team-box:hover {
                border-color: #666;
                background-color: #2c2c2e;
            }
            .team-box-inline {
                display: flex;
                align-items: center;
                gap: 20px;
                text-align: left;
            }
            .logo-inline {
                width: 48px;
                height: 48px;
                border-radius: 6px;
                flex-shrink: 0;
            }
            .team-info {
                flex-grow: 1;
            }
            .team-name {
                font-size: 1.3rem;
                font-weight: 600;
                color: #fefefe;
                margin-bottom: 0.2rem;
            }
            .comp {
                font-family: monospace;
                color: #8affc1;
                font-size: 0.95rem;
            }
            .stat {
                margin-top: 10px;
                font-size: 0.9rem;
                color: #ccc;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- Load data from Google Sheets ---
sheet_url = "https://docs.google.com/spreadsheets/d/1LCzcBgnHJXjNFTAsrY0KVk1nF81r0gxPoqKBPZkvh4M/gviz/tq?tqx=out:csv"
df = pd.read_csv(sheet_url)

# --- Title ---
st.markdown("<div class='title'>🌏 APAC Scrim Recommendation Tool</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Select a map to find the best-performing teams with their comps.</div>", unsafe_allow_html=True)

# --- Select Map ---
maps = sorted(df["Map Name"].unique())
selected_map = st.selectbox("🗺️ Choose a Map", maps)

# --- Filter Map Data ---
map_df = df[df["Map Name"] == selected_map]

# --- Process Team Performance ---
def get_summary(map_df):
    data = []
    for _, row in map_df.iterrows():
        for side in [1, 2]:
            team = row[f"Team {side} Name"]
            score = row[f"Team {side} Score"]
            opp_score = row[f"Team {3 - side} Score"]
            agents = row[f"Team {side} Agents"]
            win = int(score > opp_score)
            data.append({
                "Team": team,
                "Win": win,
                "Comp": agents
            })

    df_summary = pd.DataFrame(data)
    grouped = (
        df_summary.groupby("Team")
        .agg(
            Matches=("Win", "count"),
            Wins=("Win", "sum"),
            WinRate=("Win", lambda x: round(100 * x.mean(), 1)),
            CommonComp=("Comp", lambda x: x.mode().iloc[0] if not x.mode().empty else "N/A")
        )
        .reset_index()
        .sort_values("WinRate", ascending=False)
    )
    return grouped

# --- Display Team Results (inline logos, skip 1-match teams) ---
summary = get_summary(map_df)
summary = summary[(summary["Matches"] > 1) & (summary["WinRate"] >= 50)]  # Hide teams with only 1 match

for _, row in summary.iterrows():
    team = row['Team'].strip()
    logo_path = f"maps/{team}.png"

    if os.path.exists(logo_path):
        encoded = base64.b64encode(open(logo_path, "rb").read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded}" class="logo-inline" alt="{team} logo" />'
    else:
        logo_html = ""

    st.markdown(f"""
        <div class="team-box team-box-inline">
            {logo_html}
            <div class="team-info">
                <div class="team-name">{team}</div>
                <div class="comp">🧬 {row['CommonComp']}</div>
                <div class="stat">📊 Win Rate: {row['WinRate']}% | 🧩 {int(row['Wins'])} / {int(row['Matches'])} Wins</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
