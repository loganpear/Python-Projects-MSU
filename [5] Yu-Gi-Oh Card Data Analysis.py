###############################################################################
# CSE 231 Project 5: Yu-Gi-Oh Card Data Analysis
#
# This project lets users analyze card data for the game Yu-Gi-Oh
# It lets the user choose an option they'd like to do such as get info on all
# cards, search for specific cards based on a query, view decklists, and
# lastly there's an option to exit the program. Functions do things such as
# read card data from a CSV file, process decklists, search for
# cards based on user input, compute statistics such as minimum, maximum,
# and median prices of cards, and display formated results
#
###############################################################################

import csv
from operator import itemgetter

# CONSTANTS

CATEGORIES = ["id", "name", "type", "desc", "race", "archetype", "card price"]
MENU = "\nYu-Gi-Oh! Card Data Analysis" \
       "\n1) Check All Cards" \
       "\n2) Search Cards" \
       "\n3) View Decklist" \
       "\n4) Exit" \
       "\nEnter option: "


def open_file(prompt_str):
    """
    Requests the file name until it's able to be opened.

    Parameters:
       prompt_str (str): The initial file name input.

    Returns:
       fp: The opened file object.
   """
    file_name = prompt_str

    while True:  # breaks when a valid file is able to be opened
        try:
            fp = open(file_name, "r", encoding=" utf-8")
            break
        except FileNotFoundError:
            print("\nFile not Found. Please try again!")
            file_name = input("\nEnter cards file name: ")
    return fp


def read_card_data(fp):
    """
    Reads card data from a CSV file and sorts it.

    Parameters:
        fp (file object): The file containing the card data

    Returns:
        sorted_tuple_list: A sorted list of tuples containing each card's data.
    """
    tuple_list = []
    reader = csv.reader(fp)

    for i, row in enumerate(reader):
        if i > 0:  # skips header line

            # makes sure length is <= 45
            if len(row[1]) > 45:
                row1 = (row[1])[:45]
            else:
                row1 = row[1]

            row6 = float(row[6])
            card_tup = (row[0], row1, row[2], row[3], row[4], row[5], row6)
            tuple_list.append(card_tup)

    # sorts list by price (low-high) first then name alphabetically
    sorted_tuple_list = sorted(tuple_list, key=itemgetter(6, 1))
    return sorted_tuple_list


def read_decklist(fp, card_data):
    """
    Reads the inputted file containing id numbers and makes
    a sorted deck list of the cards with names and info.

    Parameters:
        fp (file object): The file object containing the decklist.
        card_data (list): A list of tuples representing card data.

    Returns:
        sorted_deck_list: A sorted list of tuples representing card data from
        the cards in the decklist.
    """
    deck_list = []
    reader = csv.reader(fp)

    # outer loop iterates through id numbers in the deck list
    for i, id_num in enumerate(reader):
        if i > 0:  # skips header line

            # inner loop tests to see which card in the deck the ID is for
            for card in card_data:
                if id_num[0] == card[0]:
                    deck_list.append(card)
                    break

    # sorts list by price (low-high) first then name alphabetically
    sorted_deck_list = sorted(deck_list, key=itemgetter(6, 1))
    return sorted_deck_list


def search_cards(card_data, query, category_index):
    """
    Searches for cards containing query in one specified category.

    Parameters:
        card_data (list): A list of tuples of card data.
        query (str): The search query.
        category_index (int): The index of the category to search.

    Returns:
        sorted_search_list: A sorted list of tuples containing the query.
    """
    search_list = []

    for card in card_data:
        if query in card[category_index]:
            search_list.append(card)

    # sorts list by price (low-high) first then name alphabetically
    sorted_search_list = sorted(search_list, key=itemgetter(6, 1))
    return sorted_search_list


