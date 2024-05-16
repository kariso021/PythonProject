import random
import enemies

class PatternGenerator:
    def __init__(self, screen_width, target):
        self.screen_width = screen_width
        self.target = target

    def random_pattern(self, num_enemies):
        enemy_types = [ enemies.HomingEnemy, enemies.LoopingShooterEnemy, enemies.DownwardShooterEnemy]
        enemies_list = []
        for i in range(num_enemies):
            enemy_class = random.choice(enemy_types)
            if enemy_class == enemies.HomingEnemy:
                enemy = enemy_class(target=self.target, screen_width=self.screen_width)
            else:
                x = random.randint(0, self.screen_width - 50) 
                y = random.randint(-100, -50)  
                enemy = enemy_class(x=x, y=y)
            enemies_list.append(enemy)
        return enemies_list