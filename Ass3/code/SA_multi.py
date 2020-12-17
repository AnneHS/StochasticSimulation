import numpy as np
import random
import copy
import math
import random
import os
import csv

from city import City, Route
from helpers import load, plot_route, cooling_schedule, create_initial_route, printProgressBar
'''
TODO:
In all cases, you must start with relatively small problems, so that you can
experiment with the SA parameters. Next you should try to solve (much) larger
problems and try to find out how well your solution scales for these problems.

Goals:
(i)   Find good local optimum
(ii)  Experiment with different cooling schedules and observe their effects on
        convergence
(iii) Experiment with length of Markov chains, what is the effect on convergence

((iv) Experiment with the initial temperature, etc.)

https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/

## TODO:
- cooling schedules afmaken
- cooling schedules automatiseren (alpha) --> Formules om alpha uit te rekenen
- markov chain length --> the size of the city
- discussion voor alpha/T etc.
- resultaten opslaan: beste route + lengte
'''

'''
T_START = 100                   # starting temperature
T_MIN = 0.0000001               # min temperature
COOLING_SCHEDULE = 'linear'     # 'linear', 'exponential', 'log', 'quadratic'
MAX_ITERATION = 1000           # currently not used --> now used for alpha
ALPHA = True                   # alpha used for cooling, True then alpha on basis of iterations
if ALPHA:
    if COOLING_SCHEDULE == 'linear':
        ALPHA = T_START/MAX_ITERATION
    elif COOLING_SCHEDULE == 'exponential':
        ALPHA = 0.9 # TODO
    else:
        ALPHA = 0.05
'''



def simulated_annealing(N, initial_route, cooling_type, markov_length, t_start):
    '''
    Simulated annealing with 2-opt.
    '''
    t_current = t_start             # current temperature
    current_route = initial_route   # current route
    best_route = initial_route      # best route so far
    chain_length = 0                # current Markov chain length
    current_iteration = 0           # current iteration

    while t_current > T_MIN:
        for i in range(N-3):
            for j in range(i+2, N-1):

                # New route
                new_route = current_route.two_opt(i, j)
                chain_length+=1

                # Route acceptance
                length_difference = current_route.get_length() - new_route.get_length()
                if length_difference > 0:
                    current_route = new_route
                    best_route = new_route
                elif random.uniform(0, 1) < math.exp(length_difference/t_current):
                    current_route = new_route

                # Inner-loop stopping condition: Markov Chain length
                if chain_length == markov_length:
                    t_current = cooling_schedule(t_start, current_iteration, cooling_type)
                    chain_length=0
                    current_iteration+=1

                # Outer-loop stopping condition: temperature
                if t_current <= T_MIN:
                    return best_route


    return best_route

if __name__ == '__main__':

    problem = 'a280'            # problem type 'eil51'
    schedule = 'linear'          #'linear', 'exponential', 'log', 'quadratic'

    # Params
    ITERATIONS = 10 #300                               # SA iterations
    MARKOV_LENGTHS = np.arange(1, 102, 10)
    T_MIN = 0.001
    T_START = 200

    # Load problem
    N, adjacency_matrix, opt_path, opt_path_len, cities  = load(problem)
    print('Problem: {} \nN: {} \nOptimal length: {}\n'.format(problem, N, opt_path_len))

    # Create random initial route
    initial_route = create_initial_route(N, adjacency_matrix, cities)

    # Open/create results file
    file_name = '../results/{}_{}.csv'.format(problem, schedule)
    if not os.path.isfile(file_name):
            open(file_name, 'x')

    # Run SA
    print('Running for cooling_schedule: {}'.format(schedule))

    for markov_length in MARKOV_LENGTHS:
        print('Markov length: {}'.format(markov_length))

        for i in range(ITERATIONS+1):

            # Progression bar
            #if i%5 == 0 or i == ITERATIONS:
            printProgressBar(i, ITERATIONS, prefix = 'Progress:', suffix = 'Complete', length = 50)

            # SA
            starting_route = copy.deepcopy(initial_route)
            best_route = simulated_annealing(N, starting_route, schedule, markov_length, T_START)

            # Save results
            with open(file_name, 'a') as resultsFile:
                writer = csv.writer(resultsFile)
                writer.writerow([schedule, markov_length, T_START, best_route.get_length()])
        print()
