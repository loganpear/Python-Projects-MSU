###############################################################################
# Project 6 CSE 231
#
# This code displays information about social media connections between
# users. It reads data from files containing user's names, X IDs, and
# Facebook names, and then computes statistics based on which choice the
# user using this program inputs which could be: the maximum number of
# friends intersections between X and Facebook, the percentage of people
# with no shared friends between the two platforms, a printed list of a
# person's friends on the two platforms, the percentage of people with
# more friends on X than Facebook, and the number of triangle. The program
# stops once an invalid option choice is inputted by the user.
#
###############################################################################

import sys

MENU = """
  Menu : 
     1: Max number of friends intersection between X and Facebook among all
     2: Percentage of people with no shared friends between X and Facebook
     3: Individual information
     4: Percentage of people with  more friends in X compared to Facebook
     5: The number of  triangle friendships in X
     6: The number of  triangle friendships on Facebook
     7: The number of  triangle friendships in X and Facebook together 
       Enter any other key(s) to exit

  """

INPUT_FILE_TEXTS = [
    "\nEnter a names file ~:",
    "\nEnter the twitter id file ~:",
    "\nEnter the facebook id file ~:",
]


def input(prompt=None):
    """
        DO NOT MODIFY: Uncomment this function when submitting to Codio
        or when using the run_file.py to test your code.
        This function is needed for testing in Codio to echo the input to the
        output
        Function to get user input from the standard input (stdin) with an
        optional prompt.
        Args:
            prompt (str, optional): A prompt to display before waiting for input
             Defaults to None.
        Returns:
            str: The user input received from stdin.
    """

    if prompt:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


def open_file(prompt_str):
    """
    Requests the file name until it's able to be opened.
        Parameters:
           prompt_str (str): The prompt text for the input.
        Returns:
           fp: The opened file object.
   """

    while True:  # breaks when a valid file is able to be opened
        file_name = input(prompt_str)
        try:
            fp = open(file_name, "r")
            break
        except FileNotFoundError:
            print("Error. File does not exist")
    return fp


def read_file_into_list(fp):
    """
    Turns a file into a list of each of its lines.
        Parameters:
            fp: File Pointer
        Returns:
            new_list: A list of each line in the file
    """
    new_list = []
    for line in fp:
        line = line.strip()
        new_list.append(line)
    fp.close()
    return new_list


def make_nest_dict(names_list, twt_list, fb_list):
    """
    Creates a nested dictionary from the provided lists.
        Parameters:
            names_list: A list of names.
            twt_list: A list of Twitter IDs.
            fb_list: A list of Facebook IDs.
        Returns:
            names_dict: A nested dictionary representing the social media
            connections. Each name is a key for the outer dictionary and each
            value is another dictionary containing two keys for X and FaceBook
            and for each of those values is a set of their friends (user IDs)
    """
    names_dict = {}  # this is the outer dictionary, each name is a key

    for i, name in enumerate(names_list):

        # these two blocks make each twt line into a set of user IDs
        twt_line = twt_list[i]
        twt_line = twt_line.strip(',')
        twt_mini_list = twt_line.split(',')
        twt_set = set()

        if twt_line != '':  # This makes it ignore people with no friends
            # This for loop makes each user ID an integer
            for user_num in twt_mini_list:
                num = int(user_num)
                twt_set.add(num)

        # these next blocks make each FaceBook line into a set of user IDs
        fb_line = fb_list[i]
        fb_line = fb_line.strip(',')
        fb_mini_list = fb_line.split(',')
        fb_set = set()

        if fb_line != '':  # This makes it ignore people with no friends
            for name_fb in fb_mini_list:

                # rather than add each name to the fb_set, below I get the
                # index of each name so the set consists of user IDs
                name_index = names_list.index(name_fb)
                fb_set.add(name_index)

        # This makes the nested dictionary
        social_media_dict = dict()  # inner dictionary
        social_media_dict["fb"] = fb_set
        social_media_dict["twt"] = twt_set

        names_dict[name] = social_media_dict

    return names_dict


