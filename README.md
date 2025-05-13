# 🌏 APAC Scrim Recommendation Tool

A stylish, data-driven **Streamlit app** to help Valorant teams find the best scrim opponents in the APAC region based on map performance and team composition history.

---

## 🧠 What It Does

- 🗺️ Select a map you want to practice (e.g., *Ascent*, *Icebox*)
- 📊 View top-performing APAC teams on that map
- 🧩 See each team’s **win rate**, **match count**, and **most-used composition**
- 🖼️ Displays team logos inline
- 🧼 Automatically filters out teams with:
  - Fewer than 2 matches played
  - Less than 50% win rate

---

## 🛠️ Tech Stack

- **Streamlit**
- **Pandas**
- **Custom CSS** for dark Guardian-style UI

---

## 📁 Folder Structure

scrimz/
├── app.py
└── team_logos/
    ├── DRX.png
    ├── Talon.png
    ├── Global Esports.png
    └── ...

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/Ominousx/apac-scrim-tool.git
cd apac-scrim-tool
pip install -r requirements.txt
streamlit run app.py

✍️ Credits

Built by @_SushantJha 🎮
For feedback or feature requests, open an issue or connect on Twitter/X
