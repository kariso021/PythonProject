import pygame

WHITE = (255, 255, 255)

def draw_title_screen(screen, size, font):
    title_text = font.render("Space 1945 Game", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title_text, (size[0] // 2 - title_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(start_text, (size[0] // 2 - start_text.get_width() // 2, size[1] // 2))

def draw_endgame_screen(screen, size, font, score):
    end_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(end_text, (size[0] // 2 - end_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(score_text, (size[0] // 2 - score_text.get_width() // 2, size[1] // 2))
    screen.blit(restart_text, (size[0] // 2 - restart_text.get_width() // 2, size[1] // 2 + 50))
    
def draw_endgame_clear_screen(screen, size, font, score):
    end_text = font.render("Clear!!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(end_text, (size[0] // 2 - end_text.get_width() // 2, size[1] // 2 - 50))
    screen.blit(score_text, (size[0] // 2 - score_text.get_width() // 2, size[1] // 2))
    screen.blit(restart_text, (size[0] // 2 - restart_text.get_width() // 2, size[1] // 2 + 50))
    
