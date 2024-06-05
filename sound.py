# sound.py
import pygame

class Sound:
    def __init__(self, bgfilepath):
        self.bgfilepath = bgfilepath
        self.bIsplaying = False
        pygame.mixer.music.load(self.bgfilepath)
    
    def play(self):
        if not self.bIsplaying:
            pygame.mixer.music.play(-1)  # -1 -> 뮤직루프 설정
            self.bIsplaying = True

    def stop(self):
        if self.bIsplaying:
            pygame.mixer.music.stop()
            self.bIsplaying = False