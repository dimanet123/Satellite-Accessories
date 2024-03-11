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
        self.rotation_x = f1
        self.rotation_y = f2
        self.abs_y = vert
        

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Rotation: ({self.rotation_x}, {self.rotation_y}, {self.rotation_z})"
    
       

# Пример использования:
obj = Object3D()
print(obj)  # Выводит: Position: (0, 0, 0), Rotation: (0, 0, 0)

obj.move(1, 2, 3)
obj.rotate(45, 30, 60)
print(obj)  # Выводит: Position: (1, 2, 3), Rotation: (45, 30, 60)
