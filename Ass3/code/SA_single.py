import numpy as np
import random
import copy
import math
import random
import os
import csv

from city import City, Route
from helpers import load, plot_route, cooling_schedule, create_initial_route

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
T_START = 5                   # starting temperature
T_MIN = 0.0000001               # min temperature
COOLING_SCHEDULE = 'exponential'     # 'linear', 'exponential', 'log', 'quadratic'
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

def simulated_annealing(N, initial_route, cooling_type, t_start):
    '''
    Simulated annealing with 2-opt.
    '''
    t_current = T_START             # current temperature
    current_route = initial_route   # current route
    best_route = initial_route      # best route so far

    route_lengths = [initial_route.get_length()]

    k=0
    while t_current > T_MIN and k < MAX_ITERATION:
        for i in range(N-3):
            for j in range(i+2, N-1):
                new_route = current_route.two_opt(i, j)

                # Route acceptance
                length_difference = current_route.get_length() - new_route.get_length()
                if length_difference > 0:
                    current_route = new_route
                    if new_route.get_length() < best_route.get_length():
                        best_route = new_route
                elif random.uniform(0, 1) < math.exp(length_difference/t_current):
                    current_route = new_route

                route_lengths+=[current_route.get_length()]

                # Cooling: adjust temperature
                t_current = cooling_schedule(T_START, k, cooling_type)
                print("Lenght: {}".format(best_route.get_length()))
                '''
                if k%10== 0:
                    print('iteration: {}'.format(k))
                    print('t: {}'.format(t_current))
                    print('best: {}\n'.format(best_route.get_length()))
                '''

                # SA stopping condition
                if t_current <= T_MIN:
                    return best_route, route_lengths

                k+=1

    return best_route, route_lengths

if __name__ == '__main__':

    problem = 'a280'            # problem type 'eil51'
    schedule = 'linear'          #'linear', 'exponential', 'log', 'quadratic'

    # Params
    ITERATIONS = 10                               # SA iterations
    T_MIN = 0.0000001
    T_START = 300

    # Load problem
    N, adjacency_matrix, opt_path, opt_path_len, cities  = load(problem)
    print(adjacency_matrix)
    print('Problem: {} \nN: {} \nOptimal length: {}\n'.format(problem, N, opt_path_len))

    # Create random initial route
    initial_route = create_initial_route(N, adjacency_matrix, cities)

    # Open/create results file
    file_name = '../results/single_run/{}_{}.csv'.format(problem, schedule)
    if not os.path.isfile(file_name):
            open(file_name, 'x')

    for i in range(ITERATIONS):
        starting_route = copy.deepcopy(initial_route)
        best_route, route_lengths = simulated_annealing(N, starting_route, schedule, T_START)
        # Save results
        with open(file_name, 'a') as resultsFile:
            writer = csv.writer(resultsFile)
            writer.writerow(route_lengths)

    # Plot route on 2D plane
    #plot_route(cities, route)
