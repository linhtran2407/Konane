import random
import copy

class GameError(AttributeError):
    """
    This class is used to indicate any problem in the game
    """

class KonaneBoard:
    def __init__(self, size):
        # constructor takes in the size of the board
        self.size = size
        self.resetGame() # create a starting board state

    def resetGame(self):
        """
        Resets the starting board state
        """
        self.board = []
        players = ['X', 'O']
        # iterate each row of the board and place all the pieces (with 2 types X and O) on the board alternately 
        for i in range(self.size):
            row = [players[j % 2] for j in range(self.size)]
            self.board.append(row)
            players.reverse() 

    def __str__(self):
        """
        Print the current board state
        """
        board_str = "  "
        # print the column indices 
        for i in range(self.size):
            board_str += str(i + 1) + " "
        board_str += "\n"
        # print the values row by row
        for i in range(self.size):
            board_str += str(i + 1) + " " # row indices
            # go over each column
            for j in range(self.size):
                board_str += self.board[i][j] + " "
            board_str += "\n" # move on to the next row
        return board_str

    def isValidMove(self, move):
        """Check the validity of move

        Args:
            move (tuple): the move contains row and column indices

        Returns:
            True if the move is valid. Otherwise, return false
        """
        row = move[0]
        col = move[1]
        return 0 <= row < self.size and 0 <= col < self.size

    def contains(self, board, row, col, symbol):
        """Check whether the given row and column is a valid location in the board
        and that location contains the given symbol.

        Args:
            board (2D array): representation of the game's board
            row (int): row index
            col (int): column index
            symbol (string): symbol of the player ('X' or 'O')

        Returns:
            True if the location (with given row and column) is valid and contains
            the given symbol. Otherwise, return false
        """
        return self.isValidMove((row, col)) and board[row][col] == symbol

    def opponent(self, player):
        """Returns the opponent of the current player

        Args:
            player (string): player of the game ('X' or 'O')
        """
        if player == 'X':
            return 'O'
        else:
            return 'X'
    
    def isFirstMove(self, board):
        """Check whether there is any empty space on the board. 

        Args:
            board (2D array): representation of the game's board

        Returns:
            True if there is only at most 1 empty space on the board. 
            Otherwise, return false.
        """
        emptyPieces = 0
        # iterate each row
        for r in range(self.size):
            # iterate each column
            for c in range(self.size):
                if board[r][c] == ".":
                    emptyPieces += 1
                    
        return emptyPieces <= 1

    def makeMove(self, player, move):
        """Updates the current board with the next board created by the given move.

        Args:
            player (str): player of the game ('X' or 'O')
            move (list): a list of integers containing the row and column indices before
                         and after the move: [old_row, old_col, new_row, new_col]
        """
        self.board = self.nextBoard(self.board, player, move)

    def nextBoard(self, board, player, move):
        """Returns the copy of the board after the given move.

        Args:
            board (2D Array): representation of the game's board
            player (str): player of the game ('X' or 'O')
            move (list): a list of integers containing the row and column indices before
                         and after the move: [old_row, old_col, new_row, new_col]

        Raises GameError if the move is invalid
        """
        r1, c1, r2, c2 = int(move[0]), int(move[1]), int(move[2]), int(move[3])
        next_board = copy.deepcopy(board)

        if self.isValidMove((r1, c1)) == False or self.isValidMove((r2, c2)) == False:
            # if either of the location before or after the move is invalid
            raise GameError

        if next_board[r1][c1] != player:
            # if the current location does not contain the given player
            raise GameError

        distance = abs(r1-r2 + c1-c2) # distance between two points vertically/horizontally
        
        if distance == 0:
            if self.isFirstMove(board):
                next_board[r1][c1] = "."
                return next_board

            raise GameError
        
        if next_board[r2][c2] != ".":
            raise GameError

        jumps = (int)(distance/2) # number of possible jumps
        deltaRow = (int)((r2 - r1)/distance)
        deltaCol = (int)((c2 - c1)/distance)

        for i in range(jumps):
            if next_board[r1+deltaRow][c1+deltaCol] != self.opponent(player):
                raise GameError
                # return next_board
            next_board[r1][c1] = "." # after the player jumps, the original location is empty
            next_board[r1+deltaRow][c1+deltaCol] = "." # the middle piece is removed
            r1 += 2*deltaRow
            c1 += 2*deltaCol
            next_board[r1][c1] = player # update the new location of the current player

        return next_board

    def check(self, board, row, col, rowDelta, colDelta, factor, opponent):
        """Checks whether a jump is possible starting at (row, col) and going in the
        direction determined by the row delta and the column delta.

        Args:
            board (2D Array): representation of the game's board
            row (int): row index 
            col (int): column index
            rowDelta (int): row delta
            colDelta (int): column delta
            factor (int): factor is used to recursively check for multiple jumps in the same direction
            opponent (str): opponent of the current player ('X' or 'O')

        Returns:
            Returns all possible jumps in the given direction. If there is no jump, return empty list
        """
        if self.contains(board, row + factor * rowDelta, col + factor * colDelta, opponent) and \
           self.contains(board, row + (factor + 1) * rowDelta, col + (factor + 1) * colDelta, '.'):
            return [[row, col, row + (factor + 1) * rowDelta, col + (factor + 1) * colDelta]] + \
                self.check(board, row, col, rowDelta, colDelta, factor + 2, opponent)
        else:
            return []


    def possibleNextMoves(self, board, player):
        """Generates all legal next moves for the given player using the
        current board configuration.

        Args:
            board (2D Array): representation of the game's board
            player (str): player of the game ('X' or 'O')

        Returns:
            All legal successor moves for the given player. 
        """
        if self.isFirstMove(board):
            # if we need to generate the first move
            if player == 'X':
                # remove pieces at <4, 4>
                # since the index of the array starts at 0, we need to return [[3,3,3,3]]
                # return [[3,3,3,3]]
                return [[self.size/2-1]*4]
            else:
                # remove pieces at <4, 5>
                # since the index of the array starts at 0, we need to return [[3,4,3,4]]
                # return [[3,4,3,4]]
                return [[self.size/2-1, self.size/2]*2]
        else:
            moves = []
            rowDelta = [-1, 0, 1, 0]
            colDelta = [0, 1, 0, -1]
            # iterate each row
            for row in range(self.size):
                # iterate each column
                for col in range(self.size):
                    if board[row][col] == player:
                        for i in range(len(rowDelta)):
                            # append all possible jumps to the list moves
                            moves += self.check(board, row, col, rowDelta[i], colDelta[i], 1,
                                                self.opponent(player))
            return moves

    def playOneGame(self, player1, player2, show):
        """Play a game between two given players.  Returns 'X' if black wins, or 'O' if
        white wins. 

        Args:
            player1 (str): player 'X'
            player2 (str): player 'O'
            show (boolean): if show is true, it will display each move in the game.
        """
        self.resetGame()
        player1.initialize('X')
        player2.initialize('O')
        print(player1.name, "vs", player2.name)

        while True:
            if show:
                print(self)
                print("player X's turn")
            move = player1.getMove(self.board) # get legal next moves for X
            if move == []:
                # if there are no more possible moves for X, the game is over and X loses the game
                print("Game over")
                return 'O'
            try:
                self.makeMove('X', move)
            except GameError:
                print("Game over: Invalid move by", player1.name)
                print(move)
                print(self)
                return 'O'
            if show:
                # since the index of the array starts with 0 and our board configuration displays
                # indices from 1, we need to increment each row and column indices in "move" by 1
                move = [x + 1 for x in move] 
                print(move)
                print
                print(self)
                print("player O's turn")
            move = player2.getMove(self.board)
            if move == []:
                # if there are no more possible moves for O, the game is over and O loses the game
                print("Game over")
                return 'X'
            try:
                self.makeMove('O', move)
            except GameError:
                print("Game over: Invalid move by", player2.name)
                move = [x + 1 for x in move]
                print(move)
                print(self)
                return 'X'
            if show:
                # since the index of the array starts with 0 and our board configuration displays
                # indices from 1, we need to increment each row and column indices in "move" by 1
                move = [x + 1 for x in move]
                print(move)
                print

    def playNGames(self, n, player1, player2, show):
        """Play n games between two given players.  Returns 'X' if black wins, or 'O' if
        white wins after each game. 

        Args:
            n (str): number of games needed to play
            player1 (str): player 'X'
            player2 (str): player 'O'
            show (boolean): if show is true, it will display each move in the game.
        """
        first = player1
        second = player2
        # go over each game
        for i in range(n):
            print("Game", i + 1)
            winner = self.playOneGame(first, second, show) # find the winner of the current game
            if winner == 'X':
                first.won()
                second.lost()
                print(first.name, "wins")
            else:
                first.lost()
                second.won()
                print(second.name, "wins")
            first, second = second, first
    
    def isTerminal(self, moves):
        """Check whether we already reached the terminal node of the game

        Args:
            moves (list): list of posssible next moves

        Returns:
            True if there are no more possible next moves. Otherwise, return false.
        """
        if len(moves) == 0:
            return True
        return False

