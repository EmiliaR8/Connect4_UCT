import random
import math

class UniformRandom:
    def __init__(self, simulations = 0):
        pass

    def takeTurn(self, board, verbose="None", parameter=None):
        """ Select a move uniformly at random from the board's valid moves."""
        #Gets all valid moves from the board.    
        valid_moves = board.getAvailableSpaces()

        #Checks if there are any valid moves available.
        if not valid_moves:
            raise ValueError("No valid moves available")
        #Select a random move from the valid options
        selected_move = random.choice(valid_moves)

        #Print selected move if verbose output is requested.
        if verbose != "None":
            #Display the move as 1-indexed.
            print(f"Final Move selected: {selected_move + 1}")
        return selected_move
    
class PMCGS:
    def __init__(self, simulations= 50):
        self.simulations = simulations
        self.stats = {}  # Dictionary to store (wi, ni) values for each state
    
    def takeTurn(self, board, verbose="None", parameter=None):
        from Board import Board # Had to import here because of circular dependency
        available_moves = board.getAvailableSpaces()
        if not available_moves:
            raise ValueError("No valid moves available")
            # TODO Lose?
        
        move_stats = {move: [0, 0] for move in available_moves}  # {move: [wi, ni]}
        

        # if move_stats[move][1] == 0 and verbose != "None": #FIXME the printing of stuff again
        #     print("NODE ADDED")

        for i in range(self.simulations):
            move = random.choice(available_moves)
            temp_board = Board(rows=board.row_size, cols=board.column_size, 
                               turnPlayer=board.currentTurn, board=board.board.copy())
            result = self.simulate(temp_board, move, verbose)
            
            # Update stats
            move_stats[move][1] += 1  # ni += 1
            if result == 1 and board.currentTurn == 'Y':
                move_stats[move][0] += 1  # wi += 1 for Yellow win
            elif result == -1 and board.currentTurn == 'R':
                move_stats[move][0] += 1  # wi += 1 for Red win
            
            if verbose != "None": #FIXME dont know what is supposed to print for each setting of verbose (that part was confusing)
                print(f"wi: {move_stats[move][0]}\nni: {move_stats[move][1]}\nMove selected: {move + 1}")

        if verbose != "None": #FIXME dont know what is supposed to print for each setting of verbose (that part was confusing)
            print("\nMove evaluations:")
            for m in range(7):  # Assuming 7 columns
                if m in move_stats:
                    wi, ni = move_stats[m]
                    value = wi / (ni + 1e-6)
                    print(f"Move {m + 1}: V={value:.2f} (wi={wi}, ni={ni})")
                else:
                    print(f"Move {m + 1}: Null (illegal move)")

        
        # Select best move based on win ratio
        best_move = max(available_moves, key=lambda m: move_stats[m][0] / (move_stats[m][1] + 1e-6))
        
        if verbose != "None": #FIXME dont know what is supposed to print for each setting of verbose (that part was confusing)
            print(f"Final move selected: {best_move + 1}")
        
        return best_move
    
    # def simulate(self, board, move):
    #     """Performs a random rollout from the given move until the game ends."""
    #     print("\nSIMMULATING\n\n")
    #     board.putPiece(move, board.currentTurn)
    #     game_result = board.gameOver(move, board.row_size - 1)
    #     current_turn = 'Y' if board.currentTurn == 'R' else 'R'
        
    #     while game_result is None:
    #         valid_moves = board.getAvailableSpaces()
    #         if not valid_moves:
    #             return 0  # Draw
            
    #         move = random.choice(valid_moves)
    #         board.putPiece(move, current_turn)
    #         game_result = board.gameOver(move, board.row_size - 1)
    #         current_turn = 'Y' if current_turn == 'R' else 'R'
        
    #     if game_result == 1:
    #         return 1  # Yellow win
    #     elif game_result == -1:
    #         return -1  # Red win
    #     else:
    #         return 0  #Draw ig
        

    def simulate(self, board, move, verbose = "None"):
        if verbose != "None":
            print("\nSIMMULATING\n\n")
        if board.putPiece(move, board.currentTurn) is False:
            return 0  # Illegal move fallback

        if board.getAvailableSpaces() == []:
            return 0  # draw if no moves

        if board.currentTurn == 'R':
            current_turn = 'Y'
        else:
            current_turn = 'R'

        moves_trace = [move]
        game_result = board.gameOver(move, board.row_size - 1)

        while game_result is None:
            valid_moves = board.getAvailableSpaces()
            if not valid_moves:
                game_result = 0
                break

            move = random.choice(valid_moves)
            board.putPiece(move, current_turn)
            moves_trace.append(move)
            game_result = board.gameOver(move, board.row_size - 1)
            current_turn = 'Y' if current_turn == 'R' else 'R'

        if verbose != "None":
            print("Rollout path:", moves_trace)
            print(f"TERMINAL NODE VALUE: {game_result}")

        return game_result

    
