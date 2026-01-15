import random

# Класс персонажа
class Character:
    def __init__(self):
        self.race = None
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.skill_points = 0
        self.hp = 0
        self.max_hp = 0
        self.attack = 0
        self.defense = 0 # Защита
        self.agility = 0 # Ловкость
        self.height = 0 # Рост
        self.weight = 0 # Вес
        self.inventory = []
        self.equipped = {"weapon": None, "armor": None}
        self.coins = 0
        
    def show_stats(self):
        print(f"\n=== ХАРАКТЕРИСТИКИ ===")
        print(f"Раса: {self.race}")
        print(f"Уровень: {self.level} (Опыт: {self.exp}/{self.exp_to_next})")
        print(f"Очки прокачки: {self.skill_points}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")
        print(f"Ловкость: {self.agility}")
        print(f"Рост: {self.height} см")
        print(f"Вес: {self.weight} кг")
        print(f"Монеты: {self.coins}")
        
        if self.equipped["weapon"]:
            print(f"Оружие: {self.equipped['weapon']}")
        if self.equipped["armor"]:
            print(f"Броня: {self.equipped['armor']}")

    # Получение урона        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    # Регенерация HP
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    # Полуучение опыта
    def add_exp(self, amount):
        self.exp += amount
        print(f"Получено опыта: {amount}")
        while self.exp >= self.exp_to_next:
            self.level_up()
    
    # Получение новго уровня
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        self.skill_points += 3
        self.max_hp += 10
        self.hp = self.max_hp
        print(f"\n=== УРОВЕНЬ ПОВЫШЕН! ===")
        print(f"Теперь у вас {self.level} уровень!")
        print(f"Очков прокачки: {self.skill_points}")
    
    # Повышение характеристик
    def use_skill_points(self):
        while self.skill_points > 0:
            print(f"\nОчков прокачки: {self.skill_points}")
            print("1. +10 к HP")
            print("2. +2 к атаке")
            print("3. +2 к защите")
            print("4. +2 к ловкости")
            print("5. Выйти")
            
            try:
                choice = int(input("Выберите улучшение: "))
                if choice == 1:
                    self.max_hp += 10
                    self.hp += 10
                    self.skill_points -= 1
                    print("HP увеличен!")
                elif choice == 2:
                    self.attack += 2
                    self.skill_points -= 1
                    print("Атака увеличена!")
                elif choice == 3:
                    self.defense += 2
                    self.skill_points -= 1
                    print("Защита увеличена!")
                elif choice == 4:
                    self.agility += 2
                    self.skill_points -= 1
                    print("Ловкость увеличена!")
                elif choice == 5:
                    break
                else:
                    print("Неверный выбор")
            except ValueError:
                print("Введите число от 1 до 5")

# Класс врага
class Enemy:
    def __init__(self, floor):
        types = ["Гоблин", "Скелет", "Орк", "Паук", "Зомби"]
        self.name = random.choice(types)
        self.level = random.randint(max(1, floor-1), floor+1)
        self.hp = random.randint(20, 40) + floor * 10
        self.max_hp = self.hp
        self.attack = random.randint(5, 10) + floor * 2
        self.defense = random.randint(0, 5) + floor
        self.exp_reward = random.randint(20, 40) + floor * 5
        self.coin_reward = random.randint(5, 20) + floor * 3
    
    # Показываем какой противник
    def show_stats(self):
        print(f"\nПротивник: {self.name} (Уровень {self.level})")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Атака: {self.attack}, Защита: {self.defense}")

# Создание персонажа (основные функции игры)
def create_character():
    character = Character()
    
    print("=== СОЗДАНИЕ ПЕРСОНАЖА ===")
    print("Выберите расу:")
    print("1. Человек (сбалансированный)")
    print("2. Эльф (ловкий, но хрупкий)")
    print("3. Дворф (крепкий, но медленный)")
    
    while character.race is None:
        try:
            choice = int(input("Ваш выбор: "))
            if choice == 1:
                character.race = "Человек"
                # Диапазоны для человека
                character.height = random.randint(165, 185)
                character.weight = random.randint(65, 85)
                character.max_hp = random.randint(80, 100)
                character.hp = character.max_hp
                character.attack = random.randint(8, 12)
                character.defense = random.randint(5, 8)
                character.agility = random.randint(10, 14)
                
            elif choice == 2:
                character.race = "Эльф"
                # Диапазоны для эльфа
                character.height = random.randint(175, 195)
                character.weight = random.randint(55, 75)
                character.max_hp = random.randint(70, 90)
                character.hp = character.max_hp
                character.attack = random.randint(9, 13)
                character.defense = random.randint(3, 6)
                character.agility = random.randint(14, 18)
                
            elif choice == 3:
                character.race = "Дворф"
                # Диапазоны для дворфа
                character.height = random.randint(140, 160)
                character.weight = random.randint(70, 90)
                character.max_hp = random.randint(90, 110)
                character.hp = character.max_hp
                character.attack = random.randint(10, 14)
                character.defense = random.randint(7, 10)
                character.agility = random.randint(6, 10)
                
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Введите число от 1 до 3")
    
    # Влияние роста и веса на ловкость
    bmi = character.weight / ((character.height/100) ** 2)
    if bmi < 18.5:
        character.agility += 2
    elif bmi > 25:
        character.agility -= 2
    
    print(f"\nПерсонаж создан!")
    character.show_stats()
    return character

