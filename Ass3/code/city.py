import numpy as np

class City(object):
    '''
    TSP city contains ID and coordinates.
    '''
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.id)



class Route(object):
    '''
    TSP route, to save route (list of cities in specific order), length of
    route and adjacency_matrix for TSP problem.
    '''
    def __init__(self, N, adjacency_matrix):
        self.route=[]
        self.length=0
        self.adjacency_matrix = adjacency_matrix
        self.N = N

    def add(self, new_city):
        '''Adds new city to route and updates length '''
        if len(self.route) >= 1:
            last_city = self.route[-1]
            self.length += self.adjacency_matrix[last_city.id][new_city.id]

        self.route+=[new_city]

    def two_opt(self, i, j):
        '''
        Returns new route, created from self.route by breaking two non-adjacent
        edges (links between cities), and then reconnecting these 4 cities.
        - Breaks [i]->[i+1] and [j]->[j+1]
        - Connects [i]->[j] and [i+1]->[j+1]
        '''
        new_route = Route(self.N, self.adjacency_matrix)
        for k in range(self.N):
            if k < i+1:
                new_route.add(self.route[k])
            elif k == (i+1):
                new_route.add(self.route[j])
            elif k == j:
                new_route.add(self.route[i+1])
            else:
                new_route.add(self.route[k])

        return new_route

    def get_coordinates(self):
        '''
        Returns list of city coordinates for route, in corresponding order.
        Used for plotting.
        '''
        coordinates = []
        for city in self.route:
            coordinates.append([city.x, city.y])

        return np.array(coordinates)

    def get_length(self):
        return self.length

    def __repr__(self):
        return repr([str(city) for city in self.route])
