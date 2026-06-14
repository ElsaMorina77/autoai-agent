from app.schemas.diagnostic_schema import (
    DiagnosticOutput,
    FaultCodeOutput,
    ImpactOutput,
    IntakeOutput,
    RecommendationOutput,
    RetrievalOutput,
    SensorAnalysisOutput,
)


class ReportAgent:
    """Creates a clean final diagnostic report."""

    def run(
        self,
        intake: IntakeOutput,
        fault_codes: FaultCodeOutput,
        sensor_analysis: SensorAnalysisOutput,
        retrieval: RetrievalOutput,
        diagnosis: DiagnosticOutput,
        impact: ImpactOutput,
        recommendations: RecommendationOutput,
    ) -> str:
        findings_text = "\n".join(
            [
                f"- {finding.cause} "
                f"(confidence: {finding.confidence:.0%}) | Evidence: {', '.join(finding.evidence)}"
                for finding in diagnosis.findings
            ]
        )

        actions_text = "\n".join(
            [
                f"{idx}. {action}"
                for idx, action in enumerate(
                    recommendations.recommended_actions,
                    start=1,
                )
            ]
        )

        symptoms_text = "\n".join([f"- {symptom}" for symptom in intake.symptoms])
        fault_codes_text = self._format_fault_codes(fault_codes)
        retrieved_text = self._format_retrieved_documents(retrieval)
        sensor_text = self._format_sensor_analysis(sensor_analysis)

        return f"""Source file: {intake.source_file}

Detected issue type:
{intake.detected_issue_type}

Detected symptoms:
{symptoms_text}

Detected diagnostic trouble codes:
{fault_codes_text}

Retrieved maintenance knowledge:
{retrieved_text}

Primary diagnosis:
{diagnosis.primary_diagnosis}

Diagnostic findings:
{findings_text}

Impact assessment:
- Severity: {impact.severity}
- Safety risk: {impact.safety_risk}
- Urgency: {impact.urgency}
- Cost risk: {impact.cost_risk}
- Risk score: {impact.score}/100

Recommended actions:
{actions_text}

Technician notes:
{recommendations.technician_notes}

Sensor analysis:
{sensor_text}
"""
    

    def _format_fault_codes(self, fault_codes: FaultCodeOutput) -> str:
        if not fault_codes.detected_codes:
            return "- No diagnostic trouble codes detected."

        return "\n".join(
            [
                f"- {fault.code}: {fault.description} "
                f"(severity hint: {fault.severity_hint})"
                for fault in fault_codes.detected_codes
            ]
        )

    def _format_retrieved_documents(self, retrieval: RetrievalOutput) -> str:
        if not retrieval.retrieved_documents:
            return "- No relevant maintenance documents found."

        return "\n".join(
            [
                f"- {document.document_name} "
                f"(score: {document.relevance_score}/100, "
                f"matched: {', '.join(document.matched_keywords)})"
                for document in retrieval.retrieved_documents
            ]
        )
    
    def _format_sensor_analysis(self, sensor_analysis: SensorAnalysisOutput) -> str:
        if not sensor_analysis.findings:
            return f"- {sensor_analysis.summary}"

        lines = [f"- {sensor_analysis.summary}"]

        for finding in sensor_analysis.findings:
            lines.append(
                f"- {finding.metric}: {finding.finding} "
                f"(value: {finding.value}, threshold: {finding.threshold}, severity: {finding.severity})"
            )

        return "\n".join(lines)

   
