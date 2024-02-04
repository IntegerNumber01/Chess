import pandas
import string
import math
from move_generator import Generator


class Board:
    '''
    FUNCTIONS:

    ``print_board()`` -> prints the board in the terminal in a neat format

    ``move(uci)`` -> input a uci to move piece on the board

    ``get_legal_moves(notation)`` -> input notation to get legal moves of that
    piece

    ``game_state()`` -> returns 'check' / 'checkmate' / 'draw'

    ``undo_move()`` -> undoes the last move that was made

    ``get_board_history()`` -> returns a list of FEN strings, each
    representing the board after a half-move. The last element is the current
    state of the board

    IMPORTANT VARIABLES:

    ``pawn_promotion`` -> True / False representing whether a pawn can promote
    or not
    '''

    def __init__(self, board='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        '''
        INPUTS:

        ``board`` -> input a FEN string that represents the state of the board,
        no input results in starting position
        '''
        self.pawn_promotion = False
        self.king_movement_tracker = {'K': False, 'k': False}

        # Setup board
        self.board, en_passant = self.fen_to_dataframe(board)
        self.board_history = [self.board.copy()]

        self.generator = Generator()
        self.chess_map = self.create_chess_dict(self.board)

        if not en_passant == '-':
            self.generator.en_passant = self.to_coords(en_passant)

    def print_board(self) -> None:
        transposed_board = self.board.transpose()

        # Disable row and column index labels
        # transposed_board.index.name = None
        # transposed_board.columns.name = None
        column_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        row_labels = ['8', '7', '6', '5', '4', '3', '2', '1']
        transposed_board.columns = column_labels
        transposed_board.index = row_labels

        print(transposed_board)

    def get_coords(self, side) -> list:

        '''
        Returns all the coordinates for a side input as 'white' or 'black'
        '''

        # Getting all the coordinates
        coordinates = []
        for column in self.board.columns:
            for index in self.board.index:
                coordinates.append((column, index))

        # Filtering out the opposite side coordinates
        filtered = []
        for coord in coordinates:
            letter = self.board.loc[coord]
            if (letter.islower() and side == 'black') or (letter.isupper() and
                                                          side == 'white'):
                filtered.append(coord)

        return filtered

    def get_board(self) -> str:
        '''
        Returns a FEN string representing the state of the board
        '''

        fen = ''
        count = 0

        for i in range(8):
            row = self.board[i]
            for char in row:
                if char == '':
                    count += 1
                elif char.isalpha():
                    if not count == 0:
                        fen = fen + str(count)
                        count = 0
                    fen = fen + char

            if not count == 0:
                fen = fen + str(count)
                count = 0

            fen = fen + '/'

        # Remove the last '/'
        fen = fen[:-1]

        # Adding which player's turn it is
        if self.turn == 'white':
            fen = fen + ' w '

        else:
            fen = fen + ' b '

        # Adding castling rights
        castling_rights = ''
        corners = self.generator.get_board_corners(self.board, None)

        if self.king_movement_tracker['K'] is False:
            if self.board.loc[corners[3]].lower() == 'r':
                castling_rights = castling_rights + 'K'
            if self.board.loc[corners[1]].lower() == 'r':
                castling_rights = castling_rights + 'Q'

        if self.king_movement_tracker['k'] is False:
            if self.board.loc[corners[2]].lower() == 'r':
                castling_rights = castling_rights + 'k'
            if self.board.loc[corners[0]].lower() == 'r':
                castling_rights = castling_rights + 'q'

        if castling_rights == '':
            castling_rights = '-'
        elif len(castling_rights) == 1:
            castling_rights = castling_rights + '-'
        elif len(castling_rights) == 2 and castling_rights.isupper():
            castling_rights = castling_rights + '-'

        fen = fen + castling_rights

        # Adding en passant target square
        target = self.generator.en_passant
        if not target == (None, None):
            fen = fen + ' ' + self.to_notation(target)
        else:
            fen = fen + ' -'

        # Adding halfmove clock
        fen = fen + ' ' + str(self.fifty_move_rule)

        # Adding fullmove number
        fen = fen + ' ' + str(math.floor(self.move_count))

        return fen

    def move(self, uci) -> None:
        '''
        The uci argument is a string in this format:

        a = 'coords of piece to move'
        b = 'coords of where to move piece'

        move = a + b

        NOTICE: all "coords" are the standard chess notation

        Types / examples of UCI input:
        move piece -> e2e4
        capture piece -> e4d5
        castling -> e1g1
        en passant -> e5d6
        pawn promotion -> e7e8q

        NOTES:
        - capturing a piece is in the same notation as moving a piece
        - when castling, only include the kings movement
        - in en passant, move the pawn where it would go to capture the piece
        - when promoting, the last letter represents the piece to promote to

        '''

        start = uci[:2]
        end = uci[2:4]
        promo_choice = None

        if uci[-1] == 'q' or uci[-1] == 'n' or uci[-1] == 'r' or uci[-1] == 'b':
            if self.turn == 'white':
                promo_choice = uci[-1].upper()
            else:
                promo_choice = uci[-1].lower()
        elif start[0].isalpha() and start[1].isdigit():
            pass
        else:
            raise ValueError(f'Bad UCI input -> {uci}')

        start = self.to_coords(start)
        end = self.to_coords(end)
        piece = self.board.loc[start]

        notations = self.get_coords(self.turn)

        if start not in notations:
            if self.turn == 'white':
                opposite_notations = self.get_coords('black')
            else:
                opposite_notations = self.get_coords('white')

            if start not in opposite_notations:
                raise ValueError(f'Piece does not exist! -> {uci}')

            if self.turn == 'white':
                raise ValueError("It is not blacks's turn!")
            else:
                raise ValueError("It is not white's turn!")

        moves = self.generator.get_moves(self.board, start,
                                         self.king_movement_tracker,
                                         self.rook_movement_tracker)

        self.generator.set_pawn_promotion(self.board, piece, end)
        # pawn_promotion is True if the pawn is on the end of the board
        self.pawn_promotion = self.generator.pawn_promotion

        self.generator.set_en_passant(self.board, piece, end)

        if end in moves:
            # Actually moving the piece
            if not self.board.loc[end] == '':
                self.fifty_move_rule = 0
            elif piece.lower() == 'p':
                self.fifty_move_rule = 0
            else:
                self.fifty_move_rule += 1

            if piece.lower() == 'r':
                corners = self.generator.get_board_corners(self.board, None)
                # Top left corner
                if start == corners[0]:
                    self.rook_movement_tracker['left r'] = True
                # Bottom left corner
                if start == corners[1]:
                    self.rook_movement_tracker['left R'] = True
                # Top right corner
                if start == corners[2]:
                    self.rook_movement_tracker['right r'] = True
                # Botton right corner
                if start == corners[3]:
                    self.rook_movement_tracker['right R'] = True

            self.board.loc[end] = self.board.loc[start]
            self.board.loc[start] = ''

            if self.turn == 'white':
                self.turn = 'black'
                self.king = 'k'
            else:
                self.turn = 'white'
                self.king = 'K'

            self.generator.complete_castling(self.board, end,
                                             self.king_movement_tracker,)

            if piece == 'K':
                self.king_movement_tracker['K'] = True
            elif piece == 'k':
                self.king_movement_tracker['k'] = True

            self.generator.complete_en_passant(self.board, piece, end)

            if promo_choice is not None and piece.lower() == 'p':
                self.generator.complete_pawn_promotion(self.board,
                                                       promo_choice, end)

            self.generator.set_en_passant(self.board, piece, end)

            self.board_history.append(self.board.copy())
            self.move_count += 0.5

        else:
            raise ValueError(f'Illegal UCI move -> {uci}')

    def game_state(self) -> str:
        '''
        Returns ``'checkmate'`` / ``'check'`` / ``'draw'``
        '''

        if self.generator.check_for_check(self.board, self.king):
            if self.generator.check_for_checkmate(self.board, self.king):
                return 'checkmate'

            return 'check'
        elif self.generator.check_for_draw(self.board):
            return 'draw'

    def get_legal_moves(self, notation) -> list:
        '''
        Input a notation (ex. a1, h3, c8) to get legal moves for the piece
        there.
        '''

        coordinates = self.to_coords(notation)
        piece = self.board.loc[coordinates]
        moves = self.generator.get_moves(self.board, coordinates,
                                         self.king_movement_tracker,
                                         self.rook_movement_tracker)

        add = False
        new_moves = []

        # Converting coords to notation
        for move in moves:
            notation_move = self.to_notation(move)
            # Adding the 4 promotion options
            if piece == 'p':
                if int(notation_move[1]) == 1:
                    add = True
            elif piece == 'P':
                if int(notation_move[1]) == 8:
                    add = True

            if add:
                new_moves.append(notation_move + 'q')
                new_moves.append(notation_move + 'r')
                new_moves.append(notation_move + 'b')
                new_moves.append(notation_move + 'n')
            else:
                new_moves.append(notation_move)

            add = False

        return new_moves

    def is_fen_valid(self, fen) -> bool:
        '''
        INPUT (expecting full fen):

        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1


        Raises ValueError if FEN invalid

        Returns True if valid
        '''

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        # - check if the total number of squares used is 8
        # - check if the letters are valid
        fen_letters = ''.join([char for char in fen_parts[0] if char.isalpha()])
        for char in fen_letters:
            char = char.lower()
            if not (char == 'r' or char == 'n' or char == 'b' or char == 'q'
                    or char == 'k' or char == 'p'):
                raise ValueError(f'Check letters of FEN: {fen}')

        for row in rows:
            letters = ''.join([char for char in row if char.isalpha()])
            numbers = ''.join([char for char in row if char.isdigit()])

            total = 0
            for num in numbers:
                total += int(num)

            if not len(letters) + total == 8:
                raise ValueError(f'Check length of section in FEN: {fen}')

        return True

    def fen_to_dataframe(self, fen) -> (pandas.DataFrame, str):
        '''
        Converts FEN to data frame

        Sets self.board and self.turn if provided

        Raises ValueError if FEN invalid

        Returns the board and en passant square
        '''

        # Raises error if not valid
        self.is_fen_valid(fen)

        data = {
            0: ['', '', '', '', '', '', '', ''],
            1: ['', '', '', '', '', '', '', ''],
            2: ['', '', '', '', '', '', '', ''],
            3: ['', '', '', '', '', '', '', ''],
            4: ['', '', '', '', '', '', '', ''],
            5: ['', '', '', '', '', '', '', ''],
            6: ['', '', '', '', '', '', '', ''],
            7: ['', '', '', '', '', '', '', ''],
        }

        board = pandas.DataFrame(data, index=[0, 1, 2, 3, 4, 5, 6, 7])

        fen_parts = fen.split(' ')
        rows = fen_parts[0].split('/')

        # Fills in the board
        for row_num, row in enumerate(rows):
            if not row == '8':
                i = 0
                for char in row:
                    if char.isdigit():
                        i += int(char)
                    elif char.isalpha():
                        board.loc[i, row_num] = char
                        i += 1

        # Player turn
        if fen_parts[1] == 'b':
            self.turn = 'black'
            self.king = 'k'
        elif fen_parts[1] == 'w':
            self.turn = 'white'
            self.king = 'K'

        # Castling rights
        if len(fen_parts[2]) > 4:
            raise ValueError(f'Extra character(s) in casting rights -> {fen_parts[2]}')

        self.rook_movement_tracker = {'left R': True, 'right R': True,
                                      'left r': True, 'right r': True}

        lower = ''
        upper = ''
        other = ''

        for char in fen_parts[2]:
            if char.islower():
                lower = lower + char
            elif char.isupper():
                upper = upper + char
            else:
                other = other + char

        if not lower == '':
            if len(lower) > 2 or not (('k' in lower) or ('q' in lower)):
                raise ValueError(f'Check castling rights -> {fen_parts[2]}')
        if not upper == '':
            if len(upper) > 2 or not (('K' in upper) or ('Q' in upper)):
                raise ValueError(f'Check castling rights -> {fen_parts[2]}')
        if not (other == '-' or other == ''):
            raise ValueError(f'Check castling rights -> {fen_parts[2]}')

        if 'k' in lower:
            if 'q' in lower:
                self.rook_movement_tracker['left r'] = False

            self.rook_movement_tracker['right r'] = False

        if 'K' in upper:
            if 'Q' in upper:
                self.rook_movement_tracker['left R'] = False

            self.rook_movement_tracker['right R'] = False

        if int(fen_parts[4]) < 0:
            raise ValueError(f'Check fifty move rule count -> {fen_parts[4]}')
        else:
            self.fifty_move_rule = int(fen_parts[4])

        if int(fen_parts[5]) < 1:
            raise ValueError(f'Check full move count -> {fen_parts[5]}')
        else:
            self.move_count = int(fen_parts[5])

        # Returns the board and the en passant square
        return board.copy(), fen_parts[3]

    def set_board(self, fen) -> None:
        ''''
        Resets the current board to the FEN input

        Raises ValueError if FEN not valid
        '''

        self.is_fen_valid(fen)
        self.board, en_passant = self.fen_to_dataframe(fen)
        if not en_passant == '-':
            self.generator.en_passant = self.to_coords(en_passant)

        self.board_history.append(self.board.copy())

    def get_board_history(self) -> list:
        '''
        Returns a list of FEN strings, each half-move is a seperate FEN string

        ``[0]`` -> the first position of the board

        ``[-1]`` -> current state of board
        '''

        current_board = self.board.copy()

        fen_list = []

        for board in self.board_history:
            self.board = board.copy()
            fen_list.append(self.get_board())

        self.board = current_board.copy()

        return fen_list

    def undo_move(self) -> None:
        '''
        Undoes the last move made and deletes the last board from board history
        '''

        self.board_history.pop()
        self.board = self.board_history[-1].copy()

        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def create_chess_dict(self, board) -> dict:
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

    def to_coords(self, notation) -> int:
        '''
        Converts standard chess notation into matrix coordinates
        '''

        return self.chess_map[notation]

    def to_notation(self, coords) -> str:
        '''
        Converts matrix coordinates into standard chess notation
        '''

        flipped = {value: key for key, value in self.chess_map.items()}

        return flipped[coords]

    def switch_turn(self) -> None:
        '''
        Switches whose turn it is

        -> if ``turn`` is ``'white'`` then turn switches to ``'black'``

        -> if ``turn`` is ``'black'`` then turn switches to ``'white'``
        '''

        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