class Player:
    """
    A base class for Konane players.  All players must implement
    the initialize and getMove methods.
    """
    name = "Player"
    wins = 0
    losses = 0

    def results(self):
        result = self.name
        result += " Wins:" + str(self.wins)
        result += " Losses:" + str(self.losses)
        return result

    def lost(self):
        self.losses += 1

    def won(self):
        self.wins += 1

    def resetGame(self):
        self.wins = 0
        self.losses = 0

    def initialize(self, player):
        """
        Records the player's player, either 'X' for black or
        'O' for white.  Should also set the name of the player.
        """
        abstract()

    def getMove(self, board):
        """
        Given the current board, should return a valid move.
        """
        abstract()

class RandomPlayer(KonaneBoard, Player):
    """
    Chooses a random move from the set of possible next moves.
    """
    def initialize(self, player):
        self.player = player
        self.name = "Random Player"

    def getMove(self, board):
        moves = self.possibleNextMoves(board, self.player)
        n = len(moves)
        if n == 0:
            return []
        else:
            return random.choice(moves)

class HumanPlayer(KonaneBoard, Player):
    """
    Prompts a human player for a move.
    """
    def initialize(self, player):
        self.player = player
        self.name = "Human Player"

    def getMove(self, board):
        moves = self.possibleNextMoves(board, self.player)

        while True:
            # since the index of the array starts with 0 and our board configuration displays
            # indices from 1, we need to increment each row and column indices in each possible move by 1
            moves_increased_by_1 = []
            for m in moves:
                m = [x + 1 for x in m]
                moves_increased_by_1.append(m)

            print("Possible moves:", moves_increased_by_1)
            n = len(moves)
            if n == 0:
                print("No more possible next moves! You lose!")
                return []

            index = int(input("Enter index of chosen move (0-" + str(n-1) +
                              ") or -1 to lose the game: "))
            if index == -1:
                # if the human decided to lose the game, return empty list for next possible moves
                return []

            if 0 <= index < n:
                print("Chosen move is: ", moves_increased_by_1[index])
                return moves[index]
            else:
                print("Invalid move, try again.")

