import pygame

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
    def __init__(self, x, y, speed=5, width=5, height=10):
        super().__init__(x, y, speed, width, height, color=(255, 255, 0), direction='down')
    