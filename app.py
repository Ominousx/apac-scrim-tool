import streamlit as st
import pandas as pd
import os
import base64
from summary_utils import get_summary

st.set_page_config(page_title="APAC Scrim Recommendation Tool", layout="wide")

# --- Local CSS Styling ---
def local_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
             html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif !important;
                background-color: #121212 !important;
                color: #e0e0e0 !important;
            }

            .main {
                background-color: #121212 !important;
            }

            .block-container {
                background-color: #121212 !important;
                padding-top: 2rem;
            }
            .title {
                font-size: 2.5rem;
                font-weight: 600;
                color: #f5f5f5;
                margin-bottom: 0.5rem;
                text-align: center;
            }
            .subtitle {
                color: #cccccc;
                font-size: 1.1rem;
                margin-bottom: 2rem;
                text-align: center;
            }
            .team-box {
                background-color: #121212;
                border: 1px solid #444;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            .team-box:hover {
                transform: scale(1.02);
                border-color: #666;
                background-color: #333;
            }
            .team-box-inline {
                display: flex;
                align-items: center;
                gap: 20px;
                text-align: left;
            }
            .team-box-inline[style*='border-color: #ffc107'] {
                box-shadow: 0 0 12px #ffc10788;
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
            .badge {
                background-color: #3a3a3a;
                padding: 4px 10px;
                border-radius: 8px;
                font-weight: 500;
            }
            .fire {
                display: inline-block;
                animation: pulse 1.3s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.9; }
                50% { transform: scale(1.2); opacity: 1; }
                100% { transform: scale(1); opacity: 0.9; }
            }
            .stMultiSelect [data-baseweb="tag"] {
                background-color: #3a3a3a !important;
                color: white !important;
            }
            .stMultiSelect [data-baseweb="tag"]:hover {
                background-color: #4a4a4a !important;
            }
            html, body {
                height: 100% !important;
                overflow-y: auto !important;
                scroll-behavior: smooth;
            }
            .main, .block-container {
                min-height: 100vh !important;
                overflow-y: auto !important;
                padding-top: 2rem;
            }
            body::before {
                content: '';
                display: block;
                height: 1px;
                margin-top: -1px;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

st.markdown("<div class='title'>🌏 Asia Scrim Recommendation Tool</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Get team scrim suggestions by map and region based on recent match data</div>", unsafe_allow_html=True)

from datetime import datetime

# Get today's date
last_updated = datetime.today().strftime("%B %d, %Y")

st.markdown(f"""
<div style='text-align: center; font-size: 0.9rem; color: #888; margin-bottom: 1.5rem;'>
    <span>📊 Data from: <a href="https://vlr.gg" target="_blank" style="color: #8affc1; text-decoration: none;">vlr.gg</a></span>
    &nbsp;|&nbsp;
    <span>🕒 Last updated: <span style="color: #ccc;">{last_updated}</span></span>
</div>
""", unsafe_allow_html=True)

SHEET_LINKS = {
    "VCT Pacific": "https://docs.google.com/spreadsheets/d/1LCzcBgnHJXjNFTAsrY0KVk1nF81r0gxPoqKBPZkvh4M/gviz/tq?tqx=out:csv",
    "VCL SEA": "https://docs.google.com/spreadsheets/d/1uTaneDKNLeE9XIWfwPMRrThI-AHvlqx0b9WxDiLE_eE/gviz/tq?tqx=out:csv",
    "VCL JP": "https://docs.google.com/spreadsheets/d/1CimAbYkpq3fH2-Bfz6DsNR537Dr0BIumQ8ehAv7Ga-w/gviz/tq?tqx=out:csv",
    "VCL KR": "https://docs.google.com/spreadsheets/d/1WpRhAug3qon-YE4llo_gQ8pzjwixQ3l9lC6uxjzvUoY/gviz/tq?tqx=out:csv",
    "CN": "https://docs.google.com/spreadsheets/d/1NGhZtuqgAHFzNQtdtM0KRjVihBaKKIujWh_NHCA1fA0/gviz/tq?tqx=out:csv"
}

TIER_MAP = {
    "Tier 1": ["VCT Pacific", "CN"],
    "Tier 2": ["VCL SEA", "VCL JP", "VCL KR"]
}

# --- UI Filters ---
col1, col2 = st.columns([2, 1])

with col1:
    selected_tiers = st.multiselect(
        "🔢 Select Tiers",
        options=list(TIER_MAP.keys()),
        default=list(TIER_MAP.keys()),
        help="Tier 1 = VCT Pacific + CN | Tier 2 = VCL SEA + JP + KR"
    )
    selected_regions = [region for tier in selected_tiers for region in TIER_MAP[tier]]

if selected_regions:
    dfs = [pd.read_csv(SHEET_LINKS[reg]) for reg in selected_regions if reg in SHEET_LINKS]
    df = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]

    with col2:
        maps = sorted(df["Map Name"].dropna().unique())
        selected_map = st.selectbox("🗺️ Choose a Map", maps)
