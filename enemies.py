import pygame
import random
import math
from projectile import EnemyProjectile
from command import MoveEnemyCommand, ShootEnemyCommand

class Enemy:
    def __init__(self, image_path=None, x=0, y=0, width=50, height=50, speed=5, hp=10, can_shoot=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp = hp
        self.alive = True
        self.can_shoot = can_shoot
        self.projectiles = []

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 0, 0))

        self.move_command = MoveEnemyCommand(self)
        if can_shoot:
            self.shoot_command = ShootEnemyCommand(self)
        else:
            self.shoot_command = None

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
        self.move_command.execute()
        if self.shoot_command:
            self.shoot_command.execute()
        for projectile in self.projectiles:
            projectile.move()

class MissileEnemy(Enemy):
    def __init__(self, target, screen_width, image_path='images/homingEnemy.png', width=50, height=50, speed=5, hp=100, can_shoot=False):
        x = random.randint(0, screen_width - width)
        y = 0
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
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
        self.move_command.execute()

class LoopingShooterEnemy(Enemy):
    def __init__(self, screen_width, screen_height, image_path='images/LoopingShooterEnemy.png', x=0, y=0, width=50, height=50, speed=5, shooting_interval=80, hp=100, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        #Looping 을 하는 좌표들
        self.points = [
            (150, 150),
            (screen_width - 150, 150),
            (screen_width - 150, screen_height - 250),
            (150, screen_height - 250)
        ]
        self.current_point = 0 
        self.moving_to_initial = True
        self.calculate_direction_to_point()

    def calculate_direction_to_point(self):
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
                self.current_point = (self.current_point + 1) % len(self.points)
                self.calculate_direction_to_point()

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height)
            self.projectiles.append(projectile)
            self.shooting_timer = 0

    def update(self):
        self.move_command.execute()
        self.shooting_timer += 1
        if self.shooting_timer >= self.shooting_interval:
            self.shoot_command.execute()
        for projectile in self.projectiles:
            projectile.setcolorgreen()
            projectile.move()

class DownwardShooterEnemy(Enemy):
    def __init__(self, screen_width, screen_height, image_path='images/DownwardShooterEnemy.png', x=0, y=0, targetpoint=0, width=100, height=100, speed=3, shooting_interval=50, hp=100, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.afterspeed = 1
        self.reach_to_target = False
        self.projectiles = []

        #처음 좌표로 이동하는 부분들
        self.points = [
            (100, 50),
            (200, 50),
            (300, 50),
            (400, 50)
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
        if self.reach_to_target == False:
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
            if math.sqrt((self.points[self.target_point][0] - self.x)**2 + (self.points[self.target_point][1] - self.y)**2) < self.speed:
                self.reach_to_target = True
        else:
            self.y += self.afterspeed

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height)
            self.projectiles.append(projectile)
            self.shooting_timer = 0

    def update(self):
        self.move_command.execute()
        self.shooting_timer += 1
        if self.shooting_timer >= self.shooting_interval:
            self.shoot_command.execute()
        for projectile in self.projectiles:
            projectile.move()

class BossEnemy(Enemy):
    def __init__(self, screen_width, screen_height, image_path='images/Boss.png', x=0, y=0, width=300, height=100, speed=5, shooting_interval=20, hp=500, can_shoot=True):
        super().__init__(image_path, x, y, width, height, speed, hp, can_shoot)
        self.shooting_interval = shooting_interval
        self.shooting_timer = 0
        self.bigshoot_interver= 200
        self.bigshoot_timer= 0
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.points = [
            (0, 0),
            (screen_width - 200, 0)
        ]
        self.current_point = 0 
        self.moving_to_initial = True
        self.calculate_direction_to_point()

    def calculate_direction_to_point(self):
        target_x, target_y = self.points[self.current_point]
        #벡터개념
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
                self.current_point = (self.current_point + 1) % len(self.points)
                self.calculate_direction_to_point()

    def shoot(self):
        if self.can_shoot and self.shooting_timer >= self.shooting_interval:
            self.shooting_timer = 0
            if self.bigshoot_timer>=self.bigshoot_interver:
                attack_pattern=self.big_shot
                attack_pattern()
                self.bigshoot_timer=0
            else:
                attack_pattern = random.choice([self.straight_shot, self.spread_shot, self.zigzag_shot])
                attack_pattern()

    def straight_shot(self):
        projectile = EnemyProjectile(self.x + self.width // 3, self.y + self.height)
        self.projectiles.append(projectile)
        projectile = EnemyProjectile(self.x + 2 * self.width // 3, self.y + self.height)
        self.projectiles.append(projectile)

    def spread_shot(self):
        for offset in range(-2, 3):
            projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height, speed=5, width=5, height=10)
            projectile.direction_x = offset * 0.2
            projectile.direction_y = 1
            self.projectiles.append(projectile)

    def zigzag_shot(self):
        projectile = EnemyProjectile(self.x + self.width // 3, self.y + self.height, speed=5, width=5, height=10)
        projectile.direction = 'zigzag'
        self.projectiles.append(projectile)
        projectile = EnemyProjectile(self.x + 2 * self.width // 3, self.y + self.height, speed=5, width=5, height=10)
        projectile.direction = 'zigzag'
        self.projectiles.append(projectile)
        
        
    def big_shot(self):
        projectile = EnemyProjectile(self.x + self.width // 2, self.y + self.height)
        projectile.width=50
        projectile.height=50
        self.projectiles.append(projectile)

    def update(self):
        self.move()
        self.shooting_timer += 1
        self.bigshoot_timer +=1
        if self.shooting_timer >= self.shooting_interval:
            self.shoot()
        for projectile in self.projectiles:
            if projectile.direction == 'zigzag':
                projectile.x += projectile.speed * math.sin(projectile.y / 20)#sin 값으로 왔다갔다 하게끔 하는것
            projectile.move()
            projectile.setcolorgreen()