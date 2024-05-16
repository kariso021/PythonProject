# projectile.py
import pygame

class Projectile: #투사체
    def __init__(self, x, y, speed=10, width=5, height=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.color = (255, 0, 0)
        
    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        
    def check_collision(self, otherActor):
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        enemy_rect = pygame.Rect(otherActor.x, otherActor.y, otherActor.image.get_width(), otherActor.image.get_height())
        return projectile_rect.colliderect(enemy_rect)
    
    def set_color(self, newcolor):
        self.color=newcolor
        
   