class Piece:
    def __init__(self, file, rank, white):
        self.file = file
        self.rank = rank
        self.isWhite = white
        self.pieceCode = ''
        self.taken = False


class Rook(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'r'


class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'b'


class Queen(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'q'


class King(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'k'


class Knight(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'n'


class Pawn(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.pieceCode = 'p'
