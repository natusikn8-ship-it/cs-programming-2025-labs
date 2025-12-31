from dataclasses import dataclass
from models.fuel import FuelType

@dataclass
class Tank:
    id: str
    fuel_type: FuelType
    max_level: float
    current_level: float
    min_level: float
    is_active: bool

    # Проверка может ли цистерна работать
    def can_dispense(self, amount: float) -> bool:
        if not self.is_active:
            return False
        return self.current_level >= amount

    # Откачка топлива из цистерны
    def dispense(self, amount: float) -> bool:
        if not self.can_dispense(amount):
            return False
        self.current_level -= amount
        if self.current_level <= self.min_level:
            self.if_active = False
        return True

    # Пополнение топлива
    def refill(self, amount: float) -> bool:
        if self.current_level + amount > self.max_level:
            return False
        self.current_level += amount
        return True

    def can_enable(self) -> bool:
        return self.current_level >= self.min_level

    def info(self):
        return {
            "id": self.id,
            "fuel_type": str(self.fuel_type),
            "max_level": self.max_level,
            "current_level": self.current_level,
            "min_level": self.min_level,
            "is_active": self.is_active
        }

    # Хз как работает, спизжено у нейронки, не трогать
    @classmethod
    def get_info(cls, data: dict) -> "Tank":
        return cls(
            id=data["id"],
            fuel_type=data["fuel_type"],
            max_level=data["max_level"],
            current_level=data["current_level"],
            min_level=data["min_level"],
            is_active=data["is_active"]
        )

if __name__ == "__main__":
    fuel = FuelType("Rocket", 113.5)
    tank = Tank("R1", fuel, 10000, 15000, 17000, True)
    print(tank.info())
