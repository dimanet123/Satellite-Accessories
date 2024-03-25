import socket # Модуль сетевого программирования
import time #Модуль для задержки по времени
import struct # Модуль работы с байтовым представлением
import numpy as np
import matplotlib.pyplot as plt
from class_3dobject import Object3D
from class_3dobject import pandelum
from class_3dobject import RungeKuttaSolver
from class_3dobject import oscil
from class_3dobject import x


print("Start TEST!") # Тестовое сообщение о старте программы
# Конфигурация сервера UDP
UDP_IP = "127.0.0.1" #IP Адрес сетевого подключения
UDP_PORT = 6501 # Порт сетевого подключения

print("UDP_START!!!") # Тестовое сообщение о старте канала связи UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Создаём сокет
# Реализация алгоритма управления 3D-моделью
# Тестовый пример - смещение в цикле по шагам
DAT=[1.0] #Датаграмма из 4х чисел с плавающей точкой
MAXSTEPS=200 #Максимальное число шагов
#Цикл по шагам

aba = Object3D()
aba2 = Object3D()
aba3 = Object3D()
aba4 = Object3D()
aba5 = Object3D()
aba6 = Object3D()
aba7 = Object3D()
dot = oscil()

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])
# coord_const = dot[2]
# speed_const = dot[3]
pandel = pandelum()
theta = np.pi  # Начальный угол отклонения
omega = 0  # Начальная угловая скорость\
dt = 0.01
l = 10
theta_arg = []
omega_arg = []

# Параметры
a = 0.1
b = 0
d = 0.01
f = 0.1
dt = 0.01

# Начальные условия
t0 = 0.0
u1_0 = 0.0  # Начальное значение y
u2_0 = 0.1  # Начальное значение y'
v1_0 = 0  # Начальное значение phi
v2_0 = 0.0  # Начальное значение phi'

# Общее время моделирования
T = 10.0

# Создание экземпляра класса RungeKuttaSolver
solver = RungeKuttaSolver(a, b, d, f, dt)

# Цикл для вызова метода solve() извне класса
t_values_all = []
u1_values_all = []
u2_values_all = []
v1_values_all = []
v2_values_all = []
t = 0
dat = oscil()
number_form = 4

while True:
    aba.move_abs(x(t, number_form - 1,1), x(t, number_form - 1,2) ,x(t, number_form - 1,3))
    aba2.move_abs(x(t, number_form - 1,4)+5, x(t, number_form - 1,5) ,x(t, number_form - 1,6))
    aba3.move_abs(x(t, number_form - 1,7)-5, x(t, number_form - 1,8) ,x(t, number_form - 1,9))
    aba4.move_abs(x(t, number_form - 1,10), x(t, number_form - 1,11) + 5,x(t, number_form - 1,12))
    aba5.move_abs(x(t, number_form - 1,13), x(t, number_form - 1,14) - 5,x(t, number_form - 1,15))
    aba6.move_abs(x(t, number_form - 1,16), x(t, number_form - 1,17) ,x(t, number_form - 1,18) + 5)
    aba7.move_abs(x(t, number_form - 1,19), x(t, number_form - 1,20) ,x(t, number_form - 1,21) - 5)
    
    DAT=[1.0]

    DAT += aba.form_udp()
    DAT += aba2.form_udp()
    DAT += aba3.form_udp()
    DAT += aba4.form_udp()
    DAT += aba5.form_udp()
    DAT += aba6.form_udp()
    DAT += aba7.form_udp()




     # Пакуем данные val в байты функцией struct.pack('<d', val)
     # '<d' - это метод упаковки: порядок little-endian - от младшего байта кстаршему
     # тип данных - числа с плавающей точкой double диной 8 байт или массивтаких чисел
     # Подробнее упаковку структур см. https://tirinox.ru/python-struct/

     #Вариант с кодированием параметров из списка
    buf = bytes() #создаем переменную - буфер
     # Заполняем буфер
    for val in DAT:
        buf += struct.pack('<d', val)

    sock.sendto(buf, (UDP_IP, UDP_PORT)) # Отправляем данные серверу
    time.sleep(0.05)#Задержка по времени в сек. для удобства отображения
    t += 0.05