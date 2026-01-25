import random

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
        print(f"\nХАРАКТЕРИСТИКИ")
        print(f"Раса: {self.race}")
        print(f"Уровень: {self.level}, Опыт: {self.exp}/{self.exp_to_next})")
        print(f"Очки характеристик: {self.skill_points}")
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

    # Получение опыта
    def add_exp(self, amount):
        self.exp += amount
        print(f"Получено опыта: {amount}")
        while self.exp >= self.exp_to_next:
            self.level_up()
    
    # Получение новго уровня
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = self.exp_to_next * 1.5
        self.skill_points += 1
        self.max_hp += 10
        self.hp = self.max_hp
        print(f"Уровень ПОВЫШЕН до {self.level}!")
        print(f"Очков харатеристик: {self.skill_points}")
    
    # Повышение характеристик
    def use_skill_points(self):
        while self.skill_points > 0:
            print(f"Очков характеристик доступно: {self.skill_points}")
            print("1. +5 к HP")
            print("2. +1 к атаке")
            print("3. +1 к защите")
            print("4. +1 к ловкости")
            print("5. Выйти")
            
            try:
                choice = int(input("Ваш выбор: "))
                if choice == 1:
                    self.max_hp += 5
                    self.hp += 5
                    self.skill_points -= 1
                    print("HP увеличен!")
                elif choice == 2:
                    self.attack += 1
                    self.skill_points -= 1
                    print("Атака увеличена!")
                elif choice == 3:
                    self.defense += 1
                    self.skill_points -= 1
                    print("Защита увеличена!")
                elif choice == 4:
                    self.agility += 1
                    self.skill_points -= 1
                    print("Ловкость увеличена!")
                elif choice == 5:
                    break
                else:
                    print("ОШИБКА!")
            except ValueError:
                print("Выберите число от 1 до 5")

    # Покупка предметов
    def use_coins(self):
        print("Здравствуй путешественник! Что хочешь приобрести?")

        while self.coins > 0:
            print(f"Монет доступно: {self.coins}")
            print(f"1. Малое зелье ({self.level**2 + 59} монет)")
            print(f"2. Среднее зелье ({self.level**2 + 129} монет)")
            print(f"3. Большое зелье ({self.level**2 + 199} монет")
            print(f"4. Oчко характеристик ({self.level**2 + 199} монет)")
            print(f"5. 100 опыта ({self.level**2 + 299} монет)")
            print("6. Выйти")
            
            try:
                choice = int(input("Ваш выбор: "))
                if choice == 1:
                    if self.coins >= self.level**2 + 59:
                        items = ["Малое зелье здоровья", "Малое зелье силы", "Малое зелье защиты", "Малое зелье ловкости"]
                        item = random.choice(items)
                        use = input(F"Вам предлагают: {item}. Хотите риобрести? (да/нет): ").lower()
                        if use == "да":                       
                            self.inventory.append(item)
                            self.coins -= self.level**2 + 59
                        print(f"Вы приобрели: {item}!")
                    else:
                        print("У вас недостаточно монет")
                elif choice == 2:
                    if self.coins >= self.level**2 + 129:
                        items = ["Среднее зелье здоровья", "Среднее зелье силы", "Среднее зелье защиты", "Среднее зелье ловкости"]
                        item = random.choice(items)
                        use = input(F"Вам предлагают: {item}. Хотите риобрести? (да/нет): ").lower()
                        if use == "да":                       
                            self.inventory.append(item)
                            self.coins -= self.level**2 + 129
                        print(f"Вы приобрели: {item}!")
                    else:
                        print("У вас недостаточно монет")
                elif choice == 3:
                    if self.coins >= self.level**2 + 199:
                        items = ["Большое зелье здоровья", "Большое зелье силы", "Большое зелье защиты", "Большое зелье ловкости"]
                        item = random.choice(items)
                        use = input(F"Вам предлагают: {item}. Хотите риобрести? (да/нет): ").lower()
                        if use == "да":                       
                            self.inventory.append(item)
                            self.coins -= self.level**2 + 199
                        print(f"Вы приобрели: {item}!")
                    else:
                        print("У вас недостаточно монет")                        
                elif choice == 4:
                    if self.coins >= self.level**2 + 199:
                        self.skill_points += 1
                        self.coins -= self.level**2 + 199
                        print("Вы приобрели очко характеристик!")
                    else:
                        print("У вас недостаточно монет")                      
                elif choice == 5:
                    if self.coins >= self.level**2 + 300:
                        self.exp += 100
                        self.coins -= self.level**2 + 300
                        print("Вы приобрели 50 опыта!")
                    else:
                        print("У вас недостаточно монет")                                           
                elif choice == 6:
                    print("Удачи в дороге, путешественник!")
                    break
                else:
                    print("ОШИБКА!")
            except ValueError:
                print("Выберите число от 1 до 6")

