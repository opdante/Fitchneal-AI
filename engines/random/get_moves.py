"""
A move engine that chooses a move at random from the list of legal moves.
"""

import random, time
from driver.board import Board

def get_attacker_move(board, my_time, opp_time, ply_number):
    return random.choice(board.get_legal_moves('attacker'))

def get_defender_move(board, my_time, opp_time, ply_number):
    return random.choice(board.get_legal_moves('defender'))
