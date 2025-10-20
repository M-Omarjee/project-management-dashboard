# 📈 ProjectPulse Dashboard

**ProjectPulse** is a lightweight, data-driven project management analytics tool that combines a Python FastAPI backend with a Streamlit dashboard frontend.  
It visualises project KPIs, risks, forecasts and financial performance in real-time — similar to a Power BI portfolio view, but entirely open-source.

---

## 🏗️ Features

| Area | Description |
|------|--------------|
| **FastAPI Backend** | Provides JSON endpoints for `/kpis`, `/forecast`, `/risks`, `/summary`, and `/finance`. |
| **Streamlit Frontend** | Interactive, auto-updating dashboard with responsive layout. |
| **Overview Tab** | Key portfolio metrics, delay probabilities and an executive summary. |
| **Finance Tab** | Grouped Budget vs Actual chart, variance table with conditional colouring, and CSV download. |
| **Filters** | Real-time filtering by project phase and status. |
| **Dark Theme** | Modern UI consistent with data-driven executive dashboards. |

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/M-Omarjee/projectpulse-dashboard.git
cd projectpulse-dashboard
```
### 2. Set up your virtual environment
```
python3.11 -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 🚀 Run Locally
Start the backend API:
```
uvicorn src.main:app --reload
```
It will run at http://127.0.0.1:8000
### Start the dashboard
```
streamlit run dashboard_app.py
```
The app will open at http://localhost:8501
### 🧮 Example API Outputs
/kpis
{"projects":5,"avg_completion_pct":65.8,"cost_variance_pct":-6.7,"time_variance_pct":6.3,"on_track":1,"at_risk":1,"delayed":3}
/finance
[
  {"Project_ID":"NHS-001","Budget":2192743,"Actual":2515766,"Variance_Amount":323023,"Variance_Pct":14.7},
  {"Project_ID":"NHS-002","Budget":1739911,"Actual":1710103,"Variance_Amount":-29808,"Variance_Pct":-1.7}
]
### 📊 Screenshot
Overview	Finance
(place your PNGs inside a /docs/ folder)
### 🧠 Future Enhancements
🔄 Cloud deployment via Streamlit Cloud or Hugging Face Spaces
🗂️ SQLite/PostgreSQL backend for persistent data
🧩 Power BI connector or REST-based integration
📬 Automated daily email summaries