STATION_NAME = "СеверНефть"
MIN_FUEL_WARNING = 3000
"""
Эти две переменные по хорошему надо бы в .env файл записать, 
но .env по умолчанию в .gitignore, а тебе в гитхаб заливать.
Так что чисто на будущее: названия, всякую локальную информацию,
а главное токены, ключи доступа и тому подобное зписываем только
в .env и достаём оттуда через os.getenv("NAME")
"""
# Колонки
# Формат: номер_колонки -> {fuel_type_key: tank_id}
PUMP_CONFIG = {
    1: {"AI92": "AI92_1", "AI95": "AI95_1"},
    2: {"AI92": "AI92_1", "AI95": "AI95_1"},
    3: {"AI92": "AI92_1", "AI95": "AI95_1", "AI98": "AI98_1", "DT": "DT_1"},
    4: {"AI92": "AI92_1", "AI95": "AI95_1"},
    5: {"AI92": "AI92_1", "AI95": "AI95_2", "AI98": "AI98_1", "DT": "DT_1"},
    6: {"AI92": "AI92_1", "AI95": "AI95_2", "AI98": "AI98_1", "DT": "DT_1"},
    7: {"AI95": "AI95_2", "DT": "DT_1"},
    8: {"AI95": "AI95_2", "DT": "DT_1"},
}

# Цистерны
INITIAL_TANKS = [
    {"id": "AI92_1", "fuel_type": "AI92", "max_level": 20000, "current_level": 12400, "min_level": 2000, "is_active": True},
    {"id": "AI95_1", "fuel_type": "AI95", "max_level": 20000, "current_level": 15000, "min_level": 2000, "is_active": True},
    {"id": "AI95_2", "fuel_type": "AI95", "max_level": 20000, "current_level": 18000, "min_level": 2000, "is_active": True},
    {"id": "AI98_1", "fuel_type": "AI98", "max_level": 15000, "current_level": 10000, "min_level": 1500, "is_active": True},
    {"id": "DT_1", "fuel_type": "DT", "max_level": 25000, "current_level": 15600, "min_level": 2500, "is_active": True},
]
