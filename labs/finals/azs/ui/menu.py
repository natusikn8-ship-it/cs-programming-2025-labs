""" Тут тоже почти полностью на нейонке было. Ненавижу писать ui и прочий фронтенд """
from models.pump import Pump
from services.tank_service import TankService
from services.pump_service import PumpService
from services.sales_service import SalesService
from services.refill_service import RefillService
from services.statistics_service import StatisticsService
from services.emergency_service import EmergencyService
from storage.data import DataManager
from storage.history import HistoryManager
from ui.display import Display
from ui.input_handler import InputHandler
from models.fuel import fuel_types

class MainMenu:
    def __init__(self):
        print("Инициализация системы...")
        
        # Инициализация хранилища
        self.data_manager = DataManager()
        self.history_manager = HistoryManager()
        
        tanks = self.data_manager.load_tanks()
        pumps = self.data_manager.load_pumps()
        statistics = self.data_manager.load_statistics()
        
        self.tank_service = TankService(tanks)
        self.pump_service = PumpService(pumps)
        self.sales_service = SalesService(self.tank_service, self.pump_service)
        self.refill_service = RefillService(self.tank_service)
        self.statistics_service = StatisticsService(statistics)
        self.emergency_service = EmergencyService(self.tank_service)
        
        self.display = Display()
        self.input = InputHandler()
        
        self.running = True
        
        print("Система готова к работе\n")
    
    def run(self):
        """Главный цикл программы"""
        while self.running:
            try:
                self.display.show_header()
                
                if self.emergency_service.is_active():
                    print("ВНИМАНИЕ: АКТИВИРОВАН АВАРИЙНЫЙ РЕЖИМ")
                    print(f"Причина: {self.emergency_service.emergency_reason}\n")
                else:
                    self.display.show_warnings(self.tank_service)
                
                self.display.show_main_menu()
                
                choice = self.input.get_menu_choice("> ", 0, 9)
                self.handle_menu_choice(choice)
                
            except KeyboardInterrupt:
                print("\n\nПрерывание программы...")
                self.exit_program()
                break
            except Exception as e:
                print(f"\nНепредвиденная ошибка: {e}")
                self.display.pause()
    
    def handle_menu_choice(self, choice: int):
        """Обработка выбора пункта меню. 
        Тут была пздц стрёмная конструкция с elif и так делать нельзя. 
        Обработку множества событий делать только через match...case"""
        match choice:
            case 1:
                self.handle_customer_service()
            case 2:
                self.show_tanks_status()
            case 3:
                self.handle_refill()
            case 4:
                self.show_statistics()
            case 5:
                self.show_history()
            case 6:
                self.handle_transfer()
            case 7:
                self.handle_tank_management()
            case 8: 
                self.show_pumps_status()
            case 9:
                self.handle_emergency()
            case 0:
                self.exit_program()
    
    def save_all_data(self):
        self.data_manager.save_tanks(self.tank_service.tanks)
        self.data_manager.save_pumps(self.pump_service.pumps)
        self.data_manager.save_statistics(self.statistics_service.stats)
        print("Данные сохранены")

        # === ПУНКТ 1: ОБСЛУЖИВАНИЕ КЛИЕНТА ===
    
    def handle_customer_service(self):
        print("\n--- Обслуживание клиента ---\n")
        
        # Проверка аварийного режима
        if self.emergency_service.is_active():
            print("Ошибка: Заправка заблокирована (аварийный режим)")
            self.display.pause()
            return
        
        # Выбор колонки
        print("Доступные колонки:")
        all_pumps = sorted(self.pump_service.get_all_pumps(), key=lambda p: p.number)
        
        for pump in all_pumps:
            available_count = len(self.pump_service.get_available_fuels(pump.number, self.tank_service.tanks))
            status = f"({available_count} вид(ов) топлива доступно)" if available_count > 0 else "(нет топлива)"
            print(f"{pump.number}) Колонка {pump.number} {status}")
        
        print()
        pump_num = self.input.get_int_input("Выберите колонку (0 - отмена): ", 0, 8, allow_cancel=False)
        
        if pump_num == 0:
            return
        
        # Проверка доступного топлива
        available_fuels = self.pump_service.get_available_fuels(pump_num, self.tank_service.tanks)
        
        if not available_fuels:
            print("\nОшибка: В данной колонке нет доступного топлива")
            self.display.pause()
            return
        
        # Выбор топлива
        print(f"\nКолонка {pump_num}")
        print("\nДоступные виды топлива:")
        
        for i, (fuel_key, tank_id) in enumerate(available_fuels, 1):
            fuel = fuel_types[fuel_key]
            tank = self.tank_service.get_tank(tank_id)
            print(f"{i}) {fuel.name:6} - {fuel.price} /л (цистерна {tank_id}, {tank.current_level} л)")
        
        print()
        fuel_choice = self.input.get_menu_choice("Выберите тип топлива: ", 1, len(available_fuels))
        
        fuel_key, tank_id = available_fuels[fuel_choice - 1]
        fuel = fuel_types[fuel_key]
        tank = self.tank_service.get_tank(tank_id)
        
        # Ввод количества литров
        print(f"\nВыбрано: {fuel.name}")
        print(f"Доступно в цистерне: {tank.current_level} л")
        
        amount = self.input.get_positive_float("\nВведите количество литров: ")
        
        if amount is None:
            return
        
        # Проверка достаточности
        if amount > tank.current_level:
            print(f"\Ошибка: В цистерне недостаточно топлива (доступно {tank.current_level} л)")
            self.display.pause()
            return
        
        # Расчет стоимости
        cost = self.sales_service.calculate_cost(fuel_key, amount)
        
        print(f"\nСтоимость:")
        print(f"{amount} л * {fuel.price} = {cost}")
        
        # Подтверждение
        if not self.input.get_yes_no("\nПодтвердить оплату?"):
            print("Операция отменена")
            self.display.pause()
            return
        
        success, message, transaction = self.sales_service.process_sale(pump_num, fuel_key, amount)
        
        if success:
            self.statistics_service.update_from_sale(transaction)
            
            self.history_manager.add_transaction(transaction)
            
            self.save_all_data()
            
            print("\nОперация выполнена успешно!")
            print("Спасибо за покупку!")
        else:
            print(f"\n{message}")
        
        self.display.pause()
    
    # === ПУНКТ 2: СОСТОЯНИЕ ЦИСТЕРН ===
    
    def show_tanks_status(self):
        self.display.show_tanks_status(self.tank_service.tanks)
        self.display.pause()
    
    # === ПУНКТ 3: ПОПОЛНЕНИЕ ТОПЛИВА ===
    
    def handle_refill(self):
        print("\n--- Оформление пополнения топлива ---\n")
        
        # Список цистерн
        all_tanks = self.tank_service.get_all_tanks()
        
        def display_tank(tank):
            space = tank.max_level - tank.current_level
            status = "ВКЛ" if tank.is_active else "ВЫКЛ"
            return f"{tank.id:10} | {tank.current_level}/{tank.max_level} л | Свободно: {space} л | {status}"
        
        idx, selected_tank = self.input.select_from_list(
            "Выберите цистерну для пополнения (0 - отмена): ",
            all_tanks,
            display_tank
        )
        
        # Ввод количества
        available_space = self.refill_service.get_available_space(selected_tank.id)
        
        print(f"\nВыбрана цистерна: {selected_tank.id}")
        print(f"Текущий уровень: {selected_tank.current_level} л")
        print(f"Свободное место: {available_space} л")
        
        amount = self.input.get_positive_float("\nВведите количество литров для пополнения: ")
        
        if amount is None:
            return
        
        # Подтверждение
        if not self.input.confirm_operation(f"Пополнить цистерну {selected_tank.id} на {amount} л?"):
            print("Операция отменена")
            self.display.pause()
            return
        
        # Обработка пополнения
        success, message, transaction = self.refill_service.process_refill(selected_tank.id, amount)
        
        if success:
            # Сохранение в историю
            self.history_manager.add_transaction(transaction)
            
            # Сохранение данных
            self.save_all_data()
            
            print(f"\n{message}")
        else:
            print(f"\n{message}")
        
        self.display.pause()
    
    # === ПУНКТ 4: СТАТИСТИКА ===
    
    def show_statistics(self):
        self.display.show_statistics(self.statistics_service.stats)
        self.display.pause()
    
    # === ПУНКТ 5: ИСТОРИЯ ===
    
    def show_history(self):
        recent = self.history_manager.get_recent(20)
        self.display.show_history(recent)
        self.display.pause()
    
    # === ПУНКТ 6: ПЕРЕКАЧКА ===
    
    def handle_transfer(self):
        print("\n--- Перекачка топлива ---\n")
        
        print("Выберите тип топлива для перекачки:")
        fuel_keys = list(fuel_types.keys())
        
        for i, fuel_key in enumerate(fuel_keys, 1):
            fuel = fuel_types[fuel_key]
            print(f"{i}) {fuel.name}")
        
        print()
        fuel_choice = self.input.get_menu_choice("Выберите тип топлива: ", 1, len(fuel_keys))
        selected_fuel_key = fuel_keys[fuel_choice - 1]
        
        tanks_of_type = self.tank_service.get_tanks_by_fuel(selected_fuel_key)
        
        if len(tanks_of_type) < 2:
            print("\nОшибка: Недостаточно цистерн этого типа для перекачки")
            self.display.pause()
            return
        
        print("\nВыберите цистерну-источник:")
        for i, tank in enumerate(tanks_of_type, 1):
            print(f"{i}) {tank.id} - {tank.current_level} л")
        
        print()
        source_idx = self.input.get_menu_choice("Источник: ", 1, len(tanks_of_type))
        source_tank = tanks_of_type[source_idx - 1]
        
        remaining_tanks = [t for t in tanks_of_type if t.id != source_tank.id]
        
        print("\nВыберите цистерну-приемник:")
        for i, tank in enumerate(remaining_tanks, 1):
            space = tank.max_level - tank.current_level
            print(f"{i}) {tank.id} - {tank.current_level} л (свободно: {space} л)")
        
        print()
        target_idx = self.input.get_menu_choice("Приемник: ", 1, len(remaining_tanks))
        target_tank = remaining_tanks[target_idx - 1]
        
        max_amount = min(source_tank.current_level, target_tank.max_level - target_tank.current_level)
        
        print(f"\nМаксимально можно перекачать: {max_amount} л")
        amount = self.input.get_float_input("Введите количество литров: ", 0.1, max_amount)
        
        if amount is None:
            return
        
        if not self.input.confirm_operation(
            f"Перекачать {amount} л из {source_tank.id} в {target_tank.id}?"
        ):
            print("Операция отменена")
            self.display.pause()
        success, message = self.tank_service.transfer_fuel(source_tank.id, target_tank.id, amount)
        
        if success:
            from models.transaction import Transaction
            from datetime import datetime
            
            transaction = Transaction(
                timestamp=datetime.now(),
                operation_type="transfer",
                details={
                    "source": source_tank.id,
                    "target": target_tank.id,
                    "fuel_type": selected_fuel_key,
                    "amount": amount
                }
            )
            
            self.history_manager.add_transaction(transaction)
            self.save_all_data()
            
            print(f"\n{message}")
        else:
            print(f"\n{message}")
        
        self.display.pause()

        # === ПУНКТ 7: УПРАВЛЕНИЕ ЦИСТЕРНАМИ ===
    
    def handle_tank_management(self):
        """Управление цистернами (включение/отключение)"""
        print("\n--- Управление цистернами ---\n")
        
        print("Выберите действие:")
        print("1) Включить цистерну")
        print("2) Отключить цистерну")
        print("0) Отмена")
        print()
        
        action = self.input.get_menu_choice("> ", 0, 2)
        
        if action == 0:
            return
        
        if action == 1:
            self.enable_tank()
        elif action == 2:
            self.disable_tank()
    
    def enable_tank(self):
        """Включить цистерну"""
        disabled = self.tank_service.get_disabled_tanks()
        
        if not disabled:
            print("\n✓ Все цистерны уже включены")
            self.display.pause()
            return
        
        print("\nЦистерны, доступные для включения:")
        
        can_enable = []
        for tank in disabled:
            if tank.can_enable():
                can_enable.append(tank)
        
        if not can_enable:
            print("Нет цистерн, которые можно включить (уровень топлива ниже минимума)")
            self.display.pause()
            return
        
        def display_tank(tank):
            return f"{tank.id} - {tank.current_level}/{tank.max_level} л"
        
        idx, selected = self.input.select_from_list(
            "Выберите цистерну для включения: ",
            can_enable,
            display_tank
        )
        
        success, message = self.tank_service.enable_tank(selected.id)
        
        if success:
            # Сохранение в историю
            from models.transaction import Transaction
            from datetime import datetime
            
            transaction = Transaction(
                timestamp=datetime.now(),
                operation_type="tank_enable",
                details={"tank_id": selected.id}
            )
            
            self.history_manager.add_transaction(transaction)
            self.save_all_data()
            
            print(f"\n{message}")
        else:
            print(f"\nОшибка: {message}")
        
        self.display.pause()
    
    def disable_tank(self):
        """Отключить цистерну"""
        active_tanks = [t for t in self.tank_service.get_all_tanks() if t.is_active]
        
        if not active_tanks:
            print("\n⚠ Все цистерны уже отключены")
            self.display.pause()
            return
        
        print("\nВключенные цистерны:")
        
        def display_tank(tank):
            return f"{tank.id} - {tank.current_level}/{tank.max_level} л"
        
        idx, selected = self.input.select_from_list(
            "Выберите цистерну для отключения: ",
            active_tanks,
            display_tank
        )
        
        if not self.input.confirm_operation(f"Отключить цистерну {selected.id}?"):
            print("Операция отменена")
            self.display.pause()
            return
        
        success, message = self.tank_service.disable_tank(selected.id)
        
        if success:
            # Сохранение в историю
            from models.transaction import Transaction
            from datetime import datetime
            
            transaction = Transaction(
                timestamp=datetime.now(),
                operation_type="tank_disable",
                details={"tank_id": selected.id}
            )
            
            self.history_manager.add_transaction(transaction)
            self.save_all_data()
            
            print(f"\n{message}")
        else:
            print(f"\n{message}")
        
        self.display.pause()
    
    # === ПУНКТ 8: СОСТОЯНИЕ КОЛОНОК ===
    
    def show_pumps_status(self):
        """Показать состояние колонок"""
        self.display.show_pumps_status(self.pump_service.pumps, self.tank_service.tanks)
        self.display.pause()
    
    # === ПУНКТ 9: АВАРИЙНАЯ СИТУАЦИЯ ===
    
    def handle_emergency(self):
        """Обработка аварийной ситуации"""
        if self.emergency_service.is_active():
            # Выход из аварийного режима
            print("\nАварийный режим активен")
            print(f"Причина: {self.emergency_service.emergency_reason}\n")
            
            if not self.input.get_yes_no("Деактивировать аварийный режим?"):
                return
            
            success, message, transaction = self.emergency_service.deactivate_emergency()
            
            if success:
                self.history_manager.add_transaction(transaction)
                self.save_all_data()
                
                print(f"\n{message}")
            
        else:
            # Активация аварийного режима
            print("\nАКТИВАЦИЯ АВАРИЙНОГО РЕЖИМА")
            print("Все цистерны будут немедленно заблокированы!")
            print()
            
            if not self.input.get_yes_no("Подтвердить активацию аварийного режима?"):
                print("Отменено")
                self.display.pause()
                return
            
            reason = self.input.get_string_input("Укажите причину аварии: ", allow_empty=False)
            
            success, message, transaction = self.emergency_service.activate_emergency(reason)
            
            if success:
                self.history_manager.add_transaction(transaction)
                self.save_all_data()
                
                print(f"\n{message}")
        
        self.display.pause()
    
    # === ПУНКТ 0: ВЫХОД ===
    
    def exit_program(self):
        """Выход из программы"""
        print("\nСохранение данных...")
        self.save_all_data()
        
        self.running = False
