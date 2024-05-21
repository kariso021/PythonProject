# player.py 수정
import pygame
from projectile import PlayerProjectile

class Player:
    def __init__(self, image_path='images/Plane_Forward.png', x=230, y=400, width=60, height=45,hp=50, score=0):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.hp = hp
        self.width=width
        self.height=height
        self.projectiles = [] 
        self.heart_image = pygame.image.load('images/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))  #하트사이즈
        self.score = score
        self.fire_cooldown = 300  # 쿨타임 여기서 조정하면 됨 300기준으로 0.3초?
        self.last_fire_time = 0

    def move_up(self):
        self.y -= 10

    def move_down(self):
        self.y += 10

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10

    def fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time >= self.fire_cooldown:
            new_projectile = PlayerProjectile(self.x + self.image.get_width() / 2, self.y)
            self.projectiles.append(new_projectile)
            self.last_fire_time = current_time #발사시간 업데이트 시켜서 쿨타임주기

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.move()
            if projectile.y < 0:  
                self.projectiles.remove(projectile)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.draw(screen)
        self.draw_hearts(screen)
    
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0 
    
    def draw_hearts(self, screen):
        for i in range(self.hp // 10):
            screen.blit(self.heart_image, (10 + i * 40, 450)) 

    def check_collision(self, enemy):
        player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
        return player_rect.colliderect(enemy_rect)
    
    def increase_score(self, points):
        self.score += points

    def draw_score(self, screen, font):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (350, 10))