import random
import copy

"""
The file implements Konane (Hawaiian Checkers)
@author: Linh Tran
@date: Oct 31, 2021
Reference source: https://www.cs.swarthmore.edu/~meeden/cs63/f05/konane.py
"""


class GameError(AttributeError):
    """
    This class is used to raise an error during Konane game.
    """


class Konane:
    """
    This class implements Konane and its rule, using a 2D list as the game state (board) representation.
    On the board:
       'X': black
       'O': white
       '.': empty
    X always goes first.  In the board 8x8, the first move (by X) is to remove (4, 4), and the second move
    (by O) is to remove (4, 5). Following the rule of Konane, the game stops when either X or O has no next
    possible move. The winner/loser is then printed.
    """

    def __init__(self, n):
        self.size = n
        self.reset()

    def reset(self):
        """
        Resets the starting board state.
        """
        self.board = []
        value = 'X'
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(value)
                value = self.opponent(value)
            self.board.append(row)
            if self.size % 2 == 0:
                value = self.opponent(value)

    def __str__(self):
        """
        Converts the board state into string to print out.
        """
        result = "  "
        for i in range(self.size):
            result += str(i+1) + " "
        result += "\n"
        for i in range(self.size):
            result += str(i+1) + " "
            for j in range(self.size):
                result += str(self.board[i][j]) + " "
            result += "\n"
        return result

    def valid(self, row, col):
        """
        Returns true if the given row and col is a valid location, false otherwise
        """
        return row >= 0 and col >= 0 and row < self.size and col < self.size

    def contains(self, board, row, col, symbol):
        """
        Returns true if the given row and col represent a valid location that 
        contains the passed-in symbol.
        """
        return self.valid(row, col) and board[row][col] == symbol

    def countSymbol(self, board, symbol):
        """
        Returns the number of instances of the passed-in symbol on the board.
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == symbol:
                    count += 1
        return count

    def opponent(self, player):
        """
        Returns the opponent of the passed-in player.
        """
        if player == 'X':
            return 'O'
        else:
            return 'X'

    def distance(self, r1, c1, r2, c2):
        """
        Returns the distance between two points in a vertical or
        horizontal line on the konane board. 
        """
        return abs(r1-r2 + c1-c2)

    def makeMove(self, player, move):
        """
        Updates the current board with the next board created by the given
        move.
        """
        self.board = self.nextBoard(self.board, player, move)

    def nextBoard(self, board, player, move):
        """
        Given a move for a particular player from (r1,c1) to (r2,c2) this
        executes the move on a copy of the current konane board.  It will
        raise a GameError if the move is invalid. It returns the copy of
        the board, and does not change the given board.
        """
        r1, c1, r2, c2 = int(move[0]), int(move[1]), int(move[2]), int(move[3])
        next = copy.deepcopy(board)

        # check validity
        if not (self.valid(r1, c1) and self.valid(r2, c2)):
            raise GameError
        if next[r1][c1] != player:
            raise GameError

        dist = self.distance(r1, c1, r2, c2)
        if dist == 0:
            if self.openingMove(board):
                next[r1][c1] = "."
                return next
            raise GameError

        if next[r2][c2] != ".":
            raise GameError

        jumps = (int)(dist/2)
        dr = (int)((r2 - r1)/dist)
        dc = (int)((c2 - c1)/dist)

        for i in range(jumps):
            if next[r1+dr][c1+dc] != self.opponent(player):
                raise GameError
            next[r1][c1] = "."
            next[r1+dr][c1+dc] = "."
            r1 += 2*dr
            c1 += 2*dc
            next[r1][c1] = player
        return next

    def openingMove(self, board):
        return self.countSymbol(board, ".") <= 1

    def makeFirstMove(self, board):
        """
        First move is always to remove (4,4)
        """
        moves = []
        moves.append([self.size/2-1]*4)
        return moves

    def makeSecondMove(self, board):
        """
        Second move is always to remove (4,5)
        """
        moves = []
        moves.append([self.size/2-1, self.size/2]*2)
        return moves

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

    def generateMoves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if self.openingMove(board):
            if player == 'X':
                return self.makeFirstMove(board)
            else:
                return self.makeSecondMove(board)
        else:
            moves = []
            rd = [-1, 0, 1, 0]
            cd = [0, 1, 0, -1]
            for r in range(self.size):
                for c in range(self.size):
                    if board[r][c] == player:
                        for i in range(len(rd)):
                            moves += self.check(board, r, c, rd[i], cd[i], 1,
                                                self.opponent(player))
            return moves

    def playOneGame(self, p1, p2, showGameState):
        """
        Play out a game between p1 and p2.  Returns 'X' if p1 wins, or 'O' if
        p2 wins. When showGameState is true, it will display each state
        in the game.
        """
        self.reset()
        p1.initialize('X')
        p2.initialize('O')
        print(p1.name, "vs", p2.name)

        while True:
            if showGameState:
                print(self)
                print("player X's turn")
            move = p1.getMove(self.board)
            if move == []:
                print("Game over", p2.name, "wins")
                return 'O'
            try:
                self.makeMove('X', move)
            except GameError:
                print("Game over: Invalid move by", p1.name)
                print(move)
                print(self)
                return 'O'
            if showGameState:
                print(move)
                print
                print(self)
                print("player O's turn")
            move = p2.getMove(self.board)
            if move == []:
                print("Game over", p1.name, "wins")
                return 'X'
            try:
                self.makeMove('O', move)
            except GameError:
                print("Game over: Invalid move by", p2.name)
                print(move)
                print(self)
                return 'X'
            if showGameState:
                print(move)
                print

    def playNGames(self, n, p1, p2, showGameState):
        """
        Will play out n games between player p1 and player p2.
        The players alternate going first.  Prints the total
        number of games won by each player.
        """
        first = p1
        second = p2
        for i in range(n):
            print("Game", (i+1))
            winner = self.playOneGame(first, second, showGameState)
            if winner == 'X':
                first.won()
                second.lost()
                print(first.name, "wins")
            else:
                first.lost()
                second.won()
                print(second.name, "wins")
            first, second = second, first


class Player:
    """
    A base class for Konane players.  All players must implement
    the the initialize and getMove methods.
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

    def reset(self):
        self.wins = 0
        self.losses = 0


