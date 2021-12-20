from src.board.board import Board

from src.ui.console_ui import ConsoleUI
from src.gui.graphical_ui import GUI


class Game:
    def __init__(self, mode):
        self.lines = ""
        with open("settings.properties", "r") as f:
            self.lines = f.readlines()

        temp_fen = self.lines[0].split("=")[1].strip()  # real cursed stuff
        self.start_fen = temp_fen[1:len(temp_fen)-1]  # more real cursed stuff
        self._b = Board(self.start_fen)

        if mode != "console":
            self._ui = GUI(self._b)
        else :
            self._ui = ConsoleUI(self._b)

    def start(self):
        self._ui.run()


if __name__ == "__main__":
    game = Game("console")
    game.start()
