
"""
Board is 1D NumPy memory view

Piece type numbers:
- Pawn: 1
- Knight: 2
- Bishop: 3
- Rook: 4
- Queen: 5
- King: 6
Positive for white, negative for Black
"""

import numpy as np

def class_to_piece_number(class_name):
    return {Pawn:1, Knight:2, Bishop:3, Rook:4, Queen:5, King:6}[class_name]
 
def coords_1D_to_2D(pos):
    """
    Takes in 1D coords

    Returns piece coords in tuple (x, y)
    """
    return pos % 8, pos // 8

def coords_2D_to_1D(x, y):
    return y*8 + x

class King:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.rook_castle = [True, True] #Left then right rook
        self.check_king_variable_thingy = None, [-1, -9, -8, -7, 1, 9, 8, 7, -2, 2], None, None, None

    def pin_check(self, board): 
        """
        Checks the pins
        Gets rid of any directions and its opposite if the king is in check
        """
        pinned_pieces = []
        directions = [-1, -9, -8, -7, 1, 9, 8, 7, -2, 2]
        pin_directions = [-1, -9, -8, -7, 1, 9, 8, 7]
        knight_directions = [-10, -17, -15, -6, 10, 17, 15, 6]
        check = []
        check_to_king = [] #The spaces that are in between the king the piece that is checking it
        check_inline = [] #The spaces of the direction being checked (resets after each direction)
        
        
        for d in range(8): #Loop over all directions
            x = self.pos % 8 
            y = self.pos // 8
            check_pos = knight_directions[d] + self.pos
            spaces_to_edge = [(x > 1) * (y > 0), (x > 0) * (y > 1), (x < 7) * (y > 1), (x < 6) * (y > 0), (x < 6) * (y < 7), (x < 7) * (y < 6), (x > 0) * (y < 6), (x > 1) * (y < 7)]
            if spaces_to_edge[d]:
                color_pos = board[check_pos] * self.color
                if color_pos == -2:
                    check.append(check_pos)

            spaces_to_edge = [x, min(y, x), y, min(y, 7-x), 7-x, min(7-y, 7-x), 7-y, min(7-y, x)] 
            possible_pin = 0
            if spaces_to_edge[d]:
                check_pos = directions[d] + self.pos
                color_pos = board[check_pos] * self.color
                if color_pos == -1 and (d == 1 or d == 3):
                    check.append(check_pos)

                for space in range(1, spaces_to_edge[d]+1): #Loop until you hit an opposing piece
                    check_pos = space * directions[d] + self.pos
                    color_pos = board[check_pos] * self.color
                    check_inline.append(check_pos)
                    if (color_pos == -3 or color_pos == -5) and d%2 == 1: #For Bishop and Queen moves
                        if possible_pin == 1: #Piece is pinned
                            pinned_pieces.append(pin_location)
                            pin_directions[d] = 0
                            break
                        elif possible_pin == 0: #In check diagonally
                            check.append(check_pos)
                            check_to_king.append(check_inline)
                            if space != 1: #Cannot take piece
                                directions[d] = 0
                            if d >= 4: #Does not allow king to move backward inline from the check
                                directions[d-4] = 0
                            if d <= 3: #Does not allow king to move backward inline from the check
                                directions[d+4] = 0
                                break
                    elif (color_pos == -4 or color_pos == -5) and d%2 == 0: #For Rook and Queen moves
                        if possible_pin == 1: #Piece is pinned
                            pinned_pieces.append(pin_location)
                            pin_directions[d] = 0
                            break
                        elif possible_pin == 0: #In check horizontally/vertically
                            check.append(check_pos)
                            check_to_king.append(check_inline)
                            if space != 1: #Cannot capture piece since it is too far away for the king to capture
                                directions[d] = 0
                            if d >= 4: #Does not allow king to move backward inline from the check
                                directions[d-4] = 0
                            if d <= 3: #Does not allow king to move backward inline from the check
                                directions[d+4] = 0
                            break

                    elif color_pos > 0: #Same color
                        if possible_pin == 0: #May be a possible pin
                            possible_pin = 1
                            pin_location = check_pos
                        else:
                            break
                check_inline = []
        return pinned_pieces, directions, pin_directions, check, check_to_king

    def possible_moves(self, board):
        _, directions, _, _, _ = self.check_king_variable_thingy
        castling = [True, True, True, True] #Left White, Right White, Left Black, Right Black
        x = self.pos % 8 
        y = self.pos // 8 
        possible_spaces = []

        spaces_to_edge = [x, min(y, x), y, min(y, 7-x), 7-x, min(7-y, 7-x), 7-y, min(7-y, x)]
        new_directions = [-1, -9, -8, -7, 1, 9, 8, 7, -10, -17, -15, -6, 10, 17, 15, 6]
        left_castle, right_castle = self.rook_castle
        for d in range(10): #Loop over all directions
            new_pos = directions[d] + self.pos #Sets a location to the new possible coordinate
            if new_pos >= 0 and new_pos <= 63:
                move = True #If this is true, player can move to new_pos
                color_pos = board[new_pos] * self.color
                x = new_pos % 8 
                y = new_pos // 8 
                spaces_to_edge = [x, min(y, x), y, min(y, 7-x), 7-x, min(7-y, 7-x), 7-y, min(7-y, x)]

                if directions[d] != 0 and color_pos <= 0: #Does not allow the king's space to be a possible move
                    if d == 8 and (color_pos < 0 or left_castle == False):
                        move = False
                    if d == 9 and (color_pos < 0 or right_castle == False):
                        move = False
                    if move == True:
                        for f in range(16): #Loop over all directions for new coordinate
                            
                            check_pos = new_directions[f] + new_pos
                            if not check_pos == self.pos and check_pos >= 0 and check_pos <= 63:
                                color_pos = board[check_pos] * self.color
                                spaces_to_edge = [x, min(y, x), y, min(y, 7-x), 7-x, min(7-y, 7-x), 7-y, min(7-y, x), 0, 0, 0, 0, 0, 0, 0, 0]

                                if color_pos == -2 and f > 8: #For knight moves
                                    move = False
                                    break
                                    
                                else:
                                    for space in range(1, spaces_to_edge[f]+1): #Loop until you hit an opposing piece
                                        check_pos = space * new_directions[f] + new_pos
                                        color_pos = board[check_pos] * self.color
                                        if color_pos > 0: #Running into your own piece does not mean a check so king can move there
                                            break

                                        elif (color_pos == -4 or color_pos == -5) and f%2 == 0 and f <= 7: #For Rook and part of Queen moves
                                            if d == 0:
                                                left_castle = False
                                            elif d == 4:
                                                right_castle = False    
                                            move = False
                                            break

                                        elif (color_pos == -3 or color_pos == -5) and f%2 == 1 and f <= 7: #For Bishop and other part of Queen moves
                                            if d == 0:
                                                left_castle = False
                                            elif d == 4:
                                                right_castle = False 
                                            move = False
                                            break

                                        elif color_pos == -1 and space == 1 and f%2 == 1 and f <= 3: #For Pawn moves
                                            if d == 0:
                                                left_castle = False
                                            elif d == 4:
                                                right_castle = False 
                                            move = False
                                            break
                                        
                                        elif color_pos == -6 and space == 1 and f <= 7: #For King moves
                                            if d == 0:
                                                left_castle = False
                                            elif d == 4:
                                                right_castle = False 
                                            move = False
                                            break
                                        elif d == 8 and (self.rook_castle[0] == False or left_castle == False): #Left Castle
                                            move = False
                                            break

                                        elif d == 9 and (self.rook_castle[1] == False or right_castle == False): #Right Castle
                                            move = False
                    if move:
                        possible_spaces.append(new_pos)
        
        return possible_spaces 

