import pygame
import random
import math

class Enemy:
    def __init__(self, image_path=None, x=0, y=0, width=50, height=50, speed=5,hp=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp=hp
        self.alive = True  # 적이 살아 있는지 여부

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 0, 0))  # 기본이미지생성자

    def move(self):
        pass
    
    def take_damage(self,damage):
        self.hp-= damage
        if(self.hp<=0):
            self.destroy()
    
    def destroy(self):
        self.alive=False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class HomingEnemy(Enemy):
    def __init__(self, target, screen_width, image_path='images/HomingEnemy.png', width=50, height=50, speed=5, hp=100):
        x = random.randint(0, screen_width - width)
        y = 0
        super().__init__(image_path, x, y, width, height, speed, hp) #부모클래스 호출
        self.target = target
        self.calculate_direction()

    def calculate_direction(self):
        target_x, target_y = self.target.x, self.target.y
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        if distance != 0:
            self.direction_x = direction_x / distance
            self.direction_y = direction_y / distance
        else:
            self.direction_x = 0
            self.direction_y = 1

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        
    def update(self):
        self.move()

class LoopingShooterEnemy(Enemy):
    def __init__(self, image_path='images/LoopingShooterEnemy.png', x=0, y=0, width=50, height=50, speed=5, shooting_interval=50, hp=100):
        super().__init__(image_path, x, y, width, height, speed,  hp)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0

    def move(self):
        self.y += self.speed

    def shoot(self):#설계만하고 아직
            pass

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()

class DownwardShooterEnemy(Enemy):
    def __init__(self, image_path='images/DownwardShooterEnemy.png', x=0, y=0, width=100, height=100, speed=1, shooting_interval=50, hp=100):
        super().__init__(image_path, x, y, width, height, speed,  hp)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0

    def move(self):
        self.y += self.speed #일단은 아래로 내려가는것만

    def shoot(self):#설계만하고 아직
            pass

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()