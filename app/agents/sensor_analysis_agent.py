from pathlib import Path

import pandas as pd

from app.schemas.diagnostic_schema import SensorAnalysisOutput, SensorFinding


class SensorAnalysisAgent:
    """Analyzes vehicle sensor logs for diagnostic risk indicators."""

    ENGINE_TEMP_THRESHOLD = 110.0
    COOLANT_LEVEL_THRESHOLD = 50.0
    BATTERY_VOLTAGE_THRESHOLD = 12.0

    def run(self, sensor_file: str | None) -> SensorAnalysisOutput:
        if sensor_file is None:
            return SensorAnalysisOutput(
                sensor_file=None,
                findings=[],
                summary="No sensor log provided.",
            )

        sensor_path = Path(sensor_file)

        if not sensor_path.exists():
            return SensorAnalysisOutput(
                sensor_file=sensor_file,
                findings=[],
                summary="Sensor log file was provided but could not be found.",
            )

        df = pd.read_csv(sensor_path)

        findings = []

        if "engine_temp_c" in df.columns:
            max_engine_temp = float(df["engine_temp_c"].max())

            if max_engine_temp > self.ENGINE_TEMP_THRESHOLD:
                findings.append(
                    SensorFinding(
                        metric="engine_temp_c",
                        finding="Engine temperature exceeded safe operating threshold.",
                        value=max_engine_temp,
                        threshold=self.ENGINE_TEMP_THRESHOLD,
                        severity="High",
                    )
                )

        if "coolant_level_pct" in df.columns:
            min_coolant_level = float(df["coolant_level_pct"].min())

            if min_coolant_level < self.COOLANT_LEVEL_THRESHOLD:
                findings.append(
                    SensorFinding(
                        metric="coolant_level_pct",
                        finding="Coolant level dropped below expected threshold.",
                        value=min_coolant_level,
                        threshold=self.COOLANT_LEVEL_THRESHOLD,
                        severity="High",
                    )
                )

        if "battery_voltage" in df.columns:
            min_battery_voltage = float(df["battery_voltage"].min())

            if min_battery_voltage < self.BATTERY_VOLTAGE_THRESHOLD:
                findings.append(
                    SensorFinding(
                        metric="battery_voltage",
                        finding="Battery voltage dropped below minimum threshold.",
                        value=min_battery_voltage,
                        threshold=self.BATTERY_VOLTAGE_THRESHOLD,
                        severity="Medium",
                    )
                )

        summary = self._build_summary(findings)

        return SensorAnalysisOutput(
            sensor_file=sensor_file,
            findings=findings,
            summary=summary,
        )

    def _build_summary(self, findings: list[SensorFinding]) -> str:
        if not findings:
            return "Sensor log does not show threshold violations."

        high_count = sum(1 for finding in findings if finding.severity == "High")
        medium_count = sum(1 for finding in findings if finding.severity == "Medium")

        return (
            f"Sensor log shows {high_count} high-severity and "
            f"{medium_count} medium-severity threshold violations."
        )