import numpy as np
class Object3D:
    def __init__(self, x=0, y=0, z=0, rotation_x=0, rotation_y=0, rotation_z=0, abs_y = 0):
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
               self.rotation_y, self.rotation_z, self.abs_y]
        return dat
    
    def coord_move(self, f1 = 0, f2 = 0, vert = 0):
        self.rotation_x = np.rad2deg(f1)
        self.rotation_y = np.rad2deg(f2)
        self.abs_y = vert
        

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Rotation: ({self.rotation_x}, {self.rotation_y}, {self.rotation_z})"
    
def oscil():
    m1 = 50
    m2 = 50
    m3 = 50
    k1 = 100
    k2 = 100
    k3 = 100
    k4 = 100
    
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
