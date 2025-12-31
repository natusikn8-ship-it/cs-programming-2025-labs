class FuelType:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self): # Что будет выводиться при переводе в тип str
        return self.name

AI92 = FuelType("АИ-92", 46.50)
AI95 = FuelType("АИ-95", 58.30)
AI98 = FuelType("АИ-98", 64.80)
DT = FuelType("ДТ", 52.10)

fuel_types = {
    "AI92": AI92,
    "AI95": AI95,
    "AI98": AI98,
    "DT": DT
}
