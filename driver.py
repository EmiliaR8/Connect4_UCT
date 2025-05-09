import random
import numpy
from Board import Board
from strategy import UniformRandom, PMCGS, UCT
import sys

def play_game(txt_file = "None", verbose="None", parameter=0):
    """Play a full game of Connect Four with random players"""

    #Create the Board, Alg, and Player
    if txt_file == "None":
        board = Board()

        alg = int(input("Please the algorithm you want to use for player 1 RED (1: UR, 2: PMCGS, 3:UCT): "))
        if alg == 1:
            board.bindPlayer(UniformRandom(), "R")
        elif alg == 2:
            num = int(input("Please the number of simulations for PMCGS: "))
            board.bindPlayer(PMCGS(simulations = num), "R")
        elif alg == 3:
            alg = int(input("Please the number of simulations for UCT "))
            board.bindPlayer(UCT(simulations = num), "R")
        else:
            print("wrong")

        alg = int(input("Please the algorithm you want to use for player 2 YELLOW (1: UR, 2: PMCGS, 3:UCT): "))
        if alg == 1:
            board.bindPlayer(UniformRandom(), "Y")
        elif alg == 2:
            num = int(input("Please the number of simulations for PMCGS: "))
            board.bindPlayer(PMCGS(simulations = num), "Y")
        elif alg == 3:
            num = int(input("Please the number of simulations for UCT: ")) 
            board.bindPlayer(UCT(simulations = num), "Y")
        else:
            print("wrong")

        

    else:
        alg, curr_board, player = read_file(txt_file)

        board = Board(turnPlayer = player, yellowPlayer = alg, redPlayer = alg, board = curr_board, sim_num = parameter)

    
    game_result = None
    
    game_result = board.turn(verbose, parameter)
    
    
    
    
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
    
    # Check for cmd arguments
    num_args = len(sys.argv)
    
    if num_args >= 2:
        txt_file = sys.argv[1]
    else:
        txt_file = input("Please enter Game Board txt file name: ")
    
    if num_args >= 3:
        mode = sys.argv[2]
    else:
        mode = input("Please enter mode you'd prefer (Brief, Verbose, None): ")
    
    if num_args == 4:
        sim_num = int(sys.argv[3])
    else:
        sim_num = int(input("Please enter the simmulation amount: "))
    


    play_game(txt_file, mode, sim_num) #TODO Uncomment when we will be using the above parameters and edit the function signature of play_game
    