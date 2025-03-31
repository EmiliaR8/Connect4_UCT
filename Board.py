import numpy as np


class Board():
    def __init__(self, rows = 6, cols = 7, turnPlayer = "Y", 
                 yellowPlayer = None, redPlayer = None, board = None):
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
        
        self.pY = yellowPlayer
        self.pR = redPlayer
        
        self.move_stack = np.zeros((col*row))
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


    def buildFromFile(filename):
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
        
        # TODO: full list of combinations 
        
        return Board()

if __name__ == "__main__":
    b = Board()
    print(b.board)
    help(b)
    b1 = Board.buildFromFile("game1.txt")