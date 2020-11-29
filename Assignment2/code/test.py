import sys
import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd

in_queue=[]

class Customer():
    def __init__(self, env, name, l):
        self.env = env
        self.name = name
        self.joblength = l

    def request(self, env, server, mu):
        arrival = env.now
        in_queue.append(self.name)
        print('%7.4f %s: Here I am' % (arrival, self.name))

        with server.request() as req:

            # Wait for server
            yield req
            waiting_time = env.now-arrival # waiting time

            # We got to the server
            in_queue.remove(self.name)
            print('%7.4f %s: Waited %6.3f' % (env.now, self.name, waiting_time))

            # Time until departure
            tib = random.expovariate(mu) #  time until departure
            yield env.timeout(tib) # wait until server is finished
            print('%7.4f %s: Finished' % (env.now, self.name))

            # File for temp results
            file_name = "../data/mm" + str(mu)  + "_temp.csv"
            if not os.path.isfile(file_name):
                    open(file_name, 'x')
            # Save results
            with open(file_name, 'a') as resultsFile:
                writer = csv.writer(resultsFile)
                writer.writerow([arrival, waiting_time, len(in_queue)])


def source(env, server, l, mu):
    """Source generates customers randomly"""

    i = 1 #customer counter

    while True:
        customer = Customer(env, "Customer%02d"%(i), l)
        i += 1
        env.process(customer.request(env, server, mu)) #customer arrives
        t = random.expovariate(l) #arrival time of the next customer
        yield env.timeout(t) #timeout until arrival time of next customer


def  save_means(mu, nr_of_batches, t):

    # Open temp results
    results_file = "../data/mm" + str(mu)  + "_temp.csv"
    df = pd.read_csv(results_file)
    df.columns=["arrival", "waiting_time", "len_queue"]

    # Results file
    file_name = "../data/mm" + str(mu)  + "_results.csv"
    if not os.path.isfile(file_name):
            open(file_name, 'x')

    # Save results per batch: mean waiting time, mean length queue
    batch_size = round(t/nr_of_batches)
    for i in range(nr_of_batches):

        print(df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)])
        print()

        with open(file_name, 'a') as resultsFile:
            writer = csv.writer(resultsFile)
            writer.writerow([
                df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)]["waiting_time"].mean(),
                df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)]["len_queue"].mean()
            ])


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
    server = sp.Resource(env, capacity=n)
    env.process(source(env, server, l, mu))
    env.run(until = t)

    # Save results per batch
    nr_of_batches=4
    save_means(mu, nr_of_batches, t)

if __name__ == "__main__":
    main()