class Rook:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.check_king_variable_thingy = [], None, [], None, []

    def possible_moves(self, board):
        pinned_location, _, pin_directions, _, check_to_king = self.check_king_variable_thingy

        directions = [-1, -8, 1, 8]
        x = self.pos % 8
        y = self.pos // 8
        spaces_to_edge = [x, y, 7-x, 7-y]

        possible_spaces = []
        for d in range(4): #Loop over all directions
            for space in range(1, spaces_to_edge[d]+1): #Loop until you hit an opposing piece
                check_pos = space * directions[d] + self.pos #Position being checked
                color_pos = board[check_pos] * self.color #Positive if piece is friendy, negative if not
                if check_to_king == []: #King is not in check
                    if self.pos in pinned_location and pin_directions[d*2] == 0: #When pinned, only allows to move in the pinned direction
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                    
                    elif not self.pos in pinned_location:
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                elif check_pos in check_to_king[0] and not self.pos in pinned_location and len(check_to_king) == 1: #Can capture the piece checking the king or block a check (is not pinned)
                    possible_spaces.append(check_pos)
                    break
                if color_pos > 0:
                    break

        return possible_spaces 

class Bishop:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.check_king_variable_thingy = [], None, [], None, []

    def possible_moves(self, board):
        pinned_location, _, pin_directions, _, check_to_king = self.check_king_variable_thingy

        directions = [-9, -7, 9, 7]
        x = self.pos % 8
        y = self.pos // 8
        spaces_to_edge = [min(y, x), min(y, 7-x), min(7-y, 7-x), min(7-y, x)]

        possible_spaces = []

        for d in range(4): #Loop over all directions
            for space in range(1, spaces_to_edge[d]+1): #Loop until you hit an opposing piece
                check_pos = space * directions[d] + self.pos  #Position being checked
                color_pos = board[check_pos] * self.color #Positive if piece is friendy, negative if not
                if check_to_king == []:
                    if self.pos in pinned_location and pin_directions[d*2+1] == 0: #King is not in check
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                    
                    elif not self.pos in pinned_location:
                        if color_pos > 0:
                            break
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                elif check_pos in check_to_king[0] and not self.pos in pinned_location and len(check_to_king) == 1: #Can capture the piece checking the king or block a check
                    possible_spaces.append(check_pos)
                    break

        return possible_spaces

