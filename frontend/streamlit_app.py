import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.core.orchestrator import DiagnosticOrchestrator
from app.core.report_writer import ReportWriter


st.set_page_config(
    page_title="AutoAI Vehicle Diagnostics",
    page_icon="🚗",
    layout="wide",
)


DEFAULT_CASE_TEXT = """Customer reports that the vehicle temperature gauge rises quickly after 10 minutes of driving.
The engine warning light appears on the dashboard.
OBD scan shows diagnostic trouble code P0217.
Customer noticed a burning smell and a small coolant leak under the front of the vehicle.
No major noise reported, but the driver says the car feels unsafe to continue driving.
"""


def run_diagnosis(case_text: str, source_file: str, sensor_file: str | None):
    orchestrator = DiagnosticOrchestrator()
    return orchestrator.run(
        case_text=case_text,
        source_file=source_file,
        sensor_file=sensor_file,
    )


def render_summary(result) -> None:
    st.subheader("Result Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Issue Type", result.intake.detected_issue_type)
    col2.metric("Severity", result.impact.severity)
    col3.metric("Risk Score", f"{result.impact.score}/100")
    col4.metric("OBD Codes", len(result.fault_codes.detected_codes))

    st.markdown("**Primary diagnosis**")
    st.write(result.diagnosis.primary_diagnosis)

    st.markdown("**Urgency**")
    st.write(result.impact.urgency)


def render_evidence(result) -> None:
    st.subheader("Evidence")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Symptoms",
            "OBD Codes",
            "Sensor Data",
            "Manual Evidence",
        ]
    )

    with tab1:
        if result.intake.symptoms:
            for symptom in result.intake.symptoms:
                st.write(f"- {symptom}")
        else:
            st.info("No symptoms detected.")

    with tab2:
        if result.fault_codes.detected_codes:
            for fault in result.fault_codes.detected_codes:
                st.write(f"**{fault.code}** — {fault.description}")
                st.caption(f"Severity hint: {fault.severity_hint}")
        else:
            st.info("No OBD trouble codes detected.")

    with tab3:
        st.write(result.sensor_analysis.summary)

        if result.sensor_analysis.findings:
            for finding in result.sensor_analysis.findings:
                st.write(
                    f"- **{finding.metric}**: {finding.finding} "
                    f"(value: {finding.value}, threshold: {finding.threshold}, severity: {finding.severity})"
                )

    with tab4:
        if result.retrieval.retrieved_documents:
            for document in result.retrieval.retrieved_documents:
                st.write(f"**{document.document_name}**")
                st.caption(
                    f"Score: {document.relevance_score}/100 | "
                    f"Matched: {', '.join(document.matched_keywords)}"
                )
        else:
            st.info("No matching manual evidence found.")


def render_actions(result) -> None:
    st.subheader("Recommended Actions")

    for index, action in enumerate(result.recommendations.recommended_actions, start=1):
        st.write(f"{index}. {action}")


def render_report(result) -> None:
    st.subheader("Diagnostic Report")

    st.text_area(
        "Generated report",
        value=result.final_report,
        height=360,
    )

    st.download_button(
        label="Download report as TXT",
        data=result.final_report,
        file_name="autoai_diagnostic_report.txt",
        mime="text/plain",
    )


st.title("AutoAI Vehicle Diagnostics")
st.caption(
    "A simple diagnostic interface for vehicle service cases, OBD codes, "
    "sensor logs, maintenance evidence, and risk scoring."
)

st.divider()

with st.sidebar:
    st.header("Settings")

    source_file = st.text_input(
        "Case reference",
        value="streamlit_case_001.txt",
    )

    use_sensor_log = st.checkbox("Use sensor log", value=True)

    sensor_file = st.text_input(
        "Sensor log path",
        value="datasets/sensor_logs/case_001_engine_overheating_sensors.csv",
        disabled=not use_sensor_log,
    )

    save_report = st.checkbox("Save JSON report", value=False)

case_text = st.text_area(
    "Vehicle service case",
    value=DEFAULT_CASE_TEXT,
    height=220,
)

run_button = st.button("Run Diagnosis", type="primary")

if run_button:
    if not case_text.strip():
        st.error("Please enter a vehicle service case.")
        st.stop()

    selected_sensor_file = sensor_file if use_sensor_log else None

    result = run_diagnosis(
        case_text=case_text,
        source_file=source_file,
        sensor_file=selected_sensor_file,
    )

    if save_report:
        report_path = ReportWriter().save_json_report(
            result=result,
            source_file=source_file,
        )
        st.success(f"Saved JSON report to: `{report_path}`")

    st.divider()

    render_summary(result)

    st.divider()

    render_evidence(result)

    st.divider()

    render_actions(result)

    st.divider()

    render_report(result)