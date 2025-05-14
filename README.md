# 🌏 APAC Scrim Recommendation Tool

A sleek Streamlit web app that helps analysts and teams discover the **best-performing scrim opponents by map and region** in the Asia-Pacific Valorant scene — powered by real VLR.gg data.

![Screenshot](screenshot.png)

---

## 📊 What It Does

This tool lets you:
- 🔢 **Filter by Tier 1 / Tier 2 leagues**
- 🗺️ **Choose a specific Valorant map**
- 🔍 See the **top 3 teams** based on win rate, with:
  - Streak indicators 🔥
  - Most common comps 🧬
  - W/L stats 📈
- 💡 Filter logic is based on recent match data from [vlr.gg](https://vlr.gg)

---

## ✨ Features

- ⚡ **Live Data Fetching** from Google Sheets (linked to VLR-scraped stats)
- 🌗 **Dark grey UI** with a minimal, modern layout
- 🔥 **Streak highlighting** for in-form teams
- 🎨 **Team logos and composition badges**
- 📅 **Last updated date** clearly displayed

---

## 🚀 Run Locally

Clone this repo:

```bash
git clone https://github.com/Ominousx/apac-scrim-tool.git
cd apac-scrim-tool
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Styling**: Custom CSS (Poppins font, responsive layout)
- **Data Source**: Google Sheets linked from [vlr.gg](https://vlr.gg)
- **Hosting**: Can be deployed via Streamlit Cloud / Hugging Face Spaces / GitHub Pages (static screenshot + repo)

---

## 📂 File Structure

```bash
📁 apac-scrim-tool
├── app.py
├── .streamlit/
│   └── config.toml
├── maps/
│   ├── ascent.png
│   ├── murash_logo.png
│   └── ...
├── screenshot.png
├── requirements.txt
└── README.md
```

---

## ✍️ Credits

Built by [@Ominous](https://twitter.com/_SushantJha) 🎮

For feedback, feature requests, or contributions, feel free to:
- Open an issue
- Fork the repo
- Or connect on Twitter

📊 Data from [vlr.gg](https://vlr.gg)
