import pandas as pd
import streamlit as st
import plotly.express as px
import joblib

# --- Upload + Predict ---
import joblib

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


 # Load trained model
    try:
        model = joblib.load("output/esg_risk_model.pkl")
        required_columns = ["emissions_score", "labor_compliance_score", "governance_index"]

        if all(col in df.columns for col in required_columns):
            df["predicted_esg_flagged"] = model.predict(df[required_columns])
            st.success("✅ Predictions added to uploaded file.")
        else:
            missing = [col for col in required_columns if col not in df.columns]
            st.warning(f"⚠️ Uploaded CSV is missing required columns: {missing}")
    except Exception as e:
        st.error(f"🚫 Failed to load model or predict: {e}")



    # Ensure columns exist
    try:
        input_df = df[["emissions_score", "labor_compliance_score", "governance_index"]]
        df["predicted_esg_flagged"] = model.predict(input_df)
        st.success("✅ Predictions added for uploaded file!")
    except Exception as e:
        st.error(f"⚠️ Could not apply prediction: {e}")

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
