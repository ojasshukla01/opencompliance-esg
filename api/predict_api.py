from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# Load trained model
model = joblib.load("output/esg_risk_model.pkl")

# Define request schema
class ESGRequest(BaseModel):
    org_id: str
    emissions_score: float
    labor_compliance_score: float
    governance_index: float

# Define response schema
class ESGResponse(BaseModel):
    org_id: str
    predicted_esg_flagged: bool

# Init FastAPI app
app = FastAPI(title="ESG Risk Prediction API")

@app.post("/predict", response_model=ESGResponse)
def predict_esg(data: ESGRequest):
    try:
        features = np.array([
            data.emissions_score,
            data.labor_compliance_score,
            data.governance_index
        ]).reshape(1, -1)

        prediction = model.predict(features)[0]
        return ESGResponse(org_id=data.org_id, predicted_esg_flagged=bool(prediction))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
