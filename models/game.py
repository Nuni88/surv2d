from models.titlescene import TitleScene
from models.battlescene import BattleScene


class Game:
    def __init__(self):
        self.scene = TitleScene()
        self.run()

    def run(self):
        while True:
            stage = self.scene.run()
            self.scene = BattleScene()
            self.scene.run()
            self.scene = TitleScene()


if __name__ == '__main__':
    game = Game()
