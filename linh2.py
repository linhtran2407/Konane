import random
import copy


class KonaneBoard:
    def __init__(self, size):
        self.size = size
        self.resetGame()  # create a starting board state

    def resetGame(self):
        """
        Resets the starting board state.
        """
        self.board = []
        players = ['X', 'O']
        for i in range(self.size):
            row = [players[j % 2] for j in range(self.size)]
            self.board.append(row)
            players.reverse()

    def __str__(self):
        board_str = "  "
        # print the column indices
        for i in range(self.size):
            board_str += str(i + 1) + " "
        board_str += "\n"
        # print the values row by row
        for i in range(self.size):
            board_str += str(i + 1) + " "  # row indices
            # go over each column
            for j in range(self.size):
                board_str += self.board[i][j] + " "
            board_str += "\n"  # move on to the next row
        return board_str

    def isValidMove(self, move):
        """
        Returns true if the given row and col represent a valid location on
        the KonaneBoard board.
        """
        row = move[0]
        col = move[1]
        return 0 <= row < self.size and 0 <= col < self.size

    def contains(self, board, row, col, symbol):
        """
        Returns true if the given row and col represent a valid location on
        the KonaneBoard board and that location contains the given symbol.
        """
        return self.isValidMove((row, col)) and board[row][col] == symbol

    def opponent(self, player):
        if player == "X":
            return "O"
        elif player == "O":
            return "X"
        else:
            return "Invalid player input"

    def isFirstMove(self, board):
        emptyPieces = 0
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == ".":
                    emptyPieces += 1

        return emptyPieces <= 1

    def makeMove(self, player, move):
        """
        Updates the current board with the next board created by the given
        move.
        """
        self.board = self.nextBoard(self.board, player, move)

    def nextBoard(self, board, player, move):
        """
        Given a move for a particular player from (r1,c1) to (r2,c2) this
        executes the move on a copy of the current KonaneBoard board.  It will
        raise a KonaneBoardError if the move is invalid. It returns the copy of
        the board, and does not change the given board.
        """
        r1, c1, r2, c2 = int(move[0]), int(move[1]), int(move[2]), int(move[3])
        next_board = copy.deepcopy(board)

        if self.isValidMove((r1, c1)) == False or self.isValidMove((r2, c2)) == False:
            # raise KonaneError
            return next_board

        if next_board[r1][c1] != player:
            # raise KonaneError
            return next_board

        # distance between two points vertically/horizontally
        distance = abs(r1-r2 + c1-c2)

        if distance == 0:
            if self.isFirstMove(board):
                next_board[r1][c1] = "."

            return next_board
            # raise KonaneError

        if next_board[r2][c2] != ".":
            # raise KonaneError
            return next_board

        jumps = (int)(distance/2)
        deltaRow = (int)((r2 - r1)/distance)
        deltaCol = (int)((c2 - c1)/distance)
        for i in range(jumps):
            if next_board[r1+deltaRow][c1+deltaCol] != self.opponent(player):
                # raise KonaneError
                return next_board
            next_board[r1][c1] = "."
            next_board[r1+deltaRow][c1+deltaCol] = "."
            r1 += 2*deltaRow
            c1 += 2*deltaCol
            next_board[r1][c1] = player
        return next_board

    def check(self, board, r, c, rd, cd, factor, opponent):
        """
        Checks whether a jump is possible starting at (r,c) and going in the
        direction determined by the row delta, rd, and the column delta, cd.
        The factor is used to recursively check for multiple jumps in the same
        direction.  Returns all possible jumps in the given direction.
        """
        if self.contains(board, r+factor*rd, c+factor*cd, opponent) and \
           self.contains(board, r+(factor+1)*rd, c+(factor+1)*cd, '.'):
            return [[r, c, r+(factor+1)*rd, c+(factor+1)*cd]] + \
                self.check(board, r, c, rd, cd, factor+2, opponent)
        else:
            return []

        # self.isValidMove((row, col)) and board[row][col] == symbol
        # contains(self, board, row, col, symbol):

    def possibleNextMoves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if self.isFirstMove(board):
            if player == 'X':
                return [[3, 3, 3, 3]]
            else:
                return [[3, 4, 3, 4]]
        else:
            moves = []
            rd = [-1, 0, 1, 0]
            cd = [0, 1, 0, -1]
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == player:
                        for i in range(len(rd)):
                            moves += self.check(board, row, col, rd[i], cd[i], 1,
                                                self.opponent(player))
            return moves

    def playOneGame(self, player1, player2, show):
        """
        Given two instances of players, will play out a game
        between them.  Returns 'X' if black wins, or 'O' if
        white wins. When show is true, it will display each move
        in the game.
        """
        self.resetGame()
        player1.initialize('X')
        player2.initialize('O')
        print(player1.name, "vs", player2.name)
        while True:
            if show:
                print(self)
                # self.printBoard()
                print("player B's turn")
            move = player1.getMove(self.board)
            if move == []:
                print("Game over", player1.name, "loses")
                return 'O'
            try:
                self.makeMove('X', move)
            except AttributeError:
                print("Game over: Invalid move by", player1.name)
                print(move)
                print(self)
                # self.printBoard()
                return 'O'
            if show:
                # print(move)
                # for m in move:
                #     m = [x+1 for x in m]
                move = [x + 1 for x in move]
                print(move)
                print
                print(self)
                # self.printBoard()
                print("player W's turn")
            move = player2.getMove(self.board)
            if move == []:
                print("Game over", player2.name, "loses")
                return 'X'
            try:
                self.makeMove('O', move)
            except AttributeError:
                print("Game over: Invalid move by", player2.name)
                # for m in move:
                #     m = [x+1 for x in move[m]]
                move = [x + 1 for x in move]
                print(move)
                print(self)
                # self.printBoard()
                return 'X'
            if show:
                move = [x + 1 for x in move]
                print(move)
                print

    def playNGames(self, n, player1, player2, show):
        """
        Will play out n games between player player1 and player player2.
        The players alternate going first.  Prints the total
        number of games won by each player.
        """
        first = player1
        second = player2
        for i in range(n):
            print("Game", i)
            winner = self.playOneGame(first, second, show)
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
    Chooses a random move from the set of possible moves.
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
                return []

            if 0 <= index < n:
                print("Chosen move is: ", moves_increased_by_1[index])
                return moves[index]
            else:
                print("Invalid move, try again.")