class MinimaxPlayer(KonaneBoard, Player):
    """
    Chooses a move from the set of possible next moves based on the minimax decision rule
    """
    def __init__(self, size, depth_limit):
        KonaneBoard.__init__(self, size)
        self.depth_limit = depth_limit 
    
    def initialize(self, player):
        self.player = player
        self.name = "Player with limit " + str(self.depth_limit)

    def getMove(self, board):
        moves = self.possibleNextMoves(board, self.player)
        best_val = -float("inf")
        best_index = 0 # best_index stores the index of the best move
        index = 0

        if len(moves) == 0:
            return []

        # go over each move
        for move in moves:
            backedup_val = (self.minimax(self.nextBoard(board, self.player, move), 0, self.opponent(self.player)))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index # update the besti_index
            index += 1 # move on to the next move

        return moves[best_index]

    def eval(self, n):
        """Evaluation function returns an estimate of the expected utility of state n to currrent player 

        Args:
            n (2D array): representation of the current board state of the game
        """
        # Get a list of possible moves given board state
        moves = self.possibleNextMoves(n, self.player)
        # Get a list of possible moves of the opponent 
        opponent_moves = self.possibleNextMoves(n, self.opponent(self.player))
        if len(opponent_moves) == 0:
            # if the current player wins
            return float("inf")
        if len(moves) == 0:
            # if the opponent wins
            return -float("inf")

        return len(moves) - len(opponent_moves)

    def minimax(self, n, depth, player):
        """Returns the next move based on the minimax decision rule

        Args:
            n (2D array): representation of the current board state
            depth (n): input depth to search
            player (str): player of the game ('X' or 'O')
        """
        # Get a list of possible moves given board state
        moves = self.possibleNextMoves(n, player)

        # Check whether we have reached the depth limit. If we have, return eval of board
        # and list of possible next moves (which is None)
        if depth == self.depth_limit or self.isTerminal(n):
            return (self.eval(n), None)

        isMax = (depth % 2 == 0)

        if isMax:
            # if n is a MAX node
            best_move = 0
            current_backedup_val = -float("inf")
            # iterate each move
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(n, player, move), depth + 1, self.opponent(self.player)))[0]
                if backedup_val > current_backedup_val:
                    current_backedup_val = backedup_val
                    best_move = move
            return current_backedup_val, best_move
        else:
            # if n is a MIN node
            current_backedup_val = float("inf")
            best_move = 0
            # iterate each move
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(n, player, move), depth + 1, self.player))[0]
                if backedup_val < current_backedup_val:
                    current_backedup_val = backedup_val
                    best_move = move
            return current_backedup_val, best_move

