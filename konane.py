# The file implements Konane (Hawaiian Checkers)
# @author: Linh Tran
# @date: Oct 31, 2021

import random
import copy


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
        r1 = (int)(move[0])
        c1 = (int)(move[1])
        r2 = (int)(move[2])
        c2 = (int)(move[3])
        next = copy.deepcopy(board)
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

    def generateFirstMoves(self, board):
        """
        First move is always to remove (4,4)
        """
        moves = []
        moves.append([self.size/2-1]*4)
        return moves

    def generateSecondMoves(self, board):
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
                return self.generateFirstMoves(board)
            else:
                return self.generateSecondMoves(board)
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
        Given two instances of players, will play out a game
        between them.  Returns 'X' if black wins, or 'O' if
        white wins. When showGameState is true, it will display each move
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

    def initialize(self, side):
        """
        Records the player's side, either 'X' for black or
        'O' for white.  Should also set the name of the player.
        """
        abstract()

    def getMove(self, board):
        """
        Given the current board, should return a valid move.
        """
        abstract()


class SimplePlayer(Konane, Player):
    """
    Always chooses the first move from the set of possible moves.
    """

    def initialize(self, side):
        self.side = side
        self.name = "Simple"

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        n = len(moves)
        if n == 0:
            return []
        else:
            return moves[0]


class RandomPlayer(Konane, Player):
    """
    Chooses a random move from the set of possible moves.
    """

    def initialize(self, side):
        self.side = side
        self.name = "Random"

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        n = len(moves)
        if n == 0:
            return []
        else:
            return moves[random.randrange(0, n)]


class HumanPlayer(Konane, Player):
    """
    Prompts a human player for a move.
    """

    def initialize(self, side):
        self.side = side
        self.name = "Human"

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
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


class MinimaxAlphaBetaPlayer(Konane, Player):
    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        self.limit = depthLimit

    def initialize(self, side):
        self.side = side
        self.name = "Cute Player " + str(self.limit)

    def getMove(self, board):
        # Possible moves
        moves = self.generateMoves(board, self.side)

        bestVal = -float("inf")
        bestIndex = 0
        index = 0

        if len(moves) == 0:
            return []

        for move in moves:
            val, action = self.minimaxAlphaBeta(self.nextBoard(board, self.side, move), 0, False, self.opponent(
                self.side), -float("inf"), float("inf"))
            if val == None:
                return []
            if val > bestVal:
                bestVal = val
                bestIndex = index
            # if index != len(moves) - 1:
            index += 1

        return moves[bestIndex]

    def minimaxAlphaBeta(self, board, depth, isMax, side, alpha, beta):

        # list of all possible moves
        moves = self.generateMoves(board, side)

        # if reached the depth limit, return evaluation function of board
        # and the move is null
        if self.limit == depth:
            return [self.evaluation(board), None]

        # if we're out of possible moves, we lose
        if len(moves) == 0:
            return [float("inf"), None]

        if isMax:
            # MAX's turn
            best_move = 0
            for move in moves:  # for each successor
                backup_val, current_move = self.minimaxAlphaBeta(self.nextBoard(
                    board, side, move), depth+1, False, self.opponent(self.side), alpha, beta)

                if backup_val > alpha:
                    alpha = backup_val
                    best_move = current_move
                if alpha >= beta:  # cut-off
                    return [beta, best_move]
                return [alpha, best_move]
        else:
            # MIN's turn
            best_move = 0
            for move in moves:  # for each successor
                backup_val, current_move = self.minimaxAlphaBeta(self.nextBoard(
                    board, side, move), depth+1, True, self.side, alpha, beta)

                if backup_val < beta:
                    beta = backup_val
                    best_move = current_move
                if beta <= alpha:  # cut-off
                    return [alpha, best_move]
                return [beta, best_move]

    def evaluation(self, board):
        moves = self.generateMoves(board, self.side)
        oppMoves = self.generateMoves(board, self.opponent(self.side))

        if len(oppMoves) == 0:
            # MAX wins
            return float("inf")
        if len(moves) == 0:
            # MAX loses
            return -float("inf")
        return len(moves) - len(oppMoves)


game = Konane(8)
# game.playOneGame(HumanPlayer(8), SimplePlayer(8), True)
game.playOneGame(RandomPlayer(8), SimplePlayer(8), True)
# game.playOneGame(HumanPlayer(8), HumanPlayer(8), True)
# game.playNGames(2, MinimaxAlphaBetaPlayer(8, 2), HumanPlayer(8), True)
# game.playNGames(9, MinimaxAlphaBetaPlayer(8, 4), MinimaxAlphaBetaPlayer(8, 2), False)
# game.playOneGame(MinimaxAlphaBetaPlayer(8, 2), MinimaxAlphaBetaPlayer(8, 1), True)
