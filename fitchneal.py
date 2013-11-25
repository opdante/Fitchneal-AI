"""
A Fitchneal game driver.
Runs one timed game of Fitchneal by pitting two Python modules against each other.
Each player engine is allowed to "think" only during its own turn.

To launch a game, go to the directory with this file in it and type:
    python fitchneal.py <attacker-engine> <defender-engine> result_log.txt

<attacker-engine> and <defender-engine> must be the names of subfolders inside
of the engines folder.  Several example engines have been provided:

- random: picks a legal move at random
- oneply: evaluates each legal move in terms of material count and chooses the best one
- human: allows a human player to enter moves via the keyboard

For instance, to pit the random engine against the oneply engine, you would run:
    python fitchneal.py random oneply result_log.txt

Each engine folder must contain a get_moves.py module.  This module must provide two
functions, get_attacker_move and get_defender_move.  On each player's turn, the corresponding
function for that player will be called to choose a move.  So, if oneply is the attacker,
then on oneply's turn, get_attacker_move will be called.

The folder must also contain an __init__.py module (which may be empty, but must exist).

Each get_*_move function must return a move to make in the form of a two-element list.
The first element is a (row, col) tuple identifying a piece to move.  The second
element is a (row, col) tuple identifying the square to move it to.  Returning an
illegal move will cause the player to forfeit the match.

Legal moves can be selected from the list returned by board.get_legal_moves(player),
where player is either 'attacker' or 'defender'.

Each get_*_move function is provided with four arguments:
1. board: a copy of the current board, in the form of a Board object
2. time_remaining: the time remaining on the clock for the player to move, in seconds
3. time_opponent: the time remaining for the opposing player, in seconds
4. move_number: the number of the current move, in plies
This information comprises the entire state of the game at each move.

The driver records a game log that contains the details of each move and
displays it at the end of the game.  The log is a series of tuples of the form:
    (move_num, player, move_string, time_remaining)
where player is either 'attacker' or 'defender', and time_remaining is the
number of seconds left for that player after this move.
"""

import sys, thread
from os import times
from copy import deepcopy
from driver.board import Board, move_string


PRINT_LOG = True


def opponent(player):
    if player == 'attacker':
        return 'defender'
    else:
        return 'attacker'

def player_name(player, attacker_engine, defender_engine):
    if player == 'attacker':
        return attacker_engine
    else:
        return defender_engine


def run(attacker_engine, defender_engine, results_file_path):
    engines_a = __import__('engines.' + attacker_engine + '.get_moves')
    engines_d = __import__('engines.' + defender_engine + '.get_moves')
    
    engine_a = engines_a.__dict__[attacker_engine].__dict__['get_moves']
    engine_d = engines_d.__dict__[defender_engine].__dict__['get_moves']
    
    board = Board()
    attacker_time = 5 * 60.0     # 5 minutes/game * 60 seconds/min
    defender_time = attacker_time
    currentPlayer = 'attacker'
    plyNumber = 1
    winner = None
    game_log = []
    
    while not board.is_game_over():
        board.display()
        print 'Current turn: ' + currentPlayer
        if currentPlayer == 'attacker':
            print 'Time remaining: ' + str(attacker_time)
        else:
            print 'Time remaining: ' + str(defender_time)
        
        boardCopy = deepcopy(board)
        legalMoves = board.get_legal_moves(currentPlayer)
        start_time = times()[0]    ## times()[0] is the user time elapsed
        
        # Fetch a move for the current player
        # If the player takes too long, they automatically lose
        if currentPlayer == 'attacker':
            move = engine_a.get_attacker_move(boardCopy, attacker_time, defender_time, plyNumber)
            end_time = times()[0]
            attacker_time -= (end_time - start_time)
            if attacker_time <= 0:
                print 'attacker ' + player_name(currentPlayer, attacker_engine, defender_engine) + ' ran out of time'
                winner = 'defender'
                break
        else:
            move = engine_d.get_defender_move(boardCopy, defender_time, attacker_time, plyNumber)
            end_time = times()[0]
            defender_time -= (end_time - start_time)
            if defender_time <= 0:
                print 'defender ' + player_name(currentPlayer, attacker_engine, defender_engine) + ' ran out of time'
                winner = 'attacker'
                break
        
        # Make sure the move was legal.  An illegal move causes the other player to win.
        if move not in legalMoves:
            print "Illegal move: " + move_string(move)
            print currentPlayer + ' ' + player_name(currentPlayer, attacker_engine, defender_engine) + ' forfeits'
            winner = opponent(currentPlayer)
            break
        
        if currentPlayer == 'attacker':
            game_log.append([plyNumber, currentPlayer, move_string(move), attacker_time])
        else:
            game_log.append([plyNumber, currentPlayer, move_string(move), defender_time])
        
        print str(plyNumber) + '. ' + move_string(move)
        
        # Update the board and switch to the other player.
        board = board.execute_move(move)        
        plyNumber += 1
        currentPlayer = opponent(currentPlayer)
    
    # If the game ended normally, find out who the winner was.
    if board.is_game_over():
        board.display()
        winner = board.get_winner()
        
    print 'Game over, winner is ' + winner + ' ' + player_name(winner, attacker_engine, defender_engine)
    
    if PRINT_LOG:
        print ("\nLog:\n(move_num, player, move_string, time_remaining)")
        for move in game_log:
            print move

    # Update the results file.
    result_str = "attacker=" + attacker_engine + ",defender=" + defender_engine
    if winner == 'attacker':
        result_str += ",winner=" + attacker_engine
    else:
        result_str += ",winner=" + defender_engine
    
    results_file = open(results_file_path, 'a')
    results_file.write(result_str + "\n")
    results_file.close()


if __name__ == '__main__':
    print "---------------------"
    print "Fitchneal Driver"
    print "Joshua Bonner (2009)"
    print "---------------------"
    # check syntax of command line
    if len(sys.argv) != 4:
        print "Usage: " + sys.argv[0] + " attacker_engine defender_engine result_file"
        print "\tex: " + sys.argv[0] + " random human results.log"
        sys.exit()

    results = sys.argv[3]

    run(sys.argv[1], sys.argv[2], results)
