import pygame
import random

class Item:
    def __init__(self, image_path, x, y, width=50, height=50, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.alive = True

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 255, 0))  # 기본 이미지 색상

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.y += self.speed

    def destroy(self):
        self.alive = False
        
    def check_collision(self, player):
        player_x, player_y, player_width, player_height = player.get_position_and_size()    # player 의 정보를 받아서 계산
        if (self.x < player_x + player_width and
            self.x + self.width > player_x and
            self.y < player_y + player_height and
            self.y + self.height > player_y):
            self.alive = False      # 조건 확인 후 아이템 제거
            return True
        return False
        
        
class HealthItem(Item):
    def __init__(self, x, y):
        super().__init__("images/heart_item.png", x, y)

class ScoreItem(Item):
    def __init__(self, x, y):
        super().__init__("images/score_item.png", x, y)

class SpeedItem(Item):
    def __init__(self, x, y):
        super().__init__("images/speed_item.png", x, y)
        
        