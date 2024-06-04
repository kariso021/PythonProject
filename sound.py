#sound.py
import pygame

class Sound:
    def __init__(self, bgfilepath ,bIsplaying):
        self.bgfilepath = pygame.mixer.music.load('bagroundsample.mp3')
        bIsplaying = False
    
    def soundplay(self):
        if(self.bIsplaying):
            self.bgfilepath.play()
            
            
    