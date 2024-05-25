import pygame#아이템 아직 기능구현 딱히 안해둠 

class Item:
    def __init__(self, x, y, image_path):#image_path='images/Plane_Forward.png' 이런식으로 imagepath 다르게 사용하시고
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def move(self):
        self.y += self.speed  # 적 일단 아래로 가게끔 구현 5정도 되면 부드러움
        

    