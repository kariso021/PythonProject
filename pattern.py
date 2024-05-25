import random
import enemies

class PatternGenerator:
    def __init__(self, screen_width, screen_height, target):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target = target

    def random_pattern(self, num_enemies): #디버깅용으로 RandomPattern 만들어둔거라고 보면 됨 순차적으로 하는걸 목표로 둠
        enemy_types = [enemies.LoopingShooterEnemy,enemies.DownwardShooterEnemy]
        enemies_list = []
        for i in range(num_enemies):
            enemy_class = random.choice(enemy_types)
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(-100, -50)
            enemy = enemy_class(screen_width=self.screen_width, screen_height=self.screen_height, x=x, y=y)
            enemies_list.append(enemy)
        return enemies_list
    
    def Downwoard_pattern_1(self):
        enemy_type=enemies.DownwardShooterEnemy
        enemies_list = []
        for i in range (2):
            x= i*300+100
            y =100
            enemy=enemy_type(screen_width=self.screen_width, screen_height=self.screen_height,x=x,y=y,targetpoint=3*i)
            enemies_list.append(enemy)
        return enemies_list
    
    def Downwoard_pattern_2(self):
        enemy_type=enemies.DownwardShooterEnemy
        enemies_list = []
        for i in range (4):
            x= i*100//200
            y =100
            enemy=enemy_type(screen_width=self.screen_width, screen_height=self.screen_height,x=x,y=y,targetpoint=i)
            enemies_list.append(enemy)
        return enemies_list
    
    def BossPattern(self):
        enemy_type=enemies.BossEnemy
        enemies_list = []
        x=100
        y =0
        enemy=enemy_type(screen_width=self.screen_width, screen_height=self.screen_height,x=x,y=y)
        enemies_list.append(enemy)
        return enemies_list
    
    
    def LooppingShooterPattern(self):
        enemy_type=enemies.LoopingShooterEnemy
        enemies_list = []
        for i in range (4):
            x= 500-i*100
            y =400-(i*30+50)
            enemy=enemy_type(screen_width=self.screen_width, screen_height=self.screen_height,x=x,y=y)
            enemies_list.append(enemy)
        return enemies_list
    
    
    def missile_pattern(self, num_enemies):
        enemy_type=enemies.MissileEnemy
        enemies_list = []
        for i in range(num_enemies):
            enemy = enemy_type(target=self.target, screen_width=self.screen_width) #생성자 함수 불러온거
            enemies_list.append(enemy)
        return enemies_list