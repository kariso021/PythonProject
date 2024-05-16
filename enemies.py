import pygame
import math

class Enemy:
    def __init__(self, image_path='images/Enemy.png', x=0, y=0, width=50, height=50, speed=5):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class HomingEnemy(Enemy): # EnemyClass 를 상속해서 HomingEnemy 를 만듦
    def __init__(self, target, image_path='images/HomingEnemy.png', x=0, y=0, width=50, height=50, speed=5):
        super().__init__(image_path, x, y, width, height, speed)
        self.target = target

    def move(self):
        target_x, target_y = self.target.x, self.target.y
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

class LoopingShooterEnemy(Enemy): #루트에서 계속 돌아가게끔
    def __init__(self, image_path='images/LoopingShooterEnemy.png', x=0, y=0, width=50, height=50, speed=5, shooting_interval=50):
        super().__init__(image_path, x, y, width, height, speed)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0

    def move(self):
        
        pass

    def shoot(self):
        if self.shooting_timer >= self.shooting_interval:
            self.shooting_timer = 0
            # Implement shooting logic here
            pass

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()

class DownwardShooterEnemy(Enemy): #슈팅하는 Enemy 정지 Enemy인데 좌표에 들어서고, 조금씩 천천히 아래로 내려가게끔 설계
    def __init__(self, image_path='images/DownwardShooterEnemy.png', x=0, y=0, width=50, height=50, speed=5, shooting_interval=50):
        super().__init__(image_path, x, y, width, height, speed)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0

    def move(self):
        self.y += self.speed

    def shoot(self):
        if self.shooting_timer >= self.shooting_interval:
            self.shooting_timer = 0
            # Implement shooting logic here
            pass

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()