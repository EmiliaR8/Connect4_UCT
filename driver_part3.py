import numpy as np
from Board import Board
from strategy import UCT, UCT_prime
from collections import defaultdict
import time

def test():
    #generate empty board 
    board = Board()
    
    alg = int(input("Please the algorithm you want to use for player 1 RED (1:UCT, 2: UCT Prime): "))
    if alg == 1:
        num = int(input("Please the number of simulations for UCT: "))
        board.bindPlayer(UCT(simulations = num), "R")
    elif alg == 2:
        num = int(input("Please the number of simulations for UCT prime: "))
        board.bindPlayer(UCT_prime(simulations = num), "R")
    else:
        print("wrong")

    alg = int(input("Please the algorithm you want to use for player 2 Yelliw (1:UCT, 2: UCT Prime): "))
    if alg == 1:
        num = int(input("Please the number of simulations for UCT: "))
        board.bindPlayer(UCT(simulations = num), "Y")
    elif alg == 2:
        num = int(input("Please the number of simulations for UCT prime: "))
        board.bindPlayer(UCT_prime(simulations = num), "Y")
    else:
        print("wrong")

    start_time = time.process_time()
    game_result = None
    while game_result is None:
        game_result = board.turn(verbosity = "None", parameter = num)

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
        "UCT-10000": lambda: UCT(simulations=1000), #Baseline UCT
        "Improved-UCT-10000": lambda: UCT_prime(simulations=1000) #Improved UCT
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

alg_list = ['UCT-10000' , 'Improved-UCT-10000']
red_list = [1]
yellow_list = [0]
run_tournament([alg_list[i] for i in red_list], [alg_list[j] for j in yellow_list])
# test() To run specific amount of simmulations per alg