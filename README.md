# AutoAI Vehicle Diagnostics

AutoAI Vehicle Diagnostics is an automotive AI engineering project that analyzes vehicle service cases using a structured multi-agent pipeline.

The system combines customer complaint text, OBD diagnostic trouble codes, maintenance-manual evidence, sensor-log analysis, severity scoring, technician recommendations, JSON report generation, FastAPI endpoints, MLflow tracking, and a simple Streamlit interface.

## Live Demo

The deployed Streamlit app can be found here:

```text
https://autoai-agent.streamlit.app
```

## Core Features

- Multi-agent vehicle diagnostic workflow
- Automotive issue classification
- OBD diagnostic trouble-code extraction, such as P0217 and P0562
- Maintenance-manual retrieval
- Sensor-log threshold analysis
- Severity, safety-risk, urgency, and cost-risk scoring
- Technician-style recommended actions
- Structured JSON report generation
- FastAPI backend with Swagger documentation
- Streamlit frontend for simple diagnosis demos
- MLflow tracking with SQLite backend
- Automated tests with Pytest
- GitHub Actions CI pipeline

## Architecture

```text
Vehicle Service Case
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
- Streamlit
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
├── frontend/
│   └── streamlit_app.py
│
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

## CLI Usage

Run a diagnostic case without sensor data:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --save-report
```

Run a diagnostic case with sensor data:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --sensor-log datasets/sensor_logs/case_001_engine_overheating_sensors.csv --save-report
```

Run with MLflow tracking:

```bash
python main.py --case datasets/service_cases/case_001_engine_overheating.txt --sensor-log datasets/sensor_logs/case_001_engine_overheating_sensors.csv --save-report --track-mlflow
```

## Streamlit Frontend

Run the Streamlit app locally:

```bash
streamlit run frontend/streamlit_app.py
```

The frontend provides a simple interface for:

- entering a vehicle service case
- optionally using a sensor-log CSV
- viewing issue type, severity, risk score, and OBD code count
- reviewing symptoms, OBD codes, sensor findings, and manual evidence
- viewing recommended technician actions
- downloading the generated diagnostic report

## FastAPI Backend

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
  "fault_codes": ["P0217"],
  "sensor_summary": "Sensor log shows 2 high-severity and 0 medium-severity threshold violations.",
  "retrieved_documents": ["cooling_system_manual.txt"],
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

## Deploying to Streamlit Community Cloud

This project can be deployed as a Streamlit app after it is pushed to GitHub.

Use this entrypoint:

```text
frontend/streamlit_app.py
```

Before deploying, make sure the repository includes:

- `frontend/streamlit_app.py`
- `app/`
- `datasets/`
- `requirements.txt`
- `README.md`

The Streamlit app imports the local backend code from the `app/` folder and uses the sample files in `datasets/`, so it can run as a self-contained demo without requiring a separate FastAPI server.

Recommended deployment steps:

1. Push the project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
frontend/streamlit_app.py
```

5. Deploy the app.
6. Add the deployed link to the `Live Demo` section of this README.

## Notes on Generated Files

The project can generate local reports and MLflow tracking files. These should not be committed to GitHub.

Recommended `.gitignore` entries:

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.pyc

reports/
mlflow.db
mlruns/

.env
.DS_Store
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


