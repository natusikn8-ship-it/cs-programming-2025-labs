from dataclasses import dataclass
from datetime import datetime
from models.fuel import FuelType

@dataclass
class Transaction:
    timestamp: datetime
    operation_type: str
    details: dict

    def info(self) -> dict:
        return {
            "time": self.timestamp.isoformat(),
            "type": self.operation_type,
            "details": self.details
        }

    @classmethod
    def get_info(cls, data: dict) -> "Transaction":
        return cls(
            timestamp=datetime.fromisoformat(data["time"]),
            operation_type=data["type"],
            details=data["details"]
        )