class RandomPlayer(Konane, Player):
    """
    Chooses a random move from the set of possible moves.
    """

    def initialize(self, current_player):
        self.current_player = current_player
        self.name = "Random"

    def getMove(self, board):
        moves = self.generateMoves(board, self.current_player)
        n = len(moves)
        if n == 0:
            return []
        else:
            move = moves[random.randrange(0, n)]
            # used to print movement in base 1
            moves_based1 = [x + 1 for x in move]
            print("chosen move: ", moves_based1)
            return move
            # return moves[random.randrange(0, n)]


class HumanPlayer(Konane, Player):
    """
    This class implements a human player.
    """

    def initialize(self, current_player):
        self.current_player = current_player
        self.name = "Human"

    def getMove(self, board):
        moves = self.generateMoves(board, self.current_player)

        while True:
            movesShownInBased1 = []
            for m in moves:
                moveShownInBased1 = []
                for val in m:
                    val = (int)(val+1)
                    moveShownInBased1.append(val)
                movesShownInBased1.append(moveShownInBased1)
            print("Possible moves:", movesShownInBased1)

            n = len(moves)
            if n == 0:
                print("You must concede")
                return []
            index = int(input("Enter index of chosen move (0-" + str(n-1) +
                              ") or -1 to concede: "))
            if index == -1:
                return []

            # print("index ", type(index))
            if 0 <= index <= (n-1):
                print("Move chosen is: ", movesShownInBased1[index])
                return moves[index]
            else:
                print("Invalid choice, try again.")


class MinimaxPlayer(Konane, Player):
    """
    This class implements a minimax player.
    """
    def __init__(self, size, depth_limit):
        Konane.__init__(self, size)
        self.limit = depth_limit

    def initialize(self, current_player):
        self.current_player = current_player
        self.name = "Minimax_limit_" + str(self.limit)

    def getMove(self, board):
        # Possible moves
        moves = self.generateMoves(board, self.current_player)
        best_val = -float("inf")
        best_index = 0
        index = 0

        if len(moves) == 0:
            return []

        for move in moves:
            backedup_val = (self.minimax(self.nextBoard(
                board, self.current_player, move), 0, self.opponent(self.current_player)))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index
            index += 1

        return moves[best_index]

    def evaluation(self, board):
        moves = self.generateMoves(board, self.current_player)
        opponent_moves = self.generateMoves(
            board, self.opponent(self.current_player))
        if len(opponent_moves) == 0:
            return float("inf")
        if len(moves) == 0:
            return -float("inf")
        return len(moves) - len(opponent_moves)

    def minimax(self, board, depth, current_player):

        # Get a list of possible moves given board state
        moves = self.generateMoves(board, current_player)

        # Check to see if we've reached the depth limit
        #   if we have, return eval of board
        if depth == self.limit or len(moves) == 0:
            return (self.evaluation(board), None)

        # Check to see if we're out of possible moves
        #   if so return inf to indicate a loss
        isMax = (depth % 2 == 0)

        if isMax:
            best_move = 0
            curr_backedup_val = -float("inf")
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(
                    board, current_player, move), depth + 1, self.opponent(self.current_player)))[0]
                if backedup_val > curr_backedup_val:
                    curr_backedup_val = backedup_val
                    best_move = move
            return curr_backedup_val, best_move
        else:
            best_move = 0
            curr_backedup_val = float("inf")
            for move in moves:
                backedup_val = (self.minimax(self.nextBoard(
                    board, current_player, move), depth + 1, self.current_player))[0]
                if backedup_val < curr_backedup_val:
                    curr_backedup_val = backedup_val
                    best_move = move
            return curr_backedup_val, best_move


