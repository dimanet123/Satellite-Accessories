import socket # Модуль сетевого программирования
import time #Модуль для задержки по времени
import struct # Модуль работы с байтовым представлением
import numpy as np
from class_3dobject import Object3D

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

def transform_from_triangle(obj, point_a, point_b, point_c):
# Находим центр масс треугольника
    center_x = (point_a[0] + point_b[0] + point_c[0]) / 3
    center_y = (point_a[1] + point_b[1] + point_c[1]) / 3
    center_z = (point_a[2] + point_b[2] + point_c[2]) / 3
    
    # Вычисляем смещение объекта относительно его начальной позиции
    delta_x = center_x - obj.x
    delta_y = center_y - obj.y
    delta_z = center_z - obj.z
    obj.move(delta_x, delta_y, delta_z)
    
    # Вычисляем углы поворота объекта относительно его начальной позиции
    ab = np.array([point_b[0] - point_a[0], point_b[1] - point_a[1], point_b[2] - point_a[2]])
    bc = np.array([point_c[0] - point_b[0], point_c[1] - point_b[1], point_c[2] - point_b[2]])
    
    # Находим векторное произведение
    cross_product = np.cross(ab, bc)
    norm = np.linalg.norm(cross_product)
    
    # Нормализуем векторное произведение
    if norm != 0:
        rotation_x = np.arcsin(cross_product[2] / norm)
        rotation_y = np.arcsin(cross_product[0] / norm)
        rotation_z = np.arcsin(cross_product[1] / norm)
        obj.rotate(rotation_x, rotation_y, rotation_z)

a = Object3D()
a.move(0,0,0)
for i in range(1):
    point_a = [1, 0, 0]
    point_b = [0, 1, 0]
    point_c = [0, 0, 1]
    DAT=[1.0]
    # a.rotate(0.5, 0.5, 0.5)
    # k = 0.01
    # a.move(k * np.sin(i),k * np.sin(i),k * np.sin(i))
    
    transform_from_triangle(a, point_a, point_b, point_c)

    DAT += a.form_udp()


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
    time.sleep(0.01)#Задержка по времени в сек. для удобства отображения