class ConsoleUI:
    def __init__(self, board):
        self._b = board

    def run(self):
        while self._b.ongoing:
            ConsoleUI.print_board(self._b.matrix_board)
            selected_rank, selected_file = ConsoleUI.select_piece(self._b)

            selected_piece = self._b.get_piece(selected_rank, selected_file)
            moves = selected_piece.generate_moves(self._b)
            self.print_board(self._b.selected_board(selected_rank, selected_file))

            move = ConsoleUI.select_move(moves)
            if move is None:
                continue

            selected_piece.move(move, self._b)
            self._b.do_turn()

        print(f"\n\n Game Ended. Winner: {self._b.winner}")

    @staticmethod
    def print_board(b):
        print()

        rank_counter = 8
        s = ""
        for y in b:
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

    @staticmethod
    def select_piece(board):
        ok = False
        selected_rank, selected_file = 0, 0

        while not ok:
            selected_rank, selected_file = ConsoleUI.get_input("Select a piece: ")

            piece = board.get_piece(selected_rank, selected_file)
            if piece is None:
                print("Invalid input")
                continue

            if board.side_to_move == piece.isWhite:
                ok = True
            else:
                print("Invalid piece")

        return selected_rank, selected_file

    @staticmethod
    def select_move(moves):
        ok = False
        move = None
        while not ok:
            selected_rank, selected_file = ConsoleUI.get_input("Select a move: ")

            if (selected_rank, selected_file) == (None, None):
                return None

            if (selected_rank, selected_file) not in moves:
                print("Invalid input")
                continue

            move = (selected_rank, selected_file)
            ok = True

        return move

    @staticmethod
    def get_input(msg):
        ok = False
        selected_rank, selected_file = 0, 0
        while not ok:
            selection = input(msg)

            if selection.lower() == "back":
                return None, None

            if len(selection) != 2:
                print("Invalid input")
                continue

            try:
                selected_rank = 7 - (int(selection[1]) - 1)
                files = "abcdefgh"
                selected_file = files.find(selection[0].lower())
            except ValueError:
                print("Invalid input")
                continue

            if not (0 <= selected_rank <= 7) or not (0 <= selected_file <= 7):
                print("Invalid input")
                continue

            ok = True

        return selected_rank, selected_file
