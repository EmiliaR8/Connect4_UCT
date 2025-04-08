import numpy as np
from Board import Board
from strategy import UCT, UCT_prime
from collections import defaultdict


def test():
    """
    Play a single game of Connect Four between the baseline UCT and the improved UCT.
    Allows the user to select algorithms for Red and Yellow players.
    """
    #Generate an empty board
    board = Board()

    #Prompt user to select algorithms for Red and Yellow players
    print("Select algorithm for Red player:")
    print("1: Baseline UCT (10000 simulations)")
    print("2: Improved UCT (10000 simulations)")
    red_alg_choice = int(input("Enter choice (1 or 2): "))
    if red_alg_choice == 1:
        board.bindPlayer(UCT(simulations=10000), "R")
    elif red_alg_choice == 2:
        board.bindPlayer(UCT_prime(simulations=10000), "R")
    else:
        print("Invalid choice for Red player.")
        return

    print("Select algorithm for Yellow player:")
    print("1: Baseline UCT (10000 simulations)")
    print("2: Improved UCT (10000 simulations)")
    yellow_alg_choice = int(input("Enter choice (1 or 2): "))
    if yellow_alg_choice == 1:
        board.bindPlayer(UCT(simulations=10000), "Y")
    elif yellow_alg_choice == 2:
        board.bindPlayer(UCT_prime(simulations=10000), "Y")
    else:
        print("Invalid choice for Yellow player.")
        return

    #Play the game
    game_result = None
    while game_result is None:
        game_result = board.turn(verbosity="None", parameter=10000)

    #Print the result
    if game_result == -1:
        print("Red wins!")
    elif game_result == 1:
        print("Yellow wins!")
    else:
        print("Draw!")

    #Print the final board state
    print(board.board)


def run_tournament():
    """
    Run a tournament comparing the baseline UCT (10000 simulations) with the improved UCT.
    """
    #Define the algorithms to test
    alg_configs = {
        "UCT-10000": lambda: UCT(simulations=10000), #Baseline UCT
        "Improved-UCT-10000": lambda: UCT_prime(simulations=10000) #Improved UCT
    }

    results = defaultdict(lambda: defaultdict(int))
    alg_names = list(alg_configs.keys())
    game = 1

    for i in range(len(alg_names)):
        for j in range(len(alg_names)):
            alg1_name = alg_names[i]
            alg2_name = alg_names[j]
            wins1, wins2 = 0, 0

            print("Current players: ", alg1_name, " (Red) vs ", alg2_name, " (Yellow)")
            for game_num in range(100): #Play 100 games
                print("Playing game: ", game)
                game += 1

                #Alternate first player
                if game_num % 2 == 0:
                    red_alg, yellow_alg = alg1_name, alg2_name
                else:
                    red_alg, yellow_alg = alg2_name, alg1_name

                #Initialize the board
                board = Board()
                board.bindPlayer(alg_configs[red_alg](), "R")
                board.bindPlayer(alg_configs[yellow_alg](), "Y")

                #Play the game
                result = None
                while result is None:
                    result = board.turn(verbosity="None", parameter=10000)

                #Determine the winner
                if result == 1: #Yellow wins
                    winner = yellow_alg if board.currentTurn == "R" else red_alg
                elif result == -1: #Red wins
                    winner = red_alg if board.currentTurn == "R" else yellow_alg
                else:
                    winner = None #Draw

                #Update win counts
                if winner == alg1_name:
                    wins1 += 1
                elif winner == alg2_name:
                    wins2 += 1

            #Store results as percentages
            results[alg1_name][alg2_name] = (wins1 / 100) * 100  # Percentage of wins

    #Print results as table
    print("\nTournament Results (% win rate):")
    print(f"{'':>20}", end='')
    for name in alg_names:
        print(f"{name:>20}", end='')
    print()
    for name1 in alg_names:
        print(f"{name1:>20}", end='')
        for name2 in alg_names:
            win_pct = results[name1][name2]
            print(f"{win_pct:20.2f}", end='')
        print()


# run_tournament()
test()