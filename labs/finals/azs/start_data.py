# Скрипт для создания начальных данных системы АЗС. Запускать перед первым запуском main.py

import json
import os
from config import PUMP_CONFIG, INITIAL_TANKS

def create_data_directory():
    """Создание директории data если её нет"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Создана директория data/")
    else:
        print("Директория data/ уже существует")

def create_tanks_file():
    filepath = "data/tanks.json"
    
    # Проверка существования файла
    if os.path.exists(filepath):
        response = input(f"⚠ Файл {filepath} уже существует. Перезаписать? (y/n): ").lower()
        if response not in ['y', 'yes', 'д', 'да']:
            print("  Пропущено")
            return
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(INITIAL_TANKS, f, ensure_ascii=False, indent=2)
    
    print(f"Создан файл {filepath} ({len(INITIAL_TANKS)} цистерн)")

def create_pumps_file():
    filepath = "data/pumps.json"
    
    # Проверка существования файла
    if os.path.exists(filepath):
        response = input(f"⚠ Файл {filepath} уже существует. Перезаписать? (y/n): ").lower()
        if response not in ['y', 'yes', 'д', 'да']:
            print("  Пропущено")
            return
    
    pumps_data = []
    for number, nozzles in PUMP_CONFIG.items():
        pump_data = {
            "number": number,
            "nozzles": nozzles
        }
        pumps_data.append(pump_data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(pumps_data, f, ensure_ascii=False, indent=2)
    
    print(f"Создан файл {filepath} ({len(pumps_data)} колонок)")

def create_statistics_file():
    filepath = "data/statistics.json"
    
    # Проверка существования файла
    if os.path.exists(filepath):
        response = input(f"⚠ Файл {filepath} уже существует. Перезаписать? (y/n): ").lower()
        if response not in ['y', 'yes', 'д', 'да']:
            print("  Пропущено")
            return
    
    initial_stats = {
        "total_revenue": 0.0,
        "total_cars": 0,
        "fuel_sales": {
            "AI92": {"liters": 0, "revenue": 0},
            "AI95": {"liters": 0, "revenue": 0},
            "AI98": {"liters": 0, "revenue": 0},
            "DT": {"liters": 0, "revenue": 0}
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(initial_stats, f, ensure_ascii=False, indent=2)
    
    print(f"Создан файл {filepath}")

def create_history_file():
    """Создание файла истории операций"""
    filepath = "data/history.json"
    
    # Проверка существования файла
    if os.path.exists(filepath):
        response = input(f"⚠ Файл {filepath} уже существует. Перезаписать? (y/n): ").lower()
        if response not in ['y', 'yes', 'д', 'да']:
            print("  Пропущено")
            return
    
    # Пустая история
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    
    print(f"Создан файл {filepath}")

def show_summary():
    """Показать сводку созданных данных"""
    print("\n" + "=" * 60)
    print("СВОДКА СОЗДАННЫХ ДАННЫХ")
    print("=" * 60)
    
    # Цистерны
    print(f"\nЦистерны ({len(INITIAL_TANKS)} шт.):")
    for tank in INITIAL_TANKS:
        status = "ВКЛ" if tank["is_active"] else "ВЫКЛ"
        print(f"  - {tank['id']:10} | {tank['fuel_type']:4} | "
              f"{tank['current_level']}/{tank['max_level']} л | {status}")
    
    # Колонки
    print(f"\nКолонки ({len(PUMP_CONFIG)} шт.):")
    for number, nozzles in sorted(PUMP_CONFIG.items()):
        fuel_list = ", ".join(nozzles.keys())
        print(f"  - Колонка {number}: {fuel_list}")
    
    print("\n" + "=" * 60)
    print("Инициализация завершена успешно!")
    print("=" * 60 + "\n")

def main():
    """Главная функция инициализации"""
    print("\n" + "=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ ДАННЫХ СИСТЕМЫ АЗС")
    print("=" * 60 + "\n")
    
    try:
        # Создание структуры
        create_data_directory()
        create_tanks_file()
        create_pumps_file()
        create_statistics_file()
        create_history_file()
        
        # Сводка
        show_summary()
        
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
