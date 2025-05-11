import os
import duckdb
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. Load data
con = duckdb.connect("data/esg_transformed.duckdb")
df = con.execute("SELECT * FROM esg_cleaned").fetch_df()

# 2. Prepare data
X = df[['emissions_score', 'labor_compliance_score', 'governance_index']]
y = df['esg_flagged']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. GridSearchCV: Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5],
}
grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)

# 4. Best model
best_model = grid.best_estimator_
print("🌟 Best Parameters:", grid.best_params_)

# 5. Evaluate
y_pred = best_model.predict(X_test)
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧩 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 6. Save model & predictions
os.makedirs("output", exist_ok=True)
joblib.dump(best_model, "output/esg_risk_model.pkl")
df['predicted_esg_flagged'] = best_model.predict(X)
df.to_csv("output/esg_predictions.csv", index=False)

print("✅ Tuned model saved to output/esg_risk_model.pkl")
print("✅ Predictions saved to output/esg_predictions.csv")
