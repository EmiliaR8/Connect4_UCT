import random
from Board import Board
from strategy import UniformRandom

def play_game(verbose="None", parameter=0):
    """Play a full game of Connect Four with random players"""
    board = Board()
    board.bindPlayer(UniformRandom(), "R")
    board.bindPlayer(UniformRandom(), "Y")
    
    game_result = False
    while !game_result:
        game_result = board.turn(verbose, parameter)
    
    if verbose != "None":
        if game_result == -1:
            print("Red wins!")
        elif game_result == 1:
            print("Yellow wins!")
        else:
            print("Draw!")
    
    return game_result
