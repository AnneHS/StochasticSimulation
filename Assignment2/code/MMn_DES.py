## M/M/n DES

import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt

def source(env, l, server, mu):
    """Source generates customers randomly"""
    i = 1 #customer counter
    while True:
        c = customer(env, 'Customer%02d' % i, server, mu) # initiate customer
        i += 1
        env.process(c) #customer arrives
        t = random.expovariate(l) #arrival time of the next customer
        yield env.timeout(t) #timeout until arrival time of next customer

def customer(env, name, server,mu):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with server.request() as req:
        yield req #wait for server
        wait = env.now - arrive #calculate waiting time

        # We got to the server
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

        tib = random.expovariate(mu) # time until departure
        yield env.timeout(tib) #wait until server is finished
        print('%7.4f %s: Finished' % (env.now, name))

def main():
    #variables
    mu = 1 #capacity of each of n equal servers
    n = 1 #amount of servers
    rho = 0.9 #system load
    l = rho*mu*(1/n) #arrival rate into the whole system (lambda)
    t = 20 #end timee
    RANDOM_SEED = 2
    if rho >= 1: #rho cant be larger than 1, raise error, to ensure queue is stable
        raise Exception("rho can't be 1 or larger, rho = ", rho)

    # Setup and start the simulation
    print('Start of FIFO M/M/n, lambda = ', l, ", mu = ", mu, ", n = ", n, "rho = ", rho )
    random.seed(RANDOM_SEED)
    env = sp.Environment()

    # Start processes and run
    server = sp.Resource(env, capacity=n) #keeps track if and how many servers are occupied
    env.process(source(env, l, server, mu))
    env.run(until = t)

if __name__ == "__main__":
    main()
