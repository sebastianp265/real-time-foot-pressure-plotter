from dataclasses import dataclass


@dataclass
class Sensor:
    value: str
    anomaly: str
    name: str

    def __init__(self, data: dict) -> None:
        self.value = data["value"]
        self.anomaly = "True" if data["anomaly"] else "False"
        self.name = data["name"]


@dataclass
class PatientData:
    sensors: list[Sensor]

    def __init__(self, sensors_raw: list[dict]) -> None:
        self.sensors = []
        for sensor in sensors_raw:
            self.sensors.append(Sensor(sensor))