class Knight:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.check_king_variable_thingy = [], None, None, [], []
    
    def possible_moves(self, board):
        pinned_location, _, _, check_location, check_to_king = self.check_king_variable_thingy

        directions = [-10, -17, -15, -6, 10, 17, 15, 6]
        x = self.pos % 8
        y = self.pos // 8
        spaces_to_edge = [(x > 1) * (y > 0), (x > 0) * (y > 1), (x < 7) * (y > 1), (x < 6) * (y > 0), (x < 6) * (y < 7), (x < 7) * (y < 6), (x > 0) * (y < 6), (x > 1) * (y < 7)]
        possible_spaces = []
        if not self.pos in pinned_location: 
            for d in range(8): #Loop over all directions
                if spaces_to_edge[d]:
                    check_pos = directions[d] + self.pos #Position being checked
                    color_pos = board[check_pos] * self.color #Positive if piece is friendy, negative if not
                    if color_pos <= 0 and check_location == []:
                        possible_spaces.append(check_pos) #Can move to the space being checked

                    elif len(check_to_king) == 1 and check_pos in check_to_king[0]: #Can block a check
                        possible_spaces.append(check_pos)
        return possible_spaces

class Queen:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.check_king_variable_thingy = [], None, [], None, []

    def possible_moves(self, board):
        pinned_location, _, pin_directions, _, check_to_king = self.check_king_variable_thingy

        directions = [-1, -9, -8, -7, 1, 9, 8, 7]
        x = self.pos % 8 
        y = self.pos // 8
        spaces_to_edge = [x, min(y, x), y, min(y, 7-x), 7-x, min(7-y, 7-x), 7-y, min(7-y, x)]
        possible_spaces = []
        
        for d in range(8): #Loop over all directions
            for space in range(1, spaces_to_edge[d]+1): #Loop until you hit an opposing piece
                check_pos = space * directions[d] + self.pos
                color_pos = board[check_pos] * self.color
                if check_to_king == []:
                    if self.pos in pinned_location and pin_directions[d] == 0: #King is not in check
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                    
                    elif not self.pos in pinned_location:
                        if color_pos > 0:
                            break
                        if color_pos < 0:
                            possible_spaces.append(check_pos) #Can capture
                            break
                        else:
                            possible_spaces.append(check_pos)
                elif check_pos in check_to_king[0] and not self.pos in pinned_location and len(check_to_king) == 1: #Can capture the piece checking the king or block a check
                    possible_spaces.append(check_pos)
                    break

        return possible_spaces

