import pandas
import numpy


class Generator:
    def __init__(self):
        '''
        Input ``board`` as a pandas dataframe

        Input ``interval`` as the difference between each of the rows/columns
        '''

        self.move_rook = [False, False]
        self.en_passant = (None, None)
        self.pawn_promotion = False

    def case_match(self, letter1, letter2):
        '''
        Checks if two strings' cases match
        '''

        if letter1.isupper() and letter2.isupper():
            return True
        elif letter1.islower() and letter2.islower():
            return True
        else:
            return False

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

    def check_move(self, board, piece, coords):
        '''
        Checks if the ``coords`` are in the board,
            returns ``True`` if target is an empty space
            returns ``True`` if target is hostile and the piece is not a pawn

        ``False`` if none of those match
        '''

        if coords[0] in board.index and coords[1] in board.columns:
            target = board.loc[coords[0], coords[1]]

            if target == '':
                return True
            elif self.case_match(target, piece) is False:
                return True
            else:
                return False

        return False

    def get_letters_coords(self, board, case):
        '''
        Returns all lower or upper case letters in board EXCEPT THE KING with
        coordinates in this format:
        ``('letter', (x, y))``
        The ``case`` argument should be ``'upper'`` or ``'lower'``
        '''

        letters_list = []

        # Loop over the rows
        for coord, row in board.iterrows():
            # Loop over the columns
            for thing, entry in row.items():
                if isinstance(entry, str) and ((case == 'lower' and entry.islower()) or (case == 'upper' and entry.isupper())) and not entry.lower() == 'k':
                    letters_list.append((entry, (coord, thing)))

        return letters_list

    def set_pawn_promotion(self, board, piece, coords):
        '''
        ``coords`` - Where the pawn is currently

        ``piece`` -  The pawn's name

        Sets ``pawn_promotion`` to ``True`` if the pawn is on the edge of the
        board
        '''
        if piece.lower() == 'p':
            if piece.isupper():
                if coords[1] == board.index[0]:
                    self.pawn_promotion = True
                    return
            else:
                if coords[1] == board.index[-1]:
                    self.pawn_promotion = True
                    return

        self.pawn_promotion = False

    def complete_pawn_promotion(self, board, piece, coords):
        '''
        Replaces the ``coords`` on the board with the chosen ``piece`` for
        promotion
        '''

        board.loc[coords] = piece
        self.pawn_promotion = False

        return board

    def check_target_coords(self, board, piece, target_coords):
        '''
        Currently only used to check diagonal attacks with pawns
        '''

        if target_coords[0] in board.index and target_coords[1] in board.columns:
            target = board.loc[target_coords]
            if not target == '' and self.case_match(target, piece) is False:
                return target_coords

        return None

    def pawn(self, board, piece, coords):
        '''
        Returns legal moves of pawn
        '''

        def check_pawn_move(board, piece, coords):
            '''
            Checks if the ``coords`` are in the board,
                ``True`` if target is an empty space
                ``True`` if target is hostile

            ``False`` if none of those match
            '''

            if coords[0] in board.index and coords[1] in board.columns:
                target = board.loc[coords[0], coords[1]]

                if target == '':
                    return True
                elif self.case_match(target, piece) is False and not piece.lower() == 'p':
                    return True
                else:
                    return False

            return False

        legal_moves = []

        if piece == 'P':  # White
            if coords[1] == board.index[-2]:  # 2 spaces
                if check_pawn_move(board, piece, (coords[0], coords[1] - 1)):
                    legal_moves.append((coords[0], coords[1] - 1))
                    if check_pawn_move(board, piece, (coords[0], coords[1] - 2)):
                        legal_moves.append((coords[0], coords[1] - 2))

            elif check_pawn_move(board, piece, (coords[0], coords[1] - 1)):
                legal_moves.append((coords[0], coords[1] - 1))

        if piece == 'p':  # Black
            if coords[1] == board.index[1]:  # 2 spaces
                if check_pawn_move(board, piece, (coords[0], coords[1] + 1)):
                    legal_moves.append((coords[0], coords[1] + 1))
                    if check_pawn_move(board, piece, (coords[0], coords[1] + 2)):
                        legal_moves.append((coords[0], coords[1] + 2))

            elif check_pawn_move(board, piece, (coords[0], coords[1] + 1)):
                legal_moves.append((coords[0], coords[1] + 1))

        # Diagonal moves
        if piece.isupper():
            target_coords = (coords[0] + 1, coords[1] - 1)

            add = self.check_target_coords(board, piece, target_coords)
            if add is not None:
                legal_moves.append(add)
            if target_coords == self.en_passant:
                legal_moves.append(target_coords)

            target_coords = (coords[0] - 1, coords[1] - 1)

            add = self.check_target_coords(board, piece, target_coords)
            if add is not None:
                legal_moves.append(add)
            if target_coords == self.en_passant:
                legal_moves.append(target_coords)
        else:
            target_coords = (coords[0] + 1, coords[1] + 1)

            add = self.check_target_coords(board, piece, target_coords)
            if add is not None:
                legal_moves.append(add)
            if target_coords == self.en_passant:
                legal_moves.append(target_coords)

            target_coords = (coords[0] - 1, coords[1] + 1)

            add = self.check_target_coords(board, piece, target_coords)
            if add is not None:
                legal_moves.append(add)
            if target_coords == self.en_passant:
                legal_moves.append(target_coords)

        return legal_moves

    def rook(self, board, piece, coords):
        '''
        Returns legal moves of rook
        '''

        legal_moves = []

        # Going up
        i = 1
        while self.check_move(board, piece, (coords[0], coords[1] - i)):
            target = (coords[0], coords[1] - i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going down
        i = 1
        while self.check_move(board, piece, (coords[0], coords[1] + i)):
            target = (coords[0], coords[1] + i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going left
        i = 1
        while self.check_move(board, piece, (coords[0] - i, coords[1])):
            target = (coords[0] - i, coords[1])
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going right
        i = 1
        while self.check_move(board, piece, (coords[0] + i, coords[1])):
            target = (coords[0] + i, coords[1])
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        return legal_moves

    def bishop(self, board, piece, coords):
        '''
        Returns legal moves of bishop
        '''

        legal_moves = []

        # Going left and up
        i = 1
        while self.check_move(board, piece, (coords[0] - i, coords[1] - i)):
            target = (coords[0] - i, coords[1] - i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going right and up
        i = 1
        while self.check_move(board, piece, (coords[0] + i, coords[1] - i)):
            target = (coords[0] + i, coords[1] - i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going left and down
        i = 1
        while self.check_move(board, piece, (coords[0] - i, coords[1] + i)):
            target = (coords[0] - i, coords[1] + i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        # Going right and down
        i = 1
        while self.check_move(board, piece, (coords[0] + i, coords[1] + i)):
            target = (coords[0] + i, coords[1] + i)
            legal_moves.append(target)
            i += 1
            if not board.loc[target] == '':
                break

        return legal_moves

    def knight(self, board, piece, coords):
        '''
        Returns legal moves of knight
        '''

        legal_moves = []

        # Going up and left
        if self.check_move(board, piece, (coords[0] - 1, coords[1] - 2)):
            legal_moves.append((coords[0] - 1, coords[1] - 2))

        # Going up and right
        if self.check_move(board, piece, (coords[0] + 1, coords[1] - 2)):
            legal_moves.append((coords[0] + 1, coords[1] - 2))

        # Going down and left
        if self.check_move(board, piece, (coords[0] - 1, coords[1] + 2)):
            legal_moves.append((coords[0] - 1, coords[1] + 2))

        # Going down and right
        if self.check_move(board, piece, (coords[0] + 1, coords[1] + 2)):
            legal_moves.append((coords[0] + 1, coords[1] + 2))

        # Going left and up
        if self.check_move(board, piece, (coords[0] - 2, coords[1] - 1)):
            legal_moves.append((coords[0] - 2, coords[1] - 1))

        # Going left and down
        if self.check_move(board, piece, (coords[0] - 2, coords[1] + 1)):
            legal_moves.append((coords[0] - 2, coords[1] + 1))

        # Going right and up
        if self.check_move(board, piece, (coords[0] + 2, coords[1] - 1)):
            legal_moves.append((coords[0] + 2, coords[1] - 1))

        # Going right and down
        if self.check_move(board, piece, (coords[0] + 2, coords[1] + 1)):
            legal_moves.append((coords[0] + 2, coords[1] + 1))

        return legal_moves

    def basic_king(self, board, piece, coords):
        '''
        Returns the basic 8 moves a king can take allowing attacking a piece
        and moving to an empty space

        SHOULD NOT BE USED ON ITS OWN TO GET THE COMPLETE KING FUNCTIONS
        '''

        legal_moves = []

        # Going up
        if self.check_move(board, piece, (coords[0], coords[1] - 1)):
            legal_moves.append((coords[0], coords[1] - 1))

        # Going down
        if self.check_move(board, piece, (coords[0], coords[1] + 1)):
            legal_moves.append((coords[0], coords[1] + 1))

        # Going left
        if self.check_move(board, piece, (coords[0] - 1, coords[1])):
            legal_moves.append((coords[0] - 1, coords[1]))

        # Going right
        if self.check_move(board, piece, (coords[0] + 1, coords[1])):
            legal_moves.append((coords[0] + 1, coords[1]))

        # Going up and left
        if self.check_move(board, piece, (coords[0] - 1, coords[1] - 1)):
            legal_moves.append((coords[0] - 1, coords[1] - 1))

        # Going up and right
        if self.check_move(board, piece, (coords[0] + 1, coords[1] - 1)):
            legal_moves.append((coords[0] + 1, coords[1] - 1))

        # Going down and left
        if self.check_move(board, piece, (coords[0] - 1, coords[1] + 1)):
            legal_moves.append((coords[0] - 1, coords[1] + 1))

        # Going down and right
        if self.check_move(board, piece, (coords[0] + 1, coords[1] + 1)):
            legal_moves.append((coords[0] + 1, coords[1] + 1))

        return legal_moves

    def king(self, board, piece, coords, king_movement_tracker,
             rook_movement_tracker):
        '''
        Returns legal moves of the king using the basic king function and then
        adding king_cannot_move_into_check
        '''

        legal_moves = self.basic_king(board, piece, coords)

        legal_moves = self.check_for_hostile_king(board, piece, legal_moves)

        legal_moves = self.king_cannot_move_into_check(board, piece, coords,
                                                       legal_moves,
                                                       king_movement_tracker,
                                                       rook_movement_tracker)

        legal_moves = self.is_king_defending_piece_to_attack(board, piece,
                                                             legal_moves)

        return legal_moves

    def queen(self, board, piece, coords):
        '''
        Returns legal moves of queen by combining the moves of a
        rook and bishop
        '''

        legal_moves = self.rook(board, piece, coords)
        more_moves = self.bishop(board, piece, coords)

        return legal_moves + more_moves

    def get_moves(self, board, coords, king_movement_tracker,
                  rook_movement_tracker):
        '''
        Returns the complete legal moves for a piece at given ``coords``
        '''

        self.move_rook = [False, False]
        og_piece = board.loc[coords[0], coords[1]]
        piece = og_piece.lower()

        if og_piece == '':
            return []

        if piece == 'p':
            legal_moves = self.pawn(board, og_piece, coords)
        elif piece == 'r':
            legal_moves = self.rook(board, og_piece, coords)
        elif piece == 'n':
            legal_moves = self.knight(board, og_piece, coords)
        elif piece == 'b':
            legal_moves = self.bishop(board, og_piece, coords)
        elif piece == 'q':
            legal_moves = self.queen(board, og_piece, coords)

        if piece == 'k':
            legal_moves = self.king(board, og_piece, coords,
                                    king_movement_tracker,
                                    rook_movement_tracker)
        else:
            legal_moves = self.no_ignore_check(board, og_piece, coords,
                                               legal_moves)

        return legal_moves

    def get_neighbor_entries(self, board, coords, direction):
        '''
        Returns neighbor entires in the board provided a direction:
        ``'left'`` / ``'right'``
        '''

        x, y = coords
        x_index = board.columns.tolist().index(x)

        if direction == 'left':
            if x_index - 1 < 0:
                return ''
            else:
                return board.loc[board.columns[x_index - 1], y]

        elif direction == 'right':
            if x_index + 1 >= len(board.columns):
                return ''
            else:
                return board.loc[board.columns[x_index + 1], y]
        else:
            return ''

    def set_en_passant(self, board, piece, coords):
        '''
        The ``coords`` argument is for the pawn that can get killed
        (The pawn that just moved 2 steps)

        Does'nt return anything, sets ``en_passant`` to the coordinates of the
        where the attacking pawn must go to kill a hostile pawn using En
        Passant
        '''

        # Making sure the piece moved 2 steps
        if (coords[1] == board.index[3] and piece.islower()) or (coords[1] == board.index[-4] and piece.isupper()):
            pass
        else:
            return

        left_piece = self.get_neighbor_entries(board, coords, 'left')
        right_piece = self.get_neighbor_entries(board, coords, 'right')

        if left_piece.lower() == 'p' and self.case_match(left_piece, piece) is False:
            if piece.islower():
                self.en_passant = (coords[0], coords[1] - 1)
            else:
                self.en_passant = (coords[0], coords[1] + 1)

        if right_piece.lower() == 'p' and self.case_match(right_piece, piece) is False:
            if piece.islower():
                self.en_passant = (coords[0], coords[1] - 1)
            else:
                self.en_passant = (coords[0], coords[1] + 1)

    def complete_en_passant(self, board, piece, coords):
        '''
        The argument ``coords`` are the same coordinates ``en_passant`` is
        equal to
        '''

        if board.loc[coords] == piece:
            if piece == 'P' and self.en_passant == coords:
                next_coord = coords[1] + 1
                if next_coord in board.columns:
                    board.loc[coords[0], next_coord] = ''
            elif piece == 'p' and self.en_passant == coords:
                next_coord = coords[1] - 1
                if next_coord in board.columns:
                    board.loc[coords[0], next_coord] = ''

        self.en_passant = (None, None)

        return board

    def complete_castling(self, board, king_coords, king_movement_tracker):
        '''
        Returns updated board with the rook moved. Use this function AFTER the
        king has moved into the castle positions
        '''

        if self.move_rook == [False, False] or king_movement_tracker[board.loc[king_coords]] is True:
            return board

        king = board.loc[king_coords]

        if king.islower():
            rook = 'r'
        else:
            rook = 'R'

        median_x = pandas.Series(board.columns.tolist()).median()

        if king_coords[0] < median_x:
            king_placement = -1  # King is on left side
        elif king_coords[0] > median_x:
            king_placement = 1  # King is on right side

        corners = self.get_board_corners(board, None)

        if king_placement == -1:  # Queen side
            rook_end = 1
            if king.islower():
                rook_coords = corners[0]
            else:
                rook_coords = corners[1]
        elif king_placement == 1:   # King side
            rook_end = -1
            if king.islower():
                rook_coords = corners[2]
            else:
                rook_coords = corners[3]

        if rook_end == 1 and self.move_rook[0] is True:
            board.loc[rook_coords] = ''
            board.loc[king_coords[0] + 1, king_coords[1]] = rook
        elif rook_end == -1 and self.move_rook[1] is True:
            board.loc[rook_coords] = ''
            board.loc[king_coords[0] - 1, king_coords[1]] = rook

        self.move_rook = [False, False]

        return board

    def get_board_corners(self, board, side):
        '''
        Returns in this format:

        ``[``

        ``top left,``

        ``bottom left,``

        ``top right,``

        ``bottom right,``

        ``]``

        ``side`` inputs:

        ``'white'`` for bottom left and bottom right

        ``'black'`` for top left and top right

        /ANYTHING ELSE/ for all corners
        '''
        first_row = board.index[0]  # This is the first row label
        last_row = board.index[-1]  # This is the last row label

        first_col = board.columns[0]  # This is the first (left) column label
        last_col = board.columns[-1]  # This is the last (right) column label

        if side == 'white':
            corners = [(first_row, last_col), (last_row, last_col)]
        elif side == 'black':
            corners = [(first_row, first_col), (last_row, first_col)]
        else:
            corners = [(first_row, first_col), (first_row, last_col),
                       (last_row, first_col), (last_row, last_col)]

        return corners

    def get_castle_coords(self, board, coords):
        '''
        Returns 4 coordinates in the form of tuples
        left 2, left, right, right 2

        These are the coordinates the king can move to
        '''

        x, y = coords
        x_list = list(board.columns)
        index = x_list.index(x)

        neighbours_coords = []

        if index - 2 >= 0:
            neighbours_coords.append((x_list[index - 2], y))
        if index - 1 >= 0:
            neighbours_coords.append((x_list[index - 1], y))

        # Check that the right 1 and right 2 squares exist
        if index + 1 < len(x_list):
            neighbours_coords.append((x_list[index + 1], y))
        if index + 2 < len(x_list):
            neighbours_coords.append((x_list[index + 2], y))

        return neighbours_coords

    def check_path_clear(self, board, coords):
        '''
        Returns whether left or right is clear or not in the form of

        left_clear = ``True`` / ``False``

        right_clear = ``True`` / ``False``
        '''

        x, y = coords
        x_list = list(board.columns)
        index = x_list.index(x)

        # Check path to the left
        left_clear = False
        for i in range(index - 1, -1, -1):
            if board.loc[x_list[i], y].lower() == 'r':
                left_clear = True
            elif not board.loc[x_list[i], y].lower() == '':
                break

        # Check path to right
        right_clear = False
        for i in range(index + 1, len(x_list)):
            if board.loc[x_list[i], y].lower() == 'r':
                right_clear = True
                break
            elif not board.loc[x_list[i], y].lower() == '':
                break

        return left_clear, right_clear

    def check_for_hostile_king(self, board, king, legal_moves):
        '''
        Returns list with items to remove from legal moves that could cause a
        face off between the kings
        '''

        to_remove = []

        if king == 'K':
            H_king_coords = self.find_piece(board, 'k')
            H_king_moves = self.basic_king(board, 'k', H_king_coords)
        else:
            H_king_coords = self.find_piece(board, 'K')
            H_king_moves = self.basic_king(board, 'K', H_king_coords)

        for move in legal_moves:
            if move in H_king_moves:
                to_remove.append(move)

        to_remove = list(set(to_remove))

        for i in range(len(to_remove)):
            legal_moves.remove(to_remove[0])
            to_remove.pop(0)
            i -= 1

        return legal_moves

    def is_king_defending_piece_to_attack(self, board, king, legal_moves):
        '''
        Returns a new set of legal moves that make sure the king can't attack
        a piece being defended by the opposite king

        The ``king`` argument is the king that wants to attack the piece that
        is defended
        '''

        to_remove = []

        if king == 'K':
            H_king_coords = self.find_piece(board, 'k')
        else:
            H_king_coords = self.find_piece(board, 'K')

        for move in legal_moves:
            # Checking if there is a hostile piece in the kings legal moves
            piece = board.loc[move]
            if self.case_match(king, piece) is False and not piece == '':
                piece_raycast_moves = self.basic_king(board, board.loc[move].swapcase(), move)
                if H_king_coords in piece_raycast_moves:
                    to_remove.append(move)

        to_remove = list(set(to_remove))

        for i in range(len(to_remove)):
            legal_moves.remove(to_remove[0])
            to_remove.pop(0)
            i -= 1

        return legal_moves

    def king_cannot_move_into_check(self, board, piece, coords, legal_moves,
                                    king_movement_tracker,
                                    rook_movement_tracker):
        '''
        Returns a new set of legal moves that does'nt involve the king getting
        captured
        '''

        to_remove = []
        last_long_castle_tile = None  # 3rd tile in O-O-O castling

        if king_movement_tracker[piece] is False and self.check_for_check(board, piece) is False:
            castle_coords = self.get_castle_coords(board, coords)
        else:
            castle_coords = []

        if piece.isupper():
            king = 'K'
            side = 'white'
        else:
            king = 'k'
            side = 'black'

        corners = self.get_board_corners(board, side)
        left_clear, right_clear = self.check_path_clear(board, coords)

        for move in legal_moves:
            copy = board.copy()

            copy.loc[move] = king
            copy.loc[coords] = ''

            if self.check_for_check(copy, king):
                to_remove.append(move)
                if move in castle_coords:
                    # Left of the king
                    if move == castle_coords[0] or move == castle_coords[1]:
                        left_clear = False
                    # Right of the king
                    elif move == castle_coords[2] or move == castle_coords[3]:
                        right_clear = False
            elif move in castle_coords:
                if castle_coords.index(move) == 1 and left_clear:
                    if (king == 'K' and rook_movement_tracker['left R'] is False) or (king == 'k' and rook_movement_tracker['left r'] is False):
                        last_long_castle_tile = (castle_coords[0][0] - 1,
                                                 castle_coords[0][1])
                        legal_moves.append(last_long_castle_tile)
                        legal_moves.append(castle_coords[0])

                elif castle_coords.index(move) == 2 and right_clear:
                    if (king == 'K' and rook_movement_tracker['right R'] is False) or (king == 'k' and rook_movement_tracker['right r'] is False):
                        if rook_movement_tracker['right R'] is False:
                            legal_moves.append(castle_coords[3])
                    else:
                        if rook_movement_tracker['right r'] is False:
                            legal_moves.append(castle_coords[3])

                    corners = self.get_board_corners(board, side)
                    if board.loc[corners[1]].lower() == 'r':
                        self.move_rook[1] = True

        # Means castling is not an option
        # castle_coords = [] becuase the king moved and its a check
        if last_long_castle_tile in to_remove:
            legal_moves.remove(last_long_castle_tile)
            legal_moves.remove(castle_coords[0])
            to_remove.remove(last_long_castle_tile)
        elif not castle_coords == [] and castle_coords[0] in to_remove and last_long_castle_tile is not None:
            # If the tile 2 down the left of the king is not an option, then
            # remove the 3rd one as well
            legal_moves.remove(last_long_castle_tile)
        elif not castle_coords == []:
            if king == 'K':
                if rook_movement_tracker['left R'] is False:
                    self.move_rook[0] = True
            else:
                if rook_movement_tracker['left r'] is False:
                    self.move_rook[0] = True

            if last_long_castle_tile is not None:
                legal_moves.remove(last_long_castle_tile)

        to_remove = list(set(to_remove))

        for i in range(len(to_remove)):
            legal_moves.remove(to_remove[0])
            to_remove.pop(0)
            i -= 1

        return legal_moves

    def no_ignore_check(self, board, piece, coords, legal_moves):
        '''
        Returns a new set of legal moves that makes sure the piece
        does'nt leave the king hanging while in check
        '''
        to_remove = []

        if piece.isupper():
            king = 'K'
        else:
            king = 'k'

        for move in legal_moves:
            copy = board.copy()

            copy.loc[move] = piece
            copy.loc[coords] = ''

            if self.en_passant == move:
                # Saving is nessesary because complete_en_passant can change
                saved = self.en_passant
                copy = self.complete_en_passant(copy, piece, move)
                self.en_passant = saved

            if self.check_for_check(copy, king):
                to_remove.append(move)

        to_remove = list(set(to_remove))
        for i in range(len(to_remove)):
            legal_moves.remove(to_remove[0])
            to_remove.pop(0)
            i -= 1

        return legal_moves

    def check_for_check(self, board, king):
        '''
        Checks if there is a check on the board
        The ``king`` argument is the king you want to check the CHECK
        against. Input in the form of ``'k'`` or ``'K'``
        '''

        if king.isupper():
            pieces = self.get_letters_coords(board, 'lower')
        else:
            pieces = self.get_letters_coords(board, 'upper')

        king_coords = self.find_piece(board, king)

        for i in range(len(pieces)):
            piece = pieces[i][0]
            coords = pieces[i][1]
            L_piece = piece.lower()

            if L_piece == 'p':
                legal_moves = self.pawn(board, piece, coords)
            if L_piece == 'r':
                legal_moves = self.rook(board, piece, coords)
            if L_piece == 'n':
                legal_moves = self.knight(board, piece, coords)
            if L_piece == 'b':
                legal_moves = self.bishop(board, piece, coords)
            if L_piece == 'q':
                legal_moves = self.queen(board, piece, coords)

            if king_coords in legal_moves:
                return True

        return False

    def check_for_checkmate(self, board, king):
        '''
        Checks if there is a checkmate on the board. Must check for check
        before using this function. If not, it will check for stalemate.
        '''

        if king.isupper():
            pieces = self.get_letters_coords(board, 'upper')
        else:
            pieces = self.get_letters_coords(board, 'lower')

        pieces.append((king, self.find_piece(board, king)))

        for i in range(len(pieces)):
            coords = pieces[i][1]
            legal_moves = self.get_moves(board, coords, {'K': False,
                                                         'k': False},
                                                        {'left R': False,
                                                         'right R': False,
                                                         'left r': False,
                                                         'right r': False})

            # If the piece can't do anything to prevent the check, then the
            # legal moves would be empty. If the legal moves are not empty,
            # then the piece can do something  to prevent the check and
            # therefore it is not a checkmate.
            if not legal_moves == []:
                return False

        return True

    def check_for_draw(self, board):
        '''
        Checks if there is a draw on the board. These are the conditions:

        King vs. King
        King vs. King + Bishop
        King vs. King + Knight
        King vs. King + 2 Bishops
        King vs. King + 2 Knights
        King + Bishop vs. King + Knight
        '''

        upper_letters = self.get_letters_coords(board, 'upper')
        lower_letters = self.get_letters_coords(board, 'lower')
        N = 0
        n = 0
        B = 0
        b = 0
        upper_others = 0
        lower_others = 0

        for item in upper_letters:
            if item[0] == 'N':
                N += 1
            elif item[0] == 'B':
                B += 1
            else:
                upper_others += 1

        for item in lower_letters:
            if item[0] == 'n':
                n += 1
            elif item[0] == 'b':
                b += 1
            else:
                lower_others += 1

        # If you don't check for check before checking for checkmate,
        # it becomes a check for stalemate
        if self.check_for_checkmate(board, 'K'):
            return True
        if self.check_for_checkmate(board, 'k'):
            return True
        # If the list if empty, then there is only 1 piece for that
        # side which is the king
        elif upper_letters == [] and lower_letters == []:
            return True
        # B + K vs k
        # B + B + K vs k
        elif B >= 1 and N == 0 and upper_others == 0 and lower_others == 0 and b == 0 and n == 0:
            return True
        # b + k vs K
        # b + b + k vs K
        elif b >= 1 and n == 0 and lower_others == 0 and upper_others == 0 and B == 0 and N == 0:
            return True
        # N + K vs k
        # N + N + K vs k
        elif N >= 1 and B == 0 and upper_others == 0 and lower_others == 0 and b == 0 and n == 0:
            return True
        # n + k vs K
        # n + n + k vs K
        elif n >= 1 and b == 0 and lower_others == 0 and upper_others == 0 and B == 0 and N == 0:
            return True
        # B + K vs b + k
        elif B == 1 and N == 0 and upper_others == 0 and lower_others == 0 and b == 1 and n == 0:
            return True
        # N + N + K vs k
        elif N == 2 and B == 0 and upper_others == 0 and lower_others == 0 and b == 0 and n == 0:
            return True
        # N + K vs n + k
        elif N == 1 and B == 0 and upper_others == 0 and lower_others == 0 and n == 1 and b == 0:
            return True
        # N + K vs B + K
        elif N == 1 and B == 0 and upper_others == 0 and lower_others == 0 and b == 1 and n == 0:
            return True
        # B + K vs n + K
        elif B == 1 and N == 0 and upper_others == 0 and lower_others == 0 and n == 1 and b == 0:
            return True
        else:
            return False