else:
    st.warning("Please select at least one region to view data.")
    st.stop()

map_df = df[df["Map Name"] == selected_map]

# Final filtering
all_region_dfs = [(reg, df[df["Map Name"] == selected_map]) for reg, df in zip(selected_regions, dfs)]
summary = get_summary(all_region_dfs)
#st.dataframe(summary[["Team", "WinRate", "Matches", "Streak", "Tier", "ScrimScore"]]) (test to see scores)
summary = summary.loc[(summary["Matches"] >= 3) & (summary["WinRate"] >= 50)]
top3 = summary.head(3)
others = summary.iloc[3:]

# Render block
def render_team_row(row, highlight=False):
    team = row['Team'].strip()
    logo_path = f"maps/{team}.png"
    fire = '<span class="fire">🔥</span>' if row.get("Streak", 0) >= 3 else ""
    if os.path.exists(logo_path):
        encoded = base64.b64encode(open(logo_path, "rb").read()).decode()
        logo_html = f'{fire}<img src="data:image/png;base64,{encoded}" class="logo-inline" alt="{team} logo" />'
    else:
        logo_html = ""

    border_style = "border-color: #ffc107;" if highlight else ""

    st.markdown(f"""
        <div class="team-box team-box-inline" style="{border_style}">
            {logo_html}
            <div class="team-info">
                <div class="team-name"><span class="badge">{team}</span></div>
                <div class="comp">🧬 {row['CommonComp']}</div>
                <div class="stat">📊 Win Rate: {row['WinRate']}% | 🧩 {int(row['Wins'])} / {int(row['Matches'])} Wins</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Top 3
st.markdown("<div class='team-name' style='font-size:1.5rem;margin-top:30px;'>🏆 Top Picks</div>", unsafe_allow_html=True)
for _, row in top3.iterrows():
    render_team_row(row, highlight=True)

# Others
if not others.empty:
    st.markdown("<div class='team-name' style='font-size:1.2rem;margin-top:20px;'>🧪 Other Picks</div>", unsafe_allow_html=True)
    for _, row in others.iterrows():
        render_team_row(row)

# --- Footer with X, GitHub, Medium icons ---
def encode_img(path, height=18):
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/png;base64,{encoded}" style="height:{height}px; vertical-align:middle; margin-right:6px;" />'
    return ""

x_logo = encode_img("maps/xcom.png")
gh_logo = encode_img("maps/gitHub.png")
md_logo = encode_img("maps/medium.png")

st.markdown(f"""
<hr style="margin-top: 50px; margin-bottom: 10px; border: 0.5px solid #333;" />
<div style="text-align: center; font-size: 0.9rem; color: #888;">
    📊 Data from past 60 days<br>
    {x_logo}<a href="https://twitter.com/_SushantJha" target="_blank" style="color:#8affc1;text-decoration:none;">@Ominous</a>
    &nbsp;&nbsp;&nbsp;
    {gh_logo}<a href="https://github.com/Ominousx/apac-scrim-tool" target="_blank" style="color:#8affc1;text-decoration:none;">GitHub</a>
    &nbsp;&nbsp;&nbsp;
    {md_logo}<a href="https://medium.com/@_SushantJha" target="_blank" style="color:#8affc1;text-decoration:none;">Medium</a>
</div>
""", unsafe_allow_html=True)
