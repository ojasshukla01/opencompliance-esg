from pydantic import BaseModel, Field
from datetime import date

class ESGRecord(BaseModel):
    org_id: str
    org_name: str
    sector: str
    country: str
    emissions_score: float = Field(ge=0, le=100)
    labor_compliance_score: float = Field(ge=0, le=100)
    governance_index: float = Field(ge=0, le=100)
    esg_flagged: bool
    report_date: date