# Класс врага
class Enemy:
    def __init__(self, floor):
        types = ["Слизь", "Скелет", "Паук", "Гоблин", "Скелет", "Паук", "Гоблин", "Орк"]
        self.name = random.choice(types)
        if self.name == "Слизь":
            self.level = random.randint(max(1, floor-1), floor+1)
            self.hp = random.randint(10, 15) + floor**2
            self.max_hp = self.hp
            self.attack = random.randint(0, 1) + floor 
            self.defense = random.randint(0, 1) + floor
            self.exp_reward = random.randint(5, 10) + floor**2
            self.coin_reward = random.randint(1, 5) + floor
        elif self.name == "Орк":
            self.level = random.randint(max(1, floor-1), floor+1)
            self.hp = random.randint(50, 70) + floor**2 * 2
            self.max_hp = self.hp
            self.attack = random.randint(15, 20) + floor * 8
            self.defense = random.randint(5, 10) + floor
            self.exp_reward = random.randint(40, 80) + floor * 8
            self.coin_reward = random.randint(20, 30) + floor * 5
        else:
            self.level = random.randint(max(1, floor-1), floor+1)
            self.hp = random.randint(20, 40) + floor**2 * 2
            self.max_hp = self.hp
            self.attack = random.randint(5, 10) + floor * 5
            self.defense = random.randint(0, 5) + floor
            self.exp_reward = random.randint(20, 40) + floor * 5
            self.coin_reward = random.randint(5, 20) + floor * 3
    
    def show_stats(self):
        print(f"\nВаш противник: {self.name} (Уровень {self.level})")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Атака: {self.attack}, Защита: {self.defense}")  

# Создание персонажа (основные функции игры)
def create_character():
    character = Character()
    
    print("СОЗДАНИЕ ПЕРСОНАЖА")
    print("Выберите расу:")
    print("1. Человек")
    print("2. Эльф")
    print("3. Дворф")
    print("4. Узнать информацию о расах")
    
    while character.race is None:
        try:
            choice = int(input("\nВаш выбор: "))
            if choice == 1:
                character.race = "Человек"
                character.height = random.randint(165, 185)
                character.weight = random.randint(65, 85)
                character.max_hp = random.randint(80, 100)
                character.hp = character.max_hp
                character.attack = random.randint(8, 12)
                character.defense = random.randint(5, 8)
                character.agility = random.randint(10, 14)
                
            elif choice == 2:
                character.race = "Эльф"
                character.height = random.randint(175, 195)
                character.weight = random.randint(55, 75)
                character.max_hp = random.randint(70, 90)
                character.hp = character.max_hp
                character.attack = random.randint(9, 13)
                character.defense = random.randint(3, 6)
                character.agility = random.randint(14, 18)
                
            elif choice == 3:
                character.race = "Дворф"
                character.height = random.randint(140, 160)
                character.weight = random.randint(70, 90)
                character.max_hp = random.randint(90, 110)
                character.hp = character.max_hp
                character.attack = random.randint(10, 14)
                character.defense = random.randint(7, 10)
                character.agility = random.randint(6, 10)

            elif choice == 4:
                print("\n1. Человек - доминирующая и самая многочисленная раса. " \
                "Их характеристики сбалансированы, они не имеют особенных черт.")
                print("2. Эльф - лесные обитатели, единые с природой, редко остаются на одном месте. " \
                "Они умнее и быстрее людей, зато хрупче.")
                print("3. Дворц - малочисленная раса, часто живущая в горах. " \
                "Из-за своего невысокого роста и массивного телосложения, они устойчивы к атакам с повыщеным уроном.")

            else:
                print("ОШИБКА!")
        except ValueError:
            print("Введите число от 1 до 4")
    
    # Влияние роста и веса на ловкость
    bmi = character.weight / ((character.height/100) ** 2)
    if bmi < 18.5:
        character.agility += 2
    elif bmi > 25:
        character.agility -= 2
    
    print(f"Персонаж создан!")
    character.show_stats()
    return character

