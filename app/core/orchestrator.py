from app.agents.diagnostic_agent import DiagnosticAgent
from app.agents.fault_code_agent import FaultCodeAgent
from app.agents.impact_agent import ImpactAgent
from app.agents.intake_agent import IntakeAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.report_agent import ReportAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.schemas.diagnostic_schema import PipelineResult
from app.agents.sensor_analysis_agent import SensorAnalysisAgent


class DiagnosticOrchestrator:
    """Runs the full AutoAI Agent pipeline."""

    def __init__(self) -> None:
        self.intake_agent = IntakeAgent()
        self.fault_code_agent = FaultCodeAgent()
        self.retrieval_agent = RetrievalAgent()
        self.diagnostic_agent = DiagnosticAgent()
        self.impact_agent = ImpactAgent()
        self.recommendation_agent = RecommendationAgent()
        self.report_agent = ReportAgent()
        self.sensor_analysis_agent = SensorAnalysisAgent()

    def run(self, case_text: str, source_file: str, sensor_file: str | None = None,) -> PipelineResult:
        intake = self.intake_agent.run(case_text=case_text, source_file=source_file)
        fault_codes = self.fault_code_agent.run(intake=intake)
        retrieval = self.retrieval_agent.run(intake=intake)
        sensor_analysis = self.sensor_analysis_agent.run(sensor_file=sensor_file)
        diagnosis = self.diagnostic_agent.run(
            intake=intake,
            retrieval=retrieval,
            fault_codes=fault_codes,
        )
        impact = self.impact_agent.run(
            intake=intake,
            diagnosis=diagnosis,
            fault_codes=fault_codes,
            sensor_analysis=sensor_analysis,
        )
        recommendations = self.recommendation_agent.run(
            intake=intake,
            diagnosis=diagnosis,
            impact=impact,
        )
        final_report = self.report_agent.run(
            intake=intake,
            fault_codes=fault_codes,
            sensor_analysis=sensor_analysis,
            retrieval=retrieval,
            diagnosis=diagnosis,
            impact=impact,
            recommendations=recommendations,
        )

        return PipelineResult(
            intake=intake,
            fault_codes=fault_codes,
            sensor_analysis=sensor_analysis,
            retrieval=retrieval,
            diagnosis=diagnosis,
            impact=impact,
            recommendations=recommendations,
            final_report=final_report,
        )