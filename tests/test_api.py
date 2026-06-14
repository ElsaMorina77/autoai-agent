from fastapi.testclient import TestClient

from app.main_api import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_diagnose_endpoint():
    payload = {
        "case_text": "Customer reports overheating, coolant leak, warning light, burning smell, and OBD code P0217.",
        "source_file": "api_case_001.txt",
        "sensor_file": None,
    }

    response = client.post("/diagnose", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["detected_issue_type"] == "engine_overheating"
    assert "P0217" in data["fault_codes"]
    assert data["primary_diagnosis"] == "Coolant leak or low coolant level"
    assert data["severity"] == "Critical"


def test_diagnose_endpoint_with_sensor_log():
    payload = {
        "case_text": "Customer reports overheating, coolant leak, warning light, burning smell, and OBD code P0217.",
        "source_file": "api_case_001.txt",
        "sensor_file": "datasets/sensor_logs/case_001_engine_overheating_sensors.csv",
    }

    response = client.post("/diagnose", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["detected_issue_type"] == "engine_overheating"
    assert "P0217" in data["fault_codes"]
    assert data["sensor_summary"].startswith("Sensor log shows")
    assert data["severity"] == "Critical"