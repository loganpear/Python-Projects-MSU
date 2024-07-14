##############################################################################
#
# Computer Project 08 CSE 231
#
# This project is a net force calculator program. There are two classes: Force
# and ForceCalculator. The Force class is for a force vector with its magnitude
# and angle. The ForceCalculator class manages multiple forces and
# calculates the net force. The main part of the program displays
# a menu of options for the user to choose from. Such options as:
# adding, removing, and displaying forces, computing force components, and
# finding the resultant force. There are also options to reset the
# calculator and exit the program.
#
##############################################################################

from force import ForceCalculator
import sys

MENU = '''\n:~Net Force Calculator Program
          1) Add force
          2) Remove force
          3) Show forces
          4) Find force components
          5) Compute resultant force
          6) Reset calculator
          7) Stop the program
          Enter option~:'''

":~\nEnter value for {}~:"
"\nInput {} is not a valid float number!"
":~\nEnter name of force~:"
"Magnitude (N)"
"Angle (degrees)"
"\nForce objects in the calculator"
"\nThere are no force objects in the calculator."

"\nForce components for Force object {}:"
"\nMagnitude: {}"
"\nFx = {}"
"\nFy = {}"

"\nResultant force of all forces in the calculator"

"\nInvalid option. Please Try Again!"


# def input( prompt=None ):
#     """
#         DO NOT MODIFY: Uncomment this function when using the run_file.py
#         to test your code.
#         This function is needed to echo the input to the output
#         Function to get user input from the standard input (stdin) with an
#         optional prompt.
#         Args:
#             prompt (str, optional): A prompt to display before waiting for
#             input. Defaults to None.
#         Returns:
#             str: The user input received from stdin.
#     """

#     if prompt:
#         print( prompt, end="" )
#     aaa_str = sys.stdin.readline()
#     aaa_str = aaa_str.rstrip( "\n" )
#     print( aaa_str )
#     return aaa_str


def prompt_num(prompt_str):
    """
    Prompts the user for a numeric value until a valid float value is entered
    Args:
        prompt_str: The prompt message
    Returns:
        value: The float value that the user inputted
    """
    while True:  # breaks when a valid float is entered
        try:
            value = float(input(prompt_str))
            return value
        except ValueError:
            print(f"\nInput {value} is not a valid float number!")


def main():
    calculator = ForceCalculator()

    while True:  # repeats until 7 is inputted
        option = input(MENU)

        if option == "1":  # adds force
            name = input("\n:~Enter name of force~:")

            try:  # this is the input function for getting a valid float
                magnitude = prompt_num("\n:~Enter value for Magnitude (N)~:")

            except ValueError as message:
                print(message)

            try:  # this is the input function for getting a valid float
                angle = prompt_num("\n:~Enter value for Angle (degrees)~:")

            except ValueError as message:
                print(message)

            try:  # this adds force to the calculator is possible
                calculator.add_force(name, magnitude, angle)
            except RuntimeError as message:
                print(message)

        elif option == "2":  # removes force
            name = input("\n:~Enter name of force~:")

            try:
                calculator.remove_force(name)
            except RuntimeError as message:
                print(f"{message}")

        elif option == "3":  # shows forces
            if calculator.get_forces():  # if objects are in the calculator
                print("\nForce objects in the calculator")
                print(calculator)

            else:  # if there are no objects in the calculator
                print("\nThere are no force objects in the calculator.")

        elif option == "4":  # finds force components
            name = input("\n:~Enter name of force~:")
            force = calculator.get_forces().get(name)

            if force:  # makes sure force exists
                x_component, y_component = force.get_components()
                print(f"\nForce components for Force object {name}:")
                print(f"\nMagnitude: {force.get_magnitude()}")
                print(f"\nFx = {x_component}")
                print(f"\nFy = {y_component}")

            else:  # if force does not exist
                print(f"\nForce object {name} does not exist!")

        elif option == "5":  # computes net force
            net_force = calculator.compute_net_force()
            print("\nResultant force of all forces in the calculator")
            print(net_force)

        elif option == "6":  # resets calculator
            print("\nResetting calculator...")
            calculator = ForceCalculator()

        elif option == "7":  # stops program
            break

        else:  # if invalid input option is entered
            print("\nInvalid option. Please Try Again!")


if __name__ == "__main__":
    main()
