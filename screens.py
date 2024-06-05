#screen.py
import pygame

WHITE = (255, 255, 255)

background_image = pygame.image.load('images/background.png')

def draw_title_screen(screen, size, font):
    title_text = font.render("", True, WHITE)#임시로 썼었음 -> 나중에 학번 적는데 써도 됨(아래서 위치 조정해서)
    start_text = font.render("", True, WHITE)
    screen.blit(background_image, (0, 0))
    screen.blit(title_text, (size[0] // 2 - title_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(start_text, (size[0] // 2 - start_text.get_width() // 2, size[1] // 2))

def draw_endgame_screen(screen, size, font, score):
    end_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    replay_text = font.render("If you want replay, Press P",True,WHITE)
    screen.blit(end_text, (size[0] // 2 - end_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(score_text, (size[0] // 2 - score_text.get_width() // 2, size[1] // 2))
    screen.blit(restart_text, (size[0] // 2 - restart_text.get_width() // 2, size[1] // 2 + 50))
    screen.blit(replay_text, (size[0] // 2 - replay_text.get_width() // 2, size[1] // 2 + 100))
    
def draw_endgame_clear_screen(screen, size, font, score):
    end_text = font.render("Clear!!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(end_text, (size[0] // 2 - end_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(score_text, (size[0] // 2 - score_text.get_width() // 2, size[1] // 2))
    
