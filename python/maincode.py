import socket # Модуль сетевого программирования
import time #Модуль для задержки по времени
import struct # Модуль работы с байтовым представлением
import numpy as np
import matplotlib.pyplot as plt
from class_3dobject import Object3D
from class_3dobject import pandelum

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
pandel = pandelum()
theta = np.pi - np.pi/3  # Начальный угол отклонения
omega = 0  # Начальная угловая скорость\
dt = 0.01
l = 10
theta_arg = []
omega_arg = []
for i in range(10000):
    theta, omega = pandel.rk4_step(theta, omega, dt)
    theta_arg.append(theta)
    omega_arg.append(omega)    
    a.move_abs(l*np.cos(theta),0,l*np.sin(theta))
    DAT=[1.0]
    DAT += a.form_udp()
    buf = bytes() #создаем переменную - буфер
     # Заполняем буфер
    for val in DAT:
        buf += struct.pack('<d', val)

    sock.sendto(buf, (UDP_IP, UDP_PORT)) # Отправляем данные серверу
    time.sleep(0.001)#Задержка по времени в сек. для удобства отображения

plt.plot(theta_arg, omega_arg, label='sin(x)')  # Построение графика y=sin(x)
plt.xlabel('x')  # Установка подписи для оси x
plt.ylabel('y')  # Установка подписи для оси y
plt.title('График функции sin(x)')  # Установка заголовка графика
plt.legend()  # Вывод легенды
plt.grid(True)  # Включение сетки
plt.show()  # Показать график