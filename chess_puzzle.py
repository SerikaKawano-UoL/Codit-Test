'''Chess Puzzle Programming

This is main module for the chess puzzle programming course work.

Author : Serika Kawano
Created: 2024-12-05
Updated: 2024-12-20
'''

import pdb
import random
from typing import List, NamedTuple, cast


# ---------------
# Classes
# ---------------
# < Piece Class >
#region
class Piece:
    '''
    Piece class

    Description

    Created: 2024-12-05
    Updated: 2024-12-14
    '''

    def __init__(self, pos_x: int, pos_y: int, side: bool):
        '''
        Constructor

        [arguments]
        pos_x: int - The x-coordinate of the piece
        pos_y: int - The y-coordinate of the piece
        side: bool - The side of the piece (True for White, False for Black)
        '''
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._side = side

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value: int):
        if value < 0:
            raise ValueError('The x-coordinate must be a non-negative integer.')
        self._pos_x = value

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value: int):
        if value < 0:
            raise ValueError('The y-coordinate must be a non-negative integer.')
        self._pos_y = value

    @property
    def side(self) -> bool:
        # True for White, False for Black
        return self._side

    @side.setter
    def side(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError('Side must be a boolean value (True or False).')
        self._side = value
#endregion

# < Board Variable >
#region
Board = tuple[int, list[Piece]]
#endregion

# < Bishop Class >
#region
class Bishop(Piece):
    '''
    Bishop class

    Description

    Created: 2024-12-05
    Updated: 2024-12-20
    '''

    def __init__(self, pos_x: int, pos_y: int, side: bool):
        '''
        Constructor
        
        [arguments]
        pos_x: int - The x-coordinate of the piece
        pos_y: int - The y-coordinate of the piece
        side: bool - The side of the piece (True for White, False for Black)
        '''
        super().__init__(pos_x, pos_y, side)
	

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        [specification]
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        True or False
        '''

        dx = abs(pos_X - self.pos_x)
        dy = abs(pos_Y - self.pos_y)

        # 1. Check if the move is diagonal
        if dx != dy:
            return False

        # 2. Check if there are any pieces blocking the path
        step_x = 1 if pos_X > self.pos_x else -1
        step_y = 1 if pos_Y > self.pos_y else -1
        x, y = self.pos_x + step_x, self.pos_y + step_y

        # 3. Check each intermediate position to see if it is blocked
        while (x != pos_X or y != pos_Y):
            # Check if the position is blocked
            if is_piece_at(x, y, B):
                return False
            x += step_x
            y += step_y
        
            # Break condition to prevent overshooting
            if (step_x > 0 and x > pos_X) or (step_x < 0 and x < pos_X):
                break
            if (step_y > 0 and y > pos_Y) or (step_y < 0 and y < pos_Y):
                break

        # 4. Return True if the position is reachable without blockage
        return True


    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        [specification]
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        True or False
        '''

        # 1. Check if the position is reachable
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        # 2. Check if there is a friendly piece at the target position
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            if piece.side == self.side:
                # Cannot capture a friendly piece
                return False

        # 3. Check for a check on the king
        new_board = self.move_to(pos_X, pos_Y, B)
        if is_check(self.side, new_board):
            return False

        # 4. Return
        return True


    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        [specification]
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        True or False
        '''

        # 1. Remove the piece from its original position
        new_pieces = [p for p in B[1] if p != self]
    
        # 2. Check if there is an opponent piece at the target position
        captured_piece = None
        for piece in B[1]:
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                captured_piece = piece
                break

        # 3. If there is a captured piece, remove it from the board
        if captured_piece:
            new_pieces = [p for p in new_pieces if p != captured_piece]

        # 4. Add the bishop to the new position
        new_piece = Bishop(pos_X, pos_Y, self.side)
        new_pieces.append(new_piece)
    
        # 5. Return the updated board
        new_board = Board((B[0], new_pieces))

        # 6. Return the updated board
        return new_board
#endregion

# < King Class >
#region
class King(Piece):
    '''
    King class

    Description

    Created: 2024-12-05
    Updated: 2024-12-14
    '''
    def __init__(self, pos_x: int, pos_y: int, side: bool):
        '''
        Constructor
        
        [arguments]
        pos_x: int - The x-coordinate of the piece
        pos_y: int - The y-coordinate of the piece
        side: bool - The side of the piece (True for White, False for Black)
        '''
        super().__init__(pos_x, pos_y, side)

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        [specification]
        checks if this king can move to coordinates pos_X, pos_Y on board B according to rule 
        [Rule2] and [Rule3]

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        True or False
        '''

        dx = abs(pos_X - self.pos_x)
        dy = abs(pos_Y - self.pos_y)

        # 1. Check if the king moves within 1 square
        if dx > 1 or dy > 1:
            return False

        # 2. Check if there's a friendly piece at the target position
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            if piece.side == self.side:
                return False

        # 3. Return True if all checks pass
        return True


    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        [specification]
        checks if this king can move to coordinates pos_X, pos_Y on board B 
        according to all chess rules

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        True or False
        '''

        # 1. Check if the position is reachable
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        # 2. Check if there is a friendly piece at the target position
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            if piece.side == self.side:
                return False

        # 3. Construct the new board after moving the king
        new_board = self.move_to(pos_X, pos_Y, B)

        # 4. Check if the move results in a check on the king
        if is_check(self.side, new_board):
            return False

        # 5. Return True if all checks pass
        return True


    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        [specification]
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules

        [arguments]
        pos_X: int
        pos_Y: int
        B: Board

        [return]
        object: Board
        '''
        # 1. Remove the original piece after the move
        new_pieces = [p for p in B[1] if p != self]

        # 2. Check if there is an opponent piece at the target position
        captured_piece = None
        for piece in B[1]:
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                captured_piece = piece
                break

        # 3. If there is a captured piece, remove it from the board
        if captured_piece:
            new_pieces = [p for p in new_pieces if p != captured_piece]

        # 4. Create a new King piece at the new position
        new_piece = King(pos_X, pos_Y, self.side)

        # 5. Add the new King to the board
        new_pieces.append(new_piece)

        # 6. Return the updated board
        new_board = Board((B[0], new_pieces))

        # 7. Check for check (reject the move if it results in check)
        if is_check(self.side, new_board):
            # If moving results in a check, return the original board
            return B

        # 8. Return the updated board
        return new_board
#endregion


# ---------------
# Static Methods
# ---------------
# < Board Methods >
#region
def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)

    [arguments]
    filename: str

    [return]
    object: Board
    '''
    try:
        # 1. Read the board file
        with open(filename, 'r') as file:
            lines = file.readlines()
        if not lines:
            raise ValueError('The file is empty.') 
        
        # 2. Validate the board size
        board_size = int(lines[0].strip())
        if not (3 <= board_size <= 26):
            raise ValueError(f'The board size must be between 3 and 26. It is {board_size}.')
        
        # 3. Read white pieces from the 2nd line
        white_pieces = parse_pieces(lines[1] if len(lines) > 1 else '', True)
        
        # 4. Read black pieces from the 3rd line
        black_pieces = parse_pieces(lines[2] if len(lines) > 2 else '', False)
        
        # 5. Check the number of kings for each side
        if len([p for p in white_pieces if isinstance(p, King)]) != 1:
            raise ValueError('There must be exactly one white king.')
        if len([p for p in black_pieces if isinstance(p, King)]) != 1:
            raise ValueError('There must be exactly one black king.')

        # 6. Combine white and black pieces
        pieces = white_pieces + black_pieces
        
        # 7. Return
        board = Board((board_size, pieces))
        return board
    
    except IOError:
        raise IOError(f'The file {filename} could not be opened or is invalid.')
    except ValueError as ex:
        raise ValueError(f'Invalid file content: {ex}')


def conf2unicode(B: Board) -> str:
    '''
    Converts board configuration B to a unicode format string 
    (see section Unicode board configurations).

    [arguments]
    B: Board

    [return]
    str
    '''
    # Unicode characters for chess pieces
    white_king = '\u2654'  # ♔
    white_bishop = '\u2657'  # ♗
    black_king = '\u265A'  # ♚
    black_bishop = '\u265D'  # ♝
    empty_space = '\u2001'  # (matching width space)

    # Initialise the unicode string for the board
    board_str = ''

    # Loop through each row from top to bottom (reversed y-axis for proper display)
    for y in range(B[0] - 1, -1, -1):
        for x in range(B[0]):
            # Check if there is a piece at (x, y)
            if is_piece_at(x, y, B):
                # Get the piece at position (x, y)
                piece = piece_at(x, y, B)
                if isinstance(piece, King):
                    board_str += white_king if piece.side else black_king
                elif isinstance(piece, Bishop):
                    board_str += white_bishop if piece.side else black_bishop
            else:
                # Add an empty space for no piece
                board_str += empty_space
        # Add a newline at the end of each row (except the last one)
        board_str += '\n'

    # Return the final board string, stripping the trailing newline
    return board_str.strip()


def save_board(filename: str, B: Board) -> None:
    '''
    saves board configuration into file in current directory in plain format
    
    [arguments]
    filename: str
    B: Board
    '''
    #TODO


def location2index(loc: str) -> tuple[int, int]:
    '''
    converts chess location to corresponding x and y coordinates
    
    [arguments]
    loc: str

    [return]
    index: tuple[int, int]
    '''
    x = ord(loc[0]) - ord('a') + 1
    #y = int(loc[1])
    y = int(loc[1:])

    return (x, y)

	
def index2location(x: int, y: int) -> str:
    '''
    converts  pair of coordinates to corresponding location
    
    [arguments]
    x: int
    y: int

    [return]
    location: str
    '''
    col = chr(x + ord('a') - 1)
    row = str(y)


    return col + row
#endregion

# < Check Methods >
#region
def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''
    checks if there is piece at coordinates pox_X, pos_Y of board B
    
    [arguments]
    pos_X: int
    pos_Y: int
    B: Board

    [return]
    True or False
    ''' 
    # 1. Check if there is a piece at coordinates pos_X, pos_Y on board B
    for piece in B[1]:  # Access pieces with B[1] instead of B[1]
        
        # (Use type-assertion to enable IntelliSense in Visual Studio)
        if not isinstance(piece, Piece):
            raise TypeError('Board must contain only Piece objects.')
        
        # 2. Check if the piece is at the specified coordinates
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
            
    # 3. Return
    return False
	

