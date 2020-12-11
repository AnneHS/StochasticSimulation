import sys
import numpy as np
import math

from city import City

def extract_cities(node_coord_section):
    ''' Extract cities and coordinates from input file'''
    cities=[]
    for i, line in enumerate(node_coord_section):
        splitted_line = line.split()

        x = int(splitted_line[1])
        y = int(splitted_line[2])

        city = City(i, x, y)
        cities.append(city)

    return cities

def create_adjacency_matrix(N, cities):
    ''' Creates adjacency matrix'''
    adjacency_matrix = np.zeros((N, N))
    for city1 in cities:
        for city2 in cities:
            distance = math.sqrt(abs(city1.x - city2.x)**2 + abs(city1.y - city2.y)**2) # Eucledian distance
            adjacency_matrix[city1.id][city2.id] = distance
            adjacency_matrix[city1.id][city2.id] = distance
    return adjacency_matrix

def extract_optimal_route(N, route_data, adjacency_matrix):
    ''' Extract optimal route and corresponding length'''

    # Extract optimal route
    opt_path = np.zeros((N))
    for i, line in enumerate(path_data):
        city = int(line)
        opt_path[i] = int(city-1)

    # Calculate length
    path_length = 0
    for i in range(1, N):
        a = int(opt_path[i-1])
        b = int(opt_path[i])
        path_length+=adjacency_matrix[a][b]

def load(problem):
    '''
    '''
    
    # Read problem data
    input_file_name = problem + '.tsp.txt'
    input_file = open('../input/'+ input_file_name).read().splitlines()
    N = int(str(input_file[3].strip().split(':')[1])) # Dimensions

    # Extract cities
    node_coord_section = input_file[6:-1]
    cities = extraxt_cities(node_coord_section)

    # Create adjacency matrix
    adjacency_matrix = create_adjacency_matrix(N, cities)

    # Read optimal route data
    opt_file_name = '{}.opt.tour.txt'.format(problem)
    opt_file = open('../input/'+ opt_file_name).read().splitlines()
    route_data = opt_file[5:56]

    # Extract optimal route and length
    opt_route, opt_route_length = get_optimal_route(N, route_data,adjacency_matrix)


    return N, adjacency_matrix, opt_route, route_length, cities
