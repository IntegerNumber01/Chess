# Completed beginning of October 2023

import pygame
import pandas
import numpy
import pieces
import chessAPI
import ai
import string
from exe_image_loader import resource_path

# Initalize
pygame.init()
pygame.display.set_caption('Chess')

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load new icon
# icon = resource_path('../Chess/Pixel Python Logo.png')
icon = pygame.image.load('C:/Users/arjun/OneDrive - Hindupedia/Documents/Chess/Pixel Python Logo.png')
# icon = pygame.image.load(icon)
pygame.display.set_icon(icon)
font = pygame.font.SysFont('CenturyGothic', 40)

# Pawn:   P
# Rook:   R
# Bishop: B
# Knight: N
# King:   K
# Queen:  Q

# Black:         (0, 0, 0)
# White:         (255, 255, 255)
# Greyish:       (61, 61, 61)
# Darkish Blue:  (79, 128, 191)
# Lightish Blue: (124, 161, 191)
# Beige:         (240, 217, 181)
# Easy Brown:    (181, 136, 99)

# Settings
# Variables starting with "__" are setting variables that the user can change
__show_legal_moves = True
__ai_plays = False
__ai_side = 'black'


class ChessGame:
    def __init__(self, __show_legal_moves, __ai_side, fen=None):
        '''
        ``__show_legal_moves`` and ``__ai_side`` are user defined variables.

        Set ``__ai_side`` to ``None`` if AI do'es not play. Otherwise, input
        which side AI should play ``'white'`` / ``'black'``
        '''
        # User set variables
        self.__show_legal_moves = __show_legal_moves
        self.__ai_side = __ai_side

        if fen is None:
            self.api = chessAPI.Board()
        else:
            self.api = chessAPI.Board(fen)

        # self.ai = ai.Ai(self.api.get_board(), __ai_side)
        fen = self.api.get_board()
        self.board = self.fen_to_dataframe(fen)

        self.legal_moves = []
        self.board_history = [self.board]

        if __ai_side == self.api.turn:
            self.move_ai = True
        else:
            self.move_ai = False

        self.check_show = False
        self.mouse_down = False
        self.moving = False
        self.show_legal_moves = False
        self.checkmate = False
        self.draw = False
        self.blink_on = True
        self.blink_enabled = True
        self.show_promotion_choices = False
        self.chose_piece = False
        self.starting_pos = None
        self.ending_pos = None
        self.prev_starting_pos = None
        self.saved = self.api.get_board()

        # None values
        self.winner = None  # 'white' / 'black'
        self.promotion_coords = None  # (x, y)
        self.pawn_to_move = None
        self.no_render = None
        # Dictionaries
        self.promotion_choices = {}

        # Everything else
        self.last_blink_time = pygame.time.get_ticks()
        self.index = 0
        self.turn = 'white'

        # Time format [minutes, seconds]
        # White time
        self.white_time = [4, 23]
        # Black time
        self.black_time = [3, 55]

        self.TILE_SIZE = 75
        self.BACKGROUND_COLOR = (23, 21, 19)
        self.LIGHT_COLOR = (240, 217, 181)
        self.DARK_COLOR = (181, 136, 99)

        coordinates = self.render_board()
        self.hitboxes = self.generate_hitboxes(coordinates)
        self.pieces = pieces.Pieces(screen, 0.22)

        # Normal move indicator
        self.move_indicator = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.move_indicator.fill((201, 201, 201, 230))

        # Attacking move indicator
        self.attack_indicator = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE),
                                               pygame.SRCALPHA)
        self.attack_indicator.fill((0, 0, 0, 0))
        outline_color = (201, 201, 201, 230)
        pygame.draw.rect(self.attack_indicator, outline_color,
                         self.attack_indicator.get_rect(), 5)

        # Check indicator
        self.check_indicator = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE),
                                              pygame.SRCALPHA)
        self.check_indicator.fill((250, 50, 50, 230))

        # Yellow starting position and ending position indicator
        self.position_indicator = pygame.Surface((self.TILE_SIZE,
                                                  self.TILE_SIZE),
                                                 pygame.SRCALPHA)
        self.position_indicator.fill((245, 215, 105, 125))

        # TEMP
        self.num_moves = 0

    def ai_play(self):
        '''
        Checks if AI can move and moves automatically

        Can be placed in main loop
        '''
        if self.move_ai:
            print(self.api.get_board())
            print('AI PLAYED')
            fen = self.ai.move(self.api.get_board())
            self.api.set_board(fen)
            self.board = self.fen_to_dataframe(fen)
            self.board_history.append(self.board.copy())
            self.move_ai = False
            self.turn = self.api.turn

            self.handle_game_state()

    def get_board_coords(self, board):
        '''
        Returns all the elements in the board
        (or any DataFrame)
        '''

        storage = []

        for x in board.index:
            for y in board.columns:
                storage.append((x, y))

        return storage

    def create_chess_dict(self, board):
        chess_dict = {}

        # Convert index and columns to list
        index_list = list(board.index)
        columns_list = list(board.columns)

        # Iterate over columns (vertical axis of chessboard, a-h)
        for i, col in enumerate(columns_list):
            # Iterate over index (horizontal axis of chessboard, 1-8)
            for j, row in enumerate(index_list):
                # Construct dictionary key in the format letter+number (e.g., 'a1')
                # Convert i and j to proper chess notation (a-h and 1-8)
                key = f'{string.ascii_lowercase[i]}{8 - j}'

                # Construct dictionary value as a tuple (col, row)
                value = (col, row)

                # Add to dictionary
                chess_dict[key] = value

        return chess_dict

    def to_coords(self, board, notation):
        '''
        Converts standard chess notation into matrix coordinates
        '''

        chess_map = self.create_chess_dict(board)
        if notation[-1] == 'q' or notation[-1] == 'r' or notation[-1] == 'b' or notation[-1] == 'n':
            notation = notation[:-1]

        return chess_map[notation]

    def to_notation(self, board, coords):
        '''
        Converts coords to standard chess notation
        '''

        chess_map = self.create_chess_dict(board)
        flipped = {value: key for key, value in chess_map.items()}

        return flipped[coords]

    def fen_to_dataframe(self, fen):
        '''
        Converts FEN to data frame
        '''

        data = {
            150: ['', '', '', '', '', '', '', ''],
            225: ['', '', '', '', '', '', '', ''],
            300: ['', '', '', '', '', '', '', ''],
            375: ['', '', '', '', '', '', '', ''],
            450: ['', '', '', '', '', '', '', ''],
            525: ['', '', '', '', '', '', '', ''],
            600: ['', '', '', '', '', '', '', ''],
            675: ['', '', '', '', '', '', '', ''],
        }

        board = pandas.DataFrame(data,
                                 index=[150, 225, 300, 375, 450, 525, 600, 675])

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        # Fills in the board
        for row_num, row in enumerate(rows):
            if not row == '8':
                i = 150
                for char in row:
                    if char.isdigit():
                        i += int(char) * 75
                    elif char.isalpha():
                        board.loc[i, 150 + (row_num * 75)] = char
                        i += 75

        return board

    def find_piece(self, board, piece):
        '''
        Returns the coordinates of the piece on the board
        '''

        result = numpy.where(board == piece)

        # If the entry was found, return the first pair of coordinates
        if result[0].size > 0:
            return (board.index[result[0][0]], board.columns[result[1][0]])
        else:
            return None

    def mouse_button_down_logic(self):
        '''
        Detects for event type, therefore, must be placed inside main pygame
        event detection loop
        '''

        if not self.turn == self.__ai_side:
            # Left click
            if event.button == 1 and self.board.equals(self.board_history[-1]):
                mouseX, mouseY = pygame.mouse.get_pos()

                self.snapped_piece = self.find_mouse_tile(mouseX, mouseY)

                # Returns if user clicks outside of chess board
                if self.snapped_piece is None:
                    return

                self.board = self.fen_to_dataframe(self.api.get_board())

                self.start = self.to_notation(self.board, self.snapped_piece)

                if self.show_promotion_choices:
                    self.show_legal_moves = False
                    self.clicked_out = True
                    for name, val in self.promotion_choices.items():
                        if val == self.snapped_piece:
                            self.start = self.to_notation(self.board,
                                                          self.pawn_to_move)

                            if self.api.turn == 'white':
                                end = self.start[0] + '1'
                            else:
                                end = self.start[0] + '8'

                            uci = self.start + end + name.lower()
                            self.api.undo_move()
                            self.api.switch_turn()
                            self.api.move(uci)

                            if name.islower():
                                self.king = 'K'
                            else:
                                self.king = 'k'

                            self.clicked_out = False

                            break

                    self.show_promotion_choices = False

                    if self.clicked_out is False:
                        if self.turn == 'white':
                            self.turn = 'black'
                        else:
                            self.turn = 'white'

                        self.handle_game_state()
                        if not (self.checkmate or self.draw):
                            self.move_ai = True
                    else:
                        self.api.undo_move()
                        self.api.switch_turn()

                    self.board_history = []
                    for fen in self.api.get_board_history():
                        self.board_history.append(self.fen_to_dataframe(fen))

                    self.board = self.board_history[-1].copy()

                else:
                    self.piece_name = self.board.loc[self.snapped_piece[0],
                                                     self.snapped_piece[1]]
                    if not self.piece_name == '':
                        self.prev_starting_pos = self.starting_pos
                        self.starting_pos = self.snapped_piece

                    if ((self.piece_name.isupper() and self.api.turn == 'white') or
                       (self.piece_name.islower() and self.api.turn == 'black')):
                        notation_moves = self.api.get_legal_moves(self.start)
                        self.legal_moves = []
                        for notation in notation_moves:
                            self.legal_moves.append(self.to_coords(self.board,
                                                                   notation))

                        self.mouse_down = True
                        self.show_legal_moves = True

    def mouse_button_up_logic(self):
        '''
        Detects for event type, therefore, must be placed inside main pygame
        event detection loop
        '''

        if self.mouse_down:
            self.mouse_down = False
            self.no_render = None
            mouseX, mouseY = pygame.mouse.get_pos()
            self.destination = self.find_mouse_tile(mouseX, mouseY)

            if self.destination in self.legal_moves:
                self.num_moves += 1
                self.promotion_coords = self.destination

                uci = self.start + self.to_notation(self.board,
                                                    self.destination)
                self.api.move(uci)
                self.ending_pos = self.destination
                self.prev_starting_pos = None

                self.index += 1

                self.legal_moves = []

                if self.piece_name.islower():
                    self.king = 'K'
                else:
                    self.king = 'k'

                self.handle_game_state()

                # About to present the choices
                if self.api.pawn_promotion:
                    self.show_promotion_choices = True
                    self.show_legal_moves = False
                    self.pawn_to_move = self.snapped_piece
                elif not (self.checkmate or self.draw):
                    # self.move_ai = True
                    pass
                    if self.turn == 'white':
                        self.turn = 'black'
                    else:
                        self.turn = 'white'

                self.board_history = []
                for board in self.api.get_board_history():
                    self.board_history.append(self.fen_to_dataframe(board))

                self.board = self.board_history[-1].copy()

    def timer_logic(self):
        '''
        Detects for event type, therefore, must be placed inside main pygame
        event detection loop
        '''

        # Time variable format: [minutes, seconds]

        if self.turn == 'white':  # White timer logic
            if self.white_time[1] == 0 and not self.white_time[0] == 0:
                pygame.time.set_timer(TIMER_EVENT, 1000)
                self.white_time[1] = 60

                if self.white_time[0] > 0:
                    self.white_time[0] -= 1

            self.white_time[1] -= 1

            # White runs out of time
            if self.white_time[0] == 0 and self.white_time[1] == 0:
                pygame.time.set_timer(TIMER_EVENT, 0)
                self.winner = 'black'
        else:  # Black timer logic
            if self.black_time[1] == 0 and not self.black_time[0] == 0:
                pygame.time.set_timer(TIMER_EVENT, 1000)
                self.black_time[1] = 60

                if self.black_time[0] > 0:
                    self.black_time[0] -= 1

            self.black_time[1] -= 1

            # Black runs out of time
            if self.black_time[0] == 0 and self.black_time[1] == 0:
                pygame.time.set_timer(TIMER_EVENT, 0)
                self.winner = 'white'

    def handle_move_navigation(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:  # Go back one move
            if self.index > 0:
                pygame.time.delay(150)
                self.index -= 1
                self.board = self.board_history[self.index].copy()
        if keys_pressed[pygame.K_RIGHT]:  # Go forward one move
            if self.index < len(self.board_history) - 1:
                pygame.time.delay(150)
                self.index += 1
                self.board = self.board_history[self.index].copy()
        if keys_pressed[pygame.K_UP]:   # Go to last move
            self.index = len(self.board_history) - 1
            self.board = self.board_history[self.index].copy()
        if keys_pressed[pygame.K_DOWN]:  # Go to inital board
            self.index = 0
            self.board = self.board_history[self.index].copy()

    def handle_game_state(self):
        if self.api.game_state()[0] == 'check':
            self.check_show = True
            self.blink_enabled = True
            self.checked_king = self.king
        elif self.api.game_state()[0] == 'checkmate':
            self.checkmate = True
            self.checked_king = self.king
        elif self.api.game_state()[0] == 'draw':
            self.draw = True
        else:
            self.blink_enabled = False

    def find_mouse_tile(self, mouseX, mouseY):
        '''
        Finds which tile coordinate the mouse is at
        '''
        for i in range(len(self.hitboxes)):
            left = self.hitboxes[i][0]
            right = self.hitboxes[i][1]
            up = self.hitboxes[i][2]
            down = self.hitboxes[i][3]

            if mouseX >= left and mouseX <= right:
                if mouseY >= up and mouseY <= down:
                    return (left, up)

    def generate_hitboxes(self, coordinates):
        '''
        Creates hitboxes
        '''
        storage = []

        for i in range(len(coordinates)):
            coordinateX = coordinates[i][0]
            coordinateY = coordinates[i][1]
            storage.append((coordinateX,
                            coordinateX + self.TILE_SIZE,
                            coordinateY,
                            coordinateY + self.TILE_SIZE
                            )
                           )

        return storage

    def render_board(self):
        '''
        Creates the board and returns all coordinates
        '''
        boardX = 140
        boardY = 140

        tileX = boardX + 10 + self.TILE_SIZE  # Light tile first
        tileY = boardY + 10

        coordinates = []

        alternate_tile = True

        # Blank board
        pygame.draw.rect(screen, self.LIGHT_COLOR, (boardX, boardY, 620, 620))

        # Adding color tiles
        for a in range(8):
            for b in range(4):
                pygame.draw.rect(screen, self.DARK_COLOR, (tileX, tileY,
                                 self.TILE_SIZE, self.TILE_SIZE))

                # If there is a colored tile in front
                if alternate_tile is False:
                    coordinates.append((tileX, tileY))
                    coordinates.append((tileX + self.TILE_SIZE, tileY))
                else:
                    coordinates.append((tileX - self.TILE_SIZE, tileY))
                    coordinates.append((tileX, tileY))

                tileX = tileX + (self.TILE_SIZE * 2)

            tileX = (boardX + 10) + ((a % 2) * self.TILE_SIZE)
            tileY = tileY + self.TILE_SIZE

            # Alternating starting tile
            if tileX == boardX + 10:
                alternate_tile = False
            else:
                alternate_tile = True

        return coordinates

    def render_pieces(self, board):
        listed_board = board.values.flatten().tolist()
        board_coords = self.get_board_coords(board)

        for i in range(len(listed_board)):  # Rendering pieces
            piece = listed_board[i]
            if not piece == '':
                coords = (board_coords[i][0], board_coords[i][1])
                if not self.no_render == coords:
                    self.pieces.render(piece, (coords[0] + (self.TILE_SIZE / 2),
                                               coords[1] + (self.TILE_SIZE / 2)), None)

    def handle_and_display_promotion_gui(self):
        if self.api.pawn_promotion and self.show_promotion_choices:
            x, y = self.destination
            if self.piece_name.islower():
                self.promotion_choices = {'q': (x, y),
                                          'n': (x, y - self.TILE_SIZE),
                                          'r': (x, y - (self.TILE_SIZE * 2)),
                                          'b': (x, y - (self.TILE_SIZE * 3))
                                          }
                pygame.draw.rect(screen, 'white', (self.destination[0],
                                                   self.destination[1] - (self.TILE_SIZE * 3), self.TILE_SIZE, self.TILE_SIZE * 4))
                x, y = x + (self.TILE_SIZE / 2), y + (self.TILE_SIZE / 2)
                self.pieces.render('q', (x, y), None)
                self.pieces.render('n', (x, y - self.TILE_SIZE), None)
                self.pieces.render('r', (x, y - (self.TILE_SIZE * 2)), None)
                self.pieces.render('b', (x, y - (self.TILE_SIZE * 3)), None)
            else:
                self.promotion_choices = {'Q': (x, y),
                                          'N': (x, y + self.TILE_SIZE),
                                          'R': (x, y + (self.TILE_SIZE * 2)),
                                          'B': (x, y + (self.TILE_SIZE * 3))
                                          }
                pygame.draw.rect(screen, 'white', (self.destination[0],
                                                   self.destination[1],
                                                   self.TILE_SIZE, self.TILE_SIZE * 4))
                x, y = x + (self.TILE_SIZE / 2), y + (self.TILE_SIZE / 2)
                self.pieces.render('Q', (x, y), None)
                self.pieces.render('N', (x, y + self.TILE_SIZE), None)
                self.pieces.render('R', (x, y + (self.TILE_SIZE * 2)), None)
                self.pieces.render('B', (x, y + (self.TILE_SIZE * 3)), None)

    def render_text(self, text, x, y, color):
        '''
        Renders the given ``text`` on the window at given (``x``, ``y``)

        Setting either ``x`` or ``y`` to ``'c'`` will center the text on that
        axis
        '''

        to_blit = font.render(text, True, color)
        if x == 'c':
            width = to_blit.get_width()
            x = (SCREEN_WIDTH - width) / 2

        if y == 'c':
            height = to_blit.get_height()
            y = (SCREEN_HEIGHT - height) / 2

        screen.blit(to_blit, (x, y))

    # Creates timer for either side with display_time as an argument
    def timer(self, white_time=list, black_time=list):
        '''
        Input ``white_time`` and ``black_time`` as a list in the following
        order:
        ``[white minutes, white seconds]``, ``[black minutes, black seconds]``
        '''
        x = 150

        # White clock
        y = 810
        pygame.draw.rect(screen, 'white', (x - 10, y, 150, 50))
        self.render_text(self.format_time(white_time), x, y, 'black')

        # Black clock
        y = 60
        pygame.draw.rect(screen, 'black', (x - 10, y, 150, 50))
        self.render_text(self.format_time(black_time), x, y, 'white')

    # Converts raw minutes and seconds to time format
    def format_time(self, time=list):
        '''
        Input ``time`` as a list in the following order:
        ``[minutes, seconds]``
        '''

        minutes = time[0]
        seconds = time[1]

        if len(str(minutes)) == 1:
            minutes = '0' + str(minutes)

        if len(str(seconds)) == 1:
            seconds = '0' + str(seconds)

        time = str(minutes) + ':' + str(seconds)

        return time

    def background_render(self):
        # Fill background
        screen.fill(self.BACKGROUND_COLOR)

        # Render board
        self.render_board()

        # Render legal moves
        if self.__show_legal_moves:
            if not self.legal_moves == []:
                for i in range(len(self.legal_moves)):
                    if self.board.loc[self.legal_moves[i]] == '':
                        screen.blit(self.move_indicator, (self.legal_moves[i][0] + ((self.TILE_SIZE - 20) / 2),
                                                          self.legal_moves[i][1] + ((self.TILE_SIZE - 20) / 2)))
                    else:
                        screen.blit(self.attack_indicator, (self.legal_moves[i][0],
                                                            self.legal_moves[i][1]))

        # Update indicator variables
        self.current_time = pygame.time.get_ticks()
        if self.blink_enabled and self.check_show and self.current_time - self.last_blink_time >= 480:
            self.blink_on = not self.blink_on
            self.last_blink_time = self.current_time

        # Render yellow indicators
        if self.starting_pos is not None:
            screen.blit(self.position_indicator, self.starting_pos)
            if self.ending_pos is not None:
                screen.blit(self.position_indicator, self.ending_pos)
                if self.prev_starting_pos is not None:
                    screen.blit(self.position_indicator,
                                self.prev_starting_pos)

        # Render red indicators checkmate / draw / check
        if self.checkmate:
            screen.blit(self.check_indicator,
                        self.find_piece(self.board, self.checked_king))
            if self.api.turn == 'black':
                self.winner = 'white'
            else:
                self.winner = 'black'
        elif self.draw:
            screen.blit(self.check_indicator, self.find_piece(self.board, 'K'))
            screen.blit(self.check_indicator, self.find_piece(self.board, 'k'))
        elif self.check_show and self.blink_on and self.blink_enabled:
            screen.blit(self.check_indicator,
                        self.find_piece(self.board, self.checked_king))

        # Render all pieces
        self.render_pieces(self.board)

        # Render piece moving with mouse
        if self.mouse_down:
            self.no_render = self.snapped_piece

            if self.mouse_down:
                self.pieces.render(self.piece_name, (self.snapped_piece[0] + (self.TILE_SIZE / 2),
                                                     self.snapped_piece[1] + (self.TILE_SIZE / 2)), 128)
                self.pieces.render(self.piece_name, pygame.mouse.get_pos(),
                                   None)
                self.moving = True

        # Render winner
        if self.winner == 'white':
            pygame.draw.rect(screen, (10, 171, 252), (300, 375, 300, 150))
            self.render_text('WHITE WINS', 'c', 'c', 'black')
        elif self.winner == 'black':
            pygame.draw.rect(screen, (10, 171, 252), (300, 375, 300, 150))
            self.render_text('BLACK WINS', 'c', 'c', 'black')

        # Render timer for each side
        self.timer(self.white_time, self.black_time)


# Timer setup
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # 1000 milliseconds = 1 second

# Promo
# b = '4k3/6P1/8/8/8/2K5/4p3/8 w - - 0 1'

# Promo but black has to promote
# b = 'k7/2Q5/1K6/8/8/8/5p2/8 b - - 0 1'

# Castling
# b = 'r3k2r/pppp1ppp/4pn2/8/1bPPbB2/2N1P3/PP1Q1PPP/R3K2R w KQkq - 0 1'

# # Draw
# b = '3k4/5Q2/2K5/8/8/8/8/8 w - - 0 1'

# # En passant
# b = '3k4/3p4/8/2P5/1Pp3p1/8/5P2/3K4 b - - 0 1'

# Checkmate with knight
# b = '7n/5P1k/R7/3K4/6Q1/8/8/8 w - - 0 1'

# game = ChessGame(__show_legal_moves, 'NONE', '2k2n2/R7/5Q2/8/1b4q1/8/1K6/8 w - - 0 1')

# 2 Move checkmate
# b = 'rnbqkbnr/1ppp1ppp/p7/P3p3/5PP1/8/1PPPP2P/RNBQKBNR b KQkq b6 0 1'

# En Passant history check
# b = 'rnbqkbnr/p1p1p1p1/8/1P1P1P1P/1p1p1p1p/8/P1P1P1P1/RNBQKBNR b KQkq - 0 1'
game = ChessGame(__show_legal_moves, 'None')

if '__main__' == __name__:
    running = True
else:
    running = False

while running:
    for event in pygame.event.get():
        # Quitting pygame
        if event.type == pygame.QUIT:
            running = False

        # Escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse_button_down_logic()

        if event.type == pygame.MOUSEBUTTONUP:
            game.mouse_button_up_logic()

        if event.type == TIMER_EVENT:
            game.timer_logic()

    game.handle_move_navigation()

    game.background_render()

    # game.ai_play()

    game.handle_and_display_promotion_gui()

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