def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present

    [arguments]
    pos_X: int
    pos_Y: int
    B: Board

    [return]
    object: Piece
    '''

    # (Type-assertion to enable IntelliSense in Visual Studio)
    pieces = cast(List[Piece], B[1])
    
    # 1. Iterate through the pieces to find the piece at the specified coordinates
    for piece in pieces:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece
    
    # 2. Raise an error if no piece is found at the specified position
    raise ValueError(f'Cannot find a piece at {index2location(pos_X, pos_Y)}')


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach

    [arguments]
    side: bool
    B: Board

    [return]
    True or False
    '''

    # 1. Find the position of the king for the given side
    king_pos = None
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king_pos = (piece.pos_x, piece.pos_y)
            break

    # 2. If the king is not found, raise an error
    if not king_pos:
        raise ValueError('King not found')

    # 3. Check if any opponent piece can reach the king's position using can_reach
    for piece in B[1]:
        # Check only opponent pieces (not the king of the same side)
        if piece.side != side:
            # Use can_reach to determine if the piece can attack the king
            if piece.can_reach(king_pos[0], king_pos[1], B):
                # If any opponent piece can reach the king, it's check
                return True  

    # 4. Return False if no opponent piece can reach the king
    return False


def is_checkmate(side: bool, B: Board) -> bool:
    '''
    [specification]
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_move_to

    [arguments]
    side: bool
    B: Board

    [return]
    True or False
    
    '''
    # 1. Check if the side is in check
    if not is_check(side, B):
        return False

    # 2. Iterate over all pieces belonging to the given side
    for piece in B[1]:
        if piece.side == side:
            # 3. Check if any piece can make a valid move
            # Ensure x is within the board's limits
            for x in range(1, B[0] + 1):  
                # Ensure y is within the board's limits
                for y in range(1, B[0] + 1):  
                    # Prevent can_move_to from being called recursively
                    if piece.can_move_to(x, y, B):
                        return False

    # 4. If no valid moves are found, it's checkmate
    return True


