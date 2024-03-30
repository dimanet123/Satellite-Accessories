import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../python_classes/')
from class_3dobject import Object3D, calculate_force, update_system, Spring

UDP_IP = "127.0.0.1"
UDP_PORT = 6501
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
num_all = 27
objects = [Object3D() for _ in range(num_all)]

def send_udp_data(DAT):
    # Упаковываем массив данных в байты
    buf = struct.pack('<' + 'd' * len(DAT), *DAT)
    # Отправляем упакованные данные
    sock.sendto(buf, (UDP_IP, UDP_PORT))
    
def refresh_coord():
    for i, obj in enumerate(objects):
        obj.x = -1000
        obj.y = -1000
        obj.z = -1000
    buf = bytes()
    
    DAT = [1.0] + [data for obj in objects for data in obj.form_udp()]
    for val in DAT:
        buf += struct.pack('<d', val)
    sock.sendto(buf, (UDP_IP, UDP_PORT))

refresh_coord()
    
object1 = Object3D(mass=1,x = 1, free_y = 0)
object2 = Object3D(mass=1,x = 11, free_y = 0)
object3 = Object3D(mass=1,x = 6, z = 9.66, free_y= 0)
object4 = Object3D(mass=1,x = 6, z = 3.89, y = 10.16, free_x = 0, free_z = 0, free_y = 1, force_y = 100, freq = 19)
objects = [object1, object2, object3, object4]  # Создаем два объекта
connections = [(0, 1),(1,2),(0,2),(3,0),(3,1),(3,2)]  # Связываем их
spring_constants = [100,100,100,100,100,100]  # Коэффициент упругости
rest_lengths = [9,9,9,9,9,9]  # Ненагруженная длина пружины
dt = 0.001  # Шаг времени
time_animation = 0.01
time_div = int(time_animation/dt)

spring_objects = []

for spring in range(len(connections)):
    spring_objects.append(Spring())



def calculate_total_energy(objects, connections, spring_constants, rest_lengths):
    total_kinetic_energy = sum(0.5 * obj.mass * (obj.vx**2 + obj.vy**2 + obj.vz**2) for obj in objects)
    total_potential_energy = sum(0.5 * k * (np.sqrt((objects[i].x - objects[j].x)**2 + (objects[i].y - objects[j].y)**2 + (objects[i].z - objects[j].z)**2) - l)**2 for (i, j), k, l in zip(connections, spring_constants, rest_lengths))
    return total_kinetic_energy + total_potential_energy

# def create_cube(width, height, depth, mass=1, spring_constant=10, rest_length=10):
#     objects = []
#     connections = []
#     spring_constants = []
#     rest_lengths = []

#     # Генерируем грузы
#     for x in [0, width]:
#         for y in [0, height]:
#             for z in [0, depth]:
#                 objects.append(Object3D(mass=mass, x=x, y=y, z=z))

#     # Генерируем связи
#     for i, obj_i in enumerate(objects):
#         for j, obj_j in enumerate(objects):
#             if i < j:  # Чтобы не создавать дубликаты связей
#                 distance = np.sqrt((obj_i.x - obj_j.x)**2 + (obj_i.y - obj_j.y)**2 + (obj_i.z - obj_j.z)**2)
#                 connections.append((i, j))
#                 spring_constants.append(spring_constant)
#                 rest_lengths.append(rest_length)

#     return objects, connections, spring_constants, rest_lengths

# objects, connections, spring_constants, rest_lengths = create_cube(width=3, height=3, depth=3, mass=1, spring_constant=10, rest_length=4)

# Обновляем систему


# Выводим новые положения и скорости объектов
for obj in objects:
    print(obj)
    
timer = 0

while True:
    start_time = time.time()
        
    for i in range(time_div):
        update_system(objects, connections, spring_constants, rest_lengths, dt, 1, timer)
        timer += dt
    
    for i, (num1, num2) in enumerate(connections):
        spring_objects[i].x1, spring_objects[i].y1, spring_objects[i].z1 = objects[num1].x, objects[num1].y, objects[num1].z
        spring_objects[i].x2, spring_objects[i].y2, spring_objects[i].z2 = objects[num2].x, objects[num2].y, objects[num2].z
    # Ваш код здесь
    end_time = time.time()
    time_dif = end_time - start_time
    print(f'{time_div},{time_dif}')
    print(f'Энергия системы грузов: {calculate_total_energy(objects, connections, spring_constants, rest_lengths)} Дж')
    DAT = [0]
    for obj in objects:
        DAT += obj.form_udp()
    
    for spring in spring_objects:
        DAT += spring.form_udp()
    
    send_udp_data(DAT)
    # for obj in objects:
    #     print(obj)

    
    time.sleep(time_animation)