import numpy as np
from Board import Board
from strategy import UniformRandom, PMCGS, UCT
from collections import defaultdict


# def play_game():
#     #generate empty board 
#     board = Board()
    

#     alg = int(input("Please the algorithm you want to use for player 1 RED (1: UR, 2: PMCGS, 3:UCT): "))
#     if alg == 1:
#         board.bindPlayer(UniformRandom(), "R")
#     elif alg == 2:
#         num = int(input("Please the number of simulations for PMCGS: "))
#         board.bindPlayer(PMCGS(simulations = num), "R")
#     elif alg == 3:
#         alg = int(input("Please the number of simulations for UCT "))
#         board.bindPlayer(UCT(simulations = num), "R")
#     else:
#         print("wrong")

#     alg = int(input("Please the algorithm you want to use for player 2 YELLOW (1: UR, 2: PMCGS, 3:UCT): "))
#     if alg == 1:
#         board.bindPlayer(UniformRandom(), "Y")
#     elif alg == 2:
#         num = int(input("Please the number of simulations for PMCGS: "))
#         board.bindPlayer(PMCGS(simulations = num), "Y")
#     elif alg == 3:
#         num = int(input("Please the number of simulations for UCT: ")) 
#         board.bindPlayer(UCT(simulations = num), "Y")
#     else:
#         print("wrong")

#     game_result = None
#     while game_result is None:
#         game_result = board.turn(verbose = "none", parameter = num)


def run_tournament():
    alg_configs = {
        "UR": lambda: UniformRandom(),
        "PMCGS-500": lambda: PMCGS(simulations=500),
        "PMCGS-10000": lambda: PMCGS(simulations=10000),
        "UCT-500": lambda: UCT(simulations=500),
        "UCT-10000": lambda: UCT(simulations=10000)
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
                    winner = yellow_alg if board.currentTurn == "R" else red_alg
                elif result == -1:  # Red wins
                    winner = red_alg if board.currentTurn == "R" else yellow_alg
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