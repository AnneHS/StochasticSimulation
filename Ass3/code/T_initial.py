##simulated annealing with acceptance rate to determine the initial temperature
import numpy as np
import random
import copy
import math
import random
import matplotlib.pyplot as plt

from city import City, Route
from helpers import load, plot_route, cooling_schedule

T_MAX = np.round(np.arange(1, 500, 10), 1)                  # starting temperature
T_MIN = 0.1               # min temperature
COOLING_SCHEDULE = 'exponential'     # 'linear', 'exponential', 'log', 'quadratic'
MAX_ITERATION = 100           # currently not used --> now used for alpha
ALPHA = 0.0                # alpha used for cooling, True then alpha on basis of iterations

def simulated_annealing(N, initial_route, cooling_type, non_monotonic):
    '''
    Simulated annealing with 2-opt.
    '''
    t_current = T_START             # current temperature
    current_route = initial_route   # current route
    best_route = initial_route      # best route so far

    k = 0
    accepted = 0
    proposed = 0
    while k < MAX_ITERATION:
        for i in range(N-3):
            for j in range(i+2, N-1):
                new_route = current_route.two_opt(i, j)

                # Route acceptance
                length_difference = current_route.get_length() - new_route.get_length()
                if length_difference > 0:
                    current_route = new_route
                    best_route = new_route
                    accepted += 1
                elif random.uniform(0, 1) < math.exp(length_difference/t_current):
                    current_route = new_route

                # Cooling: adjust temperature
                #t_current = cooling_schedule(T_START, k, ALPHA, cooling_type)

                """if k%500 == 0:
                    print('iteration: {}'.format(k))
                    print('t: {}'.format(t_current))
                    print('best: {}\n'.format(best_route.get_length()))"""

                proposed += 1

                # SA stopping condition
                if t_current <= T_MIN:
                    rate = accepted/proposed
                    return (best_route, rate)

                k+=1

    rate = accepted/proposed
    return(best_route, rate)

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
runs = 10
acceptance_rate = []
for T_START in T_MAX:
    print(T_START)
    acceptance_rate_T = []
    for i in range(runs):
        route, acceptance = simulated_annealing(N, initial_route, COOLING_SCHEDULE, non_monotonic=False)
        acceptance_rate_T.append(acceptance)
    #print(acceptance_rate_T)
    acceptance_rate.append(np.mean(acceptance_rate_T))
print(acceptance_rate)

# Plot acceptance rate
plt.plot(T_MAX, acceptance_rate, color = 'blue')
plt.hlines(0.8, min(T_MAX), max(T_MAX), linestyles = 'dashed', colors = 'grey')
plt.xlabel("T_max")
plt.ylabel("acceptance rate (%)")
plt.title("empirically determining initial temperature")
plt.savefig("../figures/initial_T.jpg")
plt.show()
