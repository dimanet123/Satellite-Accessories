import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
from class_3dobject import Object3D, oscil

UDP_IP = "127.0.0.1"
UDP_PORT = 6501
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

n_masses = 3 
objects = [Object3D() for _ in range(n_masses)]  # Создаем 7 объектов Object3D

dimensions = 3  

# Массы
masses = [1.0,1,1]

# Соединения и жёсткости пружин: (масса 1, масса 2, жёсткость)
springs = [(0, 1, 100), (1, 2, 100), (2, 0, 100)]


dot = oscil(n_masses,dimensions,masses,springs)

t = 0
number_form = 6

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])


def x(t, number_form,num_func):
    return matrix_form[num_func - 1,number_form] * np.cos(eigenvalues[number_form]*t)

while True:
    for i, obj in enumerate(objects):
        offset = [5, -5, 5, -5, 5, -5]  # Пример смещения для разных объектов
        if i < len(offset):
            delta = offset[i]
        else:
            delta = 0
        obj.move_abs(x(t, number_form - 1, 3*i + 1) + delta, x(t, number_form - 1, 3*i + 2) + delta, x(t, number_form - 1, 3*i + 3) + delta)

    # Собираем данные всех объектов
    DAT = [1.0] + [data for obj in objects for data in obj.form_udp()]

    # Упаковываем и отправляем данные
    buf = bytes()
    for val in DAT:
        buf += struct.pack('<d', val)
    sock.sendto(buf, (UDP_IP, UDP_PORT))
    time.sleep(0.05)
    t += 0.05