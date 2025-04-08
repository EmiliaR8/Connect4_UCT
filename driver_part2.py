import numpy as np
from Board import Board
from strategy import UniformRandom, PMCGS, UCT, UCT_prime
from collections import defaultdict
import time

def test():
    #generate empty board 
    board = Board()
    
    alg = int(input("Please the algorithm you want to use for player 1 RED (1: UR, 2: PMCGS, 3:UCT): "))
    if alg == 1:
        board.bindPlayer(UniformRandom(), "R")
        num = 0
    elif alg == 2:
        num = int(input("Please the number of simulations for PMCGS: "))
        board.bindPlayer(PMCGS(simulations = num), "R")
    elif alg == 3:
        num = int(input("Please the number of simulations for UCT "))
        board.bindPlayer(UCT(simulations = num), "R")
    elif alg == 4:
        num = int(input("Please the number of simulations for UCT "))
        board.bindPlayer(UCT_prime(simulations = num), "R")
    else:
        print("wrong")

    alg = int(input("Please the algorithm you want to use for player 2 YELLOW (1: UR, 2: PMCGS, 3:UCT): "))
    if alg == 1:
        board.bindPlayer(UniformRandom(), "Y")
        num = 0
    elif alg == 2:
        num = int(input("Please the number of simulations for PMCGS: "))
        board.bindPlayer(PMCGS(simulations = num), "Y")
    elif alg == 3:
        num = int(input("Please the number of simulations for UCT: ")) 
        board.bindPlayer(UCT(simulations = num), "Y")
    elif alg == 4:
        num = int(input("Please the number of simulations for UCT_prime: ")) 
        board.bindPlayer(UCT_prime(simulations = num), "Y")
    else:
        print("wrong")

    start_time = time.process_time()
    game_result = None
    while game_result is None:
        game_result = board.turn(verbosity = "None", parameter = num)

     #TODO this should be removed since verbose should be used to print info for ALG 2 and 3, winner should be printed in any case
    if game_result == -1:
        print("Red wins!")
    elif game_result == 1:
        print("Yellow wins!")
    else:
        print("Draw!")
    end_time = time.process_time()
    
    print(end_time - start_time)
    print(board.board)


def run_tournament(alg_names_r, alg_names_y):
    alg_configs = {
        "UR": lambda: UniformRandom(),
        "PMCGS-500": lambda: PMCGS(simulations=500),
        "PMCGS-1000": lambda: PMCGS(simulations=1000),
        "UCT-500": lambda: UCT(simulations=500),
        "UCT-1000": lambda: UCT(simulations=1000)
    }

    results = defaultdict(lambda: defaultdict(int))
    alg_names = list(alg_configs.keys())
    
    game = 1
    for i in range(len(alg_names_r)):
        for j in range(len(alg_names_y)):
            alg1_name = alg_names_r[i]
            alg2_name = alg_names_y[j]
            wins1, wins2 = 0, 0
            
            print("current players: ", alg1_name," and ", alg2_name)
            for game_num in range(100):
                print("playing game: ", game)
                game += 1
                # Alternate first player
                

                board = Board()
                board.bindPlayer(alg_configs[alg1_name](), "R")
                board.bindPlayer(alg_configs[alg2_name](), "Y")
                
                result = None
                while result is None:
                    result = board.turn(verbosity="None", parameter=0)

                if result == 1:  # Yellow wins
                    wins2 += 1 
                elif result == -1:  # Red wins
                    wins1 += 1 
                else:
                    winner = None  # draw

            results[alg1_name][alg2_name] = (wins1 / 100) * 100  # percentage

    # Print results as table
    print("\nTournament Results (% win rate):")
    print(f"{'':>15}", end='')
    for name in alg_names:
        print(f"{name:>15}", end='')
    print()
    for name1 in alg_names:
        print(f"{name1:>15}", end='')
        for name2 in alg_names:
            win_pct = results[name1][name2]
            print(f"{win_pct:15.2f}", end='')
        print()

alg_list = ['UR', 'PMCGS-500', 'PMCGS-1000', 'UCT-500', 'UCT-1000']
red_list = [0,1]
yellow_list = [0]
run_tournament([alg_list[i] for i in red_list], [alg_list[j] for j in yellow_list])
#test()