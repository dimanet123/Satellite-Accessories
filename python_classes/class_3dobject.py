import numpy as np

class Object3D:
    def __init__(self, x=0, y=0, z=0, rotation_x=0, rotation_y=0, rotation_z=0, mass=1, free_x = 1, free_y = 1, free_z = 1, force_x = 0, force_y = 0, force_z = 0, freq = 1):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0  # скорость по x
        self.vy = 0  # скорость по y
        self.vz = 0  # скорость по z
        self.v = 0
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.mass = mass  # масса объекта
        self.free_x = free_x
        self.free_y = free_y
        self.free_z = free_z
        self.force_x = force_x
        self.force_y = force_y
        self.force_z = force_z
        self.freq = freq
        
        
    def update_velocity_and_position_RK(self, ax, ay, az, dt):
        # Начальные скорости и положения
        vx0, vy0, vz0 = self.vx, self.vy, self.vz
        x0, y0, z0 = self.x, self.y, self.z

        # Вычисляем промежуточные значения для скорости и положения
        k1_vx, k1_vy, k1_vz = ax * dt, ay * dt, az * dt
        k1_x, k1_y, k1_z = vx0 * dt, vy0 * dt, vz0 * dt

        k2_vx, k2_vy, k2_vz = (ax * dt, ay * dt, az * dt)
        k2_x, k2_y, k2_z = (vx0 + k1_vx/2) * dt, (vy0 + k1_vy/2) * dt, (vz0 + k1_vz/2) * dt

        k3_vx, k3_vy, k3_vz = (ax * dt, ay * dt, az * dt)
        k3_x, k3_y, k3_z = (vx0 + k2_vx/2) * dt, (vy0 + k2_vy/2) * dt, (vz0 + k2_vz/2) * dt

        k4_vx, k4_vy, k4_vz = (ax * dt, ay * dt, az * dt)
        k4_x, k4_y, k4_z = (vx0 + k3_vx) * dt, (vy0 + k3_vy) * dt, (vz0 + k3_vz) * dt

        # Итоговые скорость и положение, обновленные с использованием метода Рунге-Кутта 4-го порядка
        self.vx += (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx) / 6
        self.vy += (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy) / 6
        self.vz += (k1_vz + 2*k2_vz + 2*k3_vz + k4_vz) / 6
        self.v = np.sqrt(self.vx**2 + self.vy**2 + self.vz**2)

        self.x += (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        self.y += (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
        self.z += (k1_z + 2*k2_z + 2*k3_z + k4_z) / 6
        
    
    def update_velocity_and_position_Verle(self, ax, ay, az, dt):
        # Сохраняем предыдущие положения
        if not hasattr(self, 'prev_x'):
            self.prev_x, self.prev_y, self.prev_z = self.x, self.y, self.z

        # Вычисляем следующие положения используя метод Верле
        next_x = 2*self.x - self.prev_x + ax*dt**2
        next_y = 2*self.y - self.prev_y + ay*dt**2
        next_z = 2*self.z - self.prev_z + az*dt**2

        # Обновляем скорости
        self.vx = (next_x - self.prev_x) / (2*dt)
        self.vy = (next_y - self.prev_y) / (2*dt)
        self.vz = (next_z - self.prev_z) / (2*dt)

        # Обновляем предыдущие положения
        self.prev_x, self.prev_y, self.prev_z = self.x, self.y, self.z

        # Обновляем текущие положения
        self.x, self.y, self.z = self.x * (1 - self.free_x) + next_x * self.free_x, self.y * (1 - self.free_y) + next_y* self.free_y, self.z * (1 - self.free_z) + next_z* self.free_z
        
    def form_udp(self):
        dat = [self.x, self.y, self.z, self.rotation_x,
               self.rotation_y, self.rotation_z]
        return dat

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Velocity: ({self.vx}, {self.vy}, {self.vz}), Rotation: ({self.rotation_x}, {self.rotation_y}, {self.rotation_z})"

def calculate_force(object1, object2, spring_constant, rest_length):
    # Рассчитываем расстояние между объектами
    dx = object2.x - object1.x
    dy = object2.y - object1.y
    dz = object2.z - object1.z
    distance = np.sqrt(dx**2 + dy**2 + dz**2)
    # Рассчитываем силу пружины
    force_magnitude = spring_constant * (distance - rest_length)
    # Рассчитываем компоненты силы
    fx = force_magnitude * (dx / distance)
    fy = force_magnitude * (dy / distance)
    fz = force_magnitude * (dz / distance)
    return fx, fy, fz

def periodic_force(objct,forces, timer):
    forces[objct][0] += objct.force_x * np.sin(objct.freq * timer)
    forces[objct][1] += objct.force_y * np.sin(objct.freq * timer)
    forces[objct][2] += objct.force_z * np.sin(objct.freq * timer)

def update_system(objects, connections, spring_constants, rest_lengths, dt, damping_coefficient, timer):
    # Подготавливаем массив для хранения результирующих сил
    forces = {obj: np.array([0.0, 0.0, 0.0]) for obj in objects}
    
    # Рассчитываем силы между всеми связанными объектами
    for (i, j), k, l0 in zip(connections, spring_constants, rest_lengths):
        f = calculate_force(objects[i], objects[j], k, l0)
        damping_force_i = damping_coefficient * np.array([objects[i].vx, objects[i].vy, objects[i].vz])
        damping_force_j = damping_coefficient * np.array([objects[j].vx, objects[j].vy, objects[j].vz])
        forces[objects[i]] += np.array(f) - damping_force_i
        forces[objects[j]] -= np.array(f) + damping_force_j
    
    # Обновляем скорости и положения объектов
    for obj in objects:
        periodic_force(obj, forces, timer)
        ax, ay, az = forces[obj] / obj.mass
        obj.update_velocity_and_position_Verle(ax, ay, az, dt)