def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to
    
    [arguments]
    side: bool
    B: board

    [return]
    True or False
    '''
    # 1. Check if the side is in check
    if is_check(side, B):
        return False

    # 2. Iterate over all pieces of the specified side
    for piece in B[1]:
        # (Use type-assertion to enable IntelliSense in Visual Studio)
        if not isinstance(piece, (King, Bishop)):
            raise TypeError('The piece should be King or Bishop objects.')

        if piece.side == side:
            # 3. Check if any piece can make a valid move
            for x in range(B[0]):
                for y in range(B[0]):
                    if piece.can_move_to(x, y, B):
                        # If a valid move is found, it is not stalemate
                        return False

    # 4. Return (stalemate)
    return True


#endregion

# < Playing Methods >
#region
def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to

    [arguments]
    B: Board

    [return]
    tuple[Piece, int, int]
    '''
    # 1. Collect all black pieces on the board
    black_pieces = [p for p in B[1] if not p.side]

    # 2. Randomly select one black piece
    piece = random.choice(black_pieces)

    # (Use type-assertion to enable IntelliSense in Visual Studio)
    if not isinstance(piece, (King, Bishop)):
        raise TypeError('The piece should be King or Bishop objects.')

    # 3. Check for a valid move for the selected piece
    for x in range(B[0]):
        for y in range(B[0]):
            if piece.can_move_to(x, y, B):
                return (piece, x, y)

    # 4. If no valid move is found, raise an exception
    raise ValueError('No valid moves found for black pieces')
