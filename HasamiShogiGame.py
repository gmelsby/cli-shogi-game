# Author: Gregory Melsby
# Date: 11/23/2021
# Description: Contains classes HasamiShogiGame, Board, and Piece.
# HasamiShogiGame models a game of Hasami Shogi and has a private data member board.
# A Board has a list of lists which represents the board and has Pieces.
# The play method of HasamiShogiGame lets the user play the game with inputs in algebraic notation.


class HasamiShogiGame:
    """
    Models a game of Hasami Shogi. Has private data members board, game state, and active player.
    """

    def __init__(self):
        """Creates a game of Hasami Shogi. First player defaults to 'BLACK'"""
        self._board = Board()
        self._game_state = 'UNFINISHED'
        self._active_player = 'BLACK'

    def get_game_state(self):
        """Returns a string of the current game state"""
        return self._game_state

    def get_active_player(self):
        """Returns a string of the current active player"""
        return self._active_player

    def get_num_captured_pieces(self, color):
        """Returns the number of pieces of the color that have been captured"""
        return self._board.get_num_captured_pieces(color)

    def make_move(self, square_from, square_to):
        """
        Attempts to move the piece at square_from to square_to.
        If not possible returns False. If possible makes move, removes captured pieces,
        and updates game state and turn. Then returns True.
        """
        if self._game_state != "UNFINISHED":
            return False

        if not self._board.make_move(square_from, square_to, self._active_player):
            return False

        self.update_game_state()
        self.switch_active_player()
        return True

    def update_game_state(self):
        """Checks if the active player has won the game. If so, updates the game state."""
        passing_player = {'BLACK': 'RED', 'RED': 'BLACK'}[self._active_player]

        if self.get_num_captured_pieces(passing_player) >= 8:
            self._game_state = f'{self._active_player}_WON'

    def switch_active_player(self):
        """Switches active player, if Black switches to Red, if Red switches to Black"""
        self._active_player = {'BLACK': 'RED', 'RED': 'BLACK'}[self._active_player]

    def get_square_occupant(self, square):
        """Returns the color of the piece that occupies the square. 'NONE' if no piece occupies the square."""
        return self._board.get_square_occupant_color(square)

    def display_board(self):
        """Displays the current state of the board."""
        self._board.display()

    def play(self):
        """Sets up and plays the game until a player wins."""
        print("Welcome to my Hasami Shogi program!")
        print("Please enter moves in form '[origin square], [destination square]'.\n")

        while self._game_state == 'UNFINISHED':

            # displays the number of pieces each player has captured
            for color, op_color in {"RED": "BLACK", "BLACK": "RED"}.items():
                print(f'{color} has captured {self.get_num_captured_pieces(op_color)} opposing pieces.')

            # displays the current player
            print(f"It is {self._active_player}'s turn.\n")

            # displays board
            self._board.display()
            print()

            # prompts for a move until a legal move is entered
            legal_move = False
            while not legal_move:

                move = input(f"{self._active_player}, enter your move: ")

                try:
                    from_square, to_square = move.split(", ")
                except ValueError:
                    from_square, to_square = 'a0', 'a0'

                legal_move = self.make_move(from_square, to_square)
                if not legal_move:
                    print("Not a legal move, try again.")

            print()

        self._board.display()
        print(f"{self._game_state.split('_')[0]} wins!")


