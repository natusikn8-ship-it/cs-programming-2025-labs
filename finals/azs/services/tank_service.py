from typing import Dict, List, Optional
from models.tank import Tank

class TankService:
    def __init__(self, tanks: Dict[str, Tank]):
        self.tanks = tanks
    
    def get_tank(self, tank_id: str) -> Optional[Tank]:
        return self.tanks.get(tank_id)
    
    def get_tanks_by_fuel(self, fuel_type_key: str) -> List[Tank]:
        return [t for t in self.tanks.values() if t.fuel_type == fuel_type_key]
    
    def get_all_tanks(self) -> List[Tank]:
        return list(self.tanks.values())
    
    def get_disabled_tanks(self) -> List[Tank]:
        return [t for t in self.tanks.values() if not t.is_active]
    
    def enable_tank(self, tank_id: str) -> tuple[bool, str]:
        tank = self.get_tank(tank_id)
        
        if not tank:
            return False, "Цистерна не найдена"
        
        if tank.is_active:
            return False, "Цистерна уже включена"
        
        if not tank.can_enable():
            return False, f"Невозможно включить: уровень топлива ({tank.current_level} л) ниже минимума ({tank.min_level} л)"
        
        tank.is_active = True
        return True, f"Цистерна {tank_id} успешно включена"
    
    def disable_tank(self, tank_id: str) -> tuple[bool, str]:
        tank = self.get_tank(tank_id)
        
        if not tank:
            return False, "Цистерна не найдена"
        
        if not tank.is_active:
            return False, "Цистерна уже отключена"
        
        tank.is_active = False
        return True, f"Цистерна {tank_id} успешно отключена"
    
    # Аварийное отключение всех цистерн
    def emergency_shutdown(self):
        for tank in self.tanks.values():
            tank.is_active = False
    
    def transfer_fuel(self, source_id: str, target_id: str, amount: float) -> tuple[bool, str]:
        source = self.get_tank(source_id)
        target = self.get_tank(target_id)
        
        if not source or not target:
            return False, "Одна из цистерн не найдена"
        
        if source.fuel_type != target.fuel_type:
            return False, "Нельзя перекачивать топливо разных типов"
        
        if source.current_level < amount:
            return False, f"В цистерне {source_id} недостаточно топлива"
        
        if target.current_level + amount > target.max_level:
            return False, f"Цистерна {target_id} переполнится"
        
        source.current_level -= amount
        target.current_level += amount
        if source.current_level < source.min_level:
            source.is_active = False
        return True, f"Перекачано {amount} л из {source_id} в {target_id}"
