class City(object):
    def __init__(self, id, N, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.distances = [0]*N

    def __str__(self):
        return str(self.id)

class Route(object):
    def __init__(self, N, adjacency_matrix):
        self.route=[]
        self.length=0
        self.adjacency_matrix = adjacency_matrix
        self.N = N

    def add(self, new_city):
        if len(self.route) >= 1:
            last_city = self.route[-1]
            self.length += self.adjacency_matrix[last_city.id][new_city.id]

        self.route+=[new_city]


    def get_length(self):
        return self.length

    def switch(self, i, j):
        '''
        Returns new route, switches city at index i+1 with city at index j+1
        OR
        Breaks link i-i+1 and j-j+1
        Creates new links i-j, i+1-j+1
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

    def return_copy(self):
        new_route = Route(self.adjacency_matrix)
        for city in self.route:
            new_route.add_city()

        return new_route

    def __repr__(self):
        return repr([str(city) for city in self.route])
