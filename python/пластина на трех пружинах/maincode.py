import socket # Модуль сетевого программирования
import time #Модуль для задержки по времени
import struct # Модуль работы с байтовым представлением
import numpy as np
from class_3dobject import Object3D
from class_3dobject import oscil
from class_3dobject import x1
from class_3dobject import x2
from class_3dobject import x3

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

a = Object3D()
b = Object3D()
k=10

dot = oscil()

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])
coord_const = dot[2]
speed_const = dot[3]
t = 0
number_form = 1

while True:    
    # a.move_abs(k*np.sin(i/k),k*np.sin(i/k),k*np.cos(i/k))
    a.coord_move(x1(t,number_form), x2(t,number_form), x3(t,number_form))
    b.coord_move(0, 0, 0)
    DAT=[1.0]
    DAT += a.form_udp()
    DAT += b.form_udp()
    buf = bytes() #создаем переменную - буфер
     # Заполняем буфер
    for val in DAT:
        buf += struct.pack('<d', val)

    sock.sendto(buf, (UDP_IP, UDP_PORT)) # Отправляем данные серверу
    time.sleep(0.05)#Задержка по времени в сек. для удобства отображения
    t += 0.05