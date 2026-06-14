from fastapi import APIRouter

from app.api.schemas import DiagnoseRequest, DiagnoseResponse
from app.core.orchestrator import DiagnosticOrchestrator

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "AutoAI Agent API"}


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose_vehicle_case(request: DiagnoseRequest) -> DiagnoseResponse:
    orchestrator = DiagnosticOrchestrator()

    result = orchestrator.run(
        case_text=request.case_text,
        source_file=request.source_file,
        sensor_file=request.sensor_file,
    )

    return DiagnoseResponse(
        detected_issue_type=result.intake.detected_issue_type,
        symptoms=result.intake.symptoms,
        fault_codes=[
            fault_code.code for fault_code in result.fault_codes.detected_codes
        ],
        sensor_summary=result.sensor_analysis.summary,
        retrieved_documents=[
            document.document_name
            for document in result.retrieval.retrieved_documents
        ],
        primary_diagnosis=result.diagnosis.primary_diagnosis,
        severity=result.impact.severity,
        safety_risk=result.impact.safety_risk,
        urgency=result.impact.urgency,
        risk_score=result.impact.score,
        recommended_actions=result.recommendations.recommended_actions,
        final_report=result.final_report,
    )