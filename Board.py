import numpy as np
import random
from strategy import UniformRandom, PMCGS, UCT

class Board():
    def __init__(self, rows = 6, cols = 7, turnPlayer = "Y", 
                 yellowPlayer = None, redPlayer = None, board = None, sim_num = 100):
        """
            Initializes a gameboard of a given size and player objects
            
        """
        
        if board is None:
            self.column_size = cols
            self.row_size = rows
            self.board = np.full((self.row_size, self.column_size),'O')
        
        else:
            self.column_size = board.shape[1]
            self.row_size = board.shape[0]
            self.board = board
        

        # Initialize the players based on alg from text file
        player_classes = {
            "UR": UniformRandom,
            "PMCGS": PMCGS,
            "UCT": UCT
        }

        # Initialize Yellow player
        if yellowPlayer in player_classes:
            self.pY = player_classes[yellowPlayer](simulations = sim_num)  # call constructor
        else:
            self.pY = yellowPlayer  # assume it's None

        # Initialize Red player
        if redPlayer in player_classes:
            self.pR = player_classes[redPlayer](simulations = sim_num)  
        else:
            self.pR = redPlayer
        
        self.move_stack = np.zeros((cols*rows), dtype='i4')
        self.currentTurn = turnPlayer
        self.stackHead = -1

    def bindPlayer(self, player, pId = "Y"):
        """
        Adds player to the object as either the yellow player or red player,
        controlled by pId
        
        Parameters:
            player: Player object to add to the game
            pId {"Y", "R"}: whether the player is yellow or red
        """
        if pId == "Y":
            self.pY = player
            
        elif pId == "R":
            self.pR = player


    def buildFromFile(filename, parameter = None):
        """
        Builds a gamestate from a file
        
        Constructs the turn player according to the specifier in the file.
        Designates which player turn it is by the second line.
        Then creates a board state
        """
        
        with open(filename, "rt") as gameReader:
            # Read in alg
            alg = gameReader.readline().strip()
            # Read in turnplayer
            turn = gameReader.readline().strip()
            # Read in board
            board = gameReader.readlines()
            # Strip all trailing newlines from rows in board
            board = list(map(str.strip, board))
        
        arrBoard = np.empty((6,7), dtype = "U1")
        for i in range(len(board)):
            for j in range(len(board[i])):
                arrBoard[i,j] = board[i][j]
        
        # TODO: full list of constructors depending on algorithm 
        if alg == "Term":
            # Use input from terminal
            rPlayer = TerminalPlayer()
            yPlayer = TerminalPlayer()
        elif alg == "UR":
            # Uniform Random
            rPlayer = UniformRandom()
            yPlayer = UniformRandom()
        
        
        return Board(board=arrBoard, turnPlayer=turn, redPlayer=rPlayer, yellowPlayer=yPlayer)

    def getAvailableSpaces(self):
        return list(filter(lambda x: self.board[0,x] == "O", range(7)))
    
    def turn(self, verbosity, parameter):
        
        if self.currentTurn == 'R':
            #Red turn
            selected_col = self.pR.takeTurn(self, verbosity, parameter)
            self.currentTurn = "Y"
            updated_row = self.putPiece(selected_col, "R")
            
        else:
            # Yellow turn
            selected_col = self.pY.takeTurn(self, verbosity, parameter)
            self.currentTurn = "R"
            updated_row = self.putPiece(selected_col,"Y")
        
        return self.gameOver(selected_col, updated_row)
    
    def putPiece(self, index, player):
        """
        Used to put a piece of a specific color in the board
        """
        col = self.board[:,index]
        # Index the last instance of 'O' and replace it with the player code
        row = np.where(col == 'O')[0][-1]
        col[row] = player
        
        # Push to move stack
        self.stackHead += 1
        self.move_stack[self.stackHead] = index*7+row
        return row
    
    def undo(self):
        last_move = self.move_stack[self.stackHead]
        row = last_move%7
        col = last_move//7
        self.board[row,col] = 'O'
        self.move_stack[self.stackHead] = -1
        self.stackHead-=1
        
    
    def gameOver(self, col, row):
        """
        Check if the game is over after placing a piece at (row, col)
        Returns: -1 for Red win, 1 for Yellow win, 0 for draw, None if game continues
        """
        player = self.board[row, col]
        if player == 'O':
            return None
        # Horizontal check
        for c in range(max(0, col - 3), min(col + 1, self.column_size - 3)):
            if (self.board[row, c] == player and 
                self.board[row, c+1] == player and 
                self.board[row, c+2] == player and 
                self.board[row, c+3] == player):
                return -1 if player == 'R' else 1
        # Vertical check
        for r in range(max(0, row - 3), min(row + 1, self.row_size - 3)):
            if (self.board[r, col] == player and 
                self.board[r+1, col] == player and 
                self.board[r+2, col] == player and 
                self.board[r+3, col] == player):
                return -1 if player == 'R' else 1
        # Diagonal (top-left to bottom-right)
        for i in range(-3, 1):
            r, c = row + i, col + i
            if (0 <= r <= self.row_size - 4 and 0 <= c <= self.column_size - 4):
                if (self.board[r, c] == player and 
                    self.board[r+1, c+1] == player and 
                    self.board[r+2, c+2] == player and 
                    self.board[r+3, c+3] == player):
                    return -1 if player == 'R' else 1

        # Diagonal (top-right to bottom-left)
        for i in range(-3, 1):
            r, c = row + i, col - i
            if (0 <= r <= self.row_size - 4 and 3 <= c < self.column_size):
                if (self.board[r, c] == player and 
                    self.board[r+1, c-1] == player and 
                    self.board[r+2, c-2] == player and 
                    self.board[r+3, c-3] == player):
                    return -1 if player == 'R' else 1
        # Check for draw
        if len(self.getAvailableSpaces()) == 0:
            return 0

        # Game continues
        return None
    
    def clone(self):
        """Create a deep copy of the board for simulations"""
        return Board(board=self.board.copy(), turnPlayer=self.currentTurn)
    
class TerminalPlayer():
    def __init__(self):
        pass


    
if __name__ == "__main__":
    b1 = Board.buildFromFile("game1.txt")
    print(b1.board)
    