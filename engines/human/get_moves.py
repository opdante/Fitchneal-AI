"""
This is a human move engine; it simply reads and validates user input
to get the move to make.

Moves should be something like "f2f5", which will move the piece at f2 to
the square at f5.
"""

from driver.board import Board, print_moves

def get_attacker_move(board, time_remaining, time_opponent, move_num):
    return read_move(board, 'attacker')

def get_defender_move(board, time_remaining, time_opponent, move_num):
    return read_move(board, 'defender')

def read_move(board, player):
    # generate the legal moves.
    legal_moves = board.get_legal_moves(player)

    input = raw_input("Enter your move: ")
    move = parse_input(legal_moves, input)
    while not move:
        print "That move is not valid. The legal moves are:"
        print_moves(legal_moves)
        input = raw_input("\nEnter your move: ")
        move = parse_input(legal_moves, input)
    return move

def parse_input(legal_moves, input):
    # parse the input
    valid = False
    # verify length
    if len(input) >= 4:
        xc = input[0]
        yc = input[1]
        
        txc = input[2]
        tyc = input[3]
        
        # validate range
        if xc>='a' and xc <='i' and yc>='1' and yc <='9' and txc>='a' and txc<='i' and tyc>='1' and tyc<='9':
            x = ord(xc)-ord('a') # convert letter to number from 0 to 8
            y = int(yc)-1        # convert numeral to int from 0 to 8
            tx = ord(txc)-ord('a')
            ty = int(tyc)-1

            # create the move
            move = [(y, x), (ty, tx)]

            # validate legality
            if move in legal_moves:
                valid = True
    if valid:
        return move
