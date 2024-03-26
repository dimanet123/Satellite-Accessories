import numpy as np
class Object3D:
    def __init__(self, x=0, y=0, z=0, rotation_x=0, rotation_y=0, rotation_z=0):
        self.x = x
        self.y = y
        self.z = z
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z

    def move(self, delta_x, delta_y, delta_z):
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z
        
    def move_abs(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def rotate_abs(self, rotation_x, rotation_y, rotation_z):
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z

    def rotate(self, delta_rotation_x, delta_rotation_y, delta_rotation_z):
        self.rotation_x += delta_rotation_x
        self.rotation_y += delta_rotation_y
        self.rotation_z += delta_rotation_z

    def form_udp(self):
        dat = [self.x, self.y, self.z, self.rotation_x,
               self.rotation_y, self.rotation_z]
        return dat

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Rotation: ({self.rotation_x}, {self.rotation_y}, {self.rotation_z})"




class pandelum:
    def __init__(self, x=0, y=0, z=0, angle = 0, l = 10, g = 10):
        self.x = 0
        self.y = 0
        self.z = 0
        self.angle = angle
        self.l = l
        self. g = 10
    
    def f(self, theta, omega):
        g_over_L = 9.8 / self.l
        return -g_over_L * np.sin(theta) - 0.1*omega

    def rk4_step(self, theta, omega, dt):
        k1_theta = omega
        k1_omega = self.f(theta, omega)
        
        k2_theta = omega + 0.5 * dt * k1_omega
        k2_omega = self.f(theta + 0.5 * dt * k1_theta, omega + 0.5 * dt * k1_omega)
        
        k3_theta = omega + 0.5 * dt * k2_omega
        k3_omega = self.f(theta + 0.5 * dt * k2_theta, omega + 0.5 * dt * k2_omega)
        
        k4_theta = omega + dt * k3_omega
        k4_omega = self.f(theta + dt * k3_theta, omega + dt * k3_omega)
        
        theta_new = theta + (dt / 6) * (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta)
        omega_new = omega + (dt / 6) * (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega)
        
        return theta_new, omega_new
    
class RungeKuttaSolver:
    def __init__(self, a, b, d, f, dt):
        self.a = a
        self.b = b
        self.d = d
        self.f = f
        self.dt = dt

    def equations(self, t, u1, u2, v1, v2):
        return u2, -self.a*u1 - np.sin(v1)*self.b, v2, -u1*np.cos(v1)*self.d - np.sin(2*v1)*self.f

    def rk4_step(self, t, u1, u2, v1, v2):
        k1_u1, k1_u2, k1_v1, k1_v2 = self.equations(t, u1, u2, v1, v2)
        k2_u1, k2_u2, k2_v1, k2_v2 = self.equations(t + 0.5*self.dt, u1 + 0.5*self.dt*k1_u1, u2 + 0.5*self.dt*k1_u2,
                                                      v1 + 0.5*self.dt*k1_v1, v2 + 0.5*self.dt*k1_v2)
        k3_u1, k3_u2, k3_v1, k3_v2 = self.equations(t + 0.5*self.dt, u1 + 0.5*self.dt*k2_u1, u2 + 0.5*self.dt*k2_u2,
                                                      v1 + 0.5*self.dt*k2_v1, v2 + 0.5*self.dt*k2_v2)
        k4_u1, k4_u2, k4_v1, k4_v2 = self.equations(t + self.dt, u1 + self.dt*k3_u1, u2 + self.dt*k3_u2,
                                                      v1 + self.dt*k3_v1, v2 + self.dt*k3_v2)
        u1_new = u1 + (self.dt/6) * (k1_u1 + 2*k2_u1 + 2*k3_u1 + k4_u1)
        u2_new = u2 + (self.dt/6) * (k1_u2 + 2*k2_u2 + 2*k3_u2 + k4_u2)
        v1_new = v1 + (self.dt/6) * (k1_v1 + 2*k2_v1 + 2*k3_v1 + k4_v1)
        v2_new = v2 + (self.dt/6) * (k1_v2 + 2*k2_v2 + 2*k3_v2 + k4_v2)
        return u1_new, u2_new, v1_new, v2_new
    





def oscil():
    m1 = 5
    m2 = 5
    m3 = 5
    m4 = 5
    m5 = 5
    k1 = 200
    k2 = 200
    k3 = 200
    k4 = 200
    k5 = 200
    

    # Количество масс и пружин
    n_masses = 3  # Пример для квадрата
    dimensions = 2  # Работаем в 2D пространстве

    # Массы (предположим, они одинаковы для упрощения)
    masses = [1.0,1,1]

    # Соединения и жёсткости пружин: (масса 1, масса 2, жёсткость)
    springs = [(0, 1, 100), (1, 2, 100), (2, 0, 100)]

    # Создание матрицы масс
    M = np.diag([mass for mass in masses for _ in range(dimensions)])

    # Инициализация матрицы жёсткости
    K = np.zeros((n_masses * dimensions, n_masses * dimensions))

    # Заполнение матрицы жёсткости
    for mass1, mass2, stiffness in springs:
        for dim in range(dimensions):
            idx1, idx2 = mass1 * dimensions + dim, mass2 * dimensions + dim
            K[idx1, idx1] += stiffness
            K[idx2, idx2] += stiffness
            K[idx1, idx2] -= stiffness
            K[idx2, idx1] -= stiffness

    # Вывод матрицы масс и жёсткости
    print("Матрица масс M:")
    print(M)
    print("\nМатрица жёсткости K:")
    print(K)
    
    # Создание матрицы
    matrix_K = K
    
    matrix_M = M
    
    diagonal_elements = np.diag(matrix_M)
    
    matrix_base = matrix_K / diagonal_elements[:, np.newaxis]

    # Находим собственные значения и собственные векторы
    eigenvalues, eigenvectors = np.linalg.eig(matrix_base)
    eigenvalues = np.sort(eigenvalues, axis=0)
    threshold = 1e-10
    eigenvalues = eigenvalues.real
    eigenvectors = eigenvectors.real
    eigenvalues = np.where(abs(eigenvalues) < threshold, 0, eigenvalues)
    eigenvectors = np.where(abs(eigenvectors) < threshold, 0, eigenvectors)
    
    matrix_form = eigenvectors
    
    x1_0 = 0
    x2_0 = 0
    x3_0 = 0
    x4_0 = 0
    x5_0 = 0
    xx1_0 = 0
    xx2_0 = 0
    xx3_0 = 0
    xx4_0 = 0
    xx5_0 = 10

    # matrix = np.array([[x1_0, xx1_0],[x2_0, xx2_0],[x3_0, xx3_0], [x4_0, xx4_0]])

    # coord_const = np.linalg.solve(matrix_form, matrix[:, 0])
    # speed_const = np.linalg.solve(matrix_form, matrix[:, 1])
        
        
    dat = [matrix_form, eigenvalues]
    return dat



dot = oscil()

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])
# coord_const = dot[2]
# speed_const = dot[3]

def x(t, number_form,num_func):
    return matrix_form[num_func - 1,number_form] * np.cos(eigenvalues[number_form]*t)



       

# Пример использования:
obj = Object3D()
print(obj)  # Выводит: Position: (0, 0, 0), Rotation: (0, 0, 0)

obj.move(1, 2, 3)
obj.rotate(45, 30, 60)
print(obj)  # Выводит: Position: (1, 2, 3), Rotation: (45, 30, 60)