# Генерация комнат
def generate_room(room_type=None):
    if room_type is None:
        room_type = random.choice(["combat", "rest", "treasure", "combat", "rest", "combat", "combat"])
    
    rooms = {
        "combat": "Боевая комната",
        "rest": "Комната отдыха",
        "treasure": "Комната с сундуком"
    }
    
    return {
        "type": room_type, # Тип комнаты
        "name": rooms[room_type],
        "visited": False 
    }

def combat_room(player):
    print("\nБОЕВАЯ КОМНАТА")
    enemy = Enemy(player.level)
    print(f"На вас напал {enemy.name}!")
    
    while enemy.hp > 0 and player.hp > 0: # Если ещё оба живы
        enemy.show_stats()
        print(f"Ваше HP: {player.hp}/{player.max_hp}")
        print("\nДоступные действия:")
        print("1. Атаковать")
        print("2. Попытаться уклониться")
        print("3. Сбежать")
        
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
                # Попытка уклонения
                dodge_chance = player.agility/100 + 0.3
                if random.random() < dodge_chance:
                    player_damage = max(1, player.attack + random.randint(-2, 3)) * 2
                    enemy.hp -= player_damage
                    print(f"Вы уклонились от атаки врага! Вы нанесли {player_damage} урона!")
                else:
                    print("Уклонение не удалось!")
                    enemy_damage = max(1, enemy.attack - player.defense)
                    player.hp -= enemy_damage
                    print(f"{enemy.name} нанес вам {enemy_damage} урона!")
                    
            elif choice == 3:
                # Сбежать из боя
                if random.random() < 0.3:
                    print("Вы успешно сбежали!")
                    return True
                else:
                    enemy_damage = max(1, enemy.attack - player.defense)
                    player.hp -= enemy_damage
                    print(f"Сбежать не удалось! {enemy.name} нанес вам {enemy_damage} урона!")
                    continue
            else:
                print("ОШИБКА!")
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
            if enemy.name == "Орк":
                items = ["Прочный доспех", "Тяжёлое оружие", "Большое зелье силы", "Среднее зелье силы"]
                item = random.choice(items)
                player.inventory.append(item)
                print(f"Найдено: {item}")
            elif enemy.name == "Скелет":
                items = ["Малое зелье здоровья","Среднее зелье здоровья", "Малое зелье силы", "Среднее зелье силы", "Лёгкий лук", "Кожаный доспех"]
                item = random.choice(items)
                player.inventory.append(item)
                print(f"Найдено: {item}")
            elif enemy.name == "Паук":
                items = ["Малое зелье защиты", "Среднее зелье защиты", "Малое зелье ловкости", "Среднее зелье ловкости", "Малое зелье силы", "Среднее зелье силы"]
                item = random.choice(items)
                player.inventory.append(item)
                print(f"Найдено: {item}")
            elif enemy.name == "Гоблин":
                items = ["Малое зелье здоровья", "Стальной меч", "Железный доспех", "Среднее зелье здоровья", "Малое зелье ловкости", "Среднее зелье ловкости"]
                item = random.choice(items)
                player.inventory.append(item)
                print(f"Найдено: {item}")
            else:
                items = ["Малое зелье здоровья", "Малое зелье защиты"]
                item = random.choice(items)
                player.inventory.append(item)
                print(f"Найдено: {item}")

        return True
    else:
        print("\nВы проиграли...")
        return False

