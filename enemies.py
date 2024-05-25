import pygame
import random
import math
from projectile import EnemyProjectile

class Enemy:
    def __init__(self, image_path=None, x=0, y=0, width=50, height=50, speed=5, hp=10, can_shoot=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp = hp
        self.alive = True  # 적이 살아 있는지 여부
        self.can_shoot = can_shoot
        self.projectiles = []  # 모든 적이 projectiles 속성을 가지도록 설정

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 0, 0))  # 기본 이미지 생성자

    def move(self):
        pass
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.destroy()
    
    def destroy(self):
        self.alive = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        pass

class MissileEnemy(Enemy):
    def __init__(self, target, screen_width, image_path='images/homingEnemy.png', width=50, height=50, speed=5, hp=100, can_shoot=False):
        x = random.randint(0, screen_width - width)
        y = 0
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.target = target
        self.calculate_direction()

    def calculate_direction(self): #정규화
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
    def __init__(self, screen_width, screen_height, image_path='images/LoopingShooterEnemy.png', x=0, y=0, width=50, height=50, speed=5, shooting_interval=80, hp=100, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 초기좌표 설정하기
        self.points = [
            (150, 150),
            (screen_width - 150, 150),
            (screen_width - 150, screen_height - 250),
            (150, screen_height - 250)
        ]
        self.current_point = 0 
        self.moving_to_initial = True
        self.calculate_direction_to_point()

    def calculate_direction_to_point(self): # 정규화
        target_x, target_y = self.points[self.current_point]
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
        if self.moving_to_initial:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.current_point][0] - self.x)**2 + (self.points[self.current_point][1] - self.y)**2) < self.speed:
                self.moving_to_initial = False
                self.current_point = (self.current_point + 1) % len(self.points)
                self.calculate_direction_to_point()
        else:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.current_point][0] - self.x)**2 + (self.points[self.current_point][1] - self.y)**2) < self.speed:
                self.current_point = (self.current_point + 1) % len(self.points)#여기서 selfpoint 의 주소값 자체를 하나 옮김
                self.calculate_direction_to_point()

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height)
            self.projectiles.append(projectile)
            self.shooting_timer = 0

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()
        for projectile in self.projectiles:
            projectile.setcolorgreen()
            projectile.move()

class DownwardShooterEnemy(Enemy):
    def __init__(self, screen_width, screen_height, image_path='images/DownwardShooterEnemy.png', x=0, y=0,targetpoint=0, width=100, height=100, speed=3, shooting_interval=50, hp=100, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.afterspeed=1
        self.reach_to_target=False
        self.projectiles = []

        self.points = [
            (100, 50),
            (200,50),
            (300,50),
            (400,50)
        ]
        self.target_point = targetpoint 
        self.calculate_direction_to_point()

    def calculate_direction_to_point(self):
        target_x, target_y = self.points[self.target_point]
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
        if self.reach_to_target==False:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.target_point][0] - self.x)**2 + (self.points[self.target_point][1] - self.y)**2) < self.speed:
                self.reach_to_target=True
        else:
            self.y += self.afterspeed

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height)
            self.projectiles.append(projectile)
            self.shooting_timer = 0

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()
        for projectile in self.projectiles:
            projectile.move()
            
            
            
class BossEnemy(Enemy):
    def __init__(self, screen_width, screen_height, image_path='images/Boss.png', x=0, y=0, width=300, height=100, speed=5, shooting_interval=20, hp=500, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 초기좌표 설정하기
        self.points = [
            (0, 0),
            (screen_width - 200, 0)
        ]
        self.current_point = 0 
        self.moving_to_initial = True
        self.calculate_direction_to_point()

    def calculate_direction_to_point(self): # 정규화
        target_x, target_y = self.points[self.current_point]
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
        if self.moving_to_initial:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.current_point][0] - self.x)**2 + (self.points[self.current_point][1] - self.y)**2) < self.speed:
                self.moving_to_initial = False
                self.current_point = (self.current_point + 1) % len(self.points)
                self.calculate_direction_to_point()
        else:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.current_point][0] - self.x)**2 + (self.points[self.current_point][1] - self.y)**2) < self.speed:
                self.current_point = (self.current_point + 1) % len(self.points)#여기서 selfpoint 의 주소값 자체를 하나 옮김
                self.calculate_direction_to_point()

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            projectile = EnemyProjectile(self.x + self.width // 3, self.y + self.height)
            self.projectiles.append(projectile)
            projectile = EnemyProjectile(self.x + self.width // 3*2, self.y + self.height)
            self.projectiles.append(projectile)
            self.shooting_timer = 0

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.shoot()
        for projectile in self.projectiles:
            projectile.setcolorgreen()
            projectile.move()