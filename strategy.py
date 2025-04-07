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
'''    
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
'''

class STNode_():
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.children = {}
        self.wi = 0
        self.ni = 0

    def is_fully_expanded(self, valid_moves):
        return all(move in self.children for move in valid_moves)

    def best_child(self, exploration_param):
        best_value = float('-inf')
        best_move = None
        total_visits = sum(child.ni for child in self.children.values())
        for move, child in self.children.items():
            if child.ni == 0:
                ucb_value = float('inf')
            else:
                win_rate = child.wi / child.ni
                exploration = exploration_param * math.sqrt(math.log(total_visits) / child.ni)
                ucb_value = win_rate + exploration
            if ucb_value > best_value:
                best_value = ucb_value
                best_move = move
        return best_move


class UCT:
    def __init__(self, simulations=500, exploration=math.sqrt(2)):
        self.simulations = simulations
        self.exploration = exploration
        self.root = None

    def takeTurn(self, board, verbose="None", parameter=None):

        if parameter is not None:
            self.simulations = parameter

        available_moves = board.getAvailableSpaces()
        if not available_moves:
            raise ValueError("No valid moves available")

        if self.root is None:
            self.root = STNode_()

        self.root = STNode_()  # Reset the tree every turn (no persistence)

        for _ in range(self.simulations):
            self._tree_search(board, self.root)

        best_move = None
        best_value = float('-inf')

        print(available_moves)
        
        for move in available_moves:
            if move in self.root.children:
                child = self.root.children[move]
                value = child.wi / child.ni if child.ni > 0 else 0
                if value > best_value:
                    best_value = value
                    best_move = move

        if best_move is None:
            best_move = random.choice(available_moves)
            print("we hit random move")

        return best_move

    # def _tree_search(self, board, node):
    #     from Board import Board
    #     visited_nodes = []
    #     current_node = node

    #     while True:
    #         visited_nodes.append(current_node)
    #         available_moves = board.getAvailableSpaces()
    #         if not available_moves:
    #             break

    #         if not current_node.is_fully_expanded(available_moves): #Expansion phase
    #             unexplored_moves = [m for m in available_moves if m not in current_node.children]
                
    #             for move in unexplored_moves:
    #                 # Only play if the column is not full       FIXME
    #                 col = board.board[:, move]
    #                 if 'O' not in col:
    #                     continue  # column is full, skip

    #                 row = board.putPiece(move, board.currentTurn)
    #                 result = board.gameOver(move, row)

    #                 if result is not None:
    #                     new_node = STNode_(move=move, parent=current_node)
    #                     current_node.children[move] = new_node
    #                     visited_nodes.append(new_node)
    #                     self.backpropagate(visited_nodes, result)
    #                     return
    #             # move = random.choice(unexplored_moves)
    #             # row = board.putPiece(move, board.currentTurn)
    #             # result = board.gameOver(move, row)

    #             new_node = STNode_(move=move, parent=current_node)
    #             current_node.children[move] = new_node

    #             # if result is not None:    FIXME
    #             #     self.backpropagate(visited_nodes, result)
    #             #     return

    #             board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
    #             result = self.simulate(board)
    #             self.backpropagate(visited_nodes, result)
    #             return

    #         #Tree policy phase
    #         move = current_node.best_child(self.exploration)
    #         current_node = current_node.children[move]
            
    #         # Skip move if the column is full  FIXME
    #         col = board.board[:, move]
    #         if 'O' not in col:
    #             return  # invalid move, abort this simulation

    #         row = board.putPiece(move, board.currentTurn)
    #         result = board.gameOver(move, row)
    #         if result is not None:
    #             self.backpropagate(visited_nodes, result)
    #             return

    #         board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'

    #     result = self.simulate(board)
    #     self.backpropagate(visited_nodes, result)

    def _tree_search(self, board, node):
        from Board import Board
        visited_nodes = []
        current_node = node

        while True:
            visited_nodes.append(current_node)
            available_moves = board.getAvailableSpaces()


            print("This is the board" ,board.board)
            print("These are the available moves", available_moves)
            # breakpoint()



            if not available_moves:
                break

            if not current_node.is_fully_expanded(available_moves):  # Expansion phase
                unexplored_moves = [m for m in available_moves if m not in current_node.children]

                for move in unexplored_moves:
                    col = board.board[:, move]
                    print("column that we are going to explore",col)
                    if 'O' not in col:
                        print("is full\n\n")
                        continue  # column is full, skip this move
                
                    row = board.putPiece(move, board.currentTurn)
                    result = board.gameOver(move, row)

                    new_node = STNode_(move=move, parent=current_node)
                    current_node.children[move] = new_node
                    visited_nodes.append(new_node)

                    if result is not None:
                        self.backpropagate(visited_nodes, result)
                        return

                    board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
                    result = self.simulate(board)
                    self.backpropagate(visited_nodes, result)
                    return  # Exit after expanding one node

                # If no valid unexplored moves were available, abort this simulation
                return

            # Tree policy phase
            move = current_node.best_child(self.exploration)
            current_node = current_node.children[move]

            # Skip move if the column is full
            col = board.board[:, move]
            print("choson move column:", col)
            if 'O' not in col:
                print("is full \n\n")
                return  # invalid move, abort this simulation

            row = board.putPiece(move, board.currentTurn)
            result = board.gameOver(move, row)
            if result is not None:
                self.backpropagate(visited_nodes, result)
                return

            board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'

        # If the while loop ends with no result (e.g. full board), run a simulation
        result = self.simulate(board)
        self.backpropagate(visited_nodes, result)


    def simulate(self, board):
        current_turn = board.currentTurn
        while True:
            valid_moves = board.getAvailableSpaces()
            if not valid_moves:
                return 0
            move = random.choice(valid_moves)
            row = board.putPiece(move, current_turn)
            result = board.gameOver(move, row)
            if result is not None:
                return result
            current_turn = 'R' if current_turn == 'Y' else 'Y'

    def backpropagate(self, visited_nodes, result):
        for node in visited_nodes:
            node.ni += 1
            if result == 1:
                node.wi += 1
            elif result == 0:
                node.wi += 0.5



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