def find_max_intersections(names_nest_dict):
    """
    Finds the maximum number of friends intersection between X and Facebook
        Parameters:
            names_nest_dict: A nested dictionary of all social media friends
        Returns:
            max_intersections (int): The maximum number of friends intersection
    """
    max_intersection = 0  # initializes

    for name, data in names_nest_dict.items():
        intersection = len(data['twt'].intersection(
            data['fb']))
        max_intersection = max(max_intersection, intersection)

    return max_intersection


def calculate_pct_no_shared_friends(names_nest_dict):
    """
    Calculates the percentage of people with no shared friends between X and Fb
        Parameters:
            names_nest_dict: A nested dictionary of all social media friends
        Returns:
            percentage_no_shared_friends (float): The percentage of people with
                no shared friends
    """
    total_people = len(names_nest_dict)
    count = 0  # count of users with no shared friends

    for name, data in names_nest_dict.items():
        intersection_num = len(data['twt'].intersection(data['fb']))
        if intersection_num == 0:
            count += 1

    percentage_no_shared_friends = (count / total_people) * 100
    return round(percentage_no_shared_friends)


def find_friends(name, names_nest_dict, names_list):
    """
    Finds and prints the friends of a person on X and Fb alphabetically
        Parameters:
            name (str): The name of the person
            names_nest_dict: A nested dictionary of all social media friends
            names_list: A list of all names we are using as data
    """
    x_ids_set = names_nest_dict[name]['twt']
    twt_find_list = []

    # makes a list of all X friends names
    for x_id in x_ids_set:
        twt_find_list.append(names_list[x_id])
    sorted_twt_list = sorted(twt_find_list)  # sorts the list alphabetically

    # displays each name with a context header
    print("-" * 14 + "\nFriends in X\n" + "*" * 14)
    for each_name in sorted_twt_list:
        print(each_name)

    fb_ids_set = names_nest_dict[name]['fb']
    fb_find_list = []

    # makes a list of all facebook friends names
    for fb_id in fb_ids_set:
        fb_find_list.append(names_list[fb_id])
    sorted_fb_list = sorted(fb_find_list)

    # displays each name with a context header
    print("-" * 20 + "\nFriends in Facebook\n" + "*" * 20)
    for each_name in sorted_fb_list:
        print(each_name)


def more_x_friends(names_nest_dict, names_list):
    """
    Calculates the percentage of people with more friends in X vs Fb
        Parameters:
            names_nest_dict (dict): A nested dictionary of social media friends
            names_list (list): A list of names
        Returns:
            percent (int): Percentage of users with more friends in X than Fb
    """
    more_x_friends_count = 0  # count of people with more friends on X
    total_names = len(names_list)

    for name in names_list:
        twt_friends_set = names_nest_dict[name]['twt']
        twt_friends_quantity = len(twt_friends_set)  # num of X friends
        fb_friends_set = names_nest_dict[name]['fb']
        fb_friends_quantity = len(fb_friends_set)  # num of Fb friends

        if twt_friends_quantity > fb_friends_quantity:
            more_x_friends_count += 1

    percent = int(more_x_friends_count / total_names * 100)
    return percent


def find_num_triangles(nest_dict, names_list, platform):
    """
    Finds the number of triangle friendships on the specified platform
        Parameters:
            nest_dict: A nested dictionary of social media friends
            names_list: A list of the names
            platform (str): The social media platform ('twt' , 'fb')
        Returns:
            int: The number of triangle friendships
    """
    triangles_list = []
    id_list = []

    # makes a list of IDs we can iterate through in the for loop after this
    for i in range(len(names_list)):
        id_list.append(i)

    # iterates through each user ID and gets the set of friends IDs
    for main_id in id_list:
        name1 = names_list[main_id]
        id_set1 = nest_dict[name1][platform]

        # iterates through each ID in the main_id's friend list to get the
        # set of each of their friend's IDs
        for id2 in id_set1:
            name2 = names_list[id2]
            id_set2 = nest_dict[name2][platform]

            # iterates through each of person 2's friends to see if they are
            # friends with the original person (main_id) which would indicate
            # a triangle friendship if True
            for id3 in id_set2:
                if id3 in id_set1:
                    triangle_tup = sorted((main_id, id2, id3))

                    # makes sure this triangle friendship hasn't been recorded
                    # already then adds it to the list
                    if triangle_tup not in triangles_list:
                        triangles_list.append(triangle_tup)

    return len(triangles_list)


