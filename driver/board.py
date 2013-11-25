from copy import deepcopy

"""
Class that represents a Fitchneal board.

The board is represented as a 9x9 two-dimensional array.  A cell at (row, column)
can be accessed using the expression board[row][column].  Each cell can contain:
    'A': attacker piece
    'D': defender piece
    'K': the king
    ' ': empty space

Board objects can be compared using the == and != operators.  Two boards are
equal if they have the same piece configuration.

Moves are represented as a two-element list, where each element is a (row, column) tuple.
The first tuple identifies a piece on the board, and the second tuple identifies the
square to move the piece to.

When the board is displayed, row 8 is shown on top and row 0 on the bottom.
These are labeled 9 and 1 respectively, like a standard chessboard.  Likewise,
columns are labeled a through i instead of 0 through 8.  Therefore, position
f2 refers to column 5, row 1.

"""
class Board:
    
    def __init__(self):
        self.__winner = None
        self.__pieces = [
            ['A', ' ', ' ', 'A', 'A', 'A', ' ', ' ', 'A'],
            [' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'D', ' ', ' ', ' ', ' '],
            ['A', ' ', ' ', ' ', 'D', ' ', ' ', ' ', 'A'],
            ['A', 'A', 'D', 'D', 'K', 'D', 'D', 'A', 'A'],
            ['A', ' ', ' ', ' ', 'D', ' ', ' ', ' ', 'A'],
            [' ', ' ', ' ', ' ', 'D', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' '],
            ['A', ' ', ' ', 'A', 'A', 'A', ' ', ' ', 'A']]
    
    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.__pieces[index]    
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__pieces == other.__pieces
        else:
            return False;
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    
    def is_game_over(self):
        """Returns True if someone has won the game, or False otherwise."""
        return self.__winner != None

    def get_winner(self):
        """Returns the winner of the game.  This will be 'attacker', 'defender',
        or None if the game isn't over yet."""
        return self.__winner
    
    
    def get_legal_moves_for_location(self, row, col):
        """Gets a list of legal moves for the piece at position (row, col)."""
        
        moves = []
        isKing = (self[row][col] == 'K')
        throneLocation = (4, 4)
        
        for destcol in range(col - 1, -1, -1):
            if self[row][destcol] != ' ':
                break
            if isKing or (row, destcol) != throneLocation:
                moves.append([(row, col), (row, destcol)])

        for destcol in range(col + 1, 9, 1):
            if self[row][destcol] != ' ':
                break
            if isKing or (row, destcol) != throneLocation:
                moves.append([(row, col), (row, destcol)])

        for destrow in range(row - 1, -1, -1):
            if self[destrow][col] != ' ':
                break
            if isKing or (destrow, col) != throneLocation:
                moves.append([(row, col), (destrow, col)])

        for destrow in range(row + 1, 9, 1):
            if self[destrow][col] != ' ':
                break
            if isKing or (destrow, col) != throneLocation:
                moves.append([(row, col), (destrow, col)])
                
        return moves
    
    
    def get_legal_moves(self, player):
        """Gets a list of legal moves for the given player, which may be
        'attacker' or 'defender'."""
        
        if player == "attacker":
            # for each A piece, get the spaces they can rook-move to

            pieceMoves = [self.get_legal_moves_for_location(row, col)
                          for row in range(9)
                          for col in range(9)
                          if self[row][col] == 'A']
            
            return [move for moveList in pieceMoves for move in moveList]
        
        else:
            # same, but for 'D' and 'K' pieces
            
            pieceMoves = [self.get_legal_moves_for_location(row, col)
                          for row in range(9)
                          for col in range(9)
                          if self[row][col] == 'D' or self[row][col] == 'K']
            return [move for moveList in pieceMoves for move in moveList]

    
    def __capture(self, attackerPos, targetPos):
        """Private helper function for capturing pieces.  Do not call this."""

        ar, ac = attackerPos
        tr, tc = targetPos
        
        # Make sure target square is on the board
        if tr < 0 or tr > 8 or tc < 0 or tc > 8:
            return
        
        attackingPiece = self[ar][ac]
        targetPiece = self[tr][tc]
        
        # Can only capture a piece belonging to the other player
        if attackingPiece == 'A' and not (targetPiece == 'D' or targetPiece == 'K'):
            return
        if attackingPiece == 'D' and not (targetPiece == 'A'):
            return
        
        if targetPiece == 'K':
            # The king must either be surrounded by four enemy pieces or
            # by three enemy pieces and the throne.
            if tr == 0 or tr == 8 or tc == 0 or tc == 8:
                return
            
            attackers = 0
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if self[tr + dr][tc + dc] == attackingPiece:
                    attackers += 1
            if abs(tr - 4) + abs(tc - 4) == 1:
                attackers += 1
                
            if attackers == 4:
                self[tr][tc] = ' '
                self.__winner = 'attacker'
            
            pass
        else:
            # Otherwise, the target must be trapped between two enemy pieces,
            # one of which is the capturing piece.
            br, bc = 2 * tr - ar, 2 * tc - ac
            if 0 <= br and br <= 8 and 0 <= bc and bc <= 8 and self[br][bc] == attackingPiece:
                self[tr][tc] = ' '
    
    
    def execute_move(self, move):
        """Returns a new board that results from applying the given move to this board."""
        
        pieceRow, pieceCol = move[0]
        targetRow, targetCol = move[1]
        piece = self[pieceRow][pieceCol]
        
        newBoard = deepcopy(self)
        newBoard[pieceRow][pieceCol], newBoard[targetRow][targetCol] = ' ', piece
        
        if piece == 'K': # check for defender win
            if targetRow == 0 or targetRow == 8 or targetCol == 0 or targetCol == 8:
                newBoard.__winner = 'defender'
            
        else: # check for captures
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                newBoard.__capture((targetRow, targetCol), (targetRow + dr, targetCol + dc))
        
        return newBoard
    

    def display(self):
        """Displays the board."""
        
        print '  ---------------------'
        for r in range(8, -1, -1):
            print str(r + 1) + ' |',
            for c in range(9):
                if r == 4 and c == 4 and self.__pieces[r][c] == ' ':
                    print 'T',
                else:
                    print self.__pieces[r][c],
            print '|'
            
        print '  ---------------------'
        print '    ' + ' '.join([get_col_char(c) for c in range(9)])


def get_col_char(col):
    """ converts 1, 2,... to 'a', 'b',... """
    return chr(ord('a')+col)

def moves_string(moves):
    """Returns the given move list as a nicely formatted string.
    example: turns [[(3,3), (3,5)], [(1, 2), (4, 2)] into "d4 => f4, c2 => c5" """
    s = ""
    for i, move in enumerate(moves):
        if i == len(moves)-1:
            s += move_string(move)
        else:
            s += move_string(move) + ', '
    return s

def print_moves(moves):
    """Prints the list of coordinates."""
    print moves_string(moves)

def move_string(move):
    """Converts a numeric (r,c) coordinate like (3,2) into a piece name like "c4" """
    (sy,sx) = move[0]
    (ty,tx) = move[1]
    return get_col_char(sx)+str(sy+1) + ' => ' + get_col_char(tx)+str(ty+1)


if __name__ == '__main__':
    board = Board()
    board.display()

    print "attacker: ",
    print_moves(board.get_legal_moves('attacker'))

    print "defender: ",
    print_moves(board.get_legal_moves('defender'))

