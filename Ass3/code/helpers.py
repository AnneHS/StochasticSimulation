import sys
import numpy as np
import math
import matplotlib.pyplot as plt

from city import City

def load(problem):

    # read city data
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

    # read optimal path data
    opt_file_name = '{}.opt.tour.txt'.format(problem)
    opt_file = open('../input/'+ opt_file_name).read().splitlines()
    path_data = opt_file[5:56]

    # get optimal path
    opt_path = np.zeros((N))
    for i, line in enumerate(path_data):
        city = int(line)
        opt_path[i] = int(city-1)

    path_length = 0
    for i in range(1, N):
        a = int(opt_path[i-1])
        b = int(opt_path[i])
        path_length+=adjacency_matrix[a][b]

    return N, adjacency_matrix, opt_path, path_length, cities

def plot_route(cities, route):

    coordinates = route.get_coordinates()
    min_y = min(coordinates[:,1])
    max_y = max(coordinates[:,1])

    fig, ax = plt.subplots(2, sharex = True, sharey=True)
    ax[0].set_ylim(top = max_y+20) # to make room for textbox
    ax[1].set_ylim(top = max_y+20) # to make room for textbox

    # plot tour
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
    # textbox
    textstr = "N nodes: {}\nTotal length: {}".format(route.N, route.get_length())
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14, # Textbox
        verticalalignment='top', bbox=props)

    plt.show()

def cooling_schedule(t_start, iteration, alpha, type):
    '''
    https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/

    # TODO:  
    '''
    if type == 'linear':
        t_current = t_start - alpha * iteration # multiplicative
        # TODO: additive

    elif type == 'exponential':
        t_current = t_start * alpha**iterations # multiplicative
        # TODO: additive

    elif type == 'log':
        t_current =  T_START/(1+ALPHA*log(iteration+1)) #multiplicative
        # TODO: additive

    elif type == 'quardratic':
        t_current = T_START/(1+ alpha * iterations**2) #multiplicative
        # TODO: additive

    return t_current