class STNode():
    def __init__(self, move=None, parent=None):
        self.move = move   #The move (column index) that led to this state.
        self.parent = parent #Pointer to the parent node.
        self.children = {} #Dictionary mapping move -> STNode.
        self.wi = 0 #Wi accumulated through this node.
        self.ni = 0 #Number of times this node was visited.

    def is_fully_expanded(self, valid_moves):
        """Returns True if every valid move from this node has been expanded."""
        return all(move in self.children for move in valid_moves)

    def best_child(self, exploration_param, current_turn):
        """Select the best move using the UCB formula."""
        best_value = float('-inf')
        best_move = None #Change from best_node to best_move
        total_visits = sum(child.ni for child in self.children.values())
        for move, child in self.children.items():
            if child.ni == 0:
                ucb_value = float('inf')
            else:
                win_rate = child.wi / child.ni
                #Adjust win rate for MIN player (assuming 'R' is MIN)
                if current_turn == 'R':
                    win_rate = 1 - win_rate
                exploration = exploration_param * math.sqrt(math.log(total_visits) / child.ni)
                ucb_value = win_rate + exploration
            if ucb_value > best_value:
                best_value = ucb_value
                best_move = move #Store move instead of node
        return best_move #Return move instead of node

#Improved UCT implementation with a traditional tree
#This version adds a heuristc eval for early game moves selection and adds proper min/max handling
class UCT_prime:
    def __init__(self, simulations=500, exploration=math.sqrt(2)):
        self.simulations = simulations
        self.exploration = exploration
        self.root = None #Root node of the search tree
    
    def takeTurn(self, board, verbose="None", parameter=None):
        from Board import Board
        
        #Passes different simulation counts when calling takeTurn().
        if parameter is not None: 
            self.simulations = parameter
            
        available_moves = board.getAvailableSpaces()
        if not available_moves:
            raise ValueError("No valid moves available")
        
        #Initialize root node if needed
        if self.root is None:
            self.root = STNode()

        #Updating the root based on the opponent's last move 
        if hasattr(board, 'move_stack') and hasattr(board, 'stackHead') and board.stackHead > 0:
            last_encoded_move = board.move_stack[board.stackHead-1]
            #Decode the move, extracting just the column from the encoded move
            last_col = last_encoded_move // board.column_size #Using int division to get the column
            
            if last_col in self.root.children:
                self.root = self.root.children[last_col]
                self.root.parent = None #Detach from parent
            else:
                #If move is not there in the tree, reset the tree
                self.root = STNode()

        
        #Check for immediate wi
        for move in available_moves:
            row = board.putPiece(move, board.currentTurn)
            result = board.gameOver(move, row)
            board.undo() #Undo the move to maintain original board

            if (result == 1 and board.currentTurn == 'Y') or (result == -1 and board.currentTurn == 'R'):
                #Return the winning move
                if verbose != "None":
                    print("Winning move found!")
                    print(f"FINAL Move selected: {move + 1}")
                return move
        
        # Save stack position
        original_stack_head = board.stackHead if hasattr(board, 'stackHead') else None

        #Run simulations using tree search
        for i in range(self.simulations):
            self._tree_search(board, self.root, verbose)
            #Restore board to original state
            if original_stack_head is not None:
                while board.stackHead > original_stack_head:
                    board.undo()
            
        #Displaying tree stats if verbose
        if verbose != "None":
            for col in range(7):
                if col in available_moves:
                    if col in self.root.children:
                        child = self.root.children[col]
                        value = child.wi / child.ni if child.ni > 0 else 0
                        print(f"Column {col+1}: {value:.2f}")
                    else:
                        print(f"Column {col+1}: Null")
                else:
                    print(f"Column {col+1}: Null")
        
        #Selecting the best move based on win ratio
        best_move = None
        best_value = float('-inf') if board.currentTurn == 'Y' else float('inf')

        for move in available_moves:
            if move in self.root.children:
                child = self.root.children[move]
                if child.ni > 0:
                    value = child.wi / child.ni
                else:
                    #Set a value that won't be chosen by current player
                    value = float('-inf') if board.currentTurn == 'Y' else float('inf')
                
                if board.currentTurn == 'Y': #MAX player
                    if value > best_value:
                        best_value = value
                        best_move = move
                else: #MIN player
                    if value < best_value:
                        best_value = value
                        best_move = move
            else:
                #If a move hasn't been explored yet, we will initialize it
                if verbose != "None":
                    print("NODE ADDED")
                #Pick this unexplored move
                best_move = move
                break
        
        #If no move was selected, pick a random one
        if best_move is None and available_moves:
            best_move = random.choice(available_moves)
            
        if verbose != "None":
            print(f"FINAL Move selected: {best_move + 1}")

        #Updating the root for the next turn
        if best_move in self.root.children:
            self.root = self.root.children[best_move]
            self.root.parent = None #Detaching from the parent
        else:
            new_node = STNode(move=best_move)
            self.root.children[best_move] = new_node
            self.root = new_node
            self.root.parent = None
            
        return best_move
    
    def _tree_search(self, board, node, verbose):
        """Perform one iteration of UCT tree search"""
        #SELECTION phase
        visited_nodes = [] #Track nodes visited for backpropagation as this allows direct access to all nodes without the need of repeated parent lookups.
        current_node = node
        
        while True:
            visited_nodes.append(current_node)
            
            #Getting available moves
            available_moves = board.getAvailableSpaces()
            if not available_moves:
                break #Terminal state
                
            #Checking if this node is fully expanded
            if not current_node.is_fully_expanded(available_moves):
                #EXPANSION to choose unexplored move
                unexplored_moves = [m for m in available_moves if m not in current_node.children]
                move = random.choice(unexplored_moves)
                if verbose == "Verbose":
                    print("NODE ADDED")
                
                #Make move
                row = board.putPiece(move, board.currentTurn)
                
                #Check for terminal state
                result = board.gameOver(move, row)
                
                #Create new child node
                new_node = STNode(move=move, parent=current_node)
                current_node.children[move] = new_node

                
                if result is not None:
                    #Backpropagate result
                    self.backpropagate(visited_nodes, result)
                    return
                    
                #Switch player
                board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
                
                #Do SIMULATION phase
                result = self.simulate(board, verbose)
                
                #Backpropagate result
                self.backpropagate(visited_nodes, result)
                return
            
            #SELECTION to use UCB to choose move
            move = current_node.best_child(self.exploration, board.currentTurn)
            current_node = current_node.children[move]
            
            if verbose == "Verbose":
                #Print UCB values
                for m in range(7):
                    if m in node.children:
                        child = node.children[m]
                        win_rate = child.wi / child.ni if child.ni > 0 else 0
                        #Adjust for MIN player
                        if board.currentTurn == 'R':
                            win_rate = 1 - win_rate
                        
                        total_visits = sum(c.ni for c in node.children.values())
                        if child.ni == 0:
                            ucb = float('inf')
                        else:
                            exploration = self.exploration * math.sqrt(math.log(total_visits) / child.ni)
                            ucb = win_rate + exploration
                        print(f"V{m+1}: {ucb:.2f}")
                    else:
                        print(f"V{m+1}: Null")
                print(f"Move selected: {move+1}")
            
            #Make move
            row = board.putPiece(move, board.currentTurn)
            
            #Check for terminal state
            result = board.gameOver(move, row)
            if result is not None:
                #Backpropagate result
                self.backpropagate(visited_nodes, result)
                return
                
            #Switch player
            board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
            
        #If we reach here, we're at a terminal state or leaf node
        #We do SIMULATION phase again
        result = self.simulate(board, verbose)
        
        #Backpropagate result
        self.backpropagate(visited_nodes, result)
    
    def simulate(self, board, verbose):
        """Perform a simulation with heuristic guidance"""
        current_turn = board.currentTurn
        playout_depth = 0
        
        #Run simulation until terminal state
        while True:
            valid_moves = board.getAvailableSpaces()
            if not valid_moves:
                return 0 #Draw
                
            #Terminal state check
            if playout_depth > 0: #Skip first iteration as its already checked
                for move in valid_moves:
                    row = board.putPiece(move, current_turn)
                    result = board.gameOver(move, row)
                    
                    if result is not None:
                        board.undo() #Undo the move to maintain the board state
                        if (result == 1 and current_turn == 'Y') or (result == -1 and current_turn == 'R'):
                            #Make the winning move
                            board.putPiece(move, current_turn)
                            return result
                        else:
                            continue
                    
                    board.undo() #Undo the move to maintain the board state
            
            #Early game heuristic
            if playout_depth < 4:
                #Use center bias for early moves
                weights = []
                for m in valid_moves:
                    if m == 3: #Center column
                        weights.append(3.0)
                    elif m in [2, 4]: #Adjacent to center
                        weights.append(2.0)
                    else: #Edge columns
                        weights.append(1.0)
                
                move = random.choices(valid_moves, weights=weights)[0]
            else:
                #Later in game, use random selection
                move = random.choice(valid_moves)
            
            #Make the move
            row = board.putPiece(move, current_turn)
            
            #Check for terminal state
            result = board.gameOver(move, row)
            if result is not None:
                return result
                
            #Switch player and increment depth
            current_turn = 'R' if current_turn == 'Y' else 'Y'
            playout_depth += 1
    
    def backpropagate(self, visited_nodes, result):
        """Update statistics for all visited nodes"""
        for node in visited_nodes:
            node.ni += 1
            
            #Updating wi based on result
            if result == 1: #Yellow win
                node.wi += 1
            elif result == -1: #Red win
                pass #0 wi for Yellow
            else: #Draw
                node.wi += 0.5
