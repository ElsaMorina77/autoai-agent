from app.core.orchestrator import DiagnosticOrchestrator


def test_orchestrator_generates_report():
    text = "Vehicle overheating with coolant leak, engine warning light, and fault code P0217."
    result = DiagnosticOrchestrator().run(case_text=text, source_file="test.txt")

    assert result.intake.detected_issue_type == "engine_overheating"
    assert result.fault_codes.detected_codes
    assert result.sensor_analysis.summary == "No sensor log provided."
    assert result.retrieval.retrieved_documents
    assert "Detected diagnostic trouble codes" in result.final_report
    assert "Sensor analysis" in result.final_report
    assert "Retrieved maintenance knowledge" in result.final_report
    assert "Primary diagnosis" in result.final_report
    assert len(result.recommendations.recommended_actions) > 0