import threading
import socket
import struct
import numpy as np
import sys
import time

sys.path.insert(0, '../../python_classes/')
from class_3dobject import Object3D, oscil, Spring

# Глобальная переменная для управления состоянием симуляции




def simulate_oscillation_control(number_form, control_event):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 6501
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    n_masses = 7 
    objects = [Object3D() for _ in range(n_masses)]
    dimensions = 3
    if number_form > n_masses * dimensions:
        number_form = 10
    spring_objects = []
    masses = [1000, 10, 10, 10, 100, 50, 50]
    springs = [(0, 1, 100), (0, 2, 100), (0, 3, 100), (0, 4, 100),(4, 5, 100),(4, 6, 100)]

    for _ in springs:
        spring_objects.append(Spring())

    dot = oscil(n_masses, dimensions, masses, springs)
    matrix_form = dot[0]
    eigenvalues = np.sqrt(dot[1])
    start_height = 7
    t = 0
    default_offset = 2

    def x(t, form, func):
        return matrix_form[func - 1, form] * np.cos(eigenvalues[form] * t)

    while not control_event.is_set():
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
            
        print('Отправка UDP')
        def send_udp_data(DAT):
            # Упаковываем массив данных в байты
            buf = struct.pack('<' + 'd' * len(DAT), *DAT)
            # Отправляем упакованные данные
            sock.sendto(buf, (UDP_IP, UDP_PORT))

        # Упаковываем и отправляем данные
        send_udp_data(DAT)
            
        
        if control_event.is_set():
            break

        time.sleep(0.05)
        t += 0.05

# Создаем событие для управления потоком

