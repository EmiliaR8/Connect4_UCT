import random
import numpy
from Board import Board
from strategy import UniformRandom, PMCGS, UCT

def play_game(txt_file = "None", verbose="None", parameter=0):
    """Play a full game of Connect Four with random players"""

    #Create the Board, Alg, and Player
    if txt_file == "None":
        board = Board()

        #TODO might want to ask what algorithm to run
        alg = int(input("Please the algorithm you want to use (1: UR, 2: PMCGS, 3:UCT): "))
        if alg == 1:
            board.bindPlayer(UniformRandom(), "R")
            board.bindPlayer(UniformRandom(), "Y")
        elif alg == 2:
            board.bindPlayer(PMCGS(), "R")
            board.bindPlayer(PMCGS(), "Y")
        elif alg == 3:
            board.bindPlayer(UCT(), "R")
            board.bindPlayer(UCT(), "Y")
        else:
            print("wrong")

    else:
        alg, curr_board, player = read_file(txt_file)

        if alg == "UR": #just to ensure that the user does not prompt Uniform Random to go with Verbose != None
            verbose="None"  #or = 0 idk

        board = Board(turnPlayer = player, yellowPlayer = alg, redPlayer = alg, board = curr_board, sim_num = parameter)

    
    game_result = None
    while game_result is None:
        game_result = board.turn(verbose, parameter)
    
    if verbose != "None": #TODO this should be removed since verbose should be used to print info for ALG 2 and 3, winner should be printed in any case
        if game_result == -1:
            print("Red wins!")
        elif game_result == 1:
            print("Yellow wins!")
        else:
            print("Draw!")
    
    print(board.board)
    
    return game_result

import numpy as np


def read_file(txt_file):
    with open(txt_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']
    
    alg = lines[0]               # First line is the algorithm
    player = lines[1]            # Second line is the player
    board_lines = lines[2:8]     # Next 6 lines are the board
    
    board = np.full((6, 7), 'O')  # Default fill
    for i in range(6):
        row = board_lines[i].replace(" ", "")  # Strip out any spaces
        board[i] = list(row)
    
    return alg, board, player


if __name__ == "__main__":
    # Unseeded randomness
    #random.seed(50)
    txt_file = input("Please enter Game Board txt file name: ")
    mode = input("Please enter mode you'd prefer (Brief, Verbose, None): ")
    sim_num = int(input("Please enter the simmulation amount: "))

    play_game(verbose = 'verbose')
    # play_game(txt_file, mode, sim_num) #TODO Uncomment when we will be using the above parameters and edit the function signature of play_game
    