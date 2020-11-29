import sys
import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd

in_system = []

class Customer():
    inSystem = 0
    def __init__(self, env, name, mu):
        self.env = env
        self.name = name
        self.joblength = random.expovariate(mu)

    def request(self, env, server, mu, n):
        arrival = env.now
        in_system.append(self.name)

        #print('%7.4f %s: Here I am' % (arrival, self.name))
        #print("customers in system", len(in_system))
        with server.request(priority=self.joblength) as req:
            # Wait for server
            yield req
            waiting_time = env.now-arrival # waiting time

            # We got to the server
            #print('%7.4f %s: Waited %6.3f' % (env.now, self.name, waiting_time))

            # Time until departure
            #tib = random.expovariate(mu) #  time until departure
            yield env.timeout(self.joblength) # wait until server is finished
            in_system.remove(self.name)
            #print("customers in system", len(in_system))
            #print('%7.4f %s: Finished' % (env.now, self.name))

            sojourn_time = waiting_time + self.joblength #total time in system

            # File for temp results
            file_name = "../data/mm1_shortestJob_test.csv"
            if not os.path.isfile(file_name):
                    open(file_name, 'x')
            # Save results
            with open(file_name, 'a') as resultsFile:
                writer = csv.writer(resultsFile)
                #customer | customers in system | arrival time | waiting time | service time | sojourn time
                writer.writerow([self.name, len(in_system), arrival, waiting_time, self.joblength, sojourn_time])


def source(env, server, l, mu, n):
    """Source generates customers randomly"""
    i = 1 #customer counter
    while True:
        customer = Customer(env, i, mu)
        i += 1
        env.process(customer.request(env, server, mu, n)) #customer arrives
        t = random.expovariate(l) #arrival time of the next customer
        yield env.timeout(t) #timeout until arrival time of next customer

def main():
    #variables
    mu = 1 #capacity of each of n equal servers
    n = 1 #amount of servers
    rho = 0.9 #system load
    l = rho*mu*(1/n) #arrival rate into the whole system (lambda)
    t = 20000 #end timee
    RANDOM_SEED = 2

    if rho >= 1: #rho cant be larger than 1, raise error, to ensure queue is stable
        raise Exception("rho can't be 1 or larger, rho = ", rho)

    # Setup and start the simulation
    print('Start of FIFO M/M/n, lambda = ', l, ", mu = ", mu, ", n = ", n, "rho = ", rho )
    random.seed(RANDOM_SEED)
    env = sp.Environment()
    server = sp.PriorityResource(env, capacity=n)
    env.process(source(env, server, l, mu, n))
    env.run(until = t)

if __name__ == "__main__":
    main()
