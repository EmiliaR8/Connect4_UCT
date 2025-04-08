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


def run_tournament():
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
    for i in range(len(alg_names)):
        for j in range(len(alg_names)):
            alg1_name = alg_names[i]
            alg2_name = alg_names[j]
            wins1, wins2 = 0, 0
            
            print("current players: ", alg1_name," and ", alg2_name)
            for game_num in range(100):
                print("playing game: ", game)
                game += 1
                # Alternate first player
                if game_num % 2 == 0:
                    red_alg, yellow_alg = alg1_name, alg2_name
                else:
                    red_alg, yellow_alg = alg2_name, alg1_name

                board = Board()
                board.bindPlayer(alg_configs[red_alg](), "R")
                board.bindPlayer(alg_configs[yellow_alg](), "Y")
                
                result = None
                while result is None:
                    result = board.turn(verbosity="None", parameter=0)

                if result == 1:  # Yellow wins
                    winner = yellow_alg 
                elif result == -1:  # Red wins
                    winner = red_alg 
                else:
                    winner = None  # draw

                if winner == alg1_name:
                    wins1 += 1
                elif winner == alg2_name:
                    wins2 += 1

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


run_tournament()
#test()