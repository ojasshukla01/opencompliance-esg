# 🛠 Run Guide – OpenCompliance ESG

Step-by-step instructions to set up and run the project.

---

## 🔧 1. Clone and Set Up

```bash
git clone https://github.com/ojasshukla01/opencompliance-esg.git
cd opencompliance-esg
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏗 2. Run Pipeline Locally

### ✅ Ingest + Validate ESG data

```bash
python scripts/ingest_and_validate.py
```

### ✅ Transform with dbt

```bash
cd transformation
dbt run
```

### ✅ Train ESG Risk Model

```bash
python transformation/ml/train_model.py
```

---

## 🌐 3. Launch Dashboard (Streamlit)

```bash
streamlit run dashboard/esg_dashboard.py
```

Access the app at: `http://localhost:8501`

---

## 🚀 4. Run Real-Time API (FastAPI)

```bash
uvicorn api.predict_api:app --reload
```

Then visit: `http://127.0.0.1:8000/docs`

---

## 🤖 5. GitHub Actions CI/CD

CI/CD pipeline runs daily & on push:

- Runs dbt + validation + model training
- Uploads predictions as artifact
- Pings FastAPI `/predict` endpoint

Workflow file: `.github/workflows/pipeline.yml`

---

## 🌍 6. Deployment Links

- **Streamlit**: [View Dashboard](https://opencompliance-esg-v9vsujgrphuxndtpx4pddh.streamlit.app)
- **FastAPI**: [View API Docs](https://opencompliance-esg.onrender.com/docs)

---

## 🔁 Automated With

- GitHub Actions (CI/CD)
- Render (FastAPI Hosting)
- Streamlit Cloud (Dashboard)
