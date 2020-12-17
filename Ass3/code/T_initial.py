##simulated annealing with acceptance rate to determine the initial temperature
import numpy as np
import random
import copy
import math
import random
import matplotlib.pyplot as plt

from city import City, Route
from helpers import load, plot_route, cooling_schedule

T_MAX = np.round(np.arange(10, 301, 10), 1)                  # starting temperature
COOLING_SCHEDULE = 'linear' # 'linear', 'exponential', 'log', 'quadratic'
MAX_ITERATION = 100000           # currently not used --> now used for alpha
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
                    accepted += 1

                # Cooling: adjust temperature
                t_current = T_START #cooling_schedule(T_START, k, ALPHA, cooling_type)

                proposed += 1
                k+=1

    rate = accepted/proposed
    return(best_route, rate)

problems = ['pcb442']#, 'pcb442']
for problem in problems:
    if problem == 'eil51':
        T_MAX = np.round(np.arange(5, 201, 5), 1)
    elif problem == 'a280':
        T_MAX = np.round(np.arange(10, 501, 10), 1)

    # Load problem
    N, adjacency_matrix, opt_path, opt_path_len, cities  = load(problem)
    print('Problem: {} \nN: {} \nOptimal length: {}\n'.format(problem, N, opt_path_len))

    # Create random initial route
    initial_route = Route(N, adjacency_matrix)
    shuffled = copy.deepcopy(cities)
    random.shuffle(shuffled)
    for city in shuffled:
        initial_route.add(city)

    runs = 1
    # Start SA
    acceptance_rate = []
    for T_START in T_MAX:
        acceptance_rate_T = []
        for i in range(runs):
            route, acceptance = simulated_annealing(N, initial_route, COOLING_SCHEDULE, non_monotonic=False)
            acceptance_rate_T.append(acceptance)
        print(T_START, np.mean(acceptance_rate_T))
        acceptance_rate.append(np.mean(acceptance_rate_T))

    # Plot acceptance rate
    plt.plot(T_MAX, acceptance_rate, label = problem)
    plt.hlines(0.8, min(T_MAX), max(T_MAX), linestyles = 'dashed', colors = 'grey')
    plt.xlabel("$T_{start}$")
    plt.ylabel("acceptance rate (%)")
    title = "problem: " + problem
    plt.title(title)
    savefig = "../figures/T_START_" + problem + ".jpg"
    plt.savefig(savefig)
    plt.show()
