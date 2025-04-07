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

'''class UCT:
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
        return game_result'''

#Improved UCT implementation with a tree
#This version adds a heuristc eval for early game moves selection and adds proper min/max handling
class UCT:
    def __init__(self, simulations=500, exploration=math.sqrt(2)):
        self.simulations = simulations
        self.exploration = exploration
        self.tree = {} #State -> [wins, visits, {move -> [wins, visits]}]
    
    def takeTurn(self, board, verbose="None", parameter=None):
        from Board import Board
        
        if parameter is not None:
            self.simulations = parameter
            
        available_moves = board.getAvailableSpaces()
        if not available_moves:
            raise ValueError("No valid moves available")
        
        #Convert board to state string
        root_state = self._board_to_state(board)
        
        #Initialize root node if needed
        if root_state not in self.tree:
            self.tree[root_state] = [0, 0, {}] #wins, visits, children
        
        #Check for immediate wins
        for move in available_moves:
            temp_board = board.clone()
            row = temp_board.putPiece(move, temp_board.currentTurn)
            result = temp_board.gameOver(move, row)
            
            if (result == 1 and board.currentTurn == 'Y') or (result == -1 and board.currentTurn == 'R'):
                if verbose != "None":
                    print("Winning move detected!")
                    print(f"FINAL Move selected: {move + 1}")
                return move
        
        #Run simulations using tree search
        for i in range(self.simulations):
            board_copy = board.clone()
            self._tree_search(board_copy, root_state, verbose)
            
        #Displaying tree stats if verbose
        if verbose != "None":
            for col in range(7):
                if col in available_moves:
                    if col in self.tree[root_state][2]:
                        wins, visits = self.tree[root_state][2][col]
                        value = wins / visits
                        print(f"Column {col+1}: {value:.2f}")
                    else:
                        print(f"Column {col+1}: Null")
                else:
                    print(f"Column {col+1}: Null")
        
        #Selecting the best move based on win ratio
        best_move = None
        best_value = float('-inf') if board.currentTurn == 'Y' else float('inf')
        
        for move in available_moves:
            if move in self.tree[root_state][2]:
                wins, visits = self.tree[root_state][2][move]
                value = wins / visits
                
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
            
        return best_move
    
    def _board_to_state(self, board):
        """Convert board to a hashable state string"""
        state = ""
        for r in range(board.row_size):
            for c in range(board.column_size):
                state += board.board[r, c]
        return state
    
    def _tree_search(self, board, state, verbose):
        """Perform one iteration of UCT tree search"""
        #SELECTION phase
        visited_path = [] #Track states and moves visited
        current_state = state
        
        while True:
            visited_path.append(current_state)
            
            #Getting available moves
            available_moves = board.getAvailableSpaces()
            if not available_moves:
                break #Terminal state
                
            #Checking if this is a leaf node
            if current_state not in self.tree:
                #Add new node to the tree
                self.tree[current_state] = [0, 0, {}]
                break
                
            #Checking if all children are in the tree
            unexplored_moves = [m for m in available_moves if m not in self.tree[current_state][2]]
            if unexplored_moves:
                #EXPANSION to choose unexplored move
                move = random.choice(unexplored_moves)
                if verbose == "Verbose":
                    print("NODE ADDED")
                
                #Initialize new child
                self.tree[current_state][2][move] = [0, 0]
                
                #Make move
                row = board.putPiece(move, board.currentTurn)
                
                #Check for terminal state
                result = board.gameOver(move, row)
                if result is not None:
                    #Backpropagate result
                    self.backpropagate(visited_path, [move], result)
                    return
                    
                #Switch player
                board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
                
                #Update state
                next_state = self._board_to_state(board)
                visited_path.append(move)
                visited_path.append(next_state)
                
                #Do SIMULATION phase
                result = self._simulate(board, verbose)
                
                #Backpropagate result
                self.backpropagate(visited_path, [move], result)
                return
            
            #SELECTION to use UCB to choose move
            move = self._select_ucb_move(current_state, board.currentTurn, available_moves)
            
            if verbose == "Verbose":
                #Print UCB values
                current_visits = sum(self.tree[current_state][2][m][1] for m in self.tree[current_state][2])
                for m in range(7):
                    if m in self.tree[current_state][2]:
                        wins, visits = self.tree[current_state][2][m]
                        win_rate = wins / visits
                        #Adjust for MIN player
                        if board.currentTurn == 'R':
                            win_rate = 1 - win_rate
                        
                        exploration = self.exploration * math.sqrt(math.log(current_visits) / visits)
                        ucb = win_rate + exploration
                        print(f"V{m+1}: {ucb:.2f}")
                    else:
                        print(f"V{m+1}: Null")
                print(f"Move selected: {move+1}")
            
            visited_path.append(move)
            
            #Make move
            row = board.putPiece(move, board.currentTurn)
            
            #Check for terminal state
            result = board.gameOver(move, row)
            if result is not None:
                #Backpropagate result
                self.backpropagate(visited_path, [], result)
                return
                
            #Switch player
            board.currentTurn = 'R' if board.currentTurn == 'Y' else 'Y'
            
            #Update state
            current_state = self._board_to_state(board)
            
        #If we reach here, we're at a terminal state or leaf node
        #We do SIMULATION phase again
        result = self._simulate(board, verbose)
        
        #Backpropagate result
        self.backpropagate(visited_path, [], result)
    
    def _select_ucb_move(self, state, current_turn, available_moves):
        """Select move using UCB formula"""
        children = self.tree[state][2]
        total_visits = sum(children[m][1] for m in children)
        
        best_move = None
        best_value = float('-inf')
        
        for move in available_moves:
            if move in children:
                wins, visits = children[move]
                win_rate = wins / visits
                
                #Adjust for MIN player
                if current_turn == 'R':
                    win_rate = 1 - win_rate
                    
                #UCB formula
                exploration = self.exploration * math.sqrt(math.log(total_visits) / visits)
                ucb_value = win_rate + exploration
                
                if ucb_value > best_value:
                    best_value = ucb_value
                    best_move = move
        
        return best_move
    
    def _simulate(self, board, verbose):
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
                    
                    board.undo()  #Undo the move to maintain the board state
            
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
    
    def backpropagate(self, visited_states, visited_moves, result):
        """Update statistics for all visited nodes"""
        #Updating states
        for i, state in enumerate(visited_states):
            self.tree[state][1] += 1 #Increment visits
            
            #Updating wins based on result
            if result == 1: #Yellow win
                self.tree[state][0] += 1
            elif result == -1: #Red win
                pass #0 wins for Yellow
            else: #Draw
                self.tree[state][0] += 0.5
                
            #Update children if applicable
            if i < len(visited_states) - 1 and i < len(visited_moves):
                move = visited_moves[i]
                self.tree[state][2][move][1] += 1 #Increment visits
                
                #Update wins based on result
                if result == 1: #Yellow win
                    self.tree[state][2][move][0] += 1
                elif result == -1: #Red win
                    pass #0 wins for Yellow 
                else: #Draw
                    self.tree[state][2][move][0] += 0.5

class STNode():
    pass