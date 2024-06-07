import pygame
import random
from player import Player
from background import Background
from pattern import PatternGenerator
from sound import Sound
import screens

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class TitleState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.change_state(PlayingState(self.game))

    def draw(self, screen):
        screens.draw_title_screen(screen, self.game.size, self.game.font)

class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.background = Background('images/skybg.png', self.game.size)
        self.player = Player(x=self.game.size[0] // 2, y=self.game.size[1] - 50)
        self.pattern_generator = PatternGenerator(screen_width=self.game.size[0], screen_height=self.game.size[1], target=self.player)
        self.pattern_list = [
            self.pattern_generator.Downwoard_pattern_1,
            self.pattern_generator.Downwoard_pattern_2,
            self.pattern_generator.LooppingShooterPattern,
            self.pattern_generator.BossPattern
        ]
        self.current_pattern_index = 0
        self.enemies_list = self.pattern_list[self.current_pattern_index]()
        self.missile_enemies_list = []
        self.sound_bg = Sound('sound/bgmusic.wav')
        self.sound_bg.play()

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move_up_command.execute()
        if keys[pygame.K_DOWN]:
            self.player.move_down_command.execute()
        if keys[pygame.K_RIGHT]:
            self.player.move_right_command.execute()
        if keys[pygame.K_LEFT]:
            self.player.move_left_command.execute()
        if keys[pygame.K_SPACE]:
            self.player.fire_command.execute()
            
            

    def update(self):
        self.background.scroll()
        self.player.update_projectiles()

        for enemy in list(self.enemies_list):
            enemy.update()
            if self.player.check_collision(enemy):
                self.player.take_damage(10)
                self.enemies_list.remove(enemy)
            #Enemy Projectile 관리
            for projectile in list(enemy.projectiles):
                if projectile.check_collision(self.player):
                    self.player.take_damage(10) 
                    enemy.projectiles.remove(projectile)
            #y 값 좌표를 넘어가면 enemy 지우기(missile enemy 때문)
            if enemy.y > self.game.size[1]:
                self.enemies_list.remove(enemy)

        
        #missile enemy 와 다른 pattern 에 나오는 enemy 는 별개로 둠(pattern enemy 는 destroy 시 다음패턴으로)
        for missile_enemy in list(self.missile_enemies_list):
            missile_enemy.update()
            if self.player.check_collision(missile_enemy):
                self.player.take_damage(1)
                self.missile_enemies_list.remove(missile_enemy)
            for projectile in list(missile_enemy.projectiles):
                if projectile.check_collision(self.player):
                    self.player.take_damage(10)
                    missile_enemy.projectiles.remove(projectile)

        #player projectile 관리
        for projectile in list(self.player.projectiles):
            for enemy in list(self.enemies_list):
                if projectile.check_collision(enemy):
                    enemy.take_damage(40)
                    if not enemy.alive:
                        self.enemies_list.remove(enemy)
                        self.player.increase_score(50)
                        self.game.score += 50 
                    self.player.projectiles.remove(projectile)
                    break
            for missile_enemy in list(self.missile_enemies_list):
                if projectile.check_collision(missile_enemy):
                    missile_enemy.take_damage(40)
                    if not missile_enemy.alive:
                        self.missile_enemies_list.remove(missile_enemy)
                        self.player.increase_score(50)
                        self.game.score += 50
                    #두개 물체가 영역이 겹치면 오류 발생하길래 널체크용으로 조건문을 넣었음
                    if(projectile in self.player.projectiles):
                        self.player.projectiles.remove(projectile)
                    break


        # 패턴 관리 -> 순차적으로 실행
        if not self.enemies_list and self.current_pattern_index < len(self.pattern_list) - 1:
            self.current_pattern_index += 1
            #self.current_pattern_index = 3
            self.enemies_list = self.pattern_list[self.current_pattern_index]()

        #패턴 완료시 ClearGameState 로 상태 변환
        if not self.enemies_list and self.current_pattern_index == len(self.pattern_list) - 1:
            self.game.change_state(ClearGameState(self.game))

        if pygame.time.get_ticks() % 5000 < 30: #계속해서 생성되는 랜덤 미사일
            self.missile_enemies_list.extend(self.pattern_generator.missile_pattern(random.randint(5, 10)))

        if self.player.hp <= 0:
            self.game.change_state(EndGameState(self.game))
            self.sound_bg.stop()

    def draw(self, screen):
        self.background.draw(screen)
        self.player.draw(screen)
        for enemy in self.enemies_list:
            enemy.draw(screen)
            for projectile in enemy.projectiles:
                projectile.draw(screen)
        for missile_enemy in self.missile_enemies_list:
            missile_enemy.draw(screen)
            for projectile in missile_enemy.projectiles:
                projectile.draw(screen)
        self.player.draw_score(screen, self.game.font)

class EndGameState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game.change_state(PlayingState(self.game))

    def draw(self, screen):
        #game.score 이랑 self.player.score 가 다른 이유 -> 객체에 있는 score 는 바로바로 화면에 나타내기 위함
        #game.player.score 는 playing game 내에서 실시간으로 점수 정보를 주기 위해서 따로 관리하는 것임
        screens.draw_endgame_screen(screen, self.game.size, self.game.font, self.game.score)
        
        
class ClearGameState(GameState):
    def draw(self, screen):
        screens.draw_endgame_clear_screen(screen, self.game.size, self.game.font, self.game.score)