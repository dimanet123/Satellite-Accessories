import tkinter as tk
from tkinter import messagebox
import sys
import threading
import socket
import struct
import numpy as np
import sys
import time
sys.path.append('generate_scene/')
sys.path.append('2_scene/')
sys.path.append('3_scene/')
sys.path.insert(0, 'python_classes/')
from class_3dobject import Object3D, oscil, Spring
from thread_controller import ThreadController



from generate_scene import generate_complete_file  # Убедитесь, что ваш скрипт находится в той же директории, что и GUI
from mode_shapes import simulate_oscillation_control
from base_struct import scene_3_1
from tetriedr import scene_3_2
from policube import scene_3_3

def on_generate():
    try:
        n_cubes = int(entry_cubes.get())
        n_springs = int(entry_springs.get())
        n_arrows = int(entry_arrows.get())
        generate_complete_file(n_cubes, n_springs, n_arrows)
        messagebox.showinfo("Успешно", "Сцена успешно сгенерирована!")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")

root = tk.Tk()
root.title("Комплексный Генератор Сцен")

# Создаем фрейм для генерации сцены и другие фреймы по необходимости
scene_generation_frame = tk.LabelFrame(root, text="Генерация Сцены", padx=10, pady=10)
scene_generation_frame.pack(padx=10, pady=10, fill="both", expand="yes")

second_scene_frame = tk.LabelFrame(root, text="Вторая сцена", padx=10, pady=10)
second_scene_frame.pack(padx=10, pady=10, fill="both", expand="yes")

third_scene_frame = tk.LabelFrame(root, text="Третья сцена", padx=10, pady=10)
third_scene_frame.pack(padx=10, pady=10, fill="both", expand="yes")

third_scene_frame_1 = tk.LabelFrame(third_scene_frame, text="УММ КА", padx=10, pady=10)
third_scene_frame_1.pack(padx=10, pady=10, fill="both", expand="yes")

third_scene_frame_2 = tk.LabelFrame(third_scene_frame, text="Тетраэдр", padx=10, pady=10)
third_scene_frame_2.pack(padx=10, pady=10, fill="both", expand="yes")

third_scene_frame_3 = tk.LabelFrame(third_scene_frame, text="Пространственный куб", padx=10, pady=10)
third_scene_frame_3.pack(padx=10, pady=10, fill="both", expand="yes")

# Теперь добавляем виджеты в фрейм scene_generation_frame вместо корня
tk.Label(scene_generation_frame, text="Кубы:").grid(row=0, column=0, sticky="w")
entry_cubes = tk.Entry(scene_generation_frame)
entry_cubes.grid(row=0, column=1)

tk.Label(scene_generation_frame, text="Пружины:").grid(row=1, column=0, sticky="w")
entry_springs = tk.Entry(scene_generation_frame)
entry_springs.grid(row=1, column=1)

tk.Label(scene_generation_frame, text="Стрелки:").grid(row=2, column=0, sticky="w")
entry_arrows = tk.Entry(scene_generation_frame)
entry_arrows.grid(row=2, column=1)

tk.Label(second_scene_frame, text="Номер форм колебаний:").grid(row=1, column=0, sticky="w")
entry_num_form = tk.Entry(second_scene_frame)
entry_num_form.grid(row=1, column=1)

tk.Label(third_scene_frame_2, text="Сила воздействия").grid(row=1, column=0, sticky="w")
entry_force_1 = tk.Entry(third_scene_frame_2)
entry_force_1.grid(row=1, column=1)

tk.Label(third_scene_frame_2, text="Частота силы").grid(row=2, column=0, sticky="w")
entry_freq_1 = tk.Entry(third_scene_frame_2)
entry_freq_1.grid(row=2, column=1)

tk.Label(third_scene_frame_3, text="Сила воздействия").grid(row=1, column=0, sticky="w")
entry_force_2 = tk.Entry(third_scene_frame_3)
entry_force_2.grid(row=1, column=1)

tk.Label(third_scene_frame_3, text="Частота силы").grid(row=2, column=0, sticky="w")
entry_freq_2 = tk.Entry(third_scene_frame_3)
entry_freq_2.grid(row=2, column=1)

generate_button = tk.Button(scene_generation_frame, text="Сгенерировать", command=on_generate)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)


thread_2_scene = ThreadController()
thread_3_scene = ThreadController()
thread_4_scene = ThreadController()
thread_5_scene = ThreadController()


def start_scene_2():
    thread_2_scene.run(simulate_oscillation_control, args=(int(entry_num_form.get()), thread_2_scene.control_event))

def stop_scene_2():
    global control_event
    thread_2_scene.stop()
    
def start_scene_3_1():
    thread_3_scene.run(scene_3_1, args=(thread_3_scene.control_event,))
    
def stop_scene_3_1():
    global control_event
    thread_3_scene.stop()
    
def start_scene_3_2():
    thread_4_scene.run(scene_3_2, args=(float(entry_force_1.get()), float(entry_freq_1.get()), thread_4_scene.control_event))
    
def stop_scene_3_2():
    global control_event
    thread_4_scene.stop()
    
def start_scene_3_3():
    thread_5_scene.run(scene_3_3, args=(float(entry_force_2.get()), float(entry_freq_2.get()), thread_5_scene.control_event))
    
def stop_scene_3_3():
    global control_event
    thread_5_scene.stop()
    
start_button = tk.Button(second_scene_frame, text="Старт", command=start_scene_2)
start_button.grid(row=2, column=1)

stop_button = tk.Button(second_scene_frame, text="Стоп", command=stop_scene_2)
stop_button.grid(row=2, column=2)

start_button_3_1 = tk.Button(third_scene_frame_1, text="Старт", command=start_scene_3_1)
start_button_3_1.grid(row=2, column=1)

stop_button_3_1 = tk.Button(third_scene_frame_1, text="Стоп", command=stop_scene_3_1)
stop_button_3_1.grid(row=2, column=2)

start_button_3_2 = tk.Button(third_scene_frame_2, text="Старт", command=start_scene_3_2)
start_button_3_2.grid(row=3, column=1)

stop_button_3_2 = tk.Button(third_scene_frame_2, text="Стоп", command=stop_scene_3_2)
stop_button_3_2.grid(row=3, column=2)

start_button_3_3 = tk.Button(third_scene_frame_3, text="Старт", command=start_scene_3_3)
start_button_3_3.grid(row=3, column=1)

stop_button_3_3 = tk.Button(third_scene_frame_3, text="Стоп", command=stop_scene_3_3)
stop_button_3_3.grid(row=3, column=2)

# Если вам нужны другие разделы, просто создайте для них свои фреймы по аналогии с scene_generation_frame

root.mainloop()
