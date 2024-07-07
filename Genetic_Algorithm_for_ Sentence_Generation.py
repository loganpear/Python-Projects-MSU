"""
CSE 231 project 4

This project uses a genetic algorithm for sentence generation.
It uses functions for: finding the fitness of individuals compared to
a target sentence, selecting individuals from a population through tournament
selection, performing mutation and crossover operations, and finding the best
individual in a population based on fitness. The main function implements
the genetic algorithm by generating a population, altering it over
multiple generations, and terminating when the target sentence is found or
after the max number of generations is reached.
"""

import random
random.seed(10)

NUM_GENERATIONS = 200
NUM_POPULATION = 100
PROBABILITY_MUTATION = 0.2
PROBABILITY_CROSSOVER = 0.8
ALPHABET = 'abcdefghijklmnopqrstuvwxyz '
BANNER = """
**************************************************************
Welcome to GeneticGuess Sentencer!
This program will attempt to guess a sentence that you input.
Simply input a sentence and the program will attempt to guess it!
**************************************************************
"""
CONTINUE_TEXT = "\nWould you like to continue? (y/n) "
TARGET_TEXT = \
    "\nPlease input the sentence you would like the program to guess: "
INVALID_TEXT = "\nIncorrect input. Please try again.\n"
THANKS_TEXT = "\n\nThank you for using GeneticGuess Sentencer!"


# NEXT ARE ALL THE DEFINITIONS
def fitness(target, individual):
    """
    Calculates the fitness of an individual compared to the target string
        target (str): The target string to compare against
        individual (str): The individual string to evaluate
    Returns the fitness score, representing the proportion of characters that
        match between the individual and the target (float)
    """
    length = len(target)
    same_count = 0
    for i, ch in enumerate(target):
        if ch == individual[i]:
            same_count += 1
    return same_count / length


def five_tournament_selection(population, target):
    """
    Uses a five tournament selection on the population to
    choose the best individual
        population (str): The population of individuals
        target (str): The target string
    Returns the selected individual from the population
    """
    length = len(target)
    highest_fitness = -1
    for count in range(5):
        beginning_index = random.randint(0, NUM_POPULATION-1) * length
        ending_index = beginning_index + length
        individual = population[beginning_index:ending_index]
        fit_amount = fitness(target, individual)
        if fit_amount > highest_fitness:
            highest_fitness = fit_amount
            output = individual
    return output


def make_population(target):
    """
    Gets the length of target word than multiplies it by the population size
        to get one long string of random combinations in ALPHABET
            length: the number of characters in the target word (int)
    Returns a string of all random individual (str)
    """
    length = len(target) * NUM_POPULATION
    output = ''
    for i in range(length):
        ch = random.choice(ALPHABET)
        output += ch
    return output


def mutation(individual):
    """
    Performs mutation on one individual string by iterating through the
        characters randomly mutating some characters.
            individual (str): The individual string to mutate
    Returns the mutated individual string (str)
    """
    new_individual = ''
    for ch in individual:
        individual_mutation = random.random()
        if individual_mutation <= PROBABILITY_MUTATION:
            new_individual += random.choice(ALPHABET)
        else:
            new_individual += ch
    return new_individual


def single_point_crossover(individual1, individual2):
    """
    Crosses over between two individual strings at a random point
        individual1 (str): The first individual string
        individual2 (str): The second individual string
    Returns a tuple of the two new individual strings after the crossover if
        it happened, otherwise just returns the two original individuals
    """
    length = len(individual1)
    random_num = random.random()

    if random_num <= PROBABILITY_CROSSOVER:
        cross_index = random.randint(0, length - 1) + 1
        new_individual_1 = \
            individual1[:cross_index] + individual2[cross_index:]
        new_individual_2 = \
            individual2[:cross_index] + individual1[cross_index:]
    else:
        new_individual_1 = individual1
        new_individual_2 = individual2
    return new_individual_1, new_individual_2


def find_best_individual(population, target):
    """
    Finds the best individual in the population based on fitness score
        population (str): The population of individuals.
        target (str): The target string to be guessed.
    Returns: The best individual string found in the population (str)
    """
    highest_fitness = -1  # initializer
    length = len(target)
    num_population_chs = len(population)  # characters in the population

    for i in range(0, num_population_chs - length + 1, length):
        individual = population[i:i + length]
        fit_amount = fitness(target, individual)
        if fit_amount > highest_fitness:
            highest_fitness = fit_amount
            fittest_individual = individual
    return fittest_individual

# BELOW IS THE MAIN FUNCTION


def main():
    print(BANNER)
    while True:
        input_continue = input(CONTINUE_TEXT)
        if input_continue.lower() != "y":
            break
        else:
            invalid_boolean = True
            # initializes this boolean so the input target loop can happen

            # this while loop continues asking for a valid target phrase until
            # a valid one is entered and the loop quits
            while invalid_boolean:  # this is the input target loop
                target_string_input = input(TARGET_TEXT)
                target_string = target_string_input.lower()
                for ch in target_string:
                    if ch in ALPHABET:
                        invalid_boolean = False
                    else:
                        invalid_boolean = True
                        print(INVALID_TEXT)
                        break  # this breaks the for loop and returns to the
                        # beginning of the while loop to re-prompt for an input

            population = make_population(target_string)  # initial population
            print("\n\nGeneticGuess results:")

            # this is the outer loop which repeats up to 200 generations
            # unless the target is found early
            for num in range(NUM_GENERATIONS):
                print(f"Generation: {num}")
                new_population = ''

                # this for loop (inner loop) performs the number of times in
                # NUM_POPULATION to pick to individuals through 5 tournament
                # selection then perform various altercations through other
                # functions get a fittest individual for each iteration
                for number in range(NUM_POPULATION):
                    individual1 = five_tournament_selection\
                        (population, target_string)
                    individual2 = five_tournament_selection\
                        (population, target_string)
                    individual_mut_1 = mutation(individual1)
                    individual_mut_2 = mutation(individual2)
                    ind_cross_1, ind_cross_2 = single_point_crossover\
                        (individual_mut_1, individual_mut_2)

                    # finds which crossed individual is more fit
                    if fitness(target_string, ind_cross_1) > \
                            fitness(target_string, ind_cross_2):
                        fittest_individual = ind_cross_1
                    else:
                        fittest_individual = ind_cross_2
                    new_population += fittest_individual
                    # adds fittest individual to the new population

                population = new_population  # sets old population to new
                best_individual = find_best_individual\
                    (population, target_string)

                # determines if target is found early
                if best_individual == target_string:
                    print("I found the sentence early!")
                    print(f"\nBest Individual: {best_individual}")
                    break

            else:  # This else only activates if best match isn't found early
                print(f"\nBest Individual: {best_individual}")
    print(THANKS_TEXT)

# this calls the main function
if __name__ == '__main__':
    main()

