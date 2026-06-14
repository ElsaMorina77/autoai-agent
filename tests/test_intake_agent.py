from app.agents.intake_agent import IntakeAgent


def test_intake_detects_engine_overheating():
    text = "The car is overheating and has a coolant leak."
    result = IntakeAgent().run(case_text=text, source_file="test.txt")

    assert result.detected_issue_type == "engine_overheating"
    assert "coolant leak" in result.symptoms


def test_intake_ignores_negated_noise_symptom():
    text = "The car is overheating. No major noise reported."
    result = IntakeAgent().run(case_text=text, source_file="test.txt")

    assert result.detected_issue_type == "engine_overheating"
    assert "noise" not in result.symptoms