import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
from class_3dobject import Object3D, oscil


def recieve_UDP(UDP_IP = "127.0.0.1", UDP_PORT_RECIEVE = 6502):
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock1.bind((UDP_IP, UDP_PORT_RECIEVE))
    data, addr = sock1.recvfrom(1024)
    print(f"Получены данные от {addr}")

    # Распаковываем полученные данные
    # '<d' означает little-endian double precision float
    # Количество элементов в зависимости от размера полученного сообщения
    values = struct.unpack('<' + 'd'*(len(data)//8), data)
    sock1.close()
    print(values)
    return values

def send_UDP(UDP_IP = "127.0.0.1", UDP_PORT_SEND = 6501, DAT=[0]):
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Упаковываем и отправляем данные
    buf = bytes()
    for val in DAT:
        buf += struct.pack('<d', val)
    sock2.sendto(buf, (UDP_IP, UDP_PORT_SEND))
    sock2.close()
  
UDP_IP = "127.0.0.1"    
UDP_PORT_RECIEVE = 6502
UDP_PORT_SEND = 6501


# n_masses = 3 
# objects = [Object3D() for _ in range(n_masses)]  # Создаем 7 объектов Object3D

# dimensions = 3  

# # Массы
# masses = [1.0,1,1]

# # Соединения и жёсткости пружин: (масса 1, масса 2, жёсткость)
# springs = [(0, 1, 100), (1, 2, 100), (2, 0, 100)]


# dot = oscil(n_masses,dimensions,masses,springs)

t = 0
# number_form = 6

# matrix_form = dot[0]
# eigenvalues = np.sqrt(dot[1])


# def x(t, number_form,num_func):
#     return matrix_form[num_func - 1,number_form] * np.cos(eigenvalues[number_form]*t)

while True:
    data_recieve = recieve_UDP()
    # Собираем данные всех объектов
    DAT = [np.sin(t)] 
    send_UDP(DAT=DAT)
    time.sleep(0.05)
    t += 0.05