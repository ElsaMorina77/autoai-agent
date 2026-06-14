from app.agents.diagnostic_agent import DiagnosticAgent
from app.agents.fault_code_agent import FaultCodeAgent
from app.agents.impact_agent import ImpactAgent
from app.agents.intake_agent import IntakeAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.sensor_analysis_agent import SensorAnalysisAgent


def test_impact_scores_overheating_as_high_risk():
    text = "Engine overheating with coolant leak, warning light, burning smell, and code P0217."

    intake = IntakeAgent().run(case_text=text, source_file="test.txt")
    fault_codes = FaultCodeAgent().run(intake=intake)
    retrieval = RetrievalAgent().run(intake=intake)
    sensor_analysis = SensorAnalysisAgent().run(sensor_file=None)
    diagnosis = DiagnosticAgent().run(
        intake=intake,
        retrieval=retrieval,
        fault_codes=fault_codes,
    )
    impact = ImpactAgent().run(
        intake=intake,
        diagnosis=diagnosis,
        fault_codes=fault_codes,
        sensor_analysis=sensor_analysis,
    )

    assert impact.score >= 80
    assert impact.severity == "Critical"