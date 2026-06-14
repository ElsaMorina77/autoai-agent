from pathlib import Path

from app.agents.sensor_analysis_agent import SensorAnalysisAgent


def test_sensor_analysis_detects_overheating_and_low_coolant(tmp_path):
    sensor_file = tmp_path / "sensors.csv"
    sensor_file.write_text(
        "timestamp,engine_temp_c,coolant_level_pct,battery_voltage\n"
        "2026-06-01T10:00:00,95,75,12.5\n"
        "2026-06-01T10:05:00,124,39,12.2\n",
        encoding="utf-8",
    )

    result = SensorAnalysisAgent().run(sensor_file=str(sensor_file))

    metrics = [finding.metric for finding in result.findings]

    assert "engine_temp_c" in metrics
    assert "coolant_level_pct" in metrics
    assert result.summary.startswith("Sensor log shows")