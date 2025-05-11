# 🌱 OpenCompliance-ESG

**End-to-End ESG Risk Prediction Platform** using Python, dbt, DuckDB, Great Expectations, and Scikit-learn — entirely open source and reproducible.

---

## 🚀 Project Overview

This project builds a reproducible data pipeline and machine learning workflow that:
- ✅ Ingests raw ESG CSV data
- ✅ Validates schema and data quality with Great Expectations
- ✅ Transforms and models data using dbt + DuckDB
- ✅ Trains a Random Forest model to predict ESG risk (`esg_flagged`)
- ✅ Saves predictions and trained model artifacts for downstream use

---

## 🧱 Tech Stack

| Tool               | Purpose                              |
|--------------------|--------------------------------------|
| `dbt`              | Data modeling & transformation       |
| `DuckDB`           | Embedded columnar database           |
| `Great Expectations` | Data validation & profiling         |
| `scikit-learn`     | Machine learning (Random Forest)     |
| `pandas`           | DataFrame operations                 |
| `joblib`           | Model serialization                  |

---

## 📁 Folder Structure

opencompliance-esg/
├── data/                     # Raw ESG data
├── output/                   # Saved model and predictions
├── transformation/           # dbt models and configs
│   ├── models/
│   ├── dbt_project.yml
│   └── ml/train_model.py     # ML training pipeline
├── scripts/                  # Utility scripts
├── great_expectations/       # Data validation config
├── README.md                 # ← You are here

---

## 🛠️ How to Run

# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate    # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build pipeline
cd transformation
dbt deps
dbt build
cd ..

# 4. Run ML model
python transformation/ml/train_model.py

---

## 📊 Outputs

| Artifact | Path |
|----------|------|
| Trained model | output/esg_risk_model.pkl |
| Predictions CSV | output/esg_predictions.csv |
| Validation reports | great_expectations/uncommitted/data_docs/ |