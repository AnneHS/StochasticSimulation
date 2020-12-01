import sys
import simpy as sp
import random #maybe not necessary
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np

def main():
    exp = 1 #capacity of each of n equal servers
    N = [1,2,4] #amount of servers
    #0 = normal(2.2); 1 = shortest job prio (2.3); 2 = long tail distribution (2.4); 3 = deterministic
    exp = 0
    if exp == 1:
        N = [1] #priority to shortest jobs only have to be exectuted for n = 1

    for n in N:
        file = "../data/exp"+ str(exp)+ "_mm" + str(n)  + "_results.csv"
        df = pd.read_csv(file)
        df.columns=["rho","waiting_time"]

        # For each unique rho value
        rhos = df.rho.unique().tolist()
        rhos = [0.05, 0.5, 0.95] #if want to check one specific rho

        for rho in rhos:
            waiting_time = df.loc[df['rho'] == rho]
            sns.distplot(waiting_time)#, hist=True, kde=False)
            title = "density plot of waiting times for n = ", n, ", and $\rho$ = " + str(rho)
            plt.title(title)
            plt.xlabel("density")
            plt.ylabel("customers")
            plt.show()


if __name__ == "__main__":
    main()
