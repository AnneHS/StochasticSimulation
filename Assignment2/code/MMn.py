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
            with server.request(priority = self.joblength) as req:
                # Wait for server
                yield req
                waiting_time = env.now-arrival # waiting time
        else:
            with server.request() as req:
                # Wait for server
                yield req
                print(env.now, arrival)
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
            print(waiting_time)
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

def save_means(n, nr_of_batches, t, exp):
    '''
    For a given n and exp, for each of the unique rho values:
        Divide dataset into given number of batches based on arrival time
        For each of the batches, save rho + corresponding mean waiting time
    '''

    # Open temp results file
    temp_file = "../data/exp"+ str(exp)+ "_mm" + str(n)  + "_temp.csv"
    df = pd.read_csv(temp_file)
    df.columns=["n", "rho", "arrival", "waiting_time"]

    # For each unique rho value
    rhos = df.rho.unique().tolist()
    for rho in rhos:

        # Select part of temp df with n == given n && rho == current rho
        relevant_data = df.loc[df['n'] == n]
        relevant_data = relevant_data.loc[relevant_data['rho'] == rho]
        print(relevant_data)

        # Create file for current exp and n
        file_name = "../data/exp"+ str(exp)+ "_mm" + str(n)  + "_results.csv"
        if not os.path.isfile(file_name):
                open(file_name, 'x')

        # Create given nr of batches based on arrival time
        batch_size = round(t/nr_of_batches)
        for i in range(nr_of_batches):
            with open(file_name, 'a') as resultsFile:

                # Save results per batch:rho, mean waiting time
                writer = csv.writer(resultsFile)
                writer.writerow([rho,
                    relevant_data[(relevant_data["arrival"] >= i * batch_size) & (relevant_data["arrival"] < (i+1) * batch_size)]["waiting_time"].mean(),
                ])

    # Remove temp results (new temp for new rho)
    #os.remove(temp_file)
    '''
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
    '''
def main():
    #variables
    mu = 1 #capacity of each of n equal servers
    N = [1,2,4] #amount of servers
    LAMBDA = np.arange(0.1,1,0.05) #arrival rate into the whole system (lambda=rho, because mu=1)

    t = 100 #end timee

    #0 = normal(2.2); 1 = shortest job prio (2.3); 2 = long tail distribution (2.4); 3 = deterministic
    exp = 0
    if exp == 1:
        N = [1] #priority to shortest jobs only have to be exectuted for n = 1

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
        nr_of_batches=4 #TODO: NR OF BATCHES???????????????????????????
        save_means(n, nr_of_batches, t, exp)

if __name__ == "__main__":
    main()
