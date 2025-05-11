import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv("output/esg_predictions.csv")

st.set_page_config(page_title="ESG Risk Dashboard", layout="wide")

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
country = st.sidebar.multiselect("Country", df["country"].unique(), default=df["country"].unique())
sector = st.sidebar.multiselect("Sector", df["sector"].unique(), default=df["sector"].unique())
flagged = st.sidebar.radio("Predicted ESG Risk", ["All", True, False], index=0)

filtered = df[df["country"].isin(country) & df["sector"].isin(sector)]
if flagged != "All":
    filtered = filtered[filtered["predicted_esg_flagged"] == flagged]

# --- KPIs ---
st.subheader("📊 KPI Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(filtered))
col2.metric("Flagged as ESG Risk", int(filtered["predicted_esg_flagged"].sum()))
col3.metric("Flag Rate (%)", round(filtered["predicted_esg_flagged"].mean() * 100, 2))

# --- Data Table ---
st.subheader("📄 Filtered Dataset")
st.dataframe(filtered)

# --- Bar Chart of Flagged Count ---
st.subheader("🔍 ESG Risk Count by Sector")
bar = filtered.groupby("sector")["predicted_esg_flagged"].sum().reset_index()
st.plotly_chart(px.bar(bar, x="sector", y="predicted_esg_flagged", color="sector",
                       labels={"predicted_esg_flagged": "Flagged Orgs"},
                       title="Flagged Organizations per Sector"), use_container_width=True)

# --- ESG Score Distributions ---
st.subheader("📈 ESG Score Distributions")
score_cols = ["emissions_score", "labor_compliance_score", "governance_index"]
for col in score_cols:
    st.plotly_chart(px.histogram(filtered, x=col, nbins=30, title=f"Distribution of {col.replace('_', ' ').title()}"), use_container_width=True)