class UCT:
    def __init__(self, simulations= 50, exploration=math.sqrt(2)):
        self.simulations = simulations
        self.exploration = exploration
        self.stats = {}  # Stores (wi, ni) for each state
    
    def takeTurn(self, board, verbose="None", parameter=None):
        from Board import Board #Same here
        available_moves = board.getAvailableSpaces()
        if not available_moves:
            raise ValueError("No valid moves available")
        
        move_stats = {move: [0, 0] for move in available_moves}  # {move: [wi, ni]}
        
        for i in range(self.simulations):
            move = self.select_move(available_moves, move_stats)
            temp_board = Board(rows=board.row_size, cols=board.column_size, 
                               turnPlayer=board.currentTurn, board=board.board.copy())
            result = self.simulate(temp_board, move, verbose)
            
            # Update stats
            move_stats[move][1] += 1  # ni += 1
            if result == 1 and board.currentTurn == 'Y':
                move_stats[move][0] += 1  # wi += 1 for Yellow win
            elif result == -1 and board.currentTurn == 'R':
                move_stats[move][0] += 1  # wi += 1 for Red win
            
            if verbose != "None":
                print(f"wi: {move_stats[move][0]}\nni: {move_stats[move][1]}")
                ucb_values = {m: (move_stats[m][0] / (move_stats[m][1] + 1e-6)) + self.exploration * math.sqrt(math.log(sum(ms[1] for ms in move_stats.values()) + 1) / (move_stats[m][1] + 1e-6)) for m in available_moves}
                for m, v in sorted(ucb_values.items()):
                    print(f"V{m + 1}: {v:.2f}")
                print(f"Move selected: {move + 1}")
        
        # Select best move based on win ratio
        best_move = max(available_moves, key=lambda m: move_stats[m][0] / (move_stats[m][1] + 1e-6))
        
        if verbose != "None":
            print(f"Final move selected: {best_move + 1}")
        
        return best_move

    def select_move(self, available_moves, move_stats):
        # First, check for any unvisited moves
        unvisited = [m for m in available_moves if move_stats[m][1] == 0]
        if unvisited:
            return random.choice(unvisited)

        # Otherwise, use UCB formula
        total_visits = sum(move_stats[m][1] for m in available_moves)
        return max(
            available_moves,
            key=lambda m: (
                (move_stats[m][0] / move_stats[m][1]) +
                self.exploration * math.sqrt(math.log(total_visits) / move_stats[m][1])
            )
        )

    def simulate(self, board, move, verbose="None"):
        moves_trace = [move]
        board.putPiece(move, board.currentTurn)
        game_result = board.gameOver(move, board.row_size - 1)
        current_turn = 'Y' if board.currentTurn == 'R' else 'R'

        while game_result is None:
            valid_moves = board.getAvailableSpaces()
            if not valid_moves:
                return 0  # Draw

            move = random.choice(valid_moves)
            moves_trace.append(move)
            board.putPiece(move, current_turn)
            game_result = board.gameOver(move, board.row_size - 1)
            current_turn = 'Y' if current_turn == 'R' else 'R'

        if verbose != "None": #FIXME change this logic to whatever the correct version is
            print("Rollout path:", moves_trace)
            print(f"TERMINAL NODE VALUE: {game_result}")
        return game_result

class GTNode():
    parent = None
    wi = 0
    ni = 0
    
    def __init__(self, parent):
        self.parent = parent
        self.children = {i:None for i in range(7)}
    
    def unexplored_children(self, available):
        """
        Takes a list of available moves and checks 
        if any children are unexplored (have None as in children)
        """
        for i in available:
            if self.children[i] is None:
                return True
        return False