def treasure_room(player):
    print("\nКОМНАТА С СУНДУКОМ")
    print("Вы нашли сундук!")
    
    treasure_type = random.choice(["coins", "item", "both"])
    
    if treasure_type in ["coins", "both"]:
        coins = random.randint(20, 50) + player.level * 10
        player.coins += coins
        print(f"Найдено монет: {coins}")
    
    if treasure_type in ["item", "both"]:
        items = ["Малое зелье здоровья", "Среднее зелье здоровья", "Большое зелье здоровья", "Малое зелье силы", 
                 "Среднее зелье силы", "Большое зелье силы", "Малое зелье ловкости", "Среднее зелье ловкости",
                 "Большое зелье ловкости", "Малое зелье защиты", "Среднее зелье защиты", "Большое зелье защиты", 
                 "Волшебный меч", "Магический доспех", "Эльфийский лук"]
        item = random.choice(items)
        player.inventory.append(item)
        print(f"Найдено: {item}")
    
    print(f"Ваши монеты: {player.coins}")

    use = input("Хотите открыть инвентарь? (да/нет): ").lower()
    if use == "да":
        manage_inventory(player)


def rest_room(player):
    print("\nКОМНАТА ОТДЫХА")
    print("Здесь безопасно. Вы можете отдохнуть.")
       
    rest_amount = player.max_hp * 0.3
    player.heal(int(rest_amount))
    print(f"Вы восстановили {int(rest_amount)} HP")

    if player.coins > 100 and random.random() < 0.5:
        print(f"\nВы встретили торговца! Монет: {player.coins}")
        use = input("Xотите подойти? (да/нет): ").lower()  # возвращает заглавные буквы к строчным
        if use == "да":
            player.use_coins()
    
    if player.skill_points > 0:
        use = input("Хотите использовать очки прокачки? (да/нет): ").lower()
        if use == "да":
            player.use_skill_points()

    use = input("Хотите открыть инвентарь? (да/нет): ").lower()
    if use == "да":
        manage_inventory(player)