class MinimaxPlayerAlphaBeta(KonaneBoard, Player):
    """
    Chooses a move from the set of possible next moves based on the minimax decision rule (with alpha-beta Pruning)
    """
    def __init__(self, size, depth_limit):
        KonaneBoard.__init__(self, size)
        self.depth_limit = depth_limit
    
    def initialize(self, player):
        self.player = player
        self.name = "Player with limit " + str(self.depth_limit)

    def getMove(self, board):
        moves = self.possibleNextMoves(board, self.player)
        best_val = -float("inf") 
        best_index = 0 # best_index stores the index of the best move
        index = 0

        if len(moves) == 0:
            return []

        # go over each move
        for move in moves:
            backedup_val = (self.minimaxAlphaBeta(self.nextBoard(board, self.player, move), 0, self.opponent(self.player), -float("inf"), float("inf")))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index # update the best_index
            index += 1 # move on to the next move

        return moves[best_index]

    def eval(self, n):
        """Evaluation function returns an estimate of the expected utility of state n to currrent player 

        Args:
            n (2D array): representation of the current board state of the game
        """
        moves = self.possibleNextMoves(n, self.player)
        opponent_moves = self.possibleNextMoves(n, self.opponent(self.player))
        if len(opponent_moves) == 0:
            # if the current player wins
            return float("inf")
        if len(moves) == 0:
            # if the opponent wins
            return -float("inf")

        return len(moves) - len(opponent_moves)

    def minimaxAlphaBeta(self, n, depth, player, alpha, beta):
        """
        Returns the next move based on the minimax alpha beta Pruning decision rule

        Args:
            n (2D array): representation of the current board state
            depth (n): input depth to search
            player (str): player of the game ('X' or 'O')
            alpha (int): the minimum score that the maximizing player is assured of 
            beta (int): the maximum score that the maximizing player is assured of 
        """
        # Get a list of possible moves given board state
        moves = self.possibleNextMoves(n, player)

        # Check whether we have reached the depth limit. If we have, return eval of board
        # and list of possible next moves (which is None)
        if depth == self.depth_limit or self.isTerminal(moves):
            return (self.eval(n), None)

        isMax = (depth % 2 == 0)

        if isMax:
            # if n is a MAX node
            best_move = 0
            # iterate each move
            for move in moves:
                backedup_val = (self.minimaxAlphaBeta(self.nextBoard(n, player, move), depth + 1, self.opponent(self.player), alpha, beta))[0]
                if backedup_val > alpha:
                    alpha = backedup_val
                    best_move = move
                if alpha >= beta:
                    return beta, best_move
            return alpha, best_move
        else:
            # if n is a MIN node
            best_move = 0
            # iterate each move
            for move in moves:
                backedup_val = (self.minimaxAlphaBeta(self.nextBoard(n, player, move), depth + 1, self.player, alpha, beta))[0]
                if backedup_val > beta:
                    beta = backedup_val
                    best_move = move
                if alpha >= beta:
                    return alpha, best_move
            return beta, best_move

game = KonaneBoard(8)
# test cases
# game.playNGames(1, MinimaxPlayerAlphaBeta(8, 6), MinimaxPlayerAlphaBeta(8, 5), False)
# game.playNGames(4, MinimaxPlayerAlphaBeta(8, 6), MinimaxPlayerAlphaBeta(8, 5), False)
print("------------------------------------------------------------")
# game.playNGames(9, MinimaxPlayer(8, 4), MinimaxPlayer(8, 2), False)
# game.playOneGame(HumanPlayer(8), HumanPlayer(8), True)

# game.playNGames(4, MinimaxPlayer(8, 6), MinimaxPlayer(8, 5), 1)
print("------------------------------------------------------------")
game.playNGames(3, MinimaxPlayer(8, 5), MinimaxPlayerAlphaBeta(8, 2), 0)