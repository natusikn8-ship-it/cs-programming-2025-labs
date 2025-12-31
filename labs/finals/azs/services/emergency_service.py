from datetime import datetime
from models.transaction import Transaction
from services.tank_service import TankService

class EmergencyService:
    def __init__(self, tank_service: TankService):
        self.tank_service = tank_service
        self.emergency_active = False
        self.emergency_reason = ""
    
    def activate_emergency(self, reason: str = "Аварийная ситуация") -> tuple[bool, str, Transaction]:
        if self.emergency_active:
            return False, "Аварийный режим уже активирован", None
        
        self.tank_service.emergency_shutdown()
        
        self.emergency_active = True
        self.emergency_reason = reason
        
        transaction = Transaction(
            timestamp=datetime.now(),
            operation_type="emergency_start",
            details={
                "reason": reason,
                "tanks_disabled": len(self.tank_service.tanks)
            }
        )
        
        message = "АВАРИЙНЫЙ РЕЖИМ АКТИВИРОВАН\n"
        message += f"Причина: {reason}\n"
        message += f"Все цистерны ({len(self.tank_service.tanks)} шт.) заблокированы\n"
        
        return True, message, transaction
    
    def deactivate_emergency(self) -> tuple[bool, str, Transaction]:
        if not self.emergency_active:
            return False, "Аварийный режим не активирован", None
        
        self.emergency_active = False
        old_reason = self.emergency_reason
        self.emergency_reason = ""
        
        transaction = Transaction(
            timestamp=datetime.now(),
            operation_type="emergency_end",
            details={
                "previous_reason": old_reason
            }
        )
        
        message = "Аварийный режим деактивирован\n"
        message += "Внимание: Цистерны остаются заблокированными\n"
        message += "Включите необходимые цистерны вручную через меню"
        
        return True, message, transaction
    
    def is_active(self) -> bool:
        return self.emergency_active
    
    def get_status(self) -> dict:
        return {
            "active": self.emergency_active,
            "reason": self.emergency_reason if self.emergency_active else None
        }
