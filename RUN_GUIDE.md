# 🛠️ How to Run OpenCompliance-ESG (End-to-End Instructions)

This guide will walk you through every step to run the Environmental, Social, and Governance(ESG) Risk Prediction platform — from setup to dashboard.

---

## 📦 Step 1: Clone the Repository

```bash
git clone https://github.com/ojasshukla01/opencompliance-esg.git
cd opencompliance-esg
```

---

## 🧪 Step 2: Create and Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate    # On Windows
```

---

## 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📁 Step 4: Run Data Validation (Great Expectations)

```bash
python scripts/ingest_and_validate.py
```

### 🔍 What this does:
- Loads `esg_sample.csv`
- Validates schema, nulls, and ranges
- Creates `ingestion_log.json`

✅ You’ll see:
```
✅ Loaded 500 records...
✅ 500 valid records...
📝 Ingestion log updated...
```

---

## 🧱 Step 5: Build Models Using dbt + DuckDB

```bash
cd transformation
dbt deps
dbt build
cd ..
```

### 🔍 What this does:
- Transforms ESG data using dbt models
- Persists cleaned results in DuckDB (`esg_cleaned`)
- Runs tests and profiling

✅ Output:
```
PASS dbt tests
OK created model esg_cleaned
```

---

## 🧠 Step 6: Train the Machine Learning Model

```bash
python transformation/ml/train_model.py
```

### 🔍 What this does:
- Loads `esg_cleaned` from DuckDB
- Trains a `RandomForestClassifier`
- Saves:
  - `output/esg_risk_model.pkl`
  - `output/esg_predictions.csv`

✅ Output includes:
- Classification Report
- Confusion Matrix
- ✅ Messages confirming saved model and predictions

---

## 🌐 Step 7: Launch Interactive Dashboard

```bash
streamlit run dashboard/esg_dashboard.py
```

📍 Go to `http://localhost:8501` or your Streamlit cloud URL.

### 🔍 Features:
- Filter by sector, country, ESG risk
- View distributions for emissions, labor, governance
- Live KPI metrics and sector breakdowns
- Human-readable field descriptions

---

## 🧼 To Interrupt / Debug

- Press `Ctrl + C` to stop any script
- If dbt fails to find a file, make sure path exists and re-run:  
  ```bash
  dbt clean && dbt deps && dbt build
  ```

---

## ✅ Summary of Key Outputs

| Output                           | Path                                     |
|----------------------------------|------------------------------------------|
| Cleaned ESG Table                | `data/esg_transformed.duckdb > esg_cleaned` |
| Ingestion Log                    | `data/ingestion_log.json`               |
| Trained ML Model                 | `output/esg_risk_model.pkl`             |
| Model Predictions                | `output/esg_predictions.csv`            |
| Streamlit Dashboard              | `dashboard/esg_dashboard.py`            |
| Data Quality Reports             | `great_expectations/uncommitted/`       |

---

## 🏁 Done!
You're now running a complete ESG prediction platform with data validation, transformation, machine learning, and visualization — all locally and open source.
