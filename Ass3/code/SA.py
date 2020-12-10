import numpy as np
from load import load
import random
import copy

from city import City, Route

def two_opt(N, initial_route):
    '''
    Switches 2 cities in route until no improvement.
    '''
    
    best_route = initial_route
    improved = True
    while improved:
        improved = False
        for i in range(N-3):
            for j in range(i+2, N-1):
                print(best_route.get_length())
                new_route = best_route.switch(i, j)

                if new_route.get_length() <= best_route.get_length():
                    best_route = new_route
                    improved = True


problem = 'eil51'## .tsp.txt'
N, adjacency_matrix, opt_path, opt_path_len, cities  = load(problem)
print('Problem: {} \nN: {} \nOptimal length: {}\n'.format(problem, N, opt_path_len))

# random initial route
initial_route = Route(N, adjacency_matrix)
shuffled = copy.deepcopy(cities)
random.shuffle(shuffled)
for city in shuffled:
    initial_route.add(city)

two_opt(N, initial_route)
