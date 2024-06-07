import pygame
import random

class BaseProjectile: #투사체 기본 클래스
    def __init__(self, x, y, speed, width, height, color, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.direction = direction
        
    def move(self):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
            
    def setcolorgreen(self):
        self.color=(0,128,0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        
    def check_collision(self, otherActor):
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        actor_rect = pygame.Rect(otherActor.x, otherActor.y, otherActor.width, otherActor.height)
        return projectile_rect.colliderect(actor_rect)
    
    
    #direction 을 다르게 둘고, 기능도 다르게 둘수 있어서 Projectile 클래스를 따로 나눠둔것 
    
    
class PlayerProjectile(BaseProjectile):
    def __init__(self, x, y, speed=10, width=5, height=10):
        super().__init__(x, y, speed, width, height, color=(255, 0, 0), direction='up')
        
class EnemyProjectile(BaseProjectile):
    def __init__(self, x, y, speed=5, width=5, height=10, explosive=False):
        super().__init__(x, y, speed, width, height, color=(255, 255, 0), direction='down')
        self.direction_x = 0
        self.direction_y = 1
        self.explosive = explosive
        self.explode_time = random.uniform(0.5 * 60, 1 * 60)  # 0.5초에서 1초 사이의 무작위 시간 (프레임 단위)
        self.timer = 0

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        if self.explosive:
            self.timer += 1

    def should_explode(self):
        return self.explosive and self.timer >= self.explode_time

    def split(self):
        small_projectiles = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_projectile = EnemyProjectile(self.x, self.y, speed=5, width=5, height=10)
                new_projectile.direction_x = i * 2.0 #speed of projectile
                new_projectile.direction_y = j * 2.0
                small_projectiles.append(new_projectile)
        return small_projectiles