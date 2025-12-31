import json
import sys
from typing import Dict
from models.tank import Tank
from models.pump import Pump
from config import PUMP_CONFIG, INITIAL_TANKS

class DataManager:
    def __init__(self, dir = "data/"):
        self.data_dir = dir

    """ Цистерны """
    def load_tanks(self) -> Dict[str, Tank]: # -> Dict[tank_id, Tank]
        tank_file = self.data_dir + "tanks.json"
        try:
            with open(tank_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            print(e)
            sys.exit()
        
        tanks = {}
        for tank_data in data:
            tank = Tank.get_info(tank_data)
            tanks[tank.id] = tank

        return tanks

    def save_tanks(self, tanks: Dict[str, Tank]):
        tank_file = self.data_dir + "tanks.json"
        data = [tank.info() for tank in tanks.values()]
        try:
            with open(tank_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            print(e)
            sys.exit()

    """ Колонки """
    def load_pumps(self) -> Dict[int, Pump]: # Dict[number, Pump]
        pump_file = self.data_dir + "pumps.json"
        try:
            with open(pump_file, "r", encoding = "utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            print(e)
            sys.exit()

        pumps = {}
        for pump_data in data:
            pump = Pump.get_info(pump_data)
            pumps[pump.number] = pump

        return pumps

    def save_pumps(self, pumps: Dict[int, Pump]):
        pump_file = self.data_dir + "pumps.json"
        data = [pump.info() for pump in pumps.values()]
        try:
            with open(pump_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            print(e)
            sys.exit()

        """ Статистика """
    def load_statistics(self) -> dict:
        stats_file = self.data_dir + "statistics.json"
        try:
            with open(stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            sys.exit()

    def save_statistics(self, stats: dict):
        stats_file = self.data_dir + "statistics.json"
        try:
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
        except FileNotFoundError:
            print(f"Не обнаружены данные. Перед первым запуском запустить start_data.py")
            sys.exit()
