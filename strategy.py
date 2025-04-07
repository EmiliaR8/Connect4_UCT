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
        
    
    def takeTurn(self, board, verbose="None", parameter=None):
        # Initialization
        root = GTNode()
        return_depth = board.stackHead
        next_turn = {"Y":"R","R":"Y"}
        current_team = board.currentTurn
        # Run simulations to build tree
        for i in range(self.simulations):
            # Tree policy random traversal
            # Node that tracks where we are in the tree
            curr = root
            in_tree = True
            curr_turn = board.currentTurn
            
            while in_tree:
                # Get the next move
                move = random.choice(board.getAvailableSpaces())
                # If selected a move that is not in tree
                if curr.children[move] is None:
                    # Escape tree policy
                    in_tree = False
                    curr.children[move] = GTNode(curr)
                    
                curr = curr.children[move]
                # Make move on board
                # Store the row of last move for gameOver checking
                last_row = board.putPiece(move, curr_turn)
                # Change player
                curr_turn = next_turn[curr_turn]
                # Check if we have won the game During tree policy
                result = board.gameOver(move, last_row)
                if result is not None:
                    in_tree = False
            # Rollout
            # Continue until the end of the game
            while result is None:
                # Rollout policy is random moves
                move = random.choice(board.getAvailableSpaces())
                last_row = board.putPiece(move, curr_turn)
                curr_turn = next_turn[curr_turn]
                
                result = board.gameOver(move, last_row)
            
            # Backpropogate
            while curr.parent is not None:
                curr.ni += 1
                curr.wi += result
                curr = curr.parent
            # Undo moves
            while board.stackHead > return_depth:
                board.undo()
        # Choose the best
        # Check to make sure all moves have been expanded at least once
        for i in board.getAvailableSpaces():
            # If a child hasn't been expanded, it will be None
            if root.children[i] is None:
                # Create a new node
                new_child = GTNode(root)
                # Give it a usage 
                new_child.ni = 1
                # Initialize it as the worst move for a player, red is min, so make it 1
                # Yellow is max, so make it -1
                new_child.wi = {"R":1, "Y":-1}[current_team]
                root.children[i] = new_child
        
        # Take the best move depending on if the current player is red or yellow
        # Red is min, so take min
        # Yellow is max, so take max
        best_move = ({"R":min,"Y":max}[current_team])(board.getAvailableSpaces(), key = lambda i: root.children[i].wi/(root.children[i].ni))
        return best_move
    
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


class GTNode:
    def __init__(self, parent = None):
        self.parent = parent
        self.wi = 0
        self.ni = 0
        self.children = [None for i in range(7)]
    
    def unexplored_children(self, available):
        """
        Takes a list of available moves and checks 
        if any children are unexplored (have None as in children)
        """
        for i in available:
            if self.children[i] is None:
                return True
        return False
