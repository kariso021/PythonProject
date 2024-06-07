import pygame

class Background:
    def __init__(self, image_path, size):
        self.image = pygame.image.load(image_path).convert()
        self.y = 0
        self.size = size

    def scroll(self):
        self.y += 2  # 이 값을 조정하여 스크롤 속도를 변경
        if self.y >= self.size[1]:
            self.y = 0 #사이즈 초기화

    def draw(self, screen):
        screen.blit(self.image, (0, self.y))
        screen.blit(self.image, (0, self.y - self.size[1]))#두개의 연결된 이미지