import sys
import numpy as np
import math

from city import City

def load(problem):

    # read input
    input_file_name = problem + '.tsp.txt'
    input_file = open('../input/'+ input_file_name).read().splitlines()
    N = int(str(input_file[3].strip().split(':')[1])) # Dimensions

    # get city coordinates
    cities=[]
    node_coord_section = input_file[6:-1]
    for i, line in enumerate(node_coord_section):
        splitted_line = line.split()

        x = int(splitted_line[1])
        y = int(splitted_line[2])

        city = City(i, N, x, y)
        cities.append(city)

    # adjacency matrix 
    adjacency_matrix = np.zeros((N, N))
    for city1 in cities:
        for city2 in cities:
            distance = math.sqrt(abs(city1.x - city2.x)**2 + abs(city1.y - city2.y)**2)
            adjacency_matrix[city1.id][city2.id] = adjacency_matrix[city1.id][city2.id] = distance

    # optimal path data
    opt_file_name = '{}.opt.tour.txt'.format(problem)
    opt_file = open('../input/'+ opt_file_name).read().splitlines()
    path_data = opt_file[5:56]

    # TODO: Route & City

    # get optimal path
    opt_path = np.zeros((N))
    for i, line in enumerate(path_data):
        city = int(line)
        opt_path[i] = int(city-1)

    # get length optimal path
    path_length = 0
    for i in range(1, N):
        a = int(opt_path[i-1])
        b = int(opt_path[i])
        path_length+=adjacency_matrix[a][b]

    return N, adjacency_matrix, opt_path, path_length, cities
