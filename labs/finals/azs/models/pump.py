from dataclasses import dataclass
from typing import Dict
from models.fuel import FuelType

@dataclass
class PumpNozzle:
    fuel_type: str
    tank_id: str

@dataclass
class Pump:
    number: int
    nozzles: Dict[str, str]  # FuelType -> tank_id
    
    def get_available_fuels(self, tanks: dict) -> list:
        available = []
        for fuel_type, tank_id in self.nozzles.items():
            tank = tanks.get(tank_id)
            if tank and tank.is_active:
                available.append((fuel_type, tank_id))
        return available

    def get_tank_for_fuel(self, fuel_type_key: str) -> str:
        return self.nozzles.get(fuel_type_key)

    def info(self):
        return {
            "number": self.number,
            "nozzles": self.nozzles
        }
    # Аналогично с tank.py, не трогать
    @classmethod
    def get_info(cls, data: dict) -> "Tank":
        return cls(
            number=data["number"],
            nozzles=data["nozzles"]
        )
