class ConsoleUI:
    def __init__(self, board):
        self._b = board

    def run(self):
        self.print_board()

    def print_board(self):
        rank_counter = 8
        s = ""
        for y in self._b.matrix_board:
            s += str(rank_counter) + ".\t"
            for x in y:
                s += x
                s += " "
            s += "\n"
            rank_counter -= 1
        s += "\nX.\t"
        for x in "ABCDEFGH":
            s += x + " "
        print(s)
