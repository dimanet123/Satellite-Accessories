import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import sys
import threading

sys.path.insert(0, '../../python_classes/')

from class_3dobject import Object3D, oscil, Spring


UDP_IP = "127.0.0.1"
UDP_PORT = 6501
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

n_masses = 4 
objects = [Object3D() for _ in range(n_masses)]  # Создаем 7 объектов Object3D

dimensions = 3  
spring_objects = []


# Массы
masses = [1,1,1,1]

# Соединения и жёсткости пружин: (масса 1, масса 2, жёсткость)

springs = [(0, 1, 100), (0, 2, 100), (1, 2, 100), (0, 3, 100),(2, 3, 100),(1, 3, 100)]

for spring in range(len(springs)):
    spring_objects.append(Spring())

dot = oscil(n_masses,dimensions,masses,springs)

start_height = 7
t = 0
number_form = 12

def send_udp_data(DAT):
    # Упаковываем массив данных в байты
    buf = struct.pack('<' + 'd' * len(DAT), *DAT)
    # Отправляем упакованные данные
    sock.sendto(buf, (UDP_IP, UDP_PORT))
    
def listen_for_input():
    global number_form
    while True:
        try:
            # Чтение нового значения из консоли
            number_form = input("Введите номер формы собственных колебаний: ")
            number_form = int(number_form)
            if number_form < 1 or number_form > (dimensions * n_masses):
                number_form = 10
            
        except ValueError:
            print("Пожалуйста, введите корректное числовое значение.")

listener_thread = threading.Thread(target=listen_for_input)
listener_thread.daemon = True  # Позволяет программе завершиться, даже если поток активен
listener_thread.start()

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])

default_offset = 4


def x(t, number_form,num_func):
    return matrix_form[num_func - 1,number_form] * np.cos(eigenvalues[number_form]*t)

while True:
    for i, obj in enumerate(objects):
        offset = [[0,0,0],[0,0,default_offset],[0,0,-default_offset],[-default_offset,0,0],[default_offset, 0, 0],[default_offset,default_offset,0],[default_offset,-default_offset,0]]  # Пример смещения для разных объектов
        if i < len(offset):
            delta = offset[i]
        else:
            delta = 0
        obj.x = float(x(t, number_form - 1, 3*i + 1) + delta[0]) 
        obj.y = float(x(t, number_form - 1, 3*i + 2) + delta[1] + start_height)
        obj.z = float(x(t, number_form - 1, 3*i + 3) + delta[2])
    
    for i, (num1, num2, num3) in enumerate(springs):
        spring_objects[i].x1, spring_objects[i].y1, spring_objects[i].z1 = objects[num1].x, objects[num1].y, objects[num1].z
        spring_objects[i].x2, spring_objects[i].y2, spring_objects[i].z2 = objects[num2].x, objects[num2].y, objects[num2].z
    # Собираем данные всех объектов
    DAT = [0]
    for obj in objects:
        DAT += obj.form_udp()
    
    for spring in spring_objects:
        DAT += spring.form_udp()

    # Упаковываем и отправляем данные
    send_udp_data(DAT)
    time.sleep(0.05)
    t += 0.05

