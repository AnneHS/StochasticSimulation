import sys
import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

class Customer():
    def __init__(self, env, name, mu, n, rho, exp):
        self.env = env
        self.name = name
        if exp == 2: # if longtaildistribution
            p = np.random.normal(0,1)
            if p > 0.75:
                job = random.expovariate(mu*5) #mu = 5 for 25%
            else:
                job = random.expovariate(mu) #mu = 1 for 75%
        elif exp == 3: #deterministic
            job = mu
        else:
            job = random.expovariate(mu) #if Markov distribution
        self.joblength = job
        self.n = n
        self.rho = rho
        self.exp = exp

    def request(self, env, server):
        arrival = env.now

        if self.exp == 1:
            with server.request(priority = self.joblength):
                # Wait for server
                yield req
                waiting_time = env.now-arrival # waiting time
        else:
            with server.request() as req:
                # Wait for server
                yield req
                waiting_time = env.now-arrival # waiting time

        # Time until departure
        yield env.timeout(self.joblength) # wait until server is finished

        # File for temp results
        file_name = "../data/exp"+ str(self.exp)+ "_mm" + str(self.n)  + "_temp.csv"

        if not os.path.isfile(file_name):
                open(file_name, 'x')
        # Save results
        with open(file_name, 'a') as resultsFile:
            writer = csv.writer(resultsFile)
            writer.writerow([self.n, self.rho, arrival, waiting_time])

def source(env, server, l, mu, n , rho, exp):
    """Source generates customers randomly"""
    i = 1 #customer counter
    while True:
        customer = Customer(env, i, mu, n, rho, exp)
        i += 1
        env.process(customer.request(env, server)) #customer arrives
        t = random.expovariate(l) #arrival time of the next customer
        yield env.timeout(t) #timeout until arrival time of next customer

def  save_means(n, nr_of_batches, t, exp):
    # Open temp results
    temp_results = "../data/exp"+ str(self.exp)+ "_mm" + str(self.n)  + "_temp.csv"
    df = pd.read_csv(temp_results)
    df.columns=["n", "rho", "arrival", "waiting_time"]

    # Results file
    file_name = "../data/exp"+ str(self.exp)+ "_mm" + str(self.n)  + "_results.csv"
    if not os.path.isfile(file_name):
            open(file_name, 'x')

    # Save results per batch: mean waiting time, mean length queue
    batch_size = round(t/nr_of_batches)
    for i in range(nr_of_batches):
        #print(df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)])

        with open(file_name, 'a') as resultsFile:
            writer = csv.writer(resultsFile)
            writer.writerow([
                df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)]["waiting_time"].mean(),
                #df[(df["arrival"] >= i * batch_size) & (df["arrival"] < (i+1) * batch_size)]["in_system"].mean()
            ])

    # Remove temp results (new temp for new rho)
    os.remove(temp_results)

def main():
    #variables
    mu = 1 #capacity of each of n equal servers
    N = [1,2,4] #amount of servers
    LAMBDA = np.arange(0.1,1,0.05) #arrival rate into the whole system (lambda=rho, because mu=1)

    t = 100000 #end timee

    #0 = normal(2.2); 1 = shortest job prio (2.3); 2 = long tail distribution (2.4); 3 = deterministic
    exp = 0
    if exp == 1:
        N = 1 #priority to shortest jobs only have to be exectuted for n = 1

    # Setup and start the simulation
    for n in N:
        for l in LAMBDA:
            #just for a nice print during the simulations
            if exp == 0:
                text = "start of FIFO M/M/"
            elif exp == 1:
                text = "start of shortest job priority M/M/"
            elif exp == 2:
                text = "start of longtaildistribution M/D/"
            elif exp == 3:
                text = "start of M/D/"
            rho = (l*n)/(n*mu) #(lambda*n) to ensure rho is same across all n, then lambda has to be higher
            print(text, n , ', lambda = ', l, ", mu = ", mu, "rho = ", rho,", exp = ", exp )
            env = sp.Environment()
            server = sp.PriorityResource(env, capacity=n)
            env.process(source(env, server, l*n , mu, n , rho, exp))
            env.run(until = t)

    # Save results per batch
    for n in N:
        nr_of_batches=4
        save_means(n, nr_of_batches, t, exp)

if __name__ == "__main__":
    main()
