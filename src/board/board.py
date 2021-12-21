from src.board.piece import Pawn, Rook, Bishop, Knight, King, Queen


class Board:
    def __init__(self, initial_fen):
        self._whitePieces = []
        self._blackPieces = []
        self._sideToMove = 1  # 1 - White / 0 - Black

        self.fen = initial_fen

        self._ongoing = True
        self._winner = None

    @property
    def fen(self):
        fen_string = ""
        for rank in self.matrix_board:
            blanks = 0
            for file in rank:
                if file != '.':
                    if blanks != 0:
                        fen_string += str(blanks)
                    blanks = 0
                    fen_string += file
                else:
                    blanks += 1
            if blanks != 0:
                fen_string += str(blanks)
            fen_string += "/"

        # TODO: add support for side-to-move, castling and possibly full FEN notation

        fen_string = fen_string[:-1]
        return fen_string

    @fen.setter
    def fen(self, fen_string):
        """
        Set board position using a FEN string

        IMPORTANT: Using minimal FEN, only first three fields in use: pieces, side to move, castling
        TODO: Support full FEN

        :param fen_string: FEN string of the position
        """

        fields = fen_string.split(" ")
        ranks = fields[0].split("/")

        for ranks_cursor in range(len(ranks)):
            file_cursor = 0
            for char in ranks[ranks_cursor]:
                if '0' <= char <= '9':
                    file_cursor += int(char)
                else:
                    if char.islower():
                        match char:
                            case 'r':
                                self._blackPieces.append(Rook(file_cursor, ranks_cursor, False))
                            case 'b':
                                self._blackPieces.append(Bishop(file_cursor, ranks_cursor, False))
                            case 'k':
                                self._blackPieces.append(King(file_cursor, ranks_cursor, False))
                            case 'n':
                                self._blackPieces.append(Knight(file_cursor, ranks_cursor, False))
                            case 'p':
                                self._blackPieces.append(Pawn(file_cursor, ranks_cursor, False))
                            case 'q':
                                self._blackPieces.append(Queen(file_cursor, ranks_cursor, False))
                    else:
                        match char.lower():
                            case 'r':
                                self._whitePieces.append(Rook(file_cursor, ranks_cursor, True))
                            case 'b':
                                self._whitePieces.append(Bishop(file_cursor, ranks_cursor, True))
                            case 'k':
                                self._whitePieces.append(King(file_cursor, ranks_cursor, True))
                            case 'n':
                                self._whitePieces.append(Knight(file_cursor, ranks_cursor, True))
                            case 'p':
                                self._whitePieces.append(Pawn(file_cursor, ranks_cursor, True))
                            case 'q':
                                self._whitePieces.append(Queen(file_cursor, ranks_cursor, True))
                    file_cursor += 1

        if fields[1] == "w":
            self._sideToMove = 1
        else:
            self._sideToMove = 0

        # TODO: parse castling rights

    @property
    def matrix_board(self):
        mat = []
        for col in range(0, 8):
            y = ['.', '.', '.', '.', '.', '.', '.', '.']
            mat.append(y)
        for piece in self._whitePieces:
            if not piece.taken:
                mat[piece.rank][piece.file] = piece.pieceCode.upper()
        for piece in self._blackPieces:
            if not piece.taken:
                mat[piece.rank][piece.file] = piece.pieceCode.lower()
        return mat

    @property
    def ongoing(self):
        return self._ongoing

    @property
    def winner(self):
        return self._winner

    @property
    def side_to_move(self):
        return self._sideToMove

    def get_piece(self, rank, file):
        for i in self._whitePieces:
            if i.rank == rank and i.file == file and not i.taken:
                return i

        for i in self._blackPieces:
            if i.rank == rank and i.file == file and not i.taken:
                return i

        return None

    def has_piece(self, rank, file):
        for i in self._whitePieces:
            if i.rank == rank and i.file == file and not i.taken:
                return True

        for i in self._blackPieces:
            if i.rank == rank and i.file == file and not i.taken:
                return True

        return False

    def selected_board(self, rank, file):
        piece = self.get_piece(rank, file)
        mat = self.matrix_board
        moves = piece.generate_moves(self)

        for m in moves:
            mat[m[0]][m[1]] = "*"

        return mat

    def do_turn(self):
        if self._sideToMove:
            self._sideToMove = 0
        else:
            self._sideToMove = 1