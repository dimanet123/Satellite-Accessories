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
    k1 = 1000
    k2 = 200
    k3 = 200
    k4 = 1000
    
    degreeFreedom = 3
    

    # Создание матрицы
    matrix_K = np.array([[k1 + k2, -k2, 0], [-k2, k2+k3, -k3],[0, -k3, k3+k4]])
    matrix_M = np.array([[m1,0,0],[0,m2,0],[0,0,m3]])
    
    diagonal_elements = np.diag(matrix_M)
    
    matrix_base = matrix_K / diagonal_elements[:, np.newaxis]

    # Находим собственные значения и собственные векторы
    eigenvalues, eigenvectors = np.linalg.eig(matrix_base)
    eigenvalues = np.sort(eigenvalues, axis=0)
    
    matrix_form = eigenvectors
    
    x1_0 = 0
    x2_0 = 0
    x3_0 = 0
    xx1_0 = 0
    xx2_0 = 0
    xx3_0 = 10

    matrix = np.array([[x1_0, xx1_0],[x2_0, xx2_0],[x3_0, xx3_0]])

    coord_const = np.linalg.solve(matrix_form, matrix[:, 0])
    speed_const = np.linalg.solve(matrix_form, matrix[:, 1])
        
        
    dat = [matrix_form, eigenvalues, coord_const, speed_const]
    return dat



dot = oscil()

matrix_form = dot[0]
eigenvalues = np.sqrt(dot[1])
coord_const = dot[2]
speed_const = dot[3]



def x1(t, number_form):
    return matrix_form[0,number_form] * np.cos(eigenvalues[number_form]*t)
            
def x2(t, number_form):
    return matrix_form[1,number_form] * np.cos(eigenvalues[number_form]*t)
            
def x3(t, number_form):
    return matrix_form[2,number_form] * np.cos(eigenvalues[number_form]*t)



       

# Пример использования:
obj = Object3D()
print(obj)  # Выводит: Position: (0, 0, 0), Rotation: (0, 0, 0)

obj.move(1, 2, 3)
obj.rotate(45, 30, 60)
print(obj)  # Выводит: Position: (1, 2, 3), Rotation: (45, 30, 60)
