import numpy as np
import random
import copy
import math
import random
import matplotlib.pyplot as plt

from city import City, Route
from helpers import load, plot_route, cooling_schedule

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

T_START = 70                   # starting temperature
T_MIN = 0.00001               # min temperature
COOLING_SCHEDULE = 'exponential'     # 'linear', 'exponential', 'log', 'quadratic'
MAX_ITERATION = 2000000           # currently not used --> now used for alpha
# alpha used for cooling, True then alpha on basis of iterations

def simulated_annealing(N, initial_route, cooling_type, non_monotonic):
    '''
    Simulated annealing with 2-opt.
    '''
    t_current = T_START             # current temperature
    current_route = initial_route   # current route
    best_route = initial_route      # best route so far

    k=0
    while t_current > T_MIN and k < MAX_ITERATION:
        for i in range(N-3):
            for j in range(i+2, N-1):
                new_route = current_route.two_opt(i, j)

                # Route acceptance
                length_difference = current_route.get_length() - new_route.get_length()
                if length_difference > 0:
                    current_route = new_route
                    best_route = new_route
                elif random.uniform(0, 1) < math.exp(length_difference/t_current):
                    current_route = new_route

                # Cooling: adjust temperature
                t_current = cooling_schedule(T_START, k, cooling_type,T_MIN)

                if k%500 == 0:
                    print('iteration: {}'.format(k))
                    print('t: {}'.format(t_current))
                    print('best: {}\n'.format(best_route.get_length()))

                # SA stopping condition
                if t_current <= T_MIN:
                    return best_route

                k+=1

    return best_route

# Load problem
problem = 'eil51'
N, adjacency_matrix, opt_path, opt_path_len, cities  = load(problem)
print('Problem: {} \nN: {} \nOptimal length: {}\n'.format(problem, N, opt_path_len))

# Create random initial route
initial_route = Route(N, adjacency_matrix)
shuffled = copy.deepcopy(cities)
random.shuffle(shuffled)
for city in shuffled:
    initial_route.add(city)

# Start SA
route = simulated_annealing(N, initial_route, COOLING_SCHEDULE, non_monotonic=False)

# Plot route on 2D plane
plot = plot_route(cities, route, problem)