def find_both_triangles(nest_dict, names_list):
    """
    Finds the number of triangle friendships in both X and Fb combined
        Parameters:
            nest_dict: A nested dictionary of social media friends
            names_list: A list of the names
        Returns:
            int: The number of triangle friendships.
    """
    triangles_list = []
    id_list = []

    # makes a list of IDs we can iterate through in the for loop after this
    for i in range(len(names_list)):
        id_list.append(i)

    # iterates through each user ID and gets the set of friends IDs
    # for both X and Fb, it merges them into one set
    for main_id in id_list:
        name1 = names_list[main_id]
        fb_set1 = nest_dict[name1]['fb']
        twt_set1 = nest_dict[name1]['twt']
        id_set1 = fb_set1.union(twt_set1)

        # iterates through each ID in the main_id's friend list to get the
        # set of each of their friend's IDs
        for id2 in id_set1:
            name2 = names_list[id2]
            fb_set2 = nest_dict[name2]['fb']
            twt_set2 = nest_dict[name2]['twt']
            id_set2 = fb_set2.union(twt_set2)

            # iterates through each of person 2's friends to see if they are
            # friends with the original person (main_id) which would indicate
            # a triangle friendship if True
            for id3 in id_set2:
                if id3 in id_set1:
                    triangle_tup = sorted((main_id, id2, id3))

                    # makes sure this triangle friendship hasn't been recorded
                    # already then adds it to the list
                    if triangle_tup not in triangles_list:
                        triangles_list.append(triangle_tup)

    return len(triangles_list)


def main():

    # iterates through each of the three different prompt strings
    # to open each file and store their file pointers
    for i, prompt_str in enumerate(INPUT_FILE_TEXTS):
        if i == 0:
            names_fp = open_file(prompt_str)
        if i == 1:
            twt_fp = open_file(prompt_str)
        if i == 2:
            fb_fp = open_file(prompt_str)

    """
    #####  Shortcut Inputs  ####
    names_fp = open_file("Names.csv")
    twt_fp = open_file("twt_Friends_id.txt")
    fb_fp = open_file("fb_Friends.txt")
    ############################
    """

    # reads each file and stores their lies as lists
    twt_list = read_file_into_list(twt_fp)
    names_list = read_file_into_list(names_fp)
    fb_list = read_file_into_list(fb_fp)
    names_nest_dict = make_nest_dict(names_list, twt_list, fb_list)

    while True:  # breaks if anything other than 1-7 are entered
        print(MENU)
        choice = input("Input a choice ~:")

        if choice == "1":
            max_intersection = find_max_intersections(names_nest_dict)
            print(f"The Max number intersection of friends between "
                  f"X and Facebook is: {max_intersection}")

        elif choice == "2":
            percent = calculate_pct_no_shared_friends(names_nest_dict)
            print(f"{percent}% of people have no friends "
                  f"in common on X and Facebook")

        elif choice == "3":
            while True:  # repeats until a valid name is entered
                input_name = input("Enter a person's name ~:")
                if input_name in names_list:
                    break
                else:
                    print("Invalid name or does not exist")

            find_friends(input_name, names_nest_dict, names_list)

        elif choice == "4":
            percent_more_x = more_x_friends(names_nest_dict, names_list)
            print(f"{percent_more_x}% of people have more friends in "
                  f"X compared to Facebook")

        elif choice == "5":
            num_triangles_x = \
                find_num_triangles(names_nest_dict, names_list, 'twt')
            print(f"The number of triangle friendships in X is: "
                  f"{num_triangles_x}")

        elif choice == "6":
            num_triangles_fb = \
                find_num_triangles(names_nest_dict, names_list, 'fb')
            print(f"The number of triangle friendships in Facebook is: "
                  f"{num_triangles_fb}")

        elif choice == "7":
            num_triangles_both = \
                find_both_triangles(names_nest_dict, names_list)
            print(f"The number of triangle friendships in X merged "
                  f"with Facebook is:  {num_triangles_both}")

        else:
            print("Thank you")
            break


if __name__ == '__main__':
    main()
