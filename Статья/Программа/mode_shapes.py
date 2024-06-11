from vpython import *
import numpy as np

# Конфигурация модели
n_masses = 4
masses = [0.15, 0.15, 0.15, 0.15]
stiffness = [100, 100, 100, 100]
natural_lengths = [0.2 for _ in range(len(stiffness) + 1)]  # Уменьшенная длина
dt = 0.001
t_max = 5

# Предварительный расчет колебаний (пример из второго блока)
freq = np.array([1.0, 1.5, 2.0, 2.5])
mode_shape = np.random.rand(n_masses, n_masses)  # Случайная матрица форм мод

# Создание сцены в VPython
scene = canvas(title='Mass-Spring System', width=800, height=600)

# Создание масс (кубов) и пружин
mass_objects = []
spring_objects = []
initial_pos = vector(-n_masses / 2 * natural_lengths[0], 0, 0)  # Центрирование объектов

for i in range(n_masses):
    mass_objects.append(box(pos=initial_pos + vector(i * natural_lengths[0], 0, 0), size=vector(0.05, 0.05, 0.05), color=color.blue))
    if i > 0:
        spring_objects.append(helix(pos=mass_objects[i - 1].pos + vector(0.05/2, 0, 0), axis=mass_objects[i].pos - mass_objects[i - 1].pos - vector(0.05, 0, 0), radius=0.005, coils=20, thickness=0.002))

# Основной цикл анимации
t = 0
while t < t_max:
    rate(100)
    for n_form in range(n_masses):
        # Расчет новых положений
        displacements = mode_shape[:, n_form] * np.sin(2 * np.pi * freq[n_form] * t) * 0.1
        for j in range(n_masses):
            mass_objects[j].pos = initial_pos + vector(j * natural_lengths[0], 0, 0) + vector(displacements[j], 0, 0)
            if j > 0:
                spring_objects[j - 1].axis = mass_objects[j].pos - mass_objects[j - 1].pos - vector(0.05, 0, 0)
    t += dt
