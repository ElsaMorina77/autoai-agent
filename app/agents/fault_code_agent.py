import re

from app.schemas.diagnostic_schema import FaultCode, FaultCodeOutput, IntakeOutput


class FaultCodeAgent:
    """Extracts and explains automotive diagnostic trouble codes from the case text."""

    CODE_LIBRARY = {
        "P0217": {
            "description": "Engine coolant over-temperature condition",
            "severity_hint": "High",
        },
        "P0300": {
            "description": "Random or multiple cylinder misfire detected",
            "severity_hint": "Medium to High",
        },
        "P0562": {
            "description": "System voltage low",
            "severity_hint": "Medium",
        },
        "C0035": {
            "description": "Left front wheel speed sensor circuit issue",
            "severity_hint": "High",
        },
        "P0700": {
            "description": "Transmission control system malfunction",
            "severity_hint": "Medium to High",
        },
    }

    CODE_PATTERN = re.compile(r"\b[PCBU][0-9]{4}\b", re.IGNORECASE)

    def run(self, intake: IntakeOutput) -> FaultCodeOutput:
        raw_codes = self.CODE_PATTERN.findall(intake.raw_case_text.upper())
        unique_codes = sorted(set(raw_codes))

        detected_codes = []

        for code in unique_codes:
            metadata = self.CODE_LIBRARY.get(
                code,
                {
                    "description": "Unknown diagnostic trouble code",
                    "severity_hint": "Unknown",
                },
            )

            detected_codes.append(
                FaultCode(
                    code=code,
                    description=metadata["description"],
                    severity_hint=metadata["severity_hint"],
                )
            )

        return FaultCodeOutput(detected_codes=detected_codes)