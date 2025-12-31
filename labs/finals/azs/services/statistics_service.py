from models.transaction import Transaction
from models.fuel import fuel_types

class StatisticsService:
    def __init__(self, stats: dict):
        self.stats = stats
    
    def update_from_sale(self, transaction: Transaction):
        if transaction.operation_type != "sale":
            return
        
        details = transaction.details
        fuel_key = details["fuel"]
        amount = details["amount"]
        cost = details["cost"]
        
        # Общая статистика
        self.stats["total_revenue"] += cost
        self.stats["total_cars"] += 1
        
        # Статистика по топливу
        self.stats["fuel_sales"][fuel_key]["liters"] += amount
        self.stats["fuel_sales"][fuel_key]["revenue"] += cost
    
    def get_summary(self) -> dict:
        return {
            "total_revenue": self.stats["total_revenue"],
            "total_cars": self.stats["total_cars"],
            "fuel_breakdown": self._get_fuel_breakdown()
        }
    
    def _get_fuel_breakdown(self) -> list:
        breakdown = []
        
        for fuel_key, data in self.stats["fuel_sales"].items():
            fuel = fuel_types[fuel_key]
            breakdown.append({
                "name": fuel.name,
                "liters": data["liters"],
                "revenue": data["revenue"]
            })
        
        return breakdown
    
    def get_best_selling_fuel(self) -> str:
        max_liters = 0
        best_fuel = None
        
        for fuel_key, data in self.stats["fuel_sales"].items():
            if data["liters"] > max_liters:
                max_liters = data["liters"]
                best_fuel = fuel_key
        
        return best_fuel if best_fuel else "N/A"
    
    def reset_statistics(self):
        self.stats["total_revenue"] = 0.0
        self.stats["total_cars"] = 0
        
        for fuel_key in self.stats["fuel_sales"]:
            self.stats["fuel_sales"][fuel_key]["liters"] = 0
            self.stats["fuel_sales"][fuel_key]["revenue"] = 0
