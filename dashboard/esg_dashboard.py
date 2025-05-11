import pandas as pd
import streamlit as st
import plotly.express as px
import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf_report import generate_esg_pdf

# --- Upload + Predict ---
uploaded_file = st.sidebar.file_uploader("📤 Upload your ESG CSV", type=["csv"])
default_df = pd.read_csv("output/esg_predictions.csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Loaded `{uploaded_file.name}` with {len(df)} records.")

    # Apply model prediction
    try:
        model = joblib.load("output/esg_risk_model.pkl")
        input_features = ["emissions_score", "labor_compliance_score", "governance_index"]

        if all(col in df.columns for col in input_features):
            df["predicted_esg_flagged"] = model.predict(df[input_features])
            st.success("✅ Predictions added to uploaded file.")
        else:
            missing = [col for col in input_features if col not in df.columns]
            st.warning(f"⚠️ Missing columns: {missing}")
    except Exception as e:
        st.error(f"❌ Failed to predict: {e}")
else:
    df = default_df.copy()
    st.info("Using default predictions from `output/esg_predictions.csv`.")

# --- Header ---
st.title("🌱 ESG Risk Prediction Dashboard")
st.markdown("""
This dashboard showcases the ESG risk prediction pipeline using machine learning.
It allows you to filter, explore, and visualize ESG scores and the model’s predictions (`esg_flagged`).
""")

# --- Data Description ---
with st.expander("📋 What the fields mean"):
    st.markdown("""
- `org_id`: Unique organization identifier  
- `org_name`: Name of the organization  
- `sector`: Economic sector  
- `country`: Country of operation  
- `emissions_score`: Score from 0–100 (lower is better environmental performance)  
- `labor_compliance_score`: Score from 0–100 (higher is better compliance)  
- `governance_index`: Governance quality indicator (0–100)  
- `esg_flagged`: Whether the org was flagged for ESG violation (`True` or `False`)  
- `predicted_esg_flagged`: What the model predicted  
- `report_date`: Date of ESG report
    """)

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Data")

# Country with select all
all_countries = df["country"].dropna().unique().tolist()
country = st.sidebar.multiselect("Country", ["All"] + all_countries, default=["All"])
selected_countries = all_countries if "All" in country else country

# Sector with select all
all_sectors = df["sector"].dropna().unique().tolist()
sector = st.sidebar.multiselect("Sector", ["All"] + all_sectors, default=["All"])
selected_sectors = all_sectors if "All" in sector else sector

# ESG Flag filter
flagged = st.sidebar.radio("Predicted ESG Risk", ["All", True, False], index=0)

# Apply filtering
if "predicted_esg_flagged" in df.columns:
    filtered = df[df["country"].isin(selected_countries) & df["sector"].isin(selected_sectors)]
    if flagged != "All":
        filtered = filtered[filtered["predicted_esg_flagged"] == flagged]
else:
    filtered = df.copy()

# --- KPIs ---
st.subheader("📊 KPI Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))

if "predicted_esg_flagged" in filtered.columns:
    flagged_count = int(filtered["predicted_esg_flagged"].sum())
    flagged_pct = round(filtered["predicted_esg_flagged"].mean() * 100, 2)
else:
    flagged_count = flagged_pct = 0

col2.metric("Flagged as ESG Risk", flagged_count)
col3.metric("Flag Rate (%)", flagged_pct)

# --- Data Table ---
st.subheader("📄 Filtered Dataset")
st.dataframe(filtered)

# --- Bar Chart of Flagged Count ---
st.subheader("🔍 ESG Risk Count by Sector")
if "predicted_esg_flagged" in filtered.columns:
    bar = filtered.groupby("sector")["predicted_esg_flagged"].sum().reset_index()
    st.plotly_chart(px.bar(
        bar,
        x="sector",
        y="predicted_esg_flagged",
        color="sector",
        labels={"predicted_esg_flagged": "Flagged Orgs"},
        title="Flagged Organizations per Sector"
    ), use_container_width=True)
else:
    st.info("Upload a file or run predictions to see ESG risk counts by sector.")

# --- ESG Score Distributions ---
st.subheader("📈 ESG Score Distributions")
score_cols = ["emissions_score", "labor_compliance_score", "governance_index"]
for col in score_cols:
    if col in filtered.columns:
        st.plotly_chart(px.histogram(filtered, x=col, nbins=30, title=f"Distribution of {col.replace('_', ' ').title()}"), use_container_width=True)

# --- Feature Importance ---
st.subheader("🧠 Feature Importance (Random Forest)")
try:
    model = joblib.load("output/esg_risk_model.pkl")
    importances = model.feature_importances_
    features = ["emissions_score", "labor_compliance_score", "governance_index"]
    importance_df = pd.DataFrame({"Feature": features, "Importance": importances})
    importance_df = importance_df.sort_values("Importance", ascending=True)
    st.bar_chart(importance_df.set_index("Feature"))
except Exception as e:
    st.warning(f"Could not load feature importances: {e}")

# --- Report Generation ---
st.subheader("🧾 Download ESG Reports")
if "predicted_esg_flagged" in filtered.columns and not filtered.empty:
    selected_org = st.selectbox("Select organization to download PDF:", filtered["org_name"].unique())
    selected_record = filtered[filtered["org_name"] == selected_org].iloc[0].to_dict()
    if st.button("📥 Generate PDF Report"):
        filename = generate_esg_pdf(selected_record)
        with open(filename, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name=filename, mime="application/pdf")
else:
    st.info("Apply filters and ensure predictions are available to download ESG reports.")