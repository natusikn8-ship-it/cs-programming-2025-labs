from typing import List, Dict
from models.tank import Tank
from models.pump import Pump
from models.fuel import fuel_types
from services.tank_service import TankService
from config import STATION_NAME
from datetime import datetime

class Display:
    def show_header(self):
        print("\n" + "=" * 60)
        print(f"{'АЗС «' + STATION_NAME + '»':^60}")
        print("=" * 60)
        print("Система управления заправочной станцией")
        print("-" * 60)
    
    def show_warnings(self, tank_service: TankService):
        disabled = tank_service.get_disabled_tanks()
        
        if disabled:
            print("\n⚠ ВНИМАНИЕ!")
            print("Обнаружены отключённые цистерны:")
            
            for tank in disabled:
                reason = "низкий уровень топлива" if tank.current_level < tank.min_level else "отключена вручную"
                print(f" - {tank.id} ({reason})")
            
            print()
    
    def show_main_menu(self):
        """Показать главное меню"""
        print("-" * 60)
        print("Выберите действие:")
        print("1) Обслужить клиента (касса)")
        print("2) Проверить состояние цистерн")
        print("3) Оформить пополнение топлива")
        print("4) Баланс и статистика")
        print("5) История операций")
        print("6) Перекачка топлива между цистернами")
        print("7) Управление цистернами (вкл/выкл)")
        print("8) Состояние колонок")
        print("9) EMERGENCY - аварийная ситуация")
        print("0) Выход")
        print()
    
    def show_tanks_status(self, tanks: Dict[str, Tank]):
        print("\n--- Состояние цистерн ---\n")
        
        for i, tank in enumerate(tanks.values(), 1):
            status = "ВКЛ" if tank.is_active else "ВЫКЛ"
            
            # Форматирование объема
            volume_str = f"{tank.current_level} / {tank.max_level} л"
            
            # Дополнительные пометки
            notes = []
            if tank.current_level < tank.min_level:
                notes.append("ниже порога")
            if tank.current_level / tank.max_level < 0.2:
                notes.append("требуется пополнение")
            
            note_str = f" ({', '.join(notes)})" if notes else ""
            
            print(f"{i}) {tank.id:10} | {volume_str:20} | {status}{note_str}")
    
    def show_pumps_status(self, pumps: Dict[int, Pump], tanks: Dict[str, Tank]):
        print("\n--- Состояние колонок ---\n")
        
        for pump in sorted(pumps.values(), key=lambda p: p.number):
            print(f"Колонка {pump.number}:")
            
            available = pump.get_available_fuels(tanks)
            
            if not available:
                print("Нет доступного топлива")
            else:
                for fuel_key, tank_id in available:
                    fuel = fuel_types[fuel_key]
                    tank = tanks[tank_id]
                    print(f"Доступно: {fuel.name} - цистерна {tank_id} ({tank.current_level} л)")
            
            # Показать недоступное топливо
            unavailable = []
            for fuel_key, tank_id in pump.nozzles.items():
                if (fuel_key, tank_id) not in available:
                    fuel = fuel_types[fuel_key]
                    unavailable.append(f"{fuel.name} (цистерна {tank_id} отключена)")
            
            if unavailable:
                for item in unavailable:
                    print(f"Недоступно: {item}")
            
            print()
    
    def show_statistics(self, stats: dict):
        print("\n--- Баланс и статистика ---\n")
        
        print(f"Обслужено автомобилей: {stats['total_cars']}")
        print(f"Общий доход: {stats['total_revenue']}".replace(",", " "))
        print("\nПродано топлива:")
        
        for fuel_key, data in stats["fuel_sales"].items():
            fuel = fuel_types[fuel_key]
            liters = data["liters"]
            revenue = data["revenue"]
            
            liters_str = f"{liters:,.0f} л".replace(",", " ")
            revenue_str = f"{revenue}".replace(",", " ")
            
            print(f"{fuel.name:6} - {liters_str:15} ({revenue_str})")
    
    def show_history(self, transactions: List):
        print("\n--- История операций ---\n")
        
        if not transactions:
            print("История пуста")
            return
        
        for trans in transactions:
            time_str = trans.timestamp.strftime("%d.%m.%Y %H:%M:%S")
            op_type = self._get_operation_name(trans.operation_type)
            
            print(f"[{time_str}] {op_type}")
            self._show_transaction_details(trans)
            print()
    
    def _get_operation_name(self, op_type: str) -> str:
        names = {
            "sale": "Продажа",
            "refill": "Пополнение",
            "transfer": "Перекачка",
            "tank_enable": "Включение цистерны",
            "tank_disable": "Отключение цистерны",
            "emergency_start": "АВАРИЙНАЯ СИТУАЦИЯ",
            "emergency_end": "Выход из аварийного режима"
        }
        return names.get(op_type, op_type)
    
    def _show_transaction_details(self, trans):
        details = trans.details
        
        if trans.operation_type == "sale":
            fuel = fuel_types[details["fuel"]]
            cost_str = f"{details['cost']}".replace(",", " ")
            
            print(f"  Колонка: {details['pump']}")
            print(f"  Топливо: {fuel.name}")
            print(f"  Объем: {details['amount']} л")
            print(f"  Стоимость: {cost_str}")
        
        elif trans.operation_type == "refill":
            fuel = fuel_types[details["fuel_type"]]
            print(f"  Цистерна: {details['tank_id']}")
            print(f"  Топливо: {fuel.name}")
            print(f"  Объем: {details['amount']} л")
        
        elif trans.operation_type == "transfer":
            print(f"  Из: {details['source']}")
            print(f"  В: {details['target']}")
            print(f"  Объем: {details['amount']} л")
        
        elif trans.operation_type == "tank_enable":
            print(f"  Цистерна: {details['tank_id']}")
        
        elif trans.operation_type == "tank_disable":
            print(f"  Цистерна: {details['tank_id']}")
        
        elif trans.operation_type == "emergency_start":
            print(f"  Причина: {details['reason']}")
            print(f"  Заблокировано цистерн: {details['tanks_disabled']}")
        
        elif trans.operation_type == "emergency_end":
            print(f"  Предыдущая причина: {details.get('previous_reason', 'N/A')}")
    
    def pause(self):
        input("\nНажмите Enter для продолжения...")
