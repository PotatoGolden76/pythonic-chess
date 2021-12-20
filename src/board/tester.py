import unittest
from src.board.piece import Pawn, Rook, Bishop, Knight, King, Queen
from src.board.board import Board


class TestBoard(unittest.TestCase):
    def test_board_constructor(self):
        b = Board("8/rbknpq2/8/8/8/8/RBKNPQ2/8 w KQkq")
        self.assertEqual(b._sideToMove, 0)

        b = Board("8/rbknpq2/8/8/8/8/RBKNPQ2/8 b KQkq")
        self.assertEqual(b._sideToMove, 1)

        ls = [Rook, Bishop, King, Knight, Pawn, Queen]
        for i in b._whitePieces:
            ls.append(type(i))

        for i in range(len(b._whitePieces)):
            self.assertEqual(type(b._whitePieces[i]), ls[i])

        for i in range(len(b._blackPieces)):
            self.assertEqual(type(b._blackPieces[i]), ls[i])

    def test_matrix_board(self):
        b = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")
        s = ""
        for y in b.matrix_board:
            for x in y:
                s += x
        self.assertEqual(s, "rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR")

    def test_fen_parsing(self):
        b = Board("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq")
        self.assertEqual(b.fen, "rnbqkbnr/8/8/8/8/8/8/RNBQKBNR")

        # TODO: add support for side-to-move, castling and possibly full FEN notation
