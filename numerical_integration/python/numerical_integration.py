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
    
def create_grid_structure(num_x, num_y, num_z, spacing, spring_constant=100, rest_length=10):
    """
    Создает сетку узлов в 3D пространстве и автоматически определяет связи между соседними узлами.
    Также задает коэффициенты упругости и ненагруженные длины для каждой связи.

    Параметры:
    - num_x, num_y, num_z: количество узлов в каждом измерении.
    - spacing: расстояние между соседними узлами.
    - spring_constant: коэффициент упругости пружин между узлами.
    - rest_length: ненагруженная длина пружин между узлами.

    Возвращает:
    - objects: список объектов Object3D, представляющих узлы.
    - connections: список связей между узлами в формате (индекс1, индекс2).
    - spring_constants: список коэффициентов упругости для каждой связи.
    - rest_lengths: список ненагруженных длин для каждой связи.
    """
    objects = []
    connections = set()
    spring_constants = []
    rest_lengths = []

    # Создаем узлы
    for x in range(num_x):
        for y in range(num_y):
            for z in range(num_z):
                objects.append(Object3D(x=x*spacing+5, y=y*spacing+5, z=z*spacing+5))

    # Создаем связи
    for i, obj_i in enumerate(objects):
        for j, obj_j in enumerate(objects):
            if i != j and ((obj_i.x - obj_j.x)**2 + (obj_i.y - obj_j.y)**2 + (obj_i.z - obj_j.z)**2) == spacing**2:
                connection = tuple(sorted((i, j)))
                if connection not in connections:
                    connections.add(connection)
                    spring_constants.append(spring_constant)  # Для каждой связи задаем коэффициент упругости
                    rest_lengths.append(rest_length)  # и ненагруженную длину

    return objects, list(connections), spring_constants, rest_lengths
    
def apply_linear_constraint(objects, constraint):
    obj1, obj2, m, c, plane = constraint
    # Получаем начальные координаты
    x1, y1, z1 = objects[obj1].x, objects[obj1].y, objects[obj1].z
    x2, y2, z2 = objects[obj2].x, objects[obj2].y, objects[obj2].z
    
    if plane == 'XY':
        # Применяем ограничение в плоскости XY
        x_relative = x2 - x1
        y_target = m * x_relative + c
        objects[obj2].y = y1 + y_target
    elif plane == 'XZ':
        # Применяем ограничение в плоскости XZ
        x_relative = x2 - x1
        z_target = m * x_relative + c
        objects[obj2].z = z1 + z_target
    elif plane == 'YZ':
        # Применяем ограничение в плоскости YZ
        y_relative = y2 - y1
        z_target = m * y_relative + c
        objects[obj2].z = z1 + z_target
    elif plane == 'X':
            objects[obj2].x = objects[obj1].x
    elif plane == 'Y':
            objects[obj2].y = objects[obj1].y
    elif plane == 'Z':
            objects[obj2].z = objects[obj1].z

refresh_coord()
    
# object1 = Object3D(mass=1,x = 1, free_y = 0)
# object2 = Object3D(mass=1,x = 11, free_y = 0)
# object3 = Object3D(mass=1,x = 6, z = 9.66, free_y= 0)
# object4 = Object3D(mass=1,x = 6, z = 3.89, y = 10.16, free_x = 0, free_z = 0, free_y = 1, force_y = 100, freq = 19)
# objects = [object1, object2, object3, object4]  # Создаем два объекта
# connections = [(0, 1),(1,2),(0,2),(3,0),(3,1),(3,2)]  # Связываем их
# spring_constants = [100,100,100,100,100,100]  # Коэффициент упругости
# rest_lengths = [9,9,9,9,9,9]  # Ненагруженная длина пружины
# dt = 0.001  # Шаг времени
# time_animation = 0.01
# time_div = int(time_animation/dt)

# spring_objects = []

# object1 = Object3D(free_x = 0, free_y=0, free_z=0)
# object2 = Object3D(free_y=0, free_z=0, x = 3)
# object3 = Object3D(free_y=0, x = 5, z = 5)
# object4 = Object3D(free_y=0, x = 5, z = -5)
# object5 = Object3D(free_y=0, x = 0, z = 5)
# object6 = Object3D(free_y=0, x = 0, z = -5)
# object7 = Object3D(free_x=0, x = 5, z = 3, y = 3)
# objects = [object1, object2, object3, object4, object5, object6, object7]
# connections = [(0,1),(1,2),(1,3),(4,2),(5,3),(1,6)]
# constraints = [(0,1,0,0,'Y'),(1, 2, 0, 0, 'X'), (1, 3, 0, 0, 'X'),(2, 4, 0, 0,'Z'),(3, 5, 0, 0,'Z'),(1,6,1,0,'YZ'),(1,6,0,0,'X')]
spring_constants = [100]
rest_lengths = [10]
dt = 0.001
time_animation = 0.01
time_div = int(time_animation/dt)

spring_objects = []

objects, connections, spring_constants, rest_lengths = create_grid_structure(3, 3, 3, 10, 100, 10)

objects[10].force_y = 20
objects[10].freq = 15
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
        
        update_system(objects, connections, spring_constants, rest_lengths, dt, 0.1, timer)
        # for constraint in constraints:
        #     apply_linear_constraint(objects, constraint)
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