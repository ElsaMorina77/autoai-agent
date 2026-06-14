from app.schemas.diagnostic_schema import IntakeOutput


class IntakeAgent:
    """Extracts the basic issue type and symptoms from a vehicle service case."""

    ISSUE_KEYWORDS = {
        "engine_overheating": ["overheat", "overheating", "temperature", "coolant", "radiator"],
        "brake_issue": ["brake", "braking", "abs", "pedal"],
        "battery_issue": ["battery", "alternator", "start", "starting", "voltage"],
        "transmission_issue": ["transmission", "gear", "shifting", "clutch"],
        "unknown": [],
    }

    SYMPTOM_KEYWORDS = [
        "warning light",
        "high temperature",
        "coolant leak",
        "smoke",
        "noise",
        "vibration",
        "loss of power",
        "hard start",
        "burning smell",
        "brake noise",
    ]

    NEGATION_PATTERNS = {
        "noise": [
            "no noise",
            "no major noise",
            "without noise",
            "noise not reported",
            "no unusual noise",
        ],
        "smoke": [
            "no smoke",
            "without smoke",
            "smoke not reported",
        ],
        "vibration": [
            "no vibration",
            "without vibration",
            "vibration not reported",
        ],
        "loss of power": [
            "no loss of power",
            "without loss of power",
            "loss of power not reported",
        ],
        "brake noise": [
            "no brake noise",
            "without brake noise",
            "brake noise not reported",
        ],
    }

    def run(self, case_text: str, source_file: str) -> IntakeOutput:
        normalized = case_text.lower()

        detected_issue_type = self._detect_issue_type(normalized)
        symptoms = self._extract_symptoms(normalized)

        if "temperature gauge" in normalized:
            symptoms.append("temperature gauge abnormal")

        symptoms = sorted(set(symptoms))

        if not symptoms:
            symptoms.append("symptoms require further inspection")

        return IntakeOutput(
            source_file=source_file,
            raw_case_text=case_text,
            detected_issue_type=detected_issue_type,
            symptoms=symptoms,
        )

    def _detect_issue_type(self, normalized_text: str) -> str:
        detected_issue_type = "unknown"
        best_match_count = 0

        for issue_type, keywords in self.ISSUE_KEYWORDS.items():
            match_count = sum(1 for keyword in keywords if keyword in normalized_text)

            if match_count > best_match_count:
                best_match_count = match_count
                detected_issue_type = issue_type

        return detected_issue_type

    def _extract_symptoms(self, normalized_text: str) -> list[str]:
        symptoms = []

        for symptom in self.SYMPTOM_KEYWORDS:
            if symptom not in normalized_text:
                continue

            if self._is_negated(symptom, normalized_text):
                continue

            symptoms.append(symptom)

        return symptoms

    def _is_negated(self, symptom: str, normalized_text: str) -> bool:
        negation_patterns = self.NEGATION_PATTERNS.get(symptom, [])

        return any(pattern in normalized_text for pattern in negation_patterns)