from pathlib import Path

import mlflow

from app.schemas.diagnostic_schema import PipelineResult


class MLflowTracker:
    """Tracks diagnostic pipeline runs with MLflow using a SQLite backend."""

    def __init__(
        self,
        experiment_name: str = "AutoAI Vehicle Diagnostics",
        tracking_db_path: str = "mlflow.db",
    ) -> None:
        tracking_db = Path(tracking_db_path)
        tracking_db.parent.mkdir(parents=True, exist_ok=True)

        mlflow.set_tracking_uri(f"sqlite:///{tracking_db.resolve()}")
        mlflow.set_experiment(experiment_name)

    def log_run(self, result: PipelineResult, source_file: str) -> str:
        with mlflow.start_run() as run:
            mlflow.log_param("source_file", source_file)
            mlflow.log_param("detected_issue_type", result.intake.detected_issue_type)
            mlflow.log_param("primary_diagnosis", result.diagnosis.primary_diagnosis)
            mlflow.log_param("severity", result.impact.severity)
            mlflow.log_param("safety_risk", result.impact.safety_risk)
            mlflow.log_param("urgency", result.impact.urgency)

            mlflow.log_metric("risk_score", result.impact.score)
            mlflow.log_metric(
                "fault_codes_count",
                len(result.fault_codes.detected_codes),
            )
            mlflow.log_metric(
                "sensor_findings_count",
                len(result.sensor_analysis.findings),
            )
            mlflow.log_metric(
                "retrieved_documents_count",
                len(result.retrieval.retrieved_documents),
            )
            mlflow.log_metric(
                "recommended_actions_count",
                len(result.recommendations.recommended_actions),
            )

            return run.info.run_id