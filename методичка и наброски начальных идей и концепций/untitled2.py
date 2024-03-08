class Ball:
    def __init__(self, color = 'white', radius = 10, material = 'rubber', mass = 10):
    # Функция класса Ball, отвечающая за инициализацию нового объекта
        self.color = color
        self.radius = radius
        self.material = material
        self.mass = mass
        
    def __str__(self):
        return f'Color = {self.color}, radius = {self.radius}, material = {self.material}, mass = {self.mass}'
    
Ball1 = Ball()
Ball2 = Ball(color='blue', radius=100,mass = 100)
Ball3 = Ball(radius = 56)

print(Ball1)
print(Ball2)
print(Ball3)
        
    
        

