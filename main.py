import pygame
import random
import player
import enemies
from pattern import PatternGenerator

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = (500, 500)
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # 폰트 설정

# 플레이어 객체 초기화
player_obj = player.Player(x=size[0]//2, y=size[1] - 50)

# 타겟 설정입니당
pattern_generator = PatternGenerator(screen_width=size[0], target=player_obj)
enemies_list = pattern_generator.random_pattern(random.randint(5, 10))  # 랜덤 패턴으로 초기화

def handle_events():
    global done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()  # 현재 눌려있는 키의 상태
    if keys[pygame.K_UP]:
        player_obj.move_up()
    if keys[pygame.K_DOWN]:
        player_obj.move_down()
    if keys[pygame.K_LEFT]:
        player_obj.move_left()
    if keys[pygame.K_RIGHT]:
        player_obj.move_right()
    if keys[pygame.K_SPACE]:
        player_obj.fire()

def run_game():
    global done  # 전역변수 global!
    while not done:
        clock.tick(30)
        screen.fill(BLACK)
        
        handle_events()

        player_obj.update_projectiles()
        player_obj.draw(screen)

        for enemy in list(enemies_list):
            enemy.move()
            enemy.draw(screen)
            if player_obj.check_collision(enemy):
                player_obj.take_damage(10)
                enemies_list.remove(enemy) 
                #player_obj.increase_score(100)  # 임시 score 확인용 코드
                
        # 투사체와 적의 충돌 처리
        for projectile in list(player_obj.projectiles):
            for enemy in list(enemies_list):
                if projectile.check_collision(enemy):
                    enemies_list.remove(enemy)
                    player_obj.projectiles.remove(projectile)
                    player_obj.increase_score(50)  # 적을 제거할 때 점수를 올림
                    break
        
        player_obj.draw_score(screen, font)
        pygame.display.update()

        # 5초마다 패턴 변경 pattern count 변수만 이용하면 됨 -> 이거 나중에 적 처치시로 바꿀거임
        if pygame.time.get_ticks() % 5000 < 30:
            enemies_list.extend(pattern_generator.random_pattern(random.randint(5, 10)))#개체수

run_game()
pygame.quit()