class Pawn:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color #1 for white, -1 for black
        self.check_king_variable_thingy = [], None, [], None, []
        self.en_passant = None
        self.directions = [-16 * self.color, -9 * self.color, -8 * self.color, -7 * self.color]

    def possible_moves(self, board):
        pinned_location, _, pin_directions, _, check_to_king = self.check_king_variable_thingy

        
        y = self.pos // 8
        move_2 = True
        possible_spaces = []
        if not self.pos in pinned_location or abs(sum(pin_directions)) == 8:
            check_pos = self.directions[2] + self.pos
            color_pos = board[check_pos] * self.color
            if color_pos == 0 and (check_to_king == [] or (check_pos in check_to_king[0] and len(check_to_king) == 1)): #Move one forward
                possible_spaces.append(check_pos)
            else: 
                move_2 = False

            check_pos = self.directions[0] + self.pos
            try:
                color_pos = board[check_pos] * self.color
            except IndexError: #Ignore if it goes off board
                pass
            if not ((2 * y) - (5 * self.color) == 7):
                move_2 = False
            if color_pos == 0 and move_2 == True and (check_to_king == [] or (check_pos in check_to_king[0] and len(check_to_king) == 1)): #Can move two forward
                possible_spaces.append(check_pos)

        if not self.pos in pinned_location:
            check_pos = self.pos - self.color
            if (check_to_king == [] or check_to_king == [check_pos]) and self.en_passant == check_pos: #En passant Left
                possible_spaces.append(self.directions[1] + self.pos)

            check_pos = self.pos + self.color
            if (check_to_king == [] or check_to_king == [check_pos]) and self.en_passant == check_pos: #En passant Right
                possible_spaces.append(self.directions[3] + self.pos)
        
        if pinned_location == [] or (self.pos in pinned_location and pin_directions[1] == 0):
            check_pos = self.directions[1] + self.pos
            color_pos = board[check_pos] * self.color
            if color_pos < 0: #Can capture diagonal left
                possible_spaces.append(check_pos)

        if pinned_location == [] or self.pos in pinned_location and pin_directions[3] == 0:
            check_pos = self.directions[3] + self.pos
            color_pos = board[check_pos] * self.color
            if color_pos < 0: #Can capture diagonal right
                possible_spaces.append(check_pos)

        return possible_spaces
        
