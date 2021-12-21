class Piece:
    def __init__(self, file, rank, white):
        self.file = file
        self.rank = rank
        self.isWhite = white
        self.pieceCode = ''
        self.taken = False

    def __str__(self):
        return f"{self.pieceCode} at {self.rank} {self.file}"

    def generate_moves(self, board):
        return []

    def move(self, m, board):
        destination = board.get_piece(m[0], m[1])
        if destination is not None:
            destination.taken = True

        self.rank = m[0]
        self.file = m[1]

    @staticmethod
    def in_bounds(rank, file):
        if not (0 <= rank <= 7) or not (0 <= file <= 7):
            return False
        return True


class Rook(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'r'
        self._directions = [(1, 0),
                            (0, 1),
                            (-1, 0),
                            (0, -1)]

    def generate_moves(self, board):
        moves = []
        for direction in self._directions:
            x = self.file
            y = self.rank

            x += direction[0]
            y += direction[1]
            while Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))
                x += direction[0]
                y += direction[1]

            if board.has_piece(y, x):
                if not (board.get_piece(y, x).isWhite == self.isWhite):
                    moves.append((y, x))

        return moves


class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'b'
        self._directions = [(1, -1),
                            (-1, 1),
                            (1, 1),
                            (-1, -1)]

    def generate_moves(self, board):
        moves = []
        for direction in self._directions:
            x = self.file
            y = self.rank

            x += direction[0]
            y += direction[1]
            while Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))
                x += direction[0]
                y += direction[1]

            if board.has_piece(y, x):
                if not (board.get_piece(y, x).isWhite == self.isWhite):
                    moves.append((y, x))

        return moves


class Queen(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'q'
        self._directions = [(0, 1),
                            (-1, 0),
                            (1, -1),
                            (-1, 1),
                            (1, 1),
                            (-1, -1),
                            (1, 0),
                            (0, -1)]

    def generate_moves(self, board):
        moves = []
        for direction in self._directions:
            x = self.file
            y = self.rank

            x += direction[0]
            y += direction[1]
            while Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))
                x += direction[0]
                y += direction[1]

            if board.has_piece(y, x):
                if not (board.get_piece(y, x).isWhite == self.isWhite):
                    moves.append((y, x))

        return moves


class King(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'k'
        self._directions = [(0, 1),
                            (1, 0),
                            (0, -1),
                            (-1, 0),
                            (1, 1),
                            (1, -1),
                            (-1, -1),
                            (-1, 1)]

    def generate_moves(self, board):
        moves = []
        for direction in self._directions:
            x = self.file
            y = self.rank

            x += direction[0]
            y += direction[1]
            if Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))

            if board.has_piece(y, x):
                if not (board.get_piece(y, x).isWhite == self.isWhite):
                    moves.append((y, x))

        return moves


class Knight(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'n'
        self._directions = [(2, 1),
                            (1, 2),
                            (2, -1),
                            (-1, 2),
                            (-2, 1),
                            (-1, -2),
                            (1, -2),
                            (-2, -1)]

    def generate_moves(self, board):
        moves = []
        for direction in self._directions:
            x = self.file
            y = self.rank

            x += direction[0]
            y += direction[1]
            if Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))

            if board.has_piece(y, x):
                if not (board.get_piece(y, x).isWhite == self.isWhite):
                    moves.append((y, x))

        return moves


class Pawn(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'p'
        self._directions = [(0, 1),
                            (1, 1),
                            (-1, 1)]

    def generate_moves(self, board):
        moves = []

        x = self.file
        y = self.rank

        if not self.isWhite:
            x += self._directions[0][0]
            y += self._directions[0][1]
            if Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))

            x = self.file + self._directions[1][0]
            y = self.rank + self._directions[1][1]
            if Piece.in_bounds(y, x) and board.has_piece(y, x):
                if board.get_piece(y, x).isWhite != self.isWhite:
                    moves.append((y, x))

            x = self.file + self._directions[2][0]
            y = self.rank + self._directions[2][1]
            if Piece.in_bounds(y, x) and board.has_piece(y, x):
                if board.get_piece(y, x).isWhite != self.isWhite:
                    moves.append((y, x))

            if self.rank == 1:
                x = self.file + 0
                y = self.rank + 2
                if not board.has_piece(y, x):
                    moves.append((y, x))
        else:
            x -= self._directions[0][0]
            y -= self._directions[0][1]
            if Piece.in_bounds(y, x) and not board.has_piece(y, x):
                moves.append((y, x))

            x = self.file - self._directions[1][0]
            y = self.rank - self._directions[1][1]
            if Piece.in_bounds(y, x) and board.has_piece(y, x):
                if board.get_piece(y, x).isWhite != self.isWhite:
                    moves.append((y, x))

            x = self.file - self._directions[2][0]
            y = self.rank - self._directions[2][1]
            if Piece.in_bounds(y, x) and board.has_piece(y, x):
                if board.get_piece(y, x).isWhite != self.isWhite:
                    moves.append((y, x))

            if self.rank == 6:
                x = self.file - 0
                y = self.rank - 2
                if not board.has_piece(y, x):
                    moves.append((y, x))

        return moves
