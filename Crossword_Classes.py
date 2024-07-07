###############################################################################
# Classes for Project 7 CSE 231
#
# The following code contains two Classes: Clue & Crossword. The clue class
# represents a single clue in the crossword puzzle while the Crossword class
# represents the entire crossword puzzle. Crossword contains methods such as
# changing the guess, revealing the answer, finding the fist instance of a wrong
# letter, and checking if the puzzle is solved.
###############################################################################

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    """
    This class: Clue, is an object that represents a clue in the
    crossword puzzle.
    """
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return (f"{self.indices} \
        {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}")

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues
         come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) +
                                                       other.indices)


class Crossword:
    """
    This class: Crossword, is an object that represents the entire puzzle.
    There are methods for it that can make changes to the board and get
    information about the crossword puzzle.
    """
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in
                      range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'],
                                          row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in
                                           range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):
        """
        Changes the guess for a specific clue in the crossword puzzle.
        If there are already characters on the board for that clue it will
            replace them.
        Parameters:
            clue: The clue object associated which the guess being changed
            new_guess (str): The new guess
        """
        if len(new_guess) != len(clue.answer):  # makes sure same length
            raise RuntimeError(
                "Guess length does not match the length of the clue.\n")
        for char in new_guess:  # checks all are valid characters
            if char == '_':
                pass
            elif char.upper() not in GUESS_CHARS:
                raise RuntimeError("Guess contains invalid characters.\n")

        # this fills in the board with the guess
        row, col = clue.indices
        for i, ch in enumerate(new_guess):
            if clue.down_across == "A":
                self.board[row][col + i] = ch
            else:
                self.board[row + i][col] = ch

    def reveal_answer(self, clue):
        """
        Reveals the answer for a given clue in the crossword puzzle
        Parameters:
            clue: The clue object associated which the guess being revealed.
        """
        # this fills the board with the correct answer
        row, col = clue.indices
        for i, ch in enumerate(clue.answer):
            if clue.down_across == "A":
                self.board[row][col + i] = ch
            else:
                self.board[row + i][col] = ch

    def find_wrong_letter(self, clue):
        """
        Finds the first wrong letter in the associated clue
        Parameters:
            clue: The clue object associated which the guess being checked
        Returns:
            int: The index of the first wrong letter in the current guess or
               -1 if the guess is already correct
        """
        row_start, col_start = clue.indices
        length = len(clue.answer)

        # this extracts their guess from the board and stores it as guess
        if clue.down_across == "A":
            guess = self.board[row_start][col_start:col_start + length]
        else:
            guess = ""
            for i in range(length):
                guess += self.board[row_start + i][col_start]

        for i in range(length):  # test if each letter is the same
            if guess[i] != clue.answer[i]:
                return i  # if a wrong letter is detected

        return -1  # if no wrong letters detected

    def is_solved(self):
        """
        Checks if the crossword puzzle is solved
        Returns:
            boolean: True if the crossword is solved or False if not
        """
        # iterates through each clue of the crossword
        for clue in self.clues.values():
            row_start, col_start = clue.indices
            length = len(clue.answer)
            guess = ""

            # this extracts the user's guess from the board
            if clue.down_across == "A":
                guess_list = self.board[row_start][col_start:col_start + length]
                for char in guess_list:
                    guess += char
            else:
                for i in range(length):
                    guess += self.board[row_start + i][col_start]

            # once one guess is incorrect it returns False
            if guess != clue.answer:
                return False

        return True  # if every guess is correct