class Game:
    def __init__(self, board=None):
        """
        If `board` is `None`, `reset()` is called.
        """
        if board:
            self.board = board
        else:
            self.reset()
        self.board = np.array(self.board)

        self.white_pieces = [
            Pawn(48, 1), Pawn(49, 1), Pawn(50, 1), Pawn(51, 1), Pawn(52, 1), Pawn(53, 1), Pawn(54, 1), Pawn(55, 1),  
            Rook(56, 1), Knight(57, 1), Bishop(58, 1), Queen(59, 1), King(60, 1), Bishop(61, 1), Knight(62, 1), Rook(63, 1),
        ]
        self.black_pieces = [
            Rook(0, -1), Knight(1, -1), Bishop(2, -1), Queen(3, -1), King(4, -1), Bishop(5, -1), Knight(6, -1), Rook(7, -1),
            Pawn(8, -1), Pawn(9, -1), Pawn(10, -1), Pawn(11, -1), Pawn(12, -1), Pawn(13, -1), Pawn(14, -1), Pawn(15, -1),  
            ]
        self.castling = [True, True, True, True] #Left White, Right White, Left Black, Right Black
        self.en_passant = None
        self.last_move = None
        self.check_location = []
        self.player_color = 1
        self.end = False

    def convert_to_board(self):
        self.board = np.zeros((8, 8))
        for piece in self.white_pieces:
            x, y = coords_1D_to_2D(piece.pos)
            self.board[y, x] = {Pawn:1, Knight:2, Bishop:3, Rook:4, Queen:5, King:6}[piece.__class__]

        for piece in self.black_pieces:
            x, y = coords_1D_to_2D(piece.pos)
            self.board[y, x] = {Pawn:-1, Knight:-2, Bishop:-3, Rook:-4, Queen:-5, King:-6}[piece.__class__]
            

    def move(self, old_coord, new_coord, promotion=None):
        piece = self.board[old_coord]

        #Get rid of pawn when En Passant
        if self.board[new_coord] == 0 and abs(piece) == 1 and (old_coord % 8 != new_coord % 8):
            captured_piece = new_coord+(self.player_color*8)
            self.board[captured_piece] = 0
            self.delete_piece(captured_piece, -self.player_color)

        #Move the piece on the board
        self.board[old_coord] = 0

        #Disable castling on rook capture
        if abs(self.board[new_coord]) == 4:
            ValueError
            try:
                self.castling[{0:2, 7:3, 56:0, 63:1}[new_coord]] = False
            except KeyError:
                pass

        if abs(piece) == 1 and (new_coord // 8) == 1 or (new_coord // 8) == 7 and not promotion: #If pawn is being promoted and promotion = None, automatically promote to queen
            promotion = 5

        if promotion: #Changes the new coord to the type of piece when a pawn is being promoted
            self.board[new_coord] = promotion * self.player_color
            self.delete_piece(old_coord, self.player_color) #Delete the pawn being promoted

            #Creating a new piece
            promotion_piece_class = {2:Knight, 3:Bishop, 4:Rook, 5:Queen}[promotion]
            if self.player_color == 1:
                self.white_pieces.append(promotion_piece_class(new_coord, self.player_color))
            else:
                self.black_pieces.append(promotion_piece_class(new_coord, self.player_color))

        else: #Changes the new coord to the piece that was at the old coord
            #Delete captured piece
            if self.board[new_coord] != 0:
                self.delete_piece(new_coord, -self.player_color)

            self.board[new_coord] = piece

        #Disable castling on rook move
        if abs(piece) == 4:
            try:
                self.castling[{0:2, 7:3, 56:0, 63:1}[old_coord]] = False
            except KeyError:
                pass
        
        #Disable castling on king move
        if abs(piece) == 6:
            try:
                self.castling[{4:2, 60:0}[old_coord]] = False
                self.castling[{4:3, 60:1}[old_coord]] = False
            except KeyError:
                pass

        if self.player_color == 1: #White castle  
            if new_coord == 58 and old_coord == 60 and piece == 6: #Left Castle
                self.board[56] = 0
                self.board[59] = 4
                self.castling[0] = False

            if new_coord == 62 and old_coord == 60 and piece == 6: #Right Castle
                self.board[63] = 0
                self.board[61] = 4
                self.castling[1] = False

        else: #Black castle
            if new_coord == 2 and old_coord == 4 and piece == -6: #Left Castle
                self.board[0] = 0
                self.board[3] = -4
                self.castling[2] = False

            if new_coord == 6 and old_coord == 4 and piece == -6: #Right Castle
                self.board[7] = 0
                self.board[5] = -4
                self.castling[3] = False
            

        
        #Pass castling status to kings
        #Update white king
        for i in range(len(self.white_pieces)):
            if self.white_pieces[i].__class__ == King:
                self.white_pieces[i].rook_castle = self.castling[0:2]
                break
            
        #Update black king
        for i in range(len(self.black_pieces)):
            if self.black_pieces[i].__class__ == King:
                self.black_pieces[i].rook_castle = self.castling[2:4]
                break

        if abs(piece) == 1 and abs(new_coord - old_coord) == 16: #Checks for En Passant possibility
            self.last_move = new_coord
        else:
            self.last_move = None

        #Pass En passant status to pawns
        pawn_double_push = abs(new_coord - old_coord) == 16
        if self.player_color == -1: #Update pawns
            for i in range(len(self.white_pieces)):
                if self.white_pieces[i].__class__ == Pawn:
                    self.white_pieces[i].en_passant = new_coord if pawn_double_push else None

        else:
            for i in range(len(self.black_pieces)):
                if self.black_pieces[i].__class__ == Pawn:
                    self.black_pieces[i].en_passant = new_coord if pawn_double_push else None


        #Update piece object location
        if not promotion:
            self.get_piece(old_coord, self.player_color).pos = new_coord


        self.game_result = self.outcome()
        if self.game_result != None:
            self.end = True

        #Update player
        self.player_color *= -1

        #Update checks and pins
        self.king_check()


    def king_check(self):
        king_pos = np.argmax(self.board * self.player_color)
        k = King(king_pos, self.player_color)
        pinned_location, directions, pin_directions, self.check_location, check_to_king = k.pin_check(self.board)
        
        if self.player_color == 1: #Update white king
            for white_piece in self.white_pieces:
                white_piece.check_king_variable_thingy = pinned_location, directions, pin_directions, self.check_location, check_to_king
            
        else: #Update black king
            for black_piece in self.black_pieces:
                black_piece.check_king_variable_thingy = pinned_location, directions, pin_directions, self.check_location, check_to_king

    def delete_piece(self, position, color):
        if color == 1: #White piece
            for i in range(len(self.white_pieces)):
                if self.white_pieces[i].pos == position:
                    piece_type = class_to_piece_number(self.white_pieces[i].__class__)
                    del self.white_pieces[i]
                    break

        else: #Black piece
            for i in range(len(self.black_pieces)):
                if self.black_pieces[i].pos == position:
                    piece_type = class_to_piece_number(self.white_pieces[i].__class__)
                    del self.black_pieces[i]
                    break

        if piece_type * color == self.board[position]: #Fail safe to correctly update self.board
            self.board[position] = 0

    def get_piece(self, position, color) -> object:
        """
        Returns the piece object in the position and color specified
        """
        for piece in (self.white_pieces if color == 1 else self.black_pieces):
            if piece.pos == position:
                return piece

        raise ValueError("No piece found")

    def get_moves(self, position, color) -> list:
        """
        Returns a list of the coords of the possible moves of a piece.
        """
        try:
            return self.get_piece(position, color).possible_moves(self.board)
        except ValueError: #Piece doesn't exist in the provided position
            return []
        

    def reset(self):
        """
        Resets to the standard start of a chess game
        """

        self.board = [
        -4, -2, -3, -5, -6, -3, -2, -4,
        -1, -1, -1, -1, -1, -1, -1, -1,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         1,  1,  1,  1,  1,  1,  1,  1,
         4,  2,  3,  5,  6,  3,  2,  4
        ]

        self.player_color = 1

        #Probably need to make sure to reset castling and other stuff later
    

    #Returns list in form [(old_coord, new_coord), ...]
    def all_white_moves(self):
        moves = []
        for piece in self.white_pieces:
            piece_number = piece.possible_moves(self.board)
            old_pos = piece.pos
            moves += [(old_pos, new_pos) for new_pos in piece_number]
        return moves

    def all_black_moves(self):
        moves = []
        for piece in self.black_pieces:
            piece_number = piece.possible_moves(self.board)
            old_pos = piece.pos
            moves += [(old_pos, new_pos) for new_pos in piece_number]
        return moves

    def outcome(self): #outcome is 1 for white win, 0 for draw, and -1 for black win
        """
        Returns 1 for white win, 0 for draw and -1 for black win.
        Otherwise it returns `None`
        """
        if self.player_color * -1 == 1:
            moves = self.all_white_moves()
            if moves == [] and self.check_location != []:
                return -1
            elif moves == []:
                return 0
            else:
                return None

        else:
            moves = self.all_black_moves()
            if moves == [] and self.check_location != []:
                return 1
            elif moves == []:
                return 0 
            else:
                return None
