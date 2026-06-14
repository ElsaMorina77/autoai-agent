import argparse
from pathlib import Path

from app.core.mlflow_tracker import MLflowTracker
from app.core.orchestrator import DiagnosticOrchestrator
from app.core.report_writer import ReportWriter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run AutoAI Agent on a vehicle service case."
    )
    parser.add_argument(
        "--case",
        required=True,
        help="Path to a vehicle service case text file.",
    )
    parser.add_argument(
        "--sensor-log",
        required=False,
        default=None,
        help="Optional path to a vehicle sensor log CSV file.",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save the diagnostic result as a JSON report.",
    )
    parser.add_argument(
        "--track-mlflow",
        action="store_true",
        help="Track the diagnostic run with MLflow.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    case_path = Path(args.case)

    if not case_path.exists():
        raise FileNotFoundError(f"Case file not found: {case_path}")

    case_text = case_path.read_text(encoding="utf-8")

    orchestrator = DiagnosticOrchestrator()
    result = orchestrator.run(
        case_text=case_text,
        source_file=str(case_path),
        sensor_file=args.sensor_log,
    )

    print("\n" + "=" * 80)
    print("AUTOAI AGENT — VEHICLE DIAGNOSTIC REPORT")
    print("=" * 80)
    print(result.final_report)
    print("=" * 80)

    if args.save_report:
        report_path = ReportWriter().save_json_report(
            result=result,
            source_file=str(case_path),
        )
        print(f"\nSaved JSON report to: {report_path}")

    if args.track_mlflow:
        run_id = MLflowTracker().log_run(
            result=result,
            source_file=str(case_path),
        )
        print(f"Logged MLflow run: {run_id}")


if __name__ == "__main__":
    main()