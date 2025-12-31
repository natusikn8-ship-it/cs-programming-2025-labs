from typing import Dict, Optional
from datetime import datetime
from models.tank import Tank
from models.fuel import fuel_types
from models.transaction import Transaction
from services.tank_service import TankService
from services.pump_service import PumpService

class SalesService:
    def __init__(self, tank_service: TankService, pump_service: PumpService):
        self.tank_service = tank_service
        self.pump_service = pump_service
    
    def calculate_cost(self, fuel_type: str, amount: float) -> float:
        fuel = fuel_types[fuel_type]
        return fuel.price * amount
    
    def process_sale(self, pump_number: int, fuel_type: str, amount: float) -> tuple[bool, str, Optional[Transaction]]:
        can_dispense, reason = self.pump_service.can_dispense(
            pump_number, fuel_type, self.tank_service.tanks
        )
        
        if not can_dispense:
            return False, f"Ошибка: {reason}", None
        
        pump = self.pump_service.get_pump(pump_number)
        tank_id = pump.get_tank_for_fuel(fuel_type)
        tank = self.tank_service.get_tank(tank_id)
        
        if not tank.can_dispense(amount):
            return False, f"Ошибка: В цистерне {tank_id} недостаточно топлива", None
        
        cost = self.calculate_cost(fuel_type, amount)
        
        success = tank.dispense(amount)
        
        if not success:
            return False, "Ошибка: Не удалось списать топливо", None
        
        transaction = Transaction(
            timestamp=datetime.now(),
            operation_type="sale",
            details={
                "pump": pump_number,
                "fuel": fuel_type,
                "tank": tank_id,
                "amount": amount,
                "cost": cost
            }
        )
        
        return True, f"Операция выполнена успешно. Списано {amount} л, стоимость {cost}", transaction
    
    def update_statistics(self, stats: dict, transaction: Transaction):
        details = transaction.details
        fuel_key = details["fuel"]
        amount = details["amount"]
        cost = details["cost"]
        
        stats["total_revenue"] += cost
        stats["total_cars"] += 1
        
        stats["fuel_sales"][fuel_key]["liters"] += amount
        stats["fuel_sales"][fuel_key]["revenue"] += cost
