from app.core.mlflow_tracker import MLflowTracker
from app.core.orchestrator import DiagnosticOrchestrator


def test_mlflow_tracker_logs_run(tmp_path):
    text = "Vehicle overheating with coolant leak, engine warning light, and fault code P0217."

    result = DiagnosticOrchestrator().run(
        case_text=text,
        source_file="test_case.txt",
    )

    tracker = MLflowTracker(
        experiment_name="AutoAI Test Experiment",
        tracking_db_path=str(tmp_path / "mlflow_test.db"),
    )

    run_id = tracker.log_run(
        result=result,
        source_file="test_case.txt",
    )

    assert isinstance(run_id, str)
    assert len(run_id) > 0