#endregion


# ---------------
# Static Methods (Added)
# ---------------
# < Check Methods >
#region
def is_valid(piece: Piece, from_x: int, from_y: int, to_x: int, to_y: int, board: Board) -> bool:
    '''
    Check if the specified piece can make a valid move

    [arguments]
    piece: Piece
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    board: Board

    [return]
    True or False
    '''
    # (Use type-assertion to enable IntelliSense in Visual Studio)
    if not isinstance(piece, (King, Bishop)):
        raise TypeError('The piece should be King or Bishop objects.')

    # Check if the piece can move to the position
    return piece.can_move_to(to_x, to_y, board)
#endregion

# < Board Methods >
#region
def apply_board(piece: Piece, from_x: int, from_y: int, to_x: int, to_y: int, board: Board) -> Board:
    '''
    Apply the specified move to the board

    [arguments]
    piece: Piece
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    board: Board

    [return]
    object: Board
    '''
    # (Use type-assertion to enable IntelliSense in Visual Studio)
    if not isinstance(piece, (King, Bishop)):
        raise TypeError('The piece should be King or Bishop objects.')

    # 1. Check if the piece can move to the position
    if is_valid(piece, from_x, from_y, to_x, to_y, board):
        return piece.move_to(to_x, to_y, board)

    # 2. If the move is invalid, the board remains unchanged
    return board

