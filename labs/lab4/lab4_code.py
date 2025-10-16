#Задание 1
temperature = float(input("Введите температуру в комнате: "))
if temperature >= 20:
    print(f"Температура {temperature}°C - Кондиционер: ВЫКЛЮЧЕН")
else:
    print(f"Температура {temperature}°C - Кондиционер: ВКЛЮЧЕН")

#Задание 2
month = int(input("Введите номер месяца от 1 до 12: "))   
if 1 <= month <= 12:
    if month in [12, 1, 2]:
        x = "Зима"
    elif month in [3, 4, 5]:
        x = "Весна"
    elif month in [6, 7, 8]:
        x = "Лето"
    elif month in [9, 10, 11]:
        x = "Осень"
        print(f"Месяц {month} относится к сезону: {x}")
else:
         print("Ошибка! Ввежите число от 1 до 12")
        