import pygame
import sys

piece_map = {
    'b': "b-bishop",
    'p': "b-pawn",
    'n': "b-knight",
    'r': "b-rook",
    'k': "b-king",
    'q': "b-queen",
    'B': "w-bishop",
    'P': "w-pawn",
    'N': "w-knight",
    'R': "w-rook",
    'K': "w-king",
    'Q': "w-queen"
}


class GUI:
    def __init__(self, board):
        self._size = width, height = 1250, 850
        self._b = board

        self._square_size = 100
        self._square_color = (238, 238, 210)
        self._square_color_alt = (118, 150, 85)

        self._panel_color = (50, 46, 43)
        self._border_color = (0, 0, 0)

        self._border_size = 5

        pygame.init()
        self._screen = pygame.display.set_mode(self._size)

        self._selected_piece = None

        pygame.display.set_caption("Chess")

    def run(self):
        self._screen.fill(self._panel_color)
        pygame.display.update()

        while 1:
            self.draw_panel()
            self.draw_board()
            pieces = self.draw_pieces()

            moves = []
            if self._selected_piece is not None:
                moves = self.draw_moves(self._selected_piece, pieces)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (50, 0) < pygame.mouse.get_pos() < (850, 800):  # check if click is inside the board
                        clicked_pieces = [x for x in pieces if x.collidepoint(pygame.mouse.get_pos())]
                        clicked_moves = []

                        if self._selected_piece is not None:
                            clicked_moves = [x for x in moves if x.collidepoint(pygame.mouse.get_pos())]

                        if len(clicked_moves) > 0:  # Click intersects a piece
                            board_file = clicked_moves[0].x // self._square_size
                            board_rank = clicked_moves[0].y // self._square_size

                            self._selected_piece.move((board_rank, board_file), self._b)
                            self._selected_piece = None
                        elif len(clicked_pieces) > 0:  # Click intersects a piece
                            board_file = clicked_pieces[0].x // self._square_size
                            board_rank = clicked_pieces[0].y // self._square_size
                            self._selected_piece = self._b.get_piece(board_rank, board_file)



            # TODO: mouse click detection and all the other stuff
            pygame.display.flip()

    def draw_panel(self):
        pygame.draw.rect(self._screen, self._panel_color,
                         (850, 0, 400, 850))

    def draw_board(self):
        pos_y = 0
        for i in range(8):
            pos_x = 50
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self._screen, self._square_color,
                                     (pos_x, pos_y, self._square_size, self._square_size))
                else:
                    pygame.draw.rect(self._screen, self._square_color_alt,
                                     (pos_x, pos_y, self._square_size, self._square_size))
                pos_x += self._square_size
            pos_y += self._square_size

    def draw_borders(self):
        pygame.draw.rect(self._screen, self._border_color,
                         (50, 0, self._border_size, 800))
        pygame.draw.rect(self._screen, self._border_color,
                         (50, 800, 800, self._border_size))
        pygame.draw.rect(self._screen, self._border_color,
                         (850, 0, 5, 800))

    def draw_pieces(self):
        images = []

        rank_offset = 0
        for rank in self._b.matrix_board:
            file_offset = 0
            for file in rank:
                f = "assets/"
                if file != '.':
                    f += piece_map[file]
                    f += ".png"

                    img = pygame.image.load(f)
                    img = pygame.transform.smoothscale(img, (100, 100))
                    images.append(self._screen.blit(img, (50+file_offset, rank_offset)))
                file_offset += self._square_size
            rank_offset += self._square_size

        return images

    def draw_moves(self, sel_piece, pieces):
        images = []
        f = "assets/selection.png"
        at = "assets/attack.png"

        rank_offset = 0
        for rank in self._b.selected_board(sel_piece.rank, sel_piece.file):
            file_offset = 0
            for file in rank:
                if file == '*':
                    if (50 + file_offset, rank_offset, self._square_size, self._square_size) in pieces:
                        img = pygame.image.load(at)
                        img = pygame.transform.smoothscale(img, (100, 100))
                        images.append(self._screen.blit(img, (50 + file_offset, rank_offset)))
                    else:
                        img = pygame.image.load(f)
                        img = pygame.transform.smoothscale(img, (100, 100))
                        images.append(self._screen.blit(img, (50 + file_offset, rank_offset)))
                file_offset += self._square_size
            rank_offset += self._square_size

        return images
