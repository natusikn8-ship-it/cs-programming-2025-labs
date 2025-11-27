# Задание 1
numbers = [5, 8, 1, 10, 9, 2, 7, 4, 6, 3]
numbers[numbers.index(3)] = 30
print(numbers)

# Задание 2
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares) 

# Задание 3
numbers = [5, 1, 3, 4, 2]
print(max(numbers)/len(numbers))

# Задание 4
numbers = (True, 2, "hello", 1.34)
if not all(isinstance(x, (int, float)) for x in numbers): # Проверяет тип переменных
    print(numbers)
else:
    print(tuple(sorted(numbers)))

# Задание 5
prices = {"яблоко": 100, "банан": 80, "груша": 120}
cheapest = min(prices, key=prices.get) # Получает значение по ключу
print("Самый дешевый товар:", cheapest)

# Задание 6
list = [1, "hello", 3.14, True, (1, 2)]
result = dict(zip(list, list)) 
print(result)

# Задание 7
prices = {"apple": "яблоко", "pear": "груша", "banana": "банан"}
word = input("Введите русское слово: ")
translation = {value: key for key, value in prices.items()} # Возвращает к виду ключ-значение
print(translation.get(word, "Перевод не найден"))

# Задание 8
import random
list = ["камень", "ножницы", "бумага", "ящерица", "спок"]
win = {
    "камень": ["ножницы", "ящерица"],
    "ножницы": ["бумага", "ящерица"],
    "бумага": ["камень", "спок"],
    "ящерица": ["спок", "бумага"],
    "спок": ["камень", "ножницы"]
}
a = input(f"Введите свой выбор:")
b = random.choice(list) 
print(f"Ваш выбор: {a}")
print(f"Выбор компьютера: {b}")
if a == b:
    print("Ничья")
elif a in win and b in win[a]:
    print("Вы победили")
else:
    print("Вы проиграли")

# Задание 9
fruits = ["яблоко", "груша", "банан", "киви", "апельсин", "ананас"]
result = { }
for fruit in fruits:
    result.setdefault(fruit[0], [ ]).append(fruit) # проверяется есть ли уже ключ в списке, добавляет переменную
print(result)

# Задание 10
students = [("Анна", [5, 4, 5]), ("Иван", [3, 4, 4]), ("Мария", [5, 5, 5])]
grades = {name: sum(grades)/len(grades) for name, grades in students}
first = max(grades, key=grades.get)
print(f"{first} имеет наивысший средний балл: {grades[first]}")