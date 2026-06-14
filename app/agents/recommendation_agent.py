from app.schemas.diagnostic_schema import (
    DiagnosticOutput,
    ImpactOutput,
    IntakeOutput,
    RecommendationOutput,
)


class RecommendationAgent:
    """Generates technician-oriented next actions."""

    def run(
        self,
        intake: IntakeOutput,
        diagnosis: DiagnosticOutput,
        impact: ImpactOutput,
    ) -> RecommendationOutput:
        issue_type = intake.detected_issue_type

        if issue_type == "engine_overheating":
            actions = [
                "Check coolant level and inspect for visible leaks.",
                "Inspect radiator, hoses, and cooling fan operation.",
                "Run cooling-system pressure test.",
                "Test thermostat opening behavior.",
                "Do not continue driving if temperature remains high.",
            ]
        elif issue_type == "brake_issue":
            actions = [
                "Inspect brake pads, rotors, and calipers.",
                "Check brake fluid level and hydraulic pressure.",
                "Scan ABS module for fault codes.",
                "Avoid driving until safety inspection is complete.",
            ]
        elif issue_type == "battery_issue":
            actions = [
                "Measure battery voltage under load.",
                "Test alternator charging output.",
                "Inspect terminals, wiring, and ground connections.",
                "Check for parasitic current draw.",
            ]
        else:
            actions = [
                "Perform full diagnostic scan.",
                "Collect additional sensor readings.",
                "Inspect vehicle manually based on customer complaint.",
            ]

        technician_notes = (
            f"Primary diagnosis: {diagnosis.primary_diagnosis}. "
            f"Severity is {impact.severity} with urgency: {impact.urgency}."
        )

        return RecommendationOutput(
            recommended_actions=actions,
            technician_notes=technician_notes,
        )
