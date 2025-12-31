from typing import Dict, Optional, List, Tuple
from models.pump import Pump
from models.tank import Tank

class PumpService:
    def __init__(self, pumps: Dict[int, Pump]):
        self.pumps = pumps
    
    def get_pump(self, number: int) -> Optional[Pump]:
        return self.pumps.get(number)
    
    def get_all_pumps(self) -> List[Pump]:
        return list(self.pumps.values())
    
    def get_available_fuels(self, pump_number: int, tanks: Dict[str, Tank]) -> List[Tuple[str, str]]:
        pump = self.get_pump(pump_number)
        
        if not pump:
            return []
        
        return pump.get_available_fuels(tanks)
    
    def can_dispense(self, pump_number: int, fuel_type_key: str, tanks: Dict[str, Tank]) -> tuple[bool, str]:
        pump = self.get_pump(pump_number)
        
        if not pump:
            return False, "Колонка не найдена"
        
        tank_id = pump.get_tank_for_fuel(fuel_type_key)
        
        if not tank_id:
            return False, f"На колонке {pump_number} нет пистолета для выбранного топлива"
        
        tank = tanks.get(tank_id)
        
        if not tank:
            return False, "Цистерна не найдена"
        
        if not tank.is_active:
            return False, f"Цистерна {tank_id} отключена"
        
        return True, ""
