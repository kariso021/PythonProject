import pygame
import random
import player
import enemies
from pattern import PatternGenerator
import screens
from background import Background  # Background 클래스 임포트

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game Title")

done = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # 폰트 설정
randomcount = 0

# 배경 객체 초기화
background = Background('images/skybg.png', size) 

# 플레이어 객체 초기화
player_obj = player.Player(x=size[0] // 2, y=size[1] - 50)

# 타겟 설정
pattern_generator = PatternGenerator(screen_width=size[0], screen_height=size[1], target=player_obj)

# 패턴 리스트 초기화
pattern_list = [
    pattern_generator.Downwoard_pattern_1,
    pattern_generator.Downwoard_pattern_2,
    pattern_generator.LooppingShooterPattern,
    pattern_generator.BossPattern
]
current_pattern_index = 0
enemies_list = pattern_list[current_pattern_index]()
missile_enemies_list = []

# 게임 상태 스테이트를 따로 설정
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_ENDGAME = 2
GAME_STATE_CLEARGAME = 3
game_state = GAME_STATE_TITLE

def handle_events():
    global done, game_state, player_obj
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_TITLE and event.key == pygame.K_SPACE:
                game_state = GAME_STATE_PLAYING
            elif game_state == GAME_STATE_ENDGAME and event.key == pygame.K_r:
                reset_game()

    if game_state == GAME_STATE_PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_obj.move_up_command.execute()
        if keys[pygame.K_DOWN]:
            player_obj.move_down_command.execute()
        if keys[pygame.K_RIGHT]:
            player_obj.move_right_command.execute()
        if keys[pygame.K_LEFT]:
            player_obj.move_left_command.execute()
        if keys[pygame.K_SPACE]:
            player_obj.fire_command.execute()

def reset_game():
    global player_obj, pattern_list, current_pattern_index, enemies_list, missile_enemies_list, game_state, background
    player_obj = player.Player(x=size[0] // 2, y=size[1] - 50)
    current_pattern_index = 0
    enemies_list = pattern_list[current_pattern_index]()
    missile_enemies_list = []
    game_state = GAME_STATE_PLAYING
    background.y = 0

def run_game():
    global done, game_state, current_pattern_index, enemies_list, missile_enemies_list
    while not done:
        clock.tick(30)
        screen.fill(BLACK)

        handle_events()

        if game_state == GAME_STATE_TITLE:
            screens.draw_title_screen(screen, size, font)
        elif game_state == GAME_STATE_PLAYING:
            background.scroll()
            background.draw(screen)
            player_obj.update_projectiles()
            player_obj.draw(screen)

            # 커맨드 패턴으로 애너미 관리
            for enemy in list(enemies_list):
                enemy.update()
                enemy.draw(screen)
                if player_obj.check_collision(enemy):
                    player_obj.take_damage(10)
                    enemies_list.remove(enemy)

                if hasattr(enemy, 'projectiles'):
                    for projectile in list(enemy.projectiles):
                        projectile.draw(screen)
                        if projectile.check_collision(player_obj):
                            player_obj.take_damage(10)
                            enemy.projectiles.remove(projectile)

                if enemy.y > size[1]:
                    enemies_list.remove(enemy)

            # PlayerProjectile 관리 부분
            for projectile in list(player_obj.projectiles):
                for enemy in list(enemies_list):
                    if projectile.check_collision(enemy):
                        enemy.take_damage(40)  # Player Damage 따로 빼야 맞지만 그냥 여기다가 함
                        if not enemy.alive:
                            enemies_list.remove(enemy)
                            player_obj.increase_score(50)
                        player_obj.projectiles.remove(projectile)
                        break

            # 미사일(계속 주기적 생성되는건 따로 관리)
            for missile_enemy in list(missile_enemies_list):
                missile_enemy.update()
                missile_enemy.draw(screen)
                if player_obj.check_collision(missile_enemy):
                    player_obj.take_damage(1)#미사일 에너미 데미지 부분인데 그냥 난이도 어려워서 1로 함
                    missile_enemies_list.remove(missile_enemy)

                if hasattr(missile_enemy, 'projectiles'):
                    for projectile in list(missile_enemy.projectiles):
                        projectile.draw(screen)
                        if projectile.check_collision(player_obj):
                            player_obj.take_damage(10)
                            missile_enemy.projectiles.remove(projectile)

            for projectile in list(player_obj.projectiles):
                for missile_enemy in list(missile_enemies_list):
                    if projectile.check_collision(missile_enemy):
                        missile_enemy.take_damage(40)
                        if not missile_enemy.alive:
                            missile_enemies_list.remove(missile_enemy)
                            player_obj.increase_score(50)
                        player_obj.projectiles.remove(projectile)
                        break

            # 패턴 조정하는거 -> 미사일에 구애 안받게 짜둠
            if not enemies_list and current_pattern_index < len(pattern_list) - 1:
                current_pattern_index += 1
                enemies_list = pattern_list[current_pattern_index]()

            # 게임 클리어 조건
            if not enemies_list and current_pattern_index == len(pattern_list) - 1:
                game_state = GAME_STATE_CLEARGAME

            # 미사일 Enemy 일정 시간마다 계속 생성하는 부분
            if pygame.time.get_ticks() % 5000 < 30:
                missile_enemies_list.extend(pattern_generator.missile_pattern(random.randint(5, 10)))

            if player_obj.hp <= 0:
                game_state = GAME_STATE_ENDGAME

            player_obj.draw_score(screen, font)
        elif game_state == GAME_STATE_ENDGAME:
            screens.draw_endgame_screen(screen, size, font, player_obj.score)
        elif game_state == GAME_STATE_CLEARGAME:
            screens.draw_endgame_clear_screen(screen, size, font, player_obj.score)

        pygame.display.update()

run_game()
pygame.quit()