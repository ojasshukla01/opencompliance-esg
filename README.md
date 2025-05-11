# 🧠 OpenCompliance: ESG Data Intelligence Platform

🚀 End-to-end ESG compliance monitoring and analytics system using open-source tools and cloud-native architecture.

---

## 🔍 Project Overview
This project simulates ESG compliance pipelines including:
- Real-time and batch data ingestion
- Schema and quality validation
- dbt-powered transformations
- ML-based ESG risk prediction
- API and frontend access
- Terraform & CI/CD for reproducibility

---

## 📁 Folder Structure

opencompliance-esg/
├── data/ # input + generated synthetic data
├── scripts/ # helper scripts (data gen, validation)
├── ingestion/ # file + api ingestion
├── validation/ # great expectations setup
├── transformation/ # dbt project
├── transformation/ml/ # model training & notebooks
├── infra/ # terraform infrastructure scripts
├── api/ # FastAPI microservices
├── dashboard/ # Streamlit or React frontend
├── notebooks/ # for data exploration
├── tests/ # unit & integration tests
├── docs/ # images, diagrams, architecture
└── .github/workflows/ # GitHub CI/CD automation


---

## 🛠️ Tech Stack
Python, dbt, DuckDB, Faker, FastAPI, Terraform, Great Expectations, Streamlit, GitHub Actions

---

## 📦 Setup (coming soon)
```bash
git clone https://github.com/ojasshukla01/opencompliance-esg.git
cd opencompliance-esg
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


📈 Roadmap
Project steps are documented in /docs and will be tracked via commits and versioned data.


Let me know once done, and we’ll proceed to:

---

## ✅ Step 1.2 – Define ESG Schema

Here is your schema file:

### 📄 Create File: `data/esg_schema.json`
```json
{
  "fields": [
    { "name": "org_id", "type": "uuid" },
    { "name": "org_name", "type": "string" },
    { "name": "sector", "type": "string" },
    { "name": "country", "type": "string" },
    { "name": "emissions_score", "type": "float", "range": [0, 100] },
    { "name": "labor_compliance_score", "type": "float", "range": [0, 100] },
    { "name": "governance_index", "type": "float", "range": [0, 100] },
    { "name": "esg_flagged", "type": "boolean" },
    { "name": "report_date", "type": "date", "format": "YYYY-MM-DD" }
  ]
}

📌 Save it inside: data/esg_schema.json