"""This class implements the board representation"""


class Board:
    def __init__(self, size):
        self.size = size
        # set the size and the opponent - human player
        self.board = []
        self.reset()

        print("Starting Board: \n")
        print(self.printBoard())

    def reset(self):
        """
        Resets the starting board state.
        """
        self.board = [['X' if (r+c) % 2 == 0 else 'O' for c in range(self.size)]
                      for r in range(self.size)]

    def printBoard(self):
        """
        Returns a string representation of the konane board.
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


game = Board(8)
