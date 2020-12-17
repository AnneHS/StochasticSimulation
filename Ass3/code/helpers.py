import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import random

from city import City, Route

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
    for c1 in cities:
        for c2 in cities:
            distance = math.sqrt(abs(c1.x - c2.x)**2 + abs(c1.y - c2.y)**2) # Eucledian distance
            adjacency_matrix[c1.id][c2.id] = distance
            adjacency_matrix[c1.id][c2.id] = distance
    return adjacency_matrix


def extract_optimal_route(N, route_data, adjacency_matrix):
    ''' Extract optimal route and corresponding length from input file'''
    # Extract optimal route
    opt_route = np.zeros((N))
    for i, line in enumerate(route_data):
        city = int(line)
        opt_route[i] = int(city-1)

    # Calculate length
    opt_route_length = 0
    for i in range(1, N):
        a = int(opt_route[i-1])
        b = int(opt_route[i])
        opt_route_length+=adjacency_matrix[a][b]

    return opt_route, opt_route_length

def load(problem):
    '''
    Load data for given TSP problem.
    Returns: number of cities (N), adjacency_matrix, optimal route,
    length optimal route, list of cities
    '''
    # Read problem data
    input_file_name = problem + '.tsp.txt'
    input_file = open('../input/'+ input_file_name).read().splitlines()
    N = int(str(input_file[3].strip().split(':')[1])) # Dimensions

    # Extract cities
    node_coord_section = input_file[6:-1]
    cities = extract_cities(node_coord_section)

    # Create adjacency matrix
    adjacency_matrix = create_adjacency_matrix(N, cities)

    # Read optimal route data
    opt_file_name = '{}.opt.tour.txt'.format(problem)
    opt_file = open('../input/'+ opt_file_name).read().splitlines()

    # Extract optimal route and length
    route_data = opt_file[5:56]
    opt_route, opt_route_length = extract_optimal_route(N, route_data,adjacency_matrix)

    return N, adjacency_matrix, opt_route, opt_route_length, cities

def create_initial_route(N, adjacency_matrix, cities):

    initial_route = Route(N, adjacency_matrix)
    shuffled = copy.deepcopy(cities)
    random.shuffle(shuffled)
    for city in shuffled:
        initial_route.add(city)

    return initial_route

def plot_route(cities, route, problem):
    '''
    Plots route
    - subplot 1: location of cities on 2d plane
    - subplot 2: subplot 1 with added route
    '''

    coordinates = route.get_coordinates()

    fig, ax = plt.subplots(2, sharex = True, sharey=True)
    max_y = max(coordinates[:,1])
    ax[0].set_ylim(top = max_y+20) # to make room for textbox
    ax[1].set_ylim(top = max_y+20) # to make room for textbox

    # Plot route
    # https://stackoverflow.com/questions/46506375/creating-graphics-for-euclidean-instances-of-tsp
    ax[0].set_title('Cities')
    ax[1].set_title('Tour')
    ax[0].scatter(coordinates[:,0], coordinates[:,1])
    ax[1].scatter(coordinates[:,0], coordinates[:,1])
    for i in range(route.N-1):
        start_pos = coordinates[i]
        end_pos = coordinates[i+1]
        ax[1].annotate("",
            xy=start_pos, xycoords='data',
            xytext=end_pos, textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))

    # Textbox
    textstr = "N nodes: {}\nTotal length: {}".format(route.N, np.round(route.get_length(),2))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14, # Textbox
        verticalalignment='top', bbox=props)

    savetitle = "../figures/route_" + problem + ".jpg"
    plt.savefig("../figures/route_eil51.jpg")
    plt.show()

def cooling_schedule(t_start, current_iteration, type):
    '''
    Used for SA: returns new temperature given the starting temperature,
    current SA iteration, alpha and the chosen cooling schedule.

    https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/

    # TODO:
    - alpha op basis van iteraties?
    '''
    if type == 'linear':
        alpha = t_start/ 10000
        t_current = t_start - alpha * current_iteration # multiplicative
        # TODO: additive

    elif type == 'exponential':
        alpha = 0.999995
        t_current = t_start * alpha**current_iteration # multiplicative
        # TODO: additive

    elif type == 'log':
        alpha = 5
        t_current =  t_start/(1+alpha*np.log(current_iteration+1)) #multiplicative
        # TODO: additiveIk

    elif type == 'quadratic':
        alpha = 0.001
        t_current = t_start/(1+ alpha * current_iteration**2) #multiplicative
        # TODO: additive

    return t_current

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
