import pandas as pd
import streamlit as st

# Load predictions
df = pd.read_csv("output/esg_predictions.csv")

st.title("🌱 ESG Risk Prediction Dashboard")

# Filters
st.sidebar.header("🔎 Filter")
countries = st.sidebar.multiselect("Country", df["country"].unique(), default=df["country"].unique())
sectors = st.sidebar.multiselect("Sector", df["sector"].unique(), default=df["sector"].unique())
flagged = st.sidebar.radio("ESG Flagged", options=["All", True, False], index=0)

# Apply filters
filtered_df = df[df["country"].isin(countries) & df["sector"].isin(sectors)]
if flagged != "All":
    filtered_df = filtered_df[filtered_df["predicted_esg_flagged"] == flagged]

st.dataframe(filtered_df)

# Show summary
st.subheader("📊 Prediction Breakdown")
st.bar_chart(filtered_df["predicted_esg_flagged"].value_counts())

# Show ESG score distribution
st.subheader("📈 ESG Score Distribution")
st.line_chart(filtered_df[["emissions_score", "labor_compliance_score", "governance_index"]])
