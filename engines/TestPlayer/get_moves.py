class Persist:
    
    def __init__(self):
        self.moves_attack = []
        self.moves_defend = []

global pers
pers = Persist()
def king_safety(board):
    
    attackers = 0
    r = None
    c = None
    for row in range(9):
        if r != None:
            break
        for col in range(9):
            if board[row][col] == 'K':
                r = row
                c = col

    for i,j in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
        if board[i][j] == 'A':
            attackers -= 1
        elif board[i][j] == 'D':
            attackers += 1

    return attackers

def in_danger_pieces(board, player):
    other = not_player(player)
    p = not_player(other[1])[1]
    danger = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == p:
                if row < 8 and row > 0:
                    if board[row + 1][col] == other[0] and capturable_check(board,other[1],row - 1,col):
                        danger += 1

                    if board[row - 1][col] == other[0] and capturable_check(board,other[1],row + 1, col):
                        danger += 1

                if col < 8 and col > 0:
                    if board[row][col + 1] == other[0] and capturable_check(board,other[1],row ,col - 1):
                        danger += 1                        
                    if board[row][col - 1] == other[0] and capturable_check(board,other[1],row,col + 1):
                        danger += 1
    return danger


def capturable_check(board, player, row, col):
    moves = board.get_legal_moves(player)
    for x in moves:
        if x[1] == (row, col):
            return True
    return False

def not_player(player):
    if player == 'attacker':
        return ('D','defender')
    else:
        return ('A','attacker')

def alpha_beta_search(board, cutoff,player):
    x = max_value(board,-100000,100000,cutoff,None,player,[])[1]
    if player == 'attacker':
        pers.moves_attack.append(x)
    else:
        pers.moves_defend.append(x)
    return x


def max_value(board,alpha,beta,cutoff,move,player,visited):
    if (cutoff == 0):
        return evaluate_position(board, player) , move        
    else:
        currentBest = move
        bestAlpha = alpha
        for m in board.get_legal_moves(player):
            b = board.execute_move(m)
            if b in visited:
                continue
            visited.append(b)

            if (b.is_game_over()):
                return evaluate_position(b, player) , m
            tempAlpha = max(bestAlpha, min_values(b,bestAlpha,beta,cutoff-1,currentBest,player,visited)[0])
            #print 'yay',tempAlpha
            if (tempAlpha != bestAlpha):
                currentBest = m
                bestAlpha = tempAlpha
 #               print 'bestAlpha', bestAlpha
            if (bestAlpha >= beta):
                #print 'alpha-inside',bestAlpha
                return bestAlpha, currentBest
#        print 'alpha', bestAlpha
        return bestAlpha, currentBest

def min_values(board,alpha,beta,cutoff,move,player,visited):
    if (cutoff == 0 or board.is_game_over()):
  #      print 'min' , evaluate_position(board, player)
        return evaluate_position(board, player) , move
    else:
        currentBest = move
        bestBeta = beta
        found = False
        for m in board.get_legal_moves(not_player(player)[1]):
            
            b = board.execute_move(m)

            if b in visited:
                continue
            visited.append(b)
            found = True
            if (b.is_game_over()):
                return evaluate_position(b, player) , m

            tempBeta = min(bestBeta, max_value(b,alpha,bestBeta,cutoff-1,currentBest,player,visited)[0])
            if (bestBeta != tempBeta):
                currentBest = m
		bestBeta = tempBeta
#                print 'bestBeta', bestBeta
            if(bestBeta <= alpha):
                #print 'beta-inside',bestBeta
                return bestBeta, currentBest
        #print 'beta', bestBeta
        if not found:
            bestBeta = -150000
        return bestBeta, currentBest

def get_defender_move(board, my_time, opp_time, ply_number):
    cutoff = cutoff_function(my_time, opp_time, ply_number,'defender')
    move = alpha_beta_search(board, cutoff, 'defender')
    print move
    return move

def get_attacker_move(board, my_time, opp_time, ply_number):
    cutoff = cutoff_function(my_time, opp_time, ply_number,'attacker')
    return alpha_beta_search(board, cutoff, 'attacker')
    

def cutoff_function(my_time, opp_time, ply_number,player):
    if ply_number > 4:
        if player == 'attacker':
            if ply_number > 6 and pers.moves_attack[-1] == pers.moves_attack[-3]:
                print 'WOWZERZ'
                return 1
            else:
                return 2
        else:
            if ply_number > 6 and pers.moves_defend[-1] == pers.moves_defend[-3]:
                print 'WOWZERZ'
                return 3
            else:
                return 2
    else:
        return 1




"""
returns the number of clear edges the king can currently move to
"""
def ClearEdges(board):
    edgesClear = 0
    king = [None, None]
    for row in range(9):
        if (king[0] != None):
            break
        for col in range(9):
            if (board[row][col] == 'K'):
                king[0] = row
                king[1] = col
                break
    moves = board.get_legal_moves_for_location(king[0], king[1])
    for move in moves:
        if (board.execute_move(move).is_game_over()):
            edgesClear += 1
    return edgesClear

def KingFreedom(board):
    king = [None, None]
    for row in range(9):
        if (king[0] != None):
            break
        for col in range(9):
            if (board[row][col] == 'K'):
                king[0] = row
                king[1] = col
                break
    moves = board.get_legal_moves_for_location(king[0], king[1])
    return len(moves)

def numberOfPieces(board, player):
    other = not_player(player)[1]
    us = not_player(other)[0]
    number = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == us:
                number += 1
    return number

def evaluate_position(board, player):
    if board.is_game_over():
        if (board.get_winner() == player):
            return 10000
        else:
            return -10000
    elif player == 'defender':
        score = 0
        ourPieces = numberOfPieces(board, player)
        opponentPieces = numberOfPieces(board, not_player(player))
        difference = (ourPieces - opponentPieces) * 100
        clearKing = ClearEdges(board) * 500
        king = king_safety(board) * 15
        InDangerPieces = in_danger_pieces(board, player) * 150
        attackablePieces = in_danger_pieces(board, not_player(player)[1]) * 50
        kingFree = KingFreedom(board) * 50
        score = clearKing + (attackablePieces - InDangerPieces) + king + kingFree + difference
    else:
        score = 0
        ourPieces = numberOfPieces(board, player)
        opponentPieces = numberOfPieces(board, not_player(player))
        difference = (ourPieces - opponentPieces) * 10
        clearKing = ClearEdges(board) * 500
        king = king_safety(board) * 5
        InDangerPieces = in_danger_pieces(board, player) * 100
        attackablePieces = in_danger_pieces(board, not_player(player)[1]) * 150
        kingFree = KingFreedom(board) * 105
        score = - clearKing + (attackablePieces - InDangerPieces) - king - kingFree + difference
    return score