class MinimaxAlphaBetaPlayer(Konane, Player):
    """
    This class implements a minimax player with alpha beta pruning.
    """

    def __init__(self, size, depth_limit):
        Konane.__init__(self, size)
        self.depth_limit = depth_limit

    def initialize(self, current_player):
        self.current_player = current_player
        self.name = "MinimaxAB_limit_" + str(self.depth_limit)

    def getMove(self, board):
        moves = self.generateMoves(board, self.current_player)
        best_val = -float("inf")
        best_index = 0
        index = 0

        if len(moves) == 0:
            return []

        for move in moves:
            backedup_val = (self.minimaxAlphaBeta(self.nextBoard(board, self.current_player, move),
                            0, self.opponent(self.current_player), -float("inf"), float("inf")))[0]
            if backedup_val == None:
                return []
            if backedup_val > best_val:
                best_val = backedup_val
                best_index = index
            index += 1

        return moves[best_index]

    def evaluation(self, board):
        moves = self.generateMoves(board, self.current_player)
        opponent_moves = self.generateMoves(
            board, self.opponent(self.current_player))

        if len(opponent_moves) == 0:
            # opponent loses
            return float("inf")
        if len(moves) == 0:
            # opponent wins
            return -float("inf")
        return len(moves) - len(opponent_moves)

    def minimaxAlphaBeta(self, board, depth, current_player, alpha, beta):
        # Get a list of possible moves given board state
        moves = self.generateMoves(board, current_player)

        # Check to see if we've reached the depth limit
        # if we have, return eval of board
        if depth == self.depth_limit or len(moves) == 0:
            return (self.evaluation(board), None)

        isMax = (depth % 2 == 0)

        if isMax:
            best_move = 0
            for move in moves:
                backedup_val = (self.minimaxAlphaBeta(self.nextBoard(
                    board, current_player, move), depth + 1, self.opponent(self.current_player), alpha, beta))[0]
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
                    board, current_player, move), depth + 1, self.current_player, alpha, beta))[0]
                if backedup_val > beta:
                    beta = backedup_val
                    best_move = move
                if alpha >= beta:
                    return alpha, best_move
            return beta, best_move


game = Konane(8)
# game.playNGames(9, RandomPlayer(8), RandomPlayer(8), False)
# game.playOneGame(RandomPlayer(8), RandomPlayer(8), True)
# game.playOneGame(MinimaxPlayer(8, 2), RandomPlayer(8), True)
# game.playNGames(5, MinimaxPlayer(8, 2), MinimaxPlayer(8, 4), False)
# game.playNGames(5, MinimaxPlayer(8, 2), RandomPlayer(8), False)
# game.playOneGame(HumanPlayer(8), RandomPlayer(8), True)
# game.playOneGame(HumanPlayer(8), HumanPlayer(8), True)
# game.playNGames(2, MinimaxAlphaBetaPlayer(8, 2), HumanPlayer(8), True)
# game.playNGames(9, MinimaxAlphaBetaPlayer(8, 4), MinimaxAlphaBetaPlayer(8, 2), False)
# game.playNGames(9, MinimaxPlayer(8, 4), MinimaxAlphaBetaPlayer(8, 2), False)
# game.playNGames(9, MinimaxAlphaBetaPlayer(8, 4), MinimaxAlphaBetaPlayer(8, 2), False)

print("------------------------------------------------------------")
# game.playOneGame(MinimaxAlphaBetaPlayer(8, 2), MinimaxAlphaBetaPlayer(8, 1), True)
game.playNGames(9, MinimaxPlayer(8, 4), MinimaxAlphaBetaPlayer(8, 1), False)
