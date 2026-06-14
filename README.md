# AutoAI Agent — Agentic AI Vehicle Diagnostics System

AutoAI Agent is an end-to-end automotive AI engineering project that uses a multi-agent pipeline to analyze vehicle service cases, diagnostic trouble codes, maintenance manuals, and sensor logs.

The project is designed to demonstrate production-oriented AI engineering skills for industrial and mobility-focused AI roles.

## Core Features

- Multi-agent diagnostic workflow
- Automotive issue classification
- Diagnostic trouble code extraction, such as P0217 and P0562
- Maintenance-manual retrieval
- Sensor-log threshold analysis
- Severity and safety-risk scoring
- Technician-style repair recommendations
- Structured JSON report generation
- FastAPI backend with Swagger documentation
- MLflow tracking with SQLite backend
- Automated tests with Pytest
- GitHub Actions CI pipeline

## Architecture

```text
Vehicle Case Input
      |
      v
Intake Agent
      |
      v
Fault Code Agent
      |
      v
Sensor Analysis Agent
      |
      v
Retrieval Agent
      |
      v
Diagnostic Agent
      |
      v
Impact Agent
      |
      v
Recommendation Agent
      |
      v
Report Agent
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pandas
- Pytest
- MLflow
- SQLite
- GitHub Actions
- Uvicorn

## Project Structure

```text
autoai-agent/
│
├── app/
│   ├── agents/
│   │   ├── intake_agent.py
│   │   ├── fault_code_agent.py
│   │   ├── sensor_analysis_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── diagnostic_agent.py
│   │   ├── impact_agent.py
│   │   ├── recommendation_agent.py
│   │   └── report_agent.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── core/
│   │   ├── orchestrator.py
│   │   ├── report_writer.py
│   │   └── mlflow_tracker.py
│   │
│   ├── schemas/
│   │   └── diagnostic_schema.py
│   │
│   └── main_api.py
│
├── datasets/
│   ├── service_cases/
│   ├── maintenance_manuals/
│   └── sensor_logs/
│
├── reports/
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── main.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Example CLI Usage

Run without a sensor log:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --save-report
```

Run with a sensor log:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --sensor-log datasets/sensor_logs/case_001_engine_overheating_sensors.csv --save-report
```

Run with MLflow tracking:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --sensor-log datasets/sensor_logs/case_001_engine_overheating_sensors.csv --save-report --track-mlflow
```

## Example API Usage

Start the API:

```bash
uvicorn app.main_api:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET /health
```

Diagnostic endpoint:

```text
POST /diagnose
```

Example request:

```json
{
  "case_text": "Customer reports overheating, coolant leak, warning light, burning smell, and OBD code P0217.",
  "source_file": "api_case_001.txt",
  "sensor_file": "datasets/sensor_logs/case_001_engine_overheating_sensors.csv"
}
```

Example response fields:

```json
{
  "detected_issue_type": "engine_overheating",
  "symptoms": [
    "burning smell",
    "coolant leak",
    "warning light"
  ],
  "fault_codes": [
    "P0217"
  ],
  "sensor_summary": "Sensor log shows 2 high-severity and 0 medium-severity threshold violations.",
  "retrieved_documents": [
    "cooling_system_manual.txt"
  ],
  "primary_diagnosis": "Coolant leak or low coolant level",
  "severity": "Critical",
  "safety_risk": "High",
  "urgency": "Immediate inspection required",
  "risk_score": 100
}
```

## Example Output

```text
Detected issue type:
engine_overheating

Detected symptoms:
- burning smell
- coolant leak
- temperature gauge abnormal
- warning light

Detected diagnostic trouble codes:
- P0217: Engine coolant over-temperature condition

Sensor analysis:
- Sensor log shows 2 high-severity and 0 medium-severity threshold violations.
- engine_temp_c: Engine temperature exceeded safe operating threshold.
- coolant_level_pct: Coolant level dropped below expected threshold.

Retrieved maintenance knowledge:
- cooling_system_manual.txt

Primary diagnosis:
Coolant leak or low coolant level

Impact assessment:
- Severity: Critical
- Safety risk: High
- Urgency: Immediate inspection required
- Risk score: 100/100
```

## MLflow Tracking

This project supports MLflow tracking for diagnostic pipeline runs using a SQLite backend.

Run a diagnostic case with MLflow tracking enabled:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --sensor-log datasets/sensor_logs/case_001_engine_overheating_sensors.csv --save-report --track-mlflow
```

Open the MLflow UI:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Then open:

```text
http://127.0.0.1:5000
```

The tracker logs:

- detected issue type
- primary diagnosis
- severity
- safety risk
- urgency
- risk score
- fault-code count
- sensor findings count
- retrieved documents count
- recommended actions count

## Testing

Run all tests:

```bash
pytest
```

The test suite covers:

- intake classification
- negated symptom handling
- fault-code extraction
- maintenance-manual retrieval
- sensor-log analysis
- impact scoring
- full orchestrator pipeline
- JSON report writing
- FastAPI endpoints
- MLflow tracking

## Continuous Integration

This project includes a GitHub Actions CI workflow that runs the test suite automatically on pushes and pull requests.

```text
.github/workflows/ci.yml
```

The CI pipeline installs dependencies and runs:

```bash
pytest
```

## Project Goal

The goal of this project is to demonstrate how agentic AI systems can support automotive diagnostics by combining:

- unstructured vehicle service descriptions
- structured diagnostic trouble codes
- maintenance knowledge retrieval
- sensor-log analysis
- risk scoring
- technician-ready reporting
- experiment tracking
- API-based deployment structure

## Why This Project Matters

AutoAI Agent demonstrates skills relevant to production AI engineering and automotive AI roles:

- Agentic workflow design
- Structured AI system architecture
- Retrieval-augmented diagnostic reasoning
- Automotive telemetry analysis
- Diagnostic trouble-code understanding
- API development with FastAPI
- Automated testing and CI
- MLflow-based experiment tracking
- Clean, modular Python engineering

## Future Improvements

- Add vector search for semantic maintenance-manual retrieval
- Add PostgreSQL for persistent case storage
- Add Streamlit dashboard
- Add Docker support
- Add cloud deployment
- Add authentication for API usage
- Add richer automotive datasets and benchmark cases
