from pathlib import Path

from app.schemas.diagnostic_schema import (
    IntakeOutput,
    RetrievedDocument,
    RetrievalOutput,
)


class RetrievalAgent:
    """Retrieves relevant automotive manual sections for the detected issue."""

    MANUAL_KEYWORDS = {
        "engine_overheating": [
            "cooling",
            "coolant",
            "radiator",
            "thermostat",
            "temperature",
            "overheating",
            "water pump",
        ],
        "battery_issue": [
            "battery",
            "alternator",
            "starter",
            "voltage",
            "charging",
            "jump start",
        ],
        "brake_issue": [
            "brake",
            "braking",
            "abs",
            "rotor",
            "caliper",
            "brake fluid",
        ],
        "transmission_issue": [
            "transmission",
            "gear",
            "shifting",
            "clutch",
        ],
    }

    def __init__(self, manual_dir: str = "datasets/maintenance_manuals") -> None:
        self.manual_dir = Path(manual_dir)

    def run(self, intake: IntakeOutput) -> RetrievalOutput:
        query_terms = self.MANUAL_KEYWORDS.get(
            intake.detected_issue_type,
            intake.symptoms,
        )

        retrieved_documents = []

        for manual_path in self.manual_dir.glob("*.txt"):
            content = manual_path.read_text(encoding="utf-8")
            normalized_content = content.lower()

            matched_keywords = [
                keyword
                for keyword in query_terms
                if keyword.lower() in normalized_content
            ]

            if not matched_keywords:
                continue

            relevance_score = min(100, len(matched_keywords) * 15)

            retrieved_documents.append(
                RetrievedDocument(
                    document_name=manual_path.name,
                    matched_keywords=matched_keywords,
                    relevance_score=relevance_score,
                    content_preview=self._build_preview(content),
                )
            )

        retrieved_documents.sort(
            key=lambda document: document.relevance_score,
            reverse=True,
        )

        query = f"{intake.detected_issue_type}: {', '.join(intake.symptoms)}"

        return RetrievalOutput(
            query=query,
            retrieved_documents=retrieved_documents[:3],
        )

    def _build_preview(self, content: str, max_chars: int = 500) -> str:
        cleaned = " ".join(content.split())

        if len(cleaned) <= max_chars:
            return cleaned

        return cleaned[:max_chars].rstrip() + "..."