# Генерация комнат
def generate_room(room_type=None):
    if room_type is None:
        room_type = random.choice(["combat", "rest", "treasure", "combat", "rest"])
    
    rooms = {
        "combat": "Боевая комната",
        "rest": "Комната отдыха",
        "treasure": "Комната с сундуком"
    }
    
    return {
        "type": room_type, # Тип комнаты
        "name": rooms[room_type],
        "visited": False # Посещение комнаты
    }

def combat_room(player):
    print("\n=== БОЕВАЯ КОМНАТА ===")
    enemy = Enemy(player.level)
    print(f"На вас напал {enemy.name}!")
    
    while enemy.hp > 0 and player.hp > 0: # Если ещё оба живы
        enemy.show_stats()
        print(f"Ваше HP: {player.hp}/{player.max_hp}")
        print("\nДоступные действия:")
        print("1. Атаковать")
        print("2. Использовать зелье")
        print("3. Попытаться уклониться")
        
        try:
            choice = int(input("Выберите действие: "))
            
            if choice == 1:
                # Атака игрока
                player_damage = max(1, player.attack + random.randint(-2, 3))
                enemy.hp -= player_damage
                print(f"Вы нанесли {player_damage} урона!")
                
                # Контратака врага, если жив
                if enemy.hp > 0:
                    if random.random() < player.agility/100:  # Шанс уклонения
                        print("Вы уклонились от атаки врага!")
                    else:
                        enemy_damage = max(1, enemy.attack - player.defense)
                        player.hp -= enemy_damage
                        print(f"{enemy.name} нанес вам {enemy_damage} урона!")
                        
            elif choice == 2:
                # Использование зелья
                healing_items = [item for item in player.inventory if "Зелье" in item]
                if healing_items:
                    player.heal(30)
                    player.inventory.remove(healing_items[0])
                    print("Вы использовали зелье лечения! +30 HP")
                else:
                    print("У вас нет зелий!")
                    continue
                    
            elif choice == 3:
                # Попытка уклонения
                dodge_chance = player.agility/100 + 0.1
                if random.random() < dodge_chance:
                    print("Вы успешно уклонились!")
                else:
                    print("Уклонение не удалось!")
                    enemy_damage = max(1, enemy.attack - player.defense)
                    player.hp -= enemy_damage
                    print(f"{enemy.name} нанес вам {enemy_damage} урона!")
            else:
                print("Неверный выбор")
                continue
                
        except ValueError:
            print("Введите число от 1 до 3")
            continue
    
    if enemy.hp <= 0:
        print(f"\nВы победили {enemy.name}!")
        player.add_exp(enemy.exp_reward)
        player.coins += enemy.coin_reward
        print(f"Получено монет: {enemy.coin_reward}")
        
        # Шанс на дроп предмета
        if random.random() < 0.3:
            items = ["Малое зелье здоровья", "Стальной меч", "Кожаный доспех"]
            item = random.choice(items)
            player.inventory.append(item)
            print(f"Найдено: {item}")
            
        return True
    else:
        print("\nВы проиграли...")
        return False

def treasure_room(player):
    print("\n=== КОМНАТА С СУНДУКОМ ===")
    print("Вы нашли сундук!")
    
    treasure_type = random.choice(["coins", "item", "both"])
    
    if treasure_type in ["coins", "both"]:
        coins = random.randint(20, 50) + player.level * 10
        player.coins += coins
        print(f"Найдено монет: {coins}")
    
    if treasure_type in ["item", "both"]:
        items = ["Зелье здоровья", "Зелье силы", "Стальной меч", 
                "Кожаный доспех", "Эльфийский лук", "Доспех гномов"]
        item = random.choice(items)
        player.inventory.append(item)
        print(f"Найдено: {item}")
    
    print(f"Ваши монеты: {player.coins}")

def rest_room(player):
    print("\n=== КОМНАТА ОТДЫХА ===")
    print("Здесь безопасно. Вы можете отдохнуть.")
    
    rest_amount = player.max_hp * 0.3
    player.heal(int(rest_amount))
    print(f"Вы восстановили {int(rest_amount)} HP")
    
    if player.skill_points > 0:
        use = input("Хотите использовать очки прокачки? (да/нет): ").lower() # lower возвращает заглавные буквы к строчным
        if use == "да":
            player.use_skill_points()

