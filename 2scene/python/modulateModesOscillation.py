import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
from class_3dobject import Object3D, oscil

UDP_IP = "127.0.0.1"
UDP_PORT = 6501
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num_all = 200
# Определяем количество объектов по осям x и y
numObjX = 20
numObjY = 10  # Можно изменять для прямоугольной формы
numObj = numObjX * numObjY  # Общее количество объектов

objects = [Object3D() for _ in range(num_all)]

t = 0
mode_x = 3
mode_y = 3
x_len = numObjX - 1
y_len = numObjY - 1

for i, obj in enumerate(objects):
    obj.move_abs(-1000, -1000, -1000)
    
buf = bytes()
DAT = [1.0] + [data for obj in objects for data in obj.form_udp()]
sock.sendto(buf, (UDP_IP, UDP_PORT))

while True:
    index = 0
    for y_coord in range(numObjY):
        y_eq = y_coord * 2  # Умножение на 2 для соответствия с предыдущим подходом по y_coord
        for x_coord in range(numObjX):
            x_eq = x_coord*2
            if index < len(objects):  # Проверка, чтобы избежать выхода за пределы списка
                obj = objects[index]
                obj.move_abs(x_eq, np.sin(np.pi*x_coord*mode_x/x_len)*np.sin(np.pi*y_eq*mode_y/y_len) * np.sin(t), y_eq)
                index += 1

    # Собираем данные всех объектов
    DAT = [1.0] + [data for obj in objects for data in obj.form_udp()]
    
    buf = bytes()
    for val in DAT:
        buf += struct.pack('<d', val)
    sock.sendto(buf, (UDP_IP, UDP_PORT))
    time.sleep(0.05)
    t += 0.05
