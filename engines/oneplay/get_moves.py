"""
A move engine that evaluates each legal move and chooses the best one.
For the attacker, a winning position is worth 1000 and a losing one is worth -1000.
All other positions are evaluated based on the difference between the number of
attacker pieces and defender pieces.  The defender uses the same scoring mechanism,
but all scores are negated.
"""

import random, time
from driver.board import Board


def evaluate_position(board):
    
    if board.is_game_over():
        if board.get_winner() == 'attacker':
            return 1000
        else:
            return -1000
    else:
        num_attackers = 0
        num_defenders = 0
        
        for row in range(9):
            for col in range(9):
                if board[row][col] == 'A':
                    num_attackers += 1
                elif board[row][col] == 'D':
                    num_defenders += 1
        
        return num_attackers - num_defenders

def get_attacker_move(board, my_time, opp_time, ply_number):
    
    best_score = -9999
    best_move = None
    
    for move in board.get_legal_moves('attacker'):
        score = evaluate_position(board.execute_move(move))
        if score > best_score:
            best_score = score
            best_move = move    
    
    return best_move

def get_defender_move(board, my_time, opp_time, ply_number):
    best_score = -9999
    best_move = None
    
    for move in board.get_legal_moves('attacker'):
        score = -1 * evaluate_position(board.execute_move(move))
        if score > best_score:
            best_score = score
            best_move = move    
    
    return best_move
