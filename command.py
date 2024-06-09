# command.py

class Command:
    def execute(self):
        pass

    def log(self, timestamp):
        return {'command': self.__class__.__name__, 'timestamp': timestamp} # 큐 형태의 작업공간에 저장을 시켜두는것

# 플레이어 커맨드
class MoveUpCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.move_up()

class MoveDownCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.move_down()

class MoveLeftCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.move_left()

class MoveRightCommand(Command):
    def __init__(self, player):
        self.player = player
        
    def execute(self):
        self.player.move_right()

class FireCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.fire()

# EnemyCommand 구현부
class MoveEnemyCommand(Command):
    def __init__(self, enemy):
        self.enemy = enemy

    def execute(self):
        self.enemy.move()

class ShootEnemyCommand(Command):
    def __init__(self, enemy):
        self.enemy = enemy

    def execute(self):
        self.enemy.shoot()
        