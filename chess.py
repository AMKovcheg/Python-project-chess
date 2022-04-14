class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)]
        self.field[1] = [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)]
        self.field[6] = [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)]
        self.field[7] = [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
    def cell(self, row, col):
        piece = self.field[row][col]
        if piece == None:
            return '  '
        color = piece.get_color()
        char = 'w' if color == WHITE else 'b'
        return char + piece.char()
    def current_player_color(self):
            return self.color
    def move_piece(self, row, col, row1, col1):
        global white_can_castling
        global black_can_castling
        global right_wB_empty
        global right_wN_empty
        global right_bB_empty
        global right_bN_empty
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece == None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if (row == 0 and col == 7) or (row == 0 and col == 4):
            white_can_castling = False
        elif (row == 7 and col == 7) or (row == 7 and col == 4):
            black_can_castling = False
        elif row == 0 and col == 5:
            right_wB_empty = True
        elif row == 0 and col == 6:
            right_wN_empty = True
        elif row == 7 and col == 5:
            right_bB_empty = True
        elif row == 7 and col == 6:
            right_bN_empty = True
        if (row1 == 0 and col1 == 7) or (row1 == 0 and col1 == 4):
            white_can_castling = False
        elif (row1 == 7 and col1 == 7) or (row1 == 7 and col1 == 4):
            black_can_castling = False
        elif row1 == 0 and col1 == 5:
            right_wB_empty = False
        elif row1 == 0 and col1 == 6:
            right_wN_empty = False
        elif row1 == 7 and col1 == 5:
            right_bB_empty = False
        elif row1 == 7 and col1 == 6:
            right_bN_empty = False
        if piece.char() == 'K':
            if self.color == WHITE:
                if row == 0 and col == 4 and row1 == 0 and col1 == 6:
                    piece1 = self.field[0][7]
                    self.field[0][7] = None
                    self.field[0][5] = piece1
            else:
                if row == 7 and col == 4 and row1 == 7 and col1 == 6:
                    piece1 = self.field[7][7]
                    self.field[7][7] = None
                    self.field[7][5] = piece1
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)
        return True


class Piece:
    def __init__(self, color):
        self.color = color
    def get_color(self):
        return self.color
    
class Pawn(Piece):
    def char(self):
        return 'P'
    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1:
            return True
        if (row == start_row and row + 2 * direction == row1 and board.field[row + direction][col] is None):
            return True
        else:
            return False
    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1 and (col + 1 == col1 or col - 1 == col1))
                

class King(Piece):
    def char(self):
        return 'K'
    def can_move(self, board, row, col, row1, col1):
        global white_can_castling
        global black_can_castling
        global right_wB_empty
        global right_wN_empty
        global right_bB_empty
        global right_bN_empty
        color = self.color
        if color == WHITE:
            if white_can_castling:
                if row1 == 0 and col1 == 6:
                    return right_wB_empty and right_wN_empty
        else:
            if black_can_castling:
                if row1 == 7 and col1 == 6:
                    return right_bB_empty and right_bN_empty
        if abs(col - col1) > 1 or abs(row - row1) > 1:
            return False
        return True
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Rook(Piece):
    def char(self):
        return 'R'
    def can_move(self, board, row, col, row1, col1):
        if col == col1:
            direction = 1 if (row < row1) else -1
            for i in range(row + direction, row1, direction):
                if board.field[i][col] is not None:
                    return False
            return True
        if row == row1:
            direction = 1 if (col < col1) else -1
            for i in range(col + direction, col1, direction):
                if board.field[row][i] is not None:
                        return False
            return True
        return False
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):
    def char(self):
        return 'B'
    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) == abs(col - col1):
            row_direction = 1 if (row < row1) else -1
            col_direction = 1 if (col < col1) else -1
            j = col + col_direction
            for i in range(row + row_direction, row1, row_direction):
                if board.field[i][j] is not None:
                    return False
                j += col_direction
            return True
        return False
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
    

class Queen(Piece):
    def char(self):
        return 'Q'
    def can_move(self, board, row, col, row1, col1):
        color = self.get_color
        rook = Rook(color)
        bishop = Bishop(color)
        if rook.can_move(board, row, col, row1, col1) or bishop.can_move(board, row, col, row1, col1):
            return True
        return False
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Piece):
    def char(self):
        return 'N'
    def can_move(self, board, row, col, row1, col1):
        if (abs(row - row1) == 2 and abs(col - col1) == 1) or (abs(row - row1) == 1 and abs(col - col1) == 2):
            return True
        return False
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
    

def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE
    
    
def correct_coords(row, col):
    if 0 <= row <= 7 and 0 <= col<= 7:
        return True
    else:
        return False


def check_end_game(board):
    wK_on_the_board = False
    bK_on_the_board = False
    for row in board.field:
        for piece in row:
            if piece is not None:
                if piece.char() == 'K':
                    color = piece.get_color()
                    if color == WHITE:
                        wK_on_the_board = True
                    else:
                        bK_on_the_board = True
    if not wK_on_the_board:
        return [True, "Black won"]
    if not bK_on_the_board:
        return [True, "White won"]
    return [False, None]
    

def print_board(board):
    print("    +----+----+----+----+----+----+----+----+")
    for row in range(7,-1,-1):
        print(" ", row, end = " ")
        for col in range(8):
            print("|", board.cell(row, col), end = " ")
        print("|")
        print("    +----+----+----+----+----+----+----+----+")
    print(end = "      ")
    for col in range(8):
        print(col, end = "    ")
    print()
    

def main():
    board = Board()
    while True:
        print_board(board)
        print("Commands")
        print("    exit")
        print("    move <row> <col> <target row> <target col>")
        if(board.current_player_color() == WHITE):
            print("white's turn")
        else:
            print("black's turn")
        command = input()
        if command == "exit":
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print("Successfully")
        else:
            print("The coordinates are incorrect. Try again")
        list_check = check_end_game(board)
        game_ended = list_check[0]
        message = list_check[1]
        if game_ended:
            print(message)
            break
            
white_can_castling = True
black_can_castling = True
right_wB_empty = False
right_wN_empty = False
right_bB_empty = False
right_bN_empty = False
WHITE = 0
BLACK = 1
if __name__ == "__main__":
    main()

