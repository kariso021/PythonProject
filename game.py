import pygame
from game_state import TitleState

class Game:
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("1945 with Python")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.done = False
        self.state = TitleState(self)
        self.score = 0

    def change_state(self, new_state):
        self.state = new_state

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
        self.state.handle_events(events)

    def run(self):
        while not self.done:
            self.clock.tick(30)
            self.screen.fill((0, 0, 0))
            self.handle_events()
            
            # 업데이트
            self.state.update()
            self.state.draw(self.screen)
            
            
            #화면 업데이트
            pygame.display.flip()
            
        #종료
        pygame.quit()