def manage_inventory(player):
    while True: # Бесконеный цикл меню
        print("\n=== ИНВЕНТАРЬ ===")
        print(f"Монеты: {player.coins}")
        print("Предметы:")
        
        if not player.inventory:
            print("Инвентарь пуст")
        else:
            for i, item in enumerate(player.inventory, 1): # enumerate выводит индекс перевд предметом
                print(f"{i}. {item}")
        
        print("\nЭкипировано:")
        print(f"Оружие: {player.equipped['weapon'] or 'Нет'}")
        print(f"Броня: {player.equipped['armor'] or 'Нет'}")
        
        print("\n1. Использовать предмет")
        print("2. Выбросить предмет")
        print("3. Экипировать предмет")
        print("4. Выйти")
        
        try:
            choice = int(input("Выберите действие: "))
            
            if choice == 1:
                if not player.inventory:
                    print("Инвентарь пуст!")
                    continue
                    
                idx = int(input("Номер предмета: ")) - 1
                if 0 <= idx < len(player.inventory):
                    item = player.inventory[idx]
                    if "Зелье" in item:
                        if "здоровья" in item.lower():
                            player.heal(50)
                            print("Восстановлено 50 HP!")
                        elif "силы" in item.lower():
                            player.attack += 5
                            print("Атака увеличена на 5 на этот бой!")
                        player.inventory.pop(idx)
                    else:
                        print("Этот предмет нельзя использовать")
                else:
                    print("Неверный номер")
                    
            elif choice == 2:
                if not player.inventory:
                    print("Инвентарь пуст!")
                    continue
                    
                idx = int(input("Номер предмета: ")) - 1
                if 0 <= idx < len(player.inventory):
                    removed = player.inventory.pop(idx)
                    print(f"Выброшено: {removed}")
                else:
                    print("Неверный номер")
                    
            elif choice == 3:
                if not player.inventory:
                    print("Инвентарь пуст!")
                    continue
                    
                idx = int(input("Номер предмета: ")) - 1
                if 0 <= idx < len(player.inventory):
                    item = player.inventory[idx]
                    if "меч" in item.lower() or "лук" in item.lower() or "оружие" in item.lower():
                        player.equipped["weapon"] = item
                        player.attack += 3
                        print(f"Экипировано оружие: {item}")
                    elif "доспех" in item.lower() or "броня" in item.lower():
                        player.equipped["armor"] = item
                        player.defense += 3
                        print(f"Экипирована броня: {item}")
                    else:
                        print("Это нельзя экипировать")
                else:
                    print("Неверный номер")
                    
            elif choice == 4:
                break
            else:
                print("Неверный выбор")
                
        except ValueError:
            print("Введите число от 1 до 4")

def main_game():
    print("=== ТЕКСТОВАЯ RPG ===")
    print("Добро пожаловать в подземелье!\n")
    
    player = create_character()
    current_floor = 1
    rooms_cleared = 0
    
    # Начальные предметы
    player.inventory.append("Малое зелье здоровья")
    player.inventory.append("Малое зелье здоровья")
    
    while player.hp > 0:
        print(f"\n=== ЭТАЖ {current_floor} ===")
        print(f"Комнат пройдено: {rooms_cleared}")
        player.show_stats()
        
        # Генерация комнат на развилке
        left_room = generate_room()
        right_room = generate_room()
        
        # Видимость комнат
        left_visible = random.choice([True, False])
        right_visible = random.choice([True, False])
        
        print("\nПеред вами развилка:")
        print(f"1. Слева: {left_room['name'] if left_visible else '???'}")
        print(f"2. Справа: {right_room['name'] if right_visible else '???'}")
        print("3. Открыть инвентарь")
        print("4. Показать характеристики")
        print("5. Выйти из игры")
        
        try:
            choice = int(input("Куда пойти? "))
            
            if choice == 1:
                selected_room = left_room
                print(f"\nВы идете налево...")
            elif choice == 2:
                selected_room = right_room
                print(f"\nВы идете направо...")
            elif choice == 3:
                manage_inventory(player)
                continue
            elif choice == 4:
                player.show_stats()
                continue
            elif choice == 5:
                print("Спасибо за игру!")
                break
            else:
                print("Неверный выбор")
                continue
                
            # Обработка выбранной комнаты
            if selected_room["type"] == "combat":
                if not combat_room(player): # Если проиграли
                    print("Игра окончена!")
                    break
            elif selected_room["type"] == "treasure":
                treasure_room(player)
            elif selected_room["type"] == "rest":
                rest_room(player)
            
            rooms_cleared += 1
            
            # Переход на следующий этаж
            if rooms_cleared % 5 == 0:
                current_floor += 1
                print(f"\n=== ВЫ СПУСТИЛИСЬ НА ЭТАЖ {current_floor}! ===")
                print("Враги стали сильнее!")
                player.heal(player.max_hp // 2) # На 50% HP
                print(f"Вы восстановили {player.max_hp // 2} HP")
                
        except ValueError:
            print("Введите число от 1 до 5")
    
    print(f"\n=== ИГРА ОКОНЧЕНА ===")
    print(f"Ваш результат:")
    print(f"Уровень: {player.level}")
    print(f"Пройдено комнат: {rooms_cleared}")
    print(f"Достигнутый этаж: {current_floor}")

# Запуск игры
if __name__ == "__main__": # При запуске игры напрямую
    try:
        main_game()
    except KeyboardInterrupt: # Если игра прервана
        print("\n\nИгра прервана")
    except Exception as e: # Если произошла очибка любого стандартного типа (деление на ноль, отсутствие файла, синтаксические ошибки и т.д)
        print(f"Произошла ошибка: {e}")