class MinimaxPlayer(KonaneBoard, Player):
    def __init__(self, size, depth_limit):
        KonaneBoard.__init__(self, size)
        self.depth_limit = depth_limit

    def initialize(self, player):
        self.player = player
        self.name = "Player with limit " + str(self.depth_limit)

    def getMove(self, board):
        # Possible moves
        moves = self.possibleNextMoves(board, self.player)
        best_val = -float("inf")
        best_index = 0
        index = 0

        if len(moves) == 0:
            return []

        for move in moves:
            backedup_val = (self.minimax(self.nextBoard(
                board, self.player, move), 0, self.opponent(self.player)))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index
            # if index != len(moves) - 1:
            index += 1

        return moves[best_index]

    def eval(self, n):
        moves = self.possibleNextMoves(n, self.player)
        opponent_moves = self.possibleNextMoves(n, self.opponent(self.player))
        if len(opponent_moves) == 0:
            return float("inf")
        if len(moves) == 0:
            return -float("inf")
        return len(moves) - len(opponent_moves)

    def minimax(self, n, depth, player):

        # Get a list of possible moves given board state
        moves = self.possibleNextMoves(n, player)

        # Check to see if we've reached the depth limit
        #   if we have, return eval of board
        if depth == self.depth_limit or self.isTerminal(n):
            return (self.eval(n), None)

        # Check to see if we're out of possible moves
        #   if so return inf to indicate a loss
        isMax = (depth % 2 == 0)

        if isMax:
            best_move = 0
            current_backedup_val = -float("inf")
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(
                    n, player, move), depth + 1, self.opponent(self.player)))[0]
                if backedup_val > current_backedup_val:
                    current_backedup_val = backedup_val
                    best_move = move
            return current_backedup_val, best_move
        else:
            current_backedup_val = float("inf")
            best_move = 0
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(
                    n, player, move), depth + 1, self.player))[0]
                if backedup_val < current_backedup_val:
                    current_backedup_val = backedup_val
                    best_move = move
            return current_backedup_val, best_move


class MinimaxPlayerAlphaBeta(KonaneBoard, Player):
    def __init__(self, size, depth_limit):
        KonaneBoard.__init__(self, size)
        self.depth_limit = depth_limit

    def initialize(self, player):
        self.player = player
        self.name = "Player with limit " + str(self.depth_limit)

    def getMove(self, board):
        # Possible moves
        moves = self.possibleNextMoves(board, self.player)
        best_val = -float("inf")
        best_index = 0
        index = 0

        if len(moves) == 0:
            return []

        for move in moves:
            backedup_val = (self.minimaxAlphaBeta(self.nextBoard(
                board, self.player, move), 0, self.opponent(self.player), -float("inf"), float("inf")))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index
            # if index != len(moves) - 1:
            index += 1

        return moves[best_index]

    def eval(self, n):
        moves = self.possibleNextMoves(n, self.player)
        opponent_moves = self.possibleNextMoves(n, self.opponent(self.player))
        if len(opponent_moves) == 0:
            # opponent is the loser
            return float("inf")
        if len(moves) == 0:
            # opponent is the winner
            return -float("inf")
        return len(moves) - len(opponent_moves)

    def minimaxAlphaBeta(self, n, depth, player, alpha, beta):
        # Get a list of possible moves given board state
        moves = self.possibleNextMoves(n, player)

        # Check to see if we've reached the depth limit
        # if we have, return eval of board
        if depth == self.depth_limit or self.isTerminal(moves):
            return (self.eval(n), None)

        isMax = (depth % 2 == 0)

        if isMax:
            best_move = 0
            for move in moves:
                backedup_val = (self.minimaxAlphaBeta(self.nextBoard(
                    n, player, move), depth + 1, self.opponent(self.player), alpha, beta))[0]
                if backedup_val > alpha:
                    alpha = backedup_val
                    best_move = move
                if alpha >= beta:
                    return beta, best_move
            return alpha, best_move
        else:
            best_move = 0
            for move in moves:
                backedup_val = (self.minimaxAlphaBeta(self.nextBoard(
                    n, player, move), depth + 1, self.player, alpha, beta))[0]
                if backedup_val > beta:
                    beta = backedup_val
                    best_move = move
                if alpha >= beta:
                    return alpha, best_move
            return beta, best_move


game = KonaneBoard(8)
print("------------------------------------------------------------")
# game.playNGames(3, MinimaxPlayer(8, 5), MinimaxPlayerAlphaBeta(8, 2), 0)
# game.playNGames(3, MinimaxPlayer(8, 5), MinimaxPlayer(8, 2), 0)
# game.playNGames(3, MinimaxPlayerAlphaBeta(8, 4), RandomPlayer(8), False)

game.playNGames(3, MinimaxPlayer(8, 4), RandomPlayer(8), False)
