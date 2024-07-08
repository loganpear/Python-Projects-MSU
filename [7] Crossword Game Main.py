###############################################################################
# Project 7 CSE 231
#
# This program lets the user play a crossword game by having them input
# a file containing all the crossword's information. It also uses the
# classes: Clue & Crossword from the crossword.py file. Users are able
# to make commands such as make guesses that the get displayed by
# the board, reveal correct answers, check which letter in their guess
# might be wrong, redisplay the clues, display the menu, restart their game,
# and quit the program. The program automatically knows when the user has
# solved the crossword and then quits the program.
#
###############################################################################

from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
    "\nC n - Display n of the current puzzle's down and across clues" \
    "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
    "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
    "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at "\
    "row i, column j" \
    "\nH - Display the menu" \
    "\nS - Restart the game" \
    "\nQ - Quit the program"

OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"


def input(prompt=None):
     """
         DO NOT MODIFY: Uncomment this function when submitting to Codio
         or when using the run_file.py to test your code.
         This function is needed for testing in Codio to echo the input to the
        output
         Function to get user input from the standard input (stdin) with an
         optional prompt.
         Args:
             prompt (str, optional): A prompt to display before waiting for
             input. Defaults to None.
         Returns:
             str: The user input received from stdin.
     """

     if prompt:
         print( prompt, end="" )
     aaa_str = sys.stdin.readline()
     aaa_str = aaa_str.rstrip( "\n" )
     print( aaa_str )
     return aaa_str


def open_file():
    """
    Opens a file containing all the information needed
    for a crossword puzzle
    Returns: Crossword: A Crossword object representing the puzzle
    """
    while True:  # breaks when a valid file is able to be opened
        file_name = input(PUZZLE_PROMPT)
        try:
            crossword = Crossword(file_name)
            return crossword

        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)


def display_clues(crossword, num_clues=0):
    """
    Displays a specified number of clues. If unspecified it displays all clues
    parameters:
        crossword: The Crossword object representing the puzzle.
        num_clues (int): Number of clues to display. Defaults to 0 which
            displays all clues
    """
    across_clues = []
    down_clues = []

    # if no amount of clues was specified, it makes the number of clues
    # displayed the same as the amount of clues there are which is all of them
    if num_clues == 0:
        num_clues = len(crossword.clues)

    # makes 2 lists, 1 for down clues and one for across clues
    for clue in crossword.clues.values():
        if clue.down_across == 'A':
            across_clues.append(clue)
        else:
            down_clues.append(clue)

    print("\nAcross")
    for clue in across_clues[:num_clues]:
        point = clue.indices
        print(f"{point} Across: {clue.clue}")

    print("\nDown")
    for clue in down_clues[:num_clues]:
        point = clue.indices
        print(f"{point} Down: {clue.clue}")


def validate_commands(crossword, string):
    """
    Validates user input commands and returns a list of valid commands.
    Parameters:
        crossword: The Crossword object representing the puzzle
        string (str): The user input string containing the command
    Returns:
        list or None: A list containing the validated command and arguments,
            or None if the command was invalid

    """
    input_list = string.split()  # makes input string into a list of items

    if len(input_list) == 0:
        return None

    try:  # if the fist item is not a letter it fails
        input_list[0] = input_list[0].upper()
    except AttributeError:
        return None

    if input_list[0] == "C":
        if len(input_list) != 2:  # tests for 2 items
            return None
        try:
            num = int(input_list[1])  # tests that second item is a number
            if num <= 0:  # makes sure its positive
                return None

        except ValueError:
            return None

    elif input_list[0] in ("H", "S", "Q"):
        if len(input_list) > 1:
            return None

    elif input_list[0] in ("G", "R", "T"):
        if len(input_list) != 4:
            return None

        for item in input_list[1:3]:
            try:  # makes sure items 2 and 3 are numbers
                num = int(item)
                if num < 0:
                    return None

                # makes a key based on the user input
                # key: (starting i, starting j, across/down)
                key = (int(input_list[1]), int(input_list[2]), input_list[3])
                if key not in crossword.clues:  # validates key is in crossword
                    return None

            except ValueError:
                return None
    else:
        return None

    return input_list


def main():
    # initialization
    crossword = open_file()
    display_clues(crossword)
    print(crossword)
    print(HELP_MENU)

    while True:  # breaks when Q is entered or the puzzle is solved

        while True:  # mini loop for a valid input choice
            input_string = input(OPTION_PROMPT)
            command = validate_commands(crossword, input_string)
            if command is None:  # if the input was not a valid command:
                print("Invalid option/arguments. Type 'H' for help.")
            else:
                break

        if command[0] == "C":
            num_clues = int(command[1])
            display_clues(crossword, num_clues)

        elif command[0] == "G":
            # makes a tuple key to find out which clue has those indices
            x_point = int(command[1])
            y_point = int(command[2])
            a_or_d = command[3]
            clue_tup = (x_point, y_point, a_or_d)
            clue = crossword.clues.get(clue_tup)

            while True:  # repeats until valid input in terms of length and
                         # valid characters
                try:
                    new_guess = input("Enter your guess (use _ for blanks): "
                                      ).upper()
                    crossword.change_guess(clue, new_guess)
                    break
                except RuntimeError as error_message:
                    print(error_message)

            print(crossword)

        elif command[0] == "R":
            # makes a tuple key to find out which clue has those indices
            x_point = int(command[1])
            y_point = int(command[2])
            a_or_d = command[3]
            clue_tup = (x_point, y_point, a_or_d)
            clue = crossword.clues.get(clue_tup)

            crossword.reveal_answer(clue)
            print(crossword)

        elif command[0] == "T":
            # makes a tuple key to find out which clue has those indices
            x_point = int(command[1])
            y_point = int(command[2])
            a_or_d = command[3]
            clue_tup = (x_point, y_point, a_or_d)
            clue = crossword.clues.get(clue_tup)

            wrong_position = crossword.find_wrong_letter(clue)
            if wrong_position >= 0:  # if -1 isn't returned by the function

                # wrong_position adds 1 to it, so it displays the location of
                # as opposed to the index calculated by the function
                print(f"Letter {wrong_position + 1} is wrong, it should be "
                      f"{clue.answer[wrong_position]}")
            else:  # if -1 is returned by the function
                print("This clue is already correct!")

        elif command[0] == "H":
            print(HELP_MENU)

        elif command[0] == "S":
            crossword = open_file()
            display_clues(crossword)  # this resets the crossword object
            print(crossword)
            print(HELP_MENU)

        elif command[0] == "Q":
            break

        if crossword.is_solved():
            print("\nPuzzle solved! Congratulations!")
            break


if __name__ == "__main__":
    main()