def parse_pieces(line: str, is_white: bool) -> list:
    '''
    Parses a line of piece positions and returns a list of Piece objects.

    [arguments]
    line: str
    is_white: bool

    [return]
    list
    '''
    pieces = []
    if line.strip():
        positions = line.strip().split(',')

        # 1. Iterate over each piece position
        for position in positions:
            position = position.strip()

            # 2. Validate position format (must be at least 3 characters')
            if len(position) < 3:
                raise ValueError(f'Invalid position format: {position}. ')

            # 3. Extract the piece type and position
            piece_type, pos = position[0], position[1:]
            column = pos[0].lower()
            row = pos[1:]

            # 4. Validate and convert row to a 0-based index
            try:
                #row = int(row) - 1
                row = int(row)
            except ValueError:
                raise ValueError(f'Invalid row format: {row}. Expected a number.')

             # 5. Validate column and convert it to a 0-based index
            if not ('a' <= column <= 'z'):
                raise ValueError(f'Invalid column format: {column}.')
            #x = ord(column) - ord('a')
            x = ord(column) - ord('a') + 1

            # 6. Create the appropriate piece object based on the piece type
            if piece_type.lower() == 'k':
                pieces.append(King(x, row, is_white))
            elif piece_type.lower() == 'b':
                pieces.append(Bishop(x, row, is_white))
            else:
                raise ValueError(f'Invalid piece type: {piece_type}')
    return pieces
#endregion

# < Playing Methods >
#region
def players_turn(board: Board) -> tuple[int, int, int, int]:
    '''
    Prompt the player (white) to input their move

    [arguments]
    board: Board

    [return]
    position: tuple[int, int, int, int]
    '''

    # 1. Prompt the player to enter their move
    move = input('It is your turn (White). Enter the position to move: ')
    from_loc, to_loc = move[:2], move[2:]
    from_x, from_y = location2index(from_loc)
    to_x, to_y = location2index(to_loc)
    
    # 2. Check if there is a piece at the start location
    if not is_piece_at(from_x, from_y, board):
        print('There is no piece at that location. Please enter again.')
        return players_turn(board)

    # 3. Check if the piece belongs to the player (White)
    piece = piece_at(from_x, from_y, board)
    if piece.side is False:  # If the piece is black
        print('That is not your piece. Please try again.')
        return players_turn(board)

    # 4. Return
    return from_x, from_y, to_x, to_y


def opponents_turn(board: Board) -> tuple[int, int, int, int]:
    '''
    Decide the move for the computer (black)

    [arguments]
    board: Board

    [return]
    position: tuple[int, int, int, int]
    '''

    # 1. Randomly select a black piece and determine the move
    piece, to_x, to_y = find_black_move(board)

    # 2. Return the positions of the selected piece and its move
    return piece.pos_x, piece.pos_y, to_x, to_y
#endregion


# ---------------
# Main Function
# ---------------
def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input('File name for initial configuration: ')
    '''
    while True:
        # 1. Initialisation
        # 1-1. Ask for the file name with the initial configuration
        filename = input('File name for initial configuration: ')

        try:
            # 1-2. Read and print the board from the file
            board = read_board(filename)
            print('The initial configuration is:')
            print(conf2unicode(board)) # TODO

            # 2. Game begins
            while True:
                # 2-1. Player's (White) turn
                # Get the player's move
                from_x, from_y, to_x, to_y = players_turn(board)
                board = apply_board(piece_at(from_x, from_y, board),from_x, from_y, to_x, to_y, board)
                # Display the board after the move
                print(conf2unicode(board))

                # 2-2. Check process
                if is_check(piece_at(to_x, to_y, board).side, board):
                    print('Check!')
                if is_checkmate(piece_at(to_x, to_y, board).side, board):
                    print('Checkmate!')
                    break
                if is_stalemate(piece_at(to_x, to_y, board).side, board):
                    print('Stalemate!')
                    break

                # 2-3. Opponent's (Black) turn
                # Get the computer's move
                from_x, from_y, to_x, to_y = opponents_turn(board)
                board = apply_board(piece_at(from_x, from_y, board),from_x, from_y, to_x, to_y, board)
                # Display the board after the move
                print(conf2unicode(board))

                # 2-4. Check process
                if is_check(piece_at(to_x, to_y, board).side, board):
                    print('Check!')
                if is_checkmate(piece_at(to_x, to_y, board).side, board):
                    print('Checkmate!')
                    break
                if is_stalemate(piece_at(to_x, to_y, board).side, board):
                    print('Stalemate!')
                    break

            # 3. Exit
            break
        except Exception as ex:
            print(f'An unexpected error occurred: {ex}')


# DEBUG
if __name__ == '__main__': #keep this in
    main()
