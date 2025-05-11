# 🌱 OpenCompliance ESG

A complete open-source pipeline for Environmental, Social, and Governance (ESG) risk analysis — built with Python, dbt, DuckDB, Great Expectations, FastAPI, and Streamlit.

## ✅ Features

- 🧼 Data ingestion & validation (Great Expectations)
- 🧱 dbt-powered transformation on DuckDB
- 🧠 ML model for ESG risk prediction (RandomForest)
- 📊 Streamlit dashboard with interactive filters & PDF export
- 🚀 Real-time prediction API with FastAPI
- 🔁 GitHub Actions for CI/CD and automation

## 📁 Project Structure

```
opencompliance-esg/
├── api/                    # FastAPI app
├── dashboard/              # Streamlit dashboard
├── ingestion/              # CSV loader
├── transformation/         # dbt + ML model training
├── validation/             # Pydantic schema + GX configs
├── output/                 # Model + predictions
├── .github/workflows/      # CI/CD pipeline
├── requirements.txt
├── README.md
└── run_guide.md
```

## 🚀 Live Demos

- **Dashboard**: [Streamlit App](https://opencompliance-esg-v9vsujgrphuxndtpx4pddh.streamlit.app)
- **API Docs**: [FastAPI Swagger](https://opencompliance-esg.onrender.com/docs)

## 📦 Requirements

- Python 3.10+
- pip, dbt-core, duckdb, streamlit, fastapi, uvicorn, joblib, plotly
