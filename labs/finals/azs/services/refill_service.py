from typing import Optional
from datetime import datetime
from models.transaction import Transaction
from services.tank_service import TankService

class RefillService:
    def __init__(self, tank_service: TankService):
        self.tank_service = tank_service
    
    def process_refill(self, tank_id: str, amount: float) -> tuple[bool, str, Optional[Transaction]]:
        tank = self.tank_service.get_tank(tank_id)
        
        if not tank:
            return False, "Ошибка: Цистерна не найдена", None
        
        # Проверка превышения вместимости
        if tank.current_level + amount > tank.max_level:
            overflow = tank.current_level + amount - tank.max_level
            return False, f"Ошибка: Превышение вместимости на {overflow:.0f} л", None
        
        # Запоминаем уровень до пополнения
        old_level = tank.current_level
        
        # Пополнение
        success = tank.refill(amount)
        
        if not success:
            return False, "Ошибка: Не удалось пополнить цистерну", None
        
        # Создание транзакции
        transaction = Transaction(
            timestamp=datetime.now(),
            operation_type="refill",
            details={
                "tank_id": tank_id,
                "fuel_type": tank.fuel_type,
                "amount": amount,
                "level_before": old_level,
                "level_after": tank.current_level
            }
        )
        
        message = f"Пополнено {amount} л в цистерну {tank_id}. "
        message += f"Уровень: {old_level} -> {tank.current_level} л"
        
        # Цистерна НЕ включается автоматически
        if not tank.is_active and tank.can_enable():
            message += "\nЦистерна отключена. Включите вручную через меню."
        
        return True, message, transaction
    
    def get_available_space(self, tank_id: str) -> Optional[float]:
        tank = self.tank_service.get_tank(tank_id)
        
        if not tank:
            return None
        
        return tank.max_level - tank.current_level
