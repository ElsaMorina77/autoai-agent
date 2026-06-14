import json

from app.core.orchestrator import DiagnosticOrchestrator
from app.core.report_writer import ReportWriter


def test_report_writer_saves_json_report(tmp_path):
    text = "Vehicle overheating with coolant leak, engine warning light, and fault code P0217."
    result = DiagnosticOrchestrator().run(case_text=text, source_file="case_001.txt")

    writer = ReportWriter(output_dir=str(tmp_path))
    output_path = writer.save_json_report(
        result=result,
        source_file="case_001.txt",
    )

    assert output_path.exists()

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["source_file"] == "case_001.txt"
    assert payload["pipeline_result"]["intake"]["detected_issue_type"] == "engine_overheating"
    assert payload["pipeline_result"]["fault_codes"]["detected_codes"][0]["code"] == "P0217"