class Board:
    """
    Represents a Hasami Shogi board as a list of lists.
    Has private data members grid (list of lists) and size (default size is 9)
    """

    def __init__(self, size=9):
        """
        Creates a Hasami Shogi board and populates it with pieces in default starting position.
        Default size is 9x9 but this can be changed by passing in a parameter.
        """
        self._grid = []
        self._size = size
        self._grid.append([Piece('RED') for col in range(size)])
        self._grid.extend([[None for col in range(size)] for row in range(size - 2)])
        self._grid.append([Piece('BLACK') for col in range(size)])

    def get_num_captured_pieces(self, color):
        """Returns the number of captured pieces of the passed in color."""
        result = self._size
        for row in self._grid:
            result -= sum(square is not None and square.get_color() == color for square in row)

        return result

    @staticmethod
    def translate_square(square):
        """Returns a tuple containing row, column as ints (index starts at 1)"""
        # converts the passed in letter to row number using ascii
        row = ord(square[0]) - 96
        # returns -1 for col if passed in value is not castable to int
        try:
            col = int(square[1:])
        except ValueError:
            col = -1

        return row, col

    def get_square_occupant_color(self, square):
        """Returns the color of the piece occupying the square, returns 'NONE' if no piece"""
        row, col = self.translate_square(square)
        if 0 >= row or row > self._size or 0 >= col or col > self._size:
            return 'NONE'

        occupant = self._grid[row - 1][col - 1]
        if occupant is None:
            return 'NONE'

        return occupant.get_color()

    def is_legal_move(self, from_square, to_square, color):
        """
        Takes in origin square, destination square, and moving player color.
        Returns True if move is legal, False if not
        """
        # makes sure inputted squares are at least length 2
        if len(from_square) < 2 or len(to_square) < 2:
            return False

        # makes sure piece to be moved matches color passed in
        # if from_square out of bounds, get_square_occupant_color also returns "NONE"
        if color != self.get_square_occupant_color(from_square):
            return False

        from_row, from_col = self.translate_square(from_square)
        to_row, to_col = self.translate_square(to_square)

        # makes sure destination is within bounds
        if 0 >= to_row or to_row > self._size or 0 >= to_col or to_col > self._size:
            return False

        # checks if the move is horizontal
        if from_row == to_row:
            direction = 1 if to_col > from_col else -1
            while to_col * direction > from_col * direction:
                from_col += direction
                if self._grid[from_row - 1][from_col - 1] is not None:
                    return False

            return True

        # checks if the move is vertical
        if from_col == to_col:
            direction = 1 if to_row > from_row else -1
            while to_row * direction > from_row * direction:
                from_row += direction
                if self._grid[from_row - 1][from_col - 1] is not None:
                    return False

            return True

        return False

    def make_move(self, from_square, to_square, color):
        """
        Attempts to make the requested move from from_square to to_square by the player of passed in color.
        Returns False if move is not legal.
        If legal, moves the piece and removes any captured pieces. Then returns True.
        """
        if not self.is_legal_move(from_square, to_square, color):
            return False

        from_row, from_col = self.translate_square(from_square)
        to_row, to_col = self.translate_square(to_square)

        # moves piece to new square, puts None in old square
        self._grid[to_row - 1][to_col - 1] = self._grid[from_row - 1][from_col - 1]
        self._grid[from_row - 1][from_col - 1] = None

        self.remove_captures(to_square)
        return True

    def remove_captures(self, square):
        """Removes pieces captured by the piece on the passed in square string"""
        row, col = self.translate_square(square)
        piece = self._grid[row - 1][col - 1]
        if piece is None:
            return False

        color = piece.get_color()

        remove_coords = []

        # deals with standard capture cases
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            trial_row = row + y
            trial_col = col + x

            while 0 < trial_row <= self._size and 0 < trial_col <= self._size:
                candidate_piece = self._grid[trial_row - 1][trial_col - 1]
                if candidate_piece is None:
                    break

                if candidate_piece.get_color() == color:
                    trial_row -= y
                    trial_col -= x

                    while trial_row * y > row * y or trial_col * x > col * x:
                        remove_coords.append((trial_col, trial_row))
                        trial_row -= y
                        trial_col -= x
                    break

                trial_row += y
                trial_col += x

        # deals with corner cases
        if (col, row) in [(1, 2), (2, 1), (self._size, self._size - 1), (self._size - 1, self._size)]:
            # reflection across diagonal
            reflection = self._grid[col - 1][row - 1]
            if reflection is not None and reflection.get_color() == color:
                if row == 1 or col == 1:
                    corner = self._grid[0][0]
                    if corner is not None and corner.get_color() != color:
                        remove_coords.append((1, 1))
                else:
                    corner = self._grid[self._size - 1][self._size - 1]
                    if corner is not None and corner.get_color() != color:
                        remove_coords.append((self._size, self._size))

        # reflection across the other diagonal
        if (col, row) in [(1, self._size - 1), (self._size - 1, 1), (2, self._size), (self._size, 2)]:
            reflection = self._grid[9 - col][9 - row]
            if reflection is not None and reflection.get_color() == color:
                if row == self._size - 1 or col == 2:
                    corner = self._grid[self._size - 1][0]
                    if corner is not None and corner.get_color() != color:
                        remove_coords.append((1, self._size))
                else:
                    corner = self._grid[0][self._size - 1]
                    if corner is not None and corner.get_color() != color:
                        remove_coords.append((self._size, 1))

        # removes the pieces to be removed
        for remove_col, remove_row in remove_coords:
            self._grid[remove_row - 1][remove_col - 1] = None

    def display(self):
        """Prints the board"""
        print(' ', *range(1, self._size + 1))
        for index, row in enumerate(self._grid):
            print(chr(97 + index), end=' ')

            for piece in row:
                if piece is None:
                    print('-', end=' ')
                else:
                    print(piece.get_color()[0], end=' ')

            print('')


class Piece:
    """Represents a Hasami Shogi game piece"""

    def __init__(self, color):
        """Creates a Hasami Shogi game piece"""
        self._color = color

    def get_color(self):
        """Returns the string color of the game piece"""
        return self._color
