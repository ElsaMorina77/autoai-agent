from typing import List

from pydantic import BaseModel


class DiagnoseRequest(BaseModel):
    case_text: str
    source_file: str = "api_input.txt"
    sensor_file: str | None = None


class DiagnoseResponse(BaseModel):
    detected_issue_type: str
    symptoms: List[str]
    fault_codes: List[str]
    sensor_summary: str
    retrieved_documents: List[str]
    primary_diagnosis: str
    severity: str
    safety_risk: str
    urgency: str
    risk_score: int
    recommended_actions: List[str]
    final_report: str