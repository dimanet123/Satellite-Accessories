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
    C1 = 150
    C2 = 300
    J = 1000
    M = 300
    L1 = 8
    L2 = 5

    a = (C1+C2)/M
    b = (C2*L2 - C1*L1)/M
    c = (C2*L2 - C1*L1)/J
    d = (C1*L1**2 + C2*L2**2)/J

    # Создание матрицы
    matrix = np.array([[a, b],
                       [c, d]])

    # Находим собственные значения и собственные векторы
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    eigenvalues = np.sort(eigenvalues, axis=0)
    print("Квадраты собственных частот:", eigenvalues)

    kap1 = eigenvalues[0]/b - a
    kap2 = eigenvalues[1]/b - a

    kap_matrix = np.array([[1, 1],
                           [kap1, kap2]])

    print("Матрицы форм:", kap_matrix)

    x1_0 = 0.2
    x2_0 = np.pi/6
    xx1_0 = 0
    xx2_0 = 0

    matrix_1 = np.array([[x1_0],
                         [x2_0]])

    matrix_2 = np.array([[xx1_0],
                         [xx2_0]])

    matrix_C1_C3 = np.linalg.inv(kap_matrix) @ matrix_1
    matrix_C2_C4 = np.linalg.inv(kap_matrix) @ matrix_2

    print('aaaaa')
    print(matrix_C1_C3)
    print(matrix_C2_C4)

    dat = [eigenvalues[0]**(1/2), eigenvalues[1]**(1/2), kap1, kap2,
           matrix_C1_C3[0], matrix_C2_C4[0], matrix_C1_C3[1], matrix_C2_C4[1]]

    return dat


def x1(dat, t):
    x1 = dat[4] * np.cos(dat[0]*t) + dat[5] * np.sin(dat[0]*t) + \
        dat[6] * np.cos(dat[1]*t) + dat[7] * np.sin(dat[1]*t)
    return x1


def x2(dat, t, form):
    if form == 0:
        x2 = dat[4] * np.cos(dat[0]*t) + dat[5] * np.sin(dat[0]*t) + \
            dat[6] * np.cos(dat[1]*t) + dat[7] * np.sin(dat[1]*t)
    else:
        x2 = dat[2]*dat[4] * np.cos(dat[0]*t) + dat[2]*dat[5] * np.sin(
            dat[0]*t) + dat[3]*dat[6] * np.cos(dat[1]*t) + dat[3]*dat[7] * np.sin(dat[1]*t)
    return np.rad2deg(x2)

       

# Пример использования:
obj = Object3D()
print(obj)  # Выводит: Position: (0, 0, 0), Rotation: (0, 0, 0)

obj.move(1, 2, 3)
obj.rotate(45, 30, 60)
print(obj)  # Выводит: Position: (1, 2, 3), Rotation: (45, 30, 60)
