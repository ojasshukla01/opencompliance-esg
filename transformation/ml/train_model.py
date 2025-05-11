import os
import duckdb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# 1. Connect to the DuckDB database file
con = duckdb.connect("data/esg_transformed.duckdb")

# 2. Load the esg_cleaned table into a DataFrame
df = con.execute("SELECT * FROM esg_cleaned").fetch_df()

# 3. Define features and target
X = df[['emissions_score', 'labor_compliance_score', 'governance_index']]
y = df['esg_flagged']

# 4. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧩 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save the model
joblib.dump(model, "output/esg_risk_model.pkl")
print("✅ Trained model saved to output/esg_risk_model.pkl")

# Save predictions
df['predicted_esg_flagged'] = model.predict(X)
df.to_csv("output/esg_predictions.csv", index=False)
print("✅ Predictions saved to output/esg_predictions.csv")

