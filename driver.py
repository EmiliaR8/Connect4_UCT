import random
from Board import Board
from strategy import UniformRandom

def play_game(verbose="None", parameter=0):
    """Play a full game of Connect Four with random players"""
    board = Board()
    board.bindPlayer(UniformRandom(), "R")
    board.bindPlayer(UniformRandom(), "Y")
    
    game_result = None
    while game_result is None:
        game_result = board.turn(verbose, parameter)
    
    if verbose != "None":
        if game_result == -1:
            print("Red wins!")
        elif game_result == 1:
            print("Yellow wins!")
        else:
            print("Draw!")
    
    print(board.board)
    
    return game_result

if __name__ == "__main__":
    # Unseeded randomness
    #random.seed(50)
    play_game(verbose = 'verbose')
    