def compute_stats(card_data):
    """
    Computes the statistics: minimum, maximum, and median prices of cards
    then makes a list of each with the prices of each as well.

    Parameters:
        card_data (list): A list of tuples representing card data.

    Returns:
        A tuple containing what's below
        - min_list (list): List of cards with the minimum price.
        - minimum (float): The minimum price among all cards.
        - max_list (list): List of cards with the maximum price.
        - maximum (float): The maximum price among all cards.
        - median_list (list): List of cards with the median price.
        - median (float): The median price among all cards.
    """
    # these are initializers
    minimum = 999999
    maximum = -1
    median_options = []  # this is just a list of all prices

    for card in card_data:
        median_options.append(card[6])

    median_options.sort()
    length = len(median_options)
    median = median_options[length // 2]

    # finds the minimum and maximum price
    for card in card_data:
        if card[6] < minimum:
            minimum = card[6]
        if card[6] > maximum:
            maximum = card[6]

    min_list = []
    max_list = []
    median_list = []

    # this builds each list
    for card in card_data:
        if card[6] == minimum:
            min_list.append(card)
        if card[6] == maximum:
            max_list.append(card)
        if card[6] == median:
            median_list.append(card)

    return min_list, minimum, max_list, maximum, median_list, median


def display_data(card_data):
    """
    Prints the card data in a formatted table.

    Parameters:
        card_data (list): A list of tuples of each card's data.
    """
    print(f"{'Name':<50}{'Type':<30}{'Race':<20}{'Archetype':<40}",
          f"{'TCGPlayer':<12}")

    total = 0  # this will be the value adding up every price
    for c in card_data:
        print(f"{c[1]:<50}{c[2]:<30}{c[4]:<20}{c[5]:<40}{c[6]:>12,.2f}")
        total += c[6]

    print(f"\n{'Totals':<50}{'':<30}{'':<20}{'':<40}{total:>13,.2f}")


def display_stats(min_cards, minimum, max_cards, maximum, med_cards, median):
    """
    Prints statistics prices of cards and the cards with in those prices.

    Parameters:
        -min_cards (list): A list of tuples of cards with the minimum price.
        -min_price (float): The minimum price.
        -max_cards (list): A list of tuples of cards with the maximum price.
        -max_price (float): The maximum price.
        -med_cards (list): A list of tuples of cards with the median price.
        -median (float): The median price.
    """

    print(f"\nThe price of the least expensive card(s) is {minimum:,.2f}")
    for card in min_cards:
        print(f"\t{card[1]}")
    print(f"\nThe price of the most expensive card(s) is {maximum:,.2f}")
    for card in max_cards:
        print(f"\t{card[1]}")
    print(f"\nThe price of the median card(s) is {median:,.2f}")
    for card in med_cards:
        print(f"\t{card[1]}")


def main():
    prompt_str = input("\nEnter cards file name: ")
    fp = open_file(prompt_str)
    data_list = read_card_data(fp)

    while True:  # repeats menu options input until '4' is entered
        menu_opt = input(MENU)  # takes input for menu option choices

        if menu_opt == '1':
            num_cards = len(data_list)
            print(f"\nThere are {num_cards} cards in the dataset.")

            # makes the card list 50 or less
            if num_cards > 50:
                cheap50_data_list = data_list[:50]
            else:
                cheap50_data_list = data_list
            display_data(cheap50_data_list)
            stats_tup = compute_stats(data_list)

            # below I unpack the stats tuple, they stand for
            # min_list, minimum, max_list, maximum, median_list, median
            mnl, mn, mxl, mx, mdl, md = stats_tup

            display_stats(mnl, mn, mxl, mx, mdl, md)

        elif menu_opt == '2':
            query = input("\nEnter query: ")

            while True:  # repeats until a correct category is inputted
                category = input("\nEnter category to search: ").lower()
                if category in CATEGORIES:
                    break
                else:
                    print("\nIncorrect category was selected!")

            category_index = CATEGORIES.index(category)
            query_list = search_cards(data_list, query, category_index)
            print("\nSearch results")
            num_cards_found = len(query_list)

            if num_cards_found > 0:
                print(f"\nThere are {num_cards_found} cards with '{query}'\
                 in the '{category}' category.")
                display_data(query_list)
                stats_tup = compute_stats(query_list)

                # below I unpack the stats tuple, they stand for
                # min_list, minimum, max_list, maximum, median_list, median
                mnl, mn, mxl, mx, mdl, md = stats_tup

                display_stats(mnl, mn, mxl, mx, mdl, md)
            else:
                print(f"\nThere are no cards with '{query}' in the\
                 '{category}' category.")

        elif menu_opt == '3':
            decklist_file_name = input("\nEnter decklist filename: ")
            print("\nSearch results")
            decklist_fp = open(decklist_file_name, "r")
            deck_list = read_decklist(decklist_fp, data_list)
            display_data(deck_list)
            stats_tup = compute_stats(deck_list)

            # below I unpack the stats tuple, they stand for
            # min_list, minimum, max_list, maximum, median_list, median
            mnl, mn, mxl, mx, mdl, md = stats_tup

            display_stats(mnl, mn, mxl, mx, mdl, md)

        elif menu_opt == '4':
            print("\nThanks for your support in Yu-Gi-Oh! TCG")
            break

        else:
            print("\nInvalid option. Please try again!")


if __name__ == "__main__":
    main()
