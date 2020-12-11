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
                #print(best_route.get_length())
                new_route = best_route.switch(i, j)

                if new_route.get_length() <= best_route.get_length():
                    best_route = new_route
                    improved = True
    return best_route
