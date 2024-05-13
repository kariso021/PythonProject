# enemy.py
import pygame

class Enemy:
    def __init__(self, image_path='images/Enemy.png', x=0, y=0, width=50, height=50, speed=5):#여기도 Enemy 종류 늘릴까 생각중
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed  # 적 일단 아래로 가게끔 구현 5정도 되면 부드러움

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    #def Fire Enemy에도 만들까 생각중 죽을때 Enemy 에다가 넣으면 될듯