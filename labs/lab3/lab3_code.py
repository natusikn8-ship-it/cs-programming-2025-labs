#задание 1
name = input ("введите ваше имя:")
age = input ("введите ваш возраст:")
for a in range (10):
    print(f"Меня зовут {name} и мне {age} лет")

#задание 2
x = int(input("число от 1 до 9")) 
for i in range (1, 11):
    print (f"{x} * {i} = {x*i}")

#задание 3
for x in range (1, 101,3):
    print(x)

#задание 4
x = int(input("введите число:"))
i = 1
for y in range (1, x+1):
    i = i * y
print (f"факториал числа {x} равен {i} ")

#Задание 5
count = 20
while count >= 0:
    print(count)
    count -= 1  # уменьшаем на 1

#задание 6
limit = int(input("Введите число: "))
a, b = 0, 1
print(f"Числа Фибоначчи до {limit} :")
while a <= limit:
    print(a)
    x = b
    b = b + a
    a = x

#задание 7
original = input("Введите строку: ")
result = ""
for i in range(len(original)):
    ch = original[i]
    result += ch + str(i + 1)
print("Результат:", result) 

##задание 8
while True:
    x = input("Введите два числа через пробел: ")
    a, b = x.split()
    s = int(a) + int(b)
    print(f"Сумма равна: {s}")
    print ()
    