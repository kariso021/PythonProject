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
pattern_generator = PatternGenerator(screen_width=size[0],screen_height=size[1], target=player_obj)
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
    global done
    while not done:
        clock.tick(30)
        screen.fill(BLACK)
        
        handle_events()

        player_obj.update_projectiles()
        player_obj.draw(screen)

        # 플레이어와 적의 충돌 처리
        for enemy in list(enemies_list):
            enemy.update()
            enemy.draw(screen)
            if player_obj.check_collision(enemy):
                player_obj.take_damage(10)
                enemies_list.remove(enemy)
            
            # 적의 투사체 업데이트 및 충돌 처리
            for projectile in list(enemy.projectiles):
                projectile.draw(screen)
                if projectile.check_collision(player_obj):
                    player_obj.take_damage(10)
                    enemy.projectiles.remove(projectile)

        #  플레이어 투사체와 적의 충돌 처리
        for projectile in list(player_obj.projectiles):
            for enemy in list(enemies_list):
                if projectile.check_collision(enemy):
                    enemy.take_damage(30)
                    if not enemy.alive:
                        enemies_list.remove(enemy)
                        player_obj.increase_score(50)
                    player_obj.projectiles.remove(projectile)
                    break

        player_obj.draw_score(screen, font)
        pygame.display.update()

run_game()
pygame.quit()

    #if pygame.time.get_ticks() % 5000 < 30:
            #enemies_list.extend(pattern_generator.missile_pattern(random.randint(5, 10)))  # 개체수