from app.schemas.diagnostic_schema import (
    DiagnosticOutput,
    FaultCodeOutput,
    ImpactOutput,
    IntakeOutput,
    SensorAnalysisOutput,
)


class ImpactAgent:
    """Scores severity, safety risk, urgency, and cost risk."""

    HIGH_RISK_TERMS = ["smoke", "burning smell", "brake", "overheating", "engine temperature"]
    MEDIUM_RISK_TERMS = ["warning light", "noise", "vibration", "loss of power"]

    HIGH_RISK_CODES = {"P0217", "C0035"}
    MEDIUM_RISK_CODES = {"P0300", "P0562", "P0700"}

    def run(
        self,
        intake: IntakeOutput,
        diagnosis: DiagnosticOutput,
        fault_codes: FaultCodeOutput,
        sensor_analysis: SensorAnalysisOutput,
    ) -> ImpactOutput:
        text = intake.raw_case_text.lower()
        issue_type = intake.detected_issue_type
        detected_code_values = {fault.code for fault in fault_codes.detected_codes}

        score = 30

        if issue_type in {"engine_overheating", "brake_issue"}:
            score += 35

        score += 10 * sum(1 for term in self.HIGH_RISK_TERMS if term in text)
        score += 5 * sum(1 for term in self.MEDIUM_RISK_TERMS if term in text)

        score += 15 * len(detected_code_values.intersection(self.HIGH_RISK_CODES))
        score += 8 * len(detected_code_values.intersection(self.MEDIUM_RISK_CODES))

        high_sensor_findings = sum(
            1 for finding in sensor_analysis.findings if finding.severity == "High"
        )
        medium_sensor_findings = sum(
            1 for finding in sensor_analysis.findings if finding.severity == "Medium"
        )

        score += high_sensor_findings * 10
        score += medium_sensor_findings * 5

        score = min(score, 100)

        if score >= 80:
            severity = "Critical"
            safety_risk = "High"
            urgency = "Immediate inspection required"
            cost_risk = "High if ignored"
        elif score >= 60:
            severity = "High"
            safety_risk = "Medium to High"
            urgency = "Inspect within 24 hours"
            cost_risk = "Medium to High"
        elif score >= 40:
            severity = "Medium"
            safety_risk = "Medium"
            urgency = "Schedule service soon"
            cost_risk = "Medium"
        else:
            severity = "Low"
            safety_risk = "Low"
            urgency = "Monitor and inspect during routine service"
            cost_risk = "Low"

        return ImpactOutput(
            severity=severity,
            safety_risk=safety_risk,
            urgency=urgency,
            cost_risk=cost_risk,
            score=score,
        )