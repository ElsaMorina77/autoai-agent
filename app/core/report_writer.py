import json
from datetime import datetime
from pathlib import Path

from app.schemas.diagnostic_schema import PipelineResult


class ReportWriter:
    """Persists diagnostic pipeline outputs to disk."""

    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_json_report(self, result: PipelineResult, source_file: str) -> Path:
        source_path = Path(source_file)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_name = f"{source_path.stem}_{timestamp}_diagnostic_report.json"
        output_path = self.output_dir / report_name

        payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "source_file": source_file,
            "pipeline_result": result.model_dump(),
        }

        output_path.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

        return output_path