def manage_inventory(player):
    while True: 
        print("\nИНВЕНТАРЬ")
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
        print("4. Снять экиперованый предмет")
        print("5. Показать характеристики")
        print("6. Выйти")
        
        try:
            choice = int(input("Выберите действие: "))
            
            if choice == 1:
                if not player.inventory:
                    print("Инвентарь пуст!")
                    continue
                    
                idx = int(input("Номер предмета: ")) - 1
                if 0 <= idx < len(player.inventory):
                    item = player.inventory[idx]
                    if "зелье" in item:
                        if "здоровья" in item:
                            if "Малое" in item:
                                player.heal(20) 
                                print("Восстановлено 20 HP!")  
                            elif "Среднее" in item:
                                player.heal(50)
                                print("Восстановлено 50 HP!")
                            elif "Большое" in item:
                                player.hp = player.max_hp
                                print("HP полностью востанновлено!")
                        elif "силы" in item:
                            if "Малое" in item:
                                player.attack += 1
                                print("Атака увеличена на 1!")
                            elif "Среднее" in item:
                                player.attack += 2
                                print("Атака увеличена на 2!")
                            elif "Большое" in item:                            
                                player.attack += 5
                                print("Атака увеличена на 5!")
                        elif "защиты" in item:
                            if "Малое" in item:
                                player.defense += 1
                                print("Защита увеличена на 1!")
                            elif "Среднее" in item:
                                player.defense += 2
                                print("Защита увеличена на 2!")
                            elif "Большое" in item:                            
                                player.defense += 5
                                print("Защита увеличена на 5!")
                        elif "ловкости" in item:
                            if "Малое" in item:
                                player.agility += 1
                                print("Ловкость увеличена на 1!")
                            elif "Среднее" in item:
                                player.agility += 2
                                print("Ловкость увеличена на 2!")
                            elif "Большое" in item:                            
                                player.agility += 5
                                print("Ловкость увеличена на 5!")
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
                    use = (input(f"Вы уверены, что хотите удалить {player.inventory[idx].lower()}? (да/нет): ")).lower()
                    if use == "да":
                        removed = player.inventory.pop(idx) # удаление предмета
                        print(f"Выброшено: {removed}")
                    elif use == "нет":
                        continue
                    else:
                        print("ОШИБКА!")
                else:
                    print("ОШИБКА! Такого предмета нет")
                    
            elif choice == 3:
                if not player.inventory:
                    print("Инвентарь пуст!")
                    continue
                elif player.equipped["armor"] == None or player.equipped["weapon"] == None:                        
                    idx = int(input("Номер предмета: ")) - 1
                    if 0 <= idx < len(player.inventory):
                        item = player.inventory[idx]
                        if "меч" in item.lower() or "лук" in item.lower() or "оружие" in item.lower():
                            if player.equipped["weapon"] == None:
                                player.equipped["weapon"] = item
                                player.attack += 3
                                print(f"Экипировано оружие: {item}")
                            else:
                                print(f"У вас уже экиперовано оружие")
                        elif "доспех" in item.lower() or "броня" in item.lower():
                            if player.equipped["armor"] == None:
                                player.equipped["armor"] = item
                                player.defense += 3
                                print(f"Экипирована броня: {item}")
                            else:
                                print(f"У вас уже экиперована броня")    
                        else:
                            print("Это нельзя экипировать")
                else:
                    print("У вас уже есть экиперованые предметы")
                    continue

            elif choice == 4:
                if not player.equipped["armor"] == None or not player.equipped["weapon"] == None:
                    print("\nВыберите действие")   
                    print("1. Снять оружие")
                    print("2. Снять броню")
                    try:
                        ch = input("Ваш выбор: ")
                        if ch == 1:
                            if not player.equipped["weapon"] == None:
                                player.equipped["weapon"] == None
                                player.attack -= 3
                            else:
                                print("ОШИБКА! У вас нет оружия, которое можно удалить")
                        elif ch == 2:
                            if not player.equipped["armor"] == None:
                                player.equipped["armor"] == None
                                player.defense -= 3                            
                            else:
                                print("ОШИБКА! У вас нет брони, которую можно удалить")
                    except ValueError:
                        print("Введите число от 1 до 2")
                else:
                    print("У вас нет предметов, которые можно снять")                                        

            elif choice == 5:
                player.show_stats()

            elif choice == 6:
                break
            else:
                print("ОШИБКА!")
                
        except ValueError:
            print("Введите число от 1 до 4")

def main_game():
    print("Загрузка игры...")
    print("RPG. Добро пожаловать в подземелье!\n")
    
    player = create_character()
    current_floor = 1
    rooms_cleared = 0
    
    # Начальные предметы
    player.inventory.append("Малое зелье здоровья")
    player.inventory.append("Малое зелье силы")
    
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
        print("3. Выйти из игры")
        
        try:
            choice = int(input("Куда пойти? "))
            
            if choice == 1:
                selected_room = left_room
                print(f"\nВы идете налево...")
            elif choice == 2:
                selected_room = right_room
                print(f"\nВы идете направо...")
            elif choice == 3:
                print("Спасибо за игру!")
                break
            else:
                print("Ошибка!")
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
                print(f"\nВЫ СПУСТИЛИСЬ НА ЭТАЖ {current_floor}!")
                print("Враги стали сильнее!")
                player.heal(player.max_hp // 2) # На 50% HP
                print(f"Вы восстановили {player.max_hp // 2} HP")
                
        except ValueError:
            print("Введите число от 1 до 5")
    
    print(f"\nИГРА ОКОНЧЕНА")
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
    except Exception as e: # Если произошла ошибка любого стандартного типа (деление на ноль, отсутствие файла, синтаксические ошибки и т.д)
        print(f"Произошла ошибка: {e}")

