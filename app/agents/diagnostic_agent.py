from app.schemas.diagnostic_schema import (
    DiagnosticFinding,
    DiagnosticOutput,
    FaultCodeOutput,
    IntakeOutput,
    RetrievalOutput,
)


class DiagnosticAgent:
    """Produces likely diagnostic causes based on issue type, fault codes, symptoms, and manuals."""

    def run(
        self,
        intake: IntakeOutput,
        retrieval: RetrievalOutput,
        fault_codes: FaultCodeOutput,
    ) -> DiagnosticOutput:
        issue_type = intake.detected_issue_type
        text = intake.raw_case_text.lower()
        retrieved_context = self._build_retrieved_context(retrieval)
        fault_code_values = {fault.code for fault in fault_codes.detected_codes}

        findings = []

        if issue_type == "engine_overheating":
            if "coolant" in text or "leak" in text or "P0217" in fault_code_values:
                findings.append(
                    DiagnosticFinding(
                        cause="Coolant leak or low coolant level",
                        confidence=0.90,
                        evidence=[
                            "Case mentions coolant/leak symptoms.",
                            "Fault code P0217 indicates coolant over-temperature condition.",
                            "Retrieved cooling-system manual recommends leak and coolant-level inspection.",
                        ],
                    )
                )

            if "radiator" in retrieved_context or "cooling fan" in retrieved_context:
                findings.append(
                    DiagnosticFinding(
                        cause="Radiator blockage or cooling fan malfunction",
                        confidence=0.78,
                        evidence=[
                            "Retrieved manual references radiator airflow and cooling fan operation.",
                        ],
                    )
                )

            if "thermostat" in retrieved_context:
                findings.append(
                    DiagnosticFinding(
                        cause="Faulty thermostat",
                        confidence=0.72,
                        evidence=[
                            "Retrieved manual recommends verifying thermostat opening behavior.",
                        ],
                    )
                )

        elif issue_type == "brake_issue":
            findings.append(
                DiagnosticFinding(
                    cause="Worn brake pads or rotor issue",
                    confidence=0.80,
                    evidence=[
                        "Brake-related symptoms detected.",
                        "Retrieved brake manual recommends pad and rotor inspection.",
                    ],
                )
            )

            if "C0035" in fault_code_values:
                findings.append(
                    DiagnosticFinding(
                        cause="Wheel speed sensor or ABS circuit issue",
                        confidence=0.82,
                        evidence=[
                            "Fault code C0035 indicates left front wheel speed sensor circuit issue.",
                        ],
                    )
                )

        elif issue_type == "battery_issue":
            findings.append(
                DiagnosticFinding(
                    cause="Weak battery or charging system fault",
                    confidence=0.84,
                    evidence=[
                        "Battery/starting/voltage keywords detected.",
                        "Retrieved manual recommends battery load test and voltage measurement.",
                    ],
                )
            )

            if "P0562" in fault_code_values:
                findings.append(
                    DiagnosticFinding(
                        cause="Low system voltage or alternator output problem",
                        confidence=0.86,
                        evidence=[
                            "Fault code P0562 indicates system voltage low.",
                            "Retrieved manual recommends alternator charging voltage test.",
                        ],
                    )
                )

        else:
            findings.append(
                DiagnosticFinding(
                    cause="Unknown fault category",
                    confidence=0.40,
                    evidence=[
                        "Input does not contain enough known diagnostic indicators.",
                    ],
                )
            )

        primary_diagnosis = max(findings, key=lambda item: item.confidence).cause

        return DiagnosticOutput(
            findings=findings,
            primary_diagnosis=primary_diagnosis,
        )

    def _build_retrieved_context(self, retrieval: RetrievalOutput) -> str:
        return " ".join(
            document.content_preview.lower()
            for document in retrieval.retrieved_documents
        )