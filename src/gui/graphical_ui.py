import pygame
import sys

# map piece code to image name
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
            # Draw the UI
            self.draw_panel()
            self.draw_board()
            # Draw Pieces, function returns a list of the piece rectangles
            pieces = self.draw_pieces()

            # Generate moves if you have a piece selected
            moves = []
            if self._selected_piece is not None:
                moves = self.draw_moves(self._selected_piece, pieces)

            # Listen for window events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # If player clicks then...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (50, 0) < pygame.mouse.get_pos() < (850, 800):  # check if click is inside the board
                        # Get all of the pieces that are underneath the mouse when i click
                        clicked_pieces = [x for x in pieces if x.collidepoint(pygame.mouse.get_pos())]
                        clicked_moves = []

                        # If i already had a piece selected then...
                        if self._selected_piece is not None:
                            # get all of the moves for the selected piece that i clicked on
                            clicked_moves = [x for x in moves if x.collidepoint(pygame.mouse.get_pos())]

                        # Basically when i select a piece i draw the possible moves it can make
                        # and if my click actually intersects with one, then it means i get to make the move
                        if len(clicked_moves) > 0:  # Click intersects a move
                            # X and Y of the clicked move (in chess board coodinates), i get it by dividing the
                            # position (pixels) by the size of the drawn square
                            board_file = clicked_moves[0].x // self._square_size
                            board_rank = clicked_moves[0].y // self._square_size

                            # move the piece to the given coords (chess board coords)
                            self._selected_piece.move((board_rank, board_file), self._b)
                            # have no selected piece anymore
                            self._selected_piece = None
                            # go to next turn (_b is the board)
                            self._b.do_turn()
                        # If i don't click on a move, but i clicked on another piece then i swap
                        # the currently selected piece (or if i had no piece clicked select the one i just clicked)
                        elif len(clicked_pieces) > 0:  # Click intersects a piece
                            # Get board coords
                            board_file = clicked_pieces[0].x // self._square_size
                            board_rank = clicked_pieces[0].y // self._square_size
                            # Get selected piece
                            self._selected_piece = self._b.get_piece(board_rank, board_file) if self._b.get_piece(board_rank, board_file).isWhite == self._b.side_to_move else None

            # This ... should be the last thing in the main "display" loop of pygame but don't ask me why
            # Look up what it does cus idk :))
            pygame.display.flip()

    def draw_panel(self):
        # Draw..something, i forgot that this panel is exactly, if i remove it it looks the same
        pygame.draw.rect(self._screen, self._panel_color,
                         (850, 0, 400, 850))

    def draw_board(self):
        pos_y = 0
        # draw the board squares
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
        # I forgot i even have borders, but oh well
        # These are just rectangles around the board
        pygame.draw.rect(self._screen, self._border_color,
                         (50, 0, self._border_size, 800))
        pygame.draw.rect(self._screen, self._border_color,
                         (50, 800, 800, self._border_size))
        pygame.draw.rect(self._screen, self._border_color,
                         (850, 0, 5, 800))

    def draw_pieces(self):
        images = []

        # Draw pieces and return them as rectangles in an array
        rank_offset = 0
        # matrix_board returns the board as a...matrix of characters

        #   r n b q k b n r
        #   p p p p p p p p
        #   . . . . . . . .
        #   . . . . . . . .
        #   . . . . . . . .
        #   . . . . . . . .
        #   P P P P P P P P
        #   R N B Q K B N R

        # This is how a standard starting board would look like (in character matrix form
        # Take every row
        for rank in self._b.matrix_board:
            file_offset = 0 # offset so you draw the image where you need to (cus board coord != screen coord)
            # Take every element of the row 1 by 1
            for file in rank:
                f = "assets/"
                # if we have a piece there then we ...
                if file != '.':
                    # Piece map is a link between a piece code (in the FEN string) and a name
                    f += piece_map[file]
                    f += ".png"

                    # Load the image "assets/[name].png
                    img = pygame.image.load(f)
                    # Scale it to fit the board square
                    img = pygame.transform.smoothscale(img, (100, 100))
                    # _screen.blit draws the image to the screen and returns a Rectangle object with its data
                    # add it to the return array
                    images.append(self._screen.blit(img, (50+file_offset, rank_offset)))
                # Traverse the board
                file_offset += self._square_size
            rank_offset += self._square_size

        # Return array of rects representing the pieces
        return images

    def draw_moves(self, sel_piece, pieces):
        # Draw the possible moves for a selected piece (sel_piece)
        images = []
        # Load the images
        f = "assets/selection.png"
        at = "assets/attack.png"

        # Same story as for the pieces but ...
        # selected_board contains * in the places where the selected piece can move
        rank_offset = 0
        for rank in self._b.selected_board(sel_piece.rank, sel_piece.file):
            file_offset = 0
            for file in rank:
                if file == '*':
                    # If there is a piece on that place place the attack texture
                    if (50 + file_offset, rank_offset, self._square_size, self._square_size) in pieces:
                        img = pygame.image.load(at)
                        img = pygame.transform.smoothscale(img, (100, 100))
                        images.append(self._screen.blit(img, (50 + file_offset, rank_offset)))
                    # else place the selection (move) texture
                    else:
                        img = pygame.image.load(f)
                        img = pygame.transform.smoothscale(img, (100, 100))
                        images.append(self._screen.blit(img, (50 + file_offset, rank_offset)))
                file_offset += self._square_size
            rank_offset += self._square_size

        return images
