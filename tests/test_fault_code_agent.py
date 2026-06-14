from app.agents.fault_code_agent import FaultCodeAgent
from app.agents.intake_agent import IntakeAgent


def test_fault_code_agent_detects_known_code():
    text = "OBD scan shows diagnostic trouble code P0217."
    intake = IntakeAgent().run(case_text=text, source_file="test.txt")

    result = FaultCodeAgent().run(intake=intake)

    assert len(result.detected_codes) == 1
    assert result.detected_codes[0].code == "P0217"
    assert result.detected_codes[0].description == "Engine coolant over-temperature condition"


def test_fault_code_agent_detects_unknown_code():
    text = "OBD scan shows diagnostic trouble code P9999."
    intake = IntakeAgent().run(case_text=text, source_file="test.txt")

    result = FaultCodeAgent().run(intake=intake)

    assert len(result.detected_codes) == 1
    assert result.detected_codes[0].code == "P9999"
    assert result.detected_codes[0].description == "Unknown diagnostic trouble code"