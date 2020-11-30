import sys
import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np

waiting = []

class Customer():
    def __init__(self, env, name, mu):
        self.env = env
        self.name = name
        self.joblength = random.expovariate(1/mu)

    def request(self, env, server, mu):
        arrival = env.now

        with server.request() as req:
            # Wait for server
            yield req
            waiting_time = env.now-arrival # waiting time

            # Time until departure
            yield env.timeout(self.joblength) # wait until server is finished
            waiting.append(waiting_time)

def source(env, server, l, mu):
    """Source generates customers randomly"""
    i = 1 #customer counter
    while True:
        customer = Customer(env, i, mu)
        i += 1
        env.process(customer.request(env, server, mu)) #customer arrives
        t = random.expovariate(l) #arrival time of the next customer
        yield env.timeout(t) #timeout until arrival time of next customer

def main():
    #variables
    runs = 500
    mu = 1 #capacity of each of n equal servers
    n = 1 #amount of servers
    l = 0.9 #arrival rate into the whole system (lambda)
    rho = (l*n)/(n*mu) #(lambda * n) to ensure rho is same across all n, then lambda has to be higher
    t = 1000 #end timee

    if rho >= 1: #rho cant be larger than 1, raise error, to ensure queue is stable
        raise Exception("rho can't be 1 or larger, rho = ", rho)

    # Setup and start the simulation
    print('Start of FIFO M/M/', n , ', lambda = ', l, ", mu = ", mu, "rho = ", rho )
    Wtimes = []
    for run in range(runs):
        print(len(np.unique(waiting)))
        waiting.clear()
        env = sp.Environment()
        server = sp.Resource(env, capacity=n)
        env.process(source(env, server, l*n , mu))
        env.run(until = t)
        print(run)
        Wtimes.append(waiting)

    #print(len(Wtimes), len(waiting))
    Wtimes = pd.DataFrame(Wtimes)
    Wtimes = Wtimes.transpose()
    print(Wtimes)
    Wtimes_mean = Wtimes.mean(axis=0)

    #print(np.unique(waiting_time))
    sns.distplot(Wtimes_mean)#, hist=True, kde=False)
    title = "density plot of waiting times for n = 1, rho = " + str(rho)
    plt.title(title)
    plt.xlabel("waiting time")
    plt.ylabel("customers")
    plt.show()


if __name__ == "__main__":
    main()
