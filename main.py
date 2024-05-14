# 
import random
import pygame
import player
import enemies

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = (500, 500)
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # 폰트설정
num_enemies = random.randint(5, 10)


player_obj = player.Player()
enemies_list = [enemies.Enemy(x=random.randint(100, 400), y=-50) for _ in range(num_enemies)] #일단 테스트용으로 List로 만들었는데 Dictionary 를 통해서 수정하면 더 좋을거같음 적 종류같은거
font = pygame.font.Font(None, 36)  # font지정해주는거


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


def runGame():
    global done#전역변수 쓸때 해줘야하는거
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
                enemies_list.remove(enemy)  # 충돌 처리 그냥 Enemy 삭제시키는 방향으로 함
                player_obj.increase_score(100) #임시 score 확인용으로 만들어둔 코드
                
        # 투사체와 적의 충돌 처리
        for projectile in player_obj.projectiles:
            for enemy in list(enemies_list):
                if projectile.check_collision(enemy):
                    enemies_list.remove(enemy)
                    player_obj.projectiles.remove(projectile)
                    player_obj.increase_score(50)  # 적을 제거할 때 점수를 올림
                    break
        
        player_obj.draw_score(screen,font)
        pygame.display.update()

runGame()
pygame.quit()