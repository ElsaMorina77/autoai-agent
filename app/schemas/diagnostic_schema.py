from typing import List
from pydantic import BaseModel, Field


class IntakeOutput(BaseModel):
    source_file: str
    raw_case_text: str
    detected_issue_type: str
    symptoms: List[str]


class FaultCode(BaseModel):
    code: str
    description: str
    severity_hint: str


class FaultCodeOutput(BaseModel):
    detected_codes: List[FaultCode]


class SensorFinding(BaseModel):
    metric: str
    finding: str
    value: float
    threshold: float
    severity: str


class SensorAnalysisOutput(BaseModel):
    sensor_file: str | None
    findings: List[SensorFinding]
    summary: str


class RetrievedDocument(BaseModel):
    document_name: str
    matched_keywords: List[str]
    relevance_score: int = Field(ge=0, le=100)
    content_preview: str


class RetrievalOutput(BaseModel):
    query: str
    retrieved_documents: List[RetrievedDocument]


class DiagnosticFinding(BaseModel):
    cause: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[str]


class DiagnosticOutput(BaseModel):
    findings: List[DiagnosticFinding]
    primary_diagnosis: str


class ImpactOutput(BaseModel):
    severity: str
    safety_risk: str
    urgency: str
    cost_risk: str
    score: int = Field(ge=0, le=100)


class RecommendationOutput(BaseModel):
    recommended_actions: List[str]
    technician_notes: str


class PipelineResult(BaseModel):
    intake: IntakeOutput
    fault_codes: FaultCodeOutput
    sensor_analysis: SensorAnalysisOutput
    retrieval: RetrievalOutput
    diagnosis: DiagnosticOutput
    impact: ImpactOutput
    recommendations: RecommendationOutput
    final_report: str