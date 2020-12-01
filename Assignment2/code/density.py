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
    #N = [1] #amount of servers

    #0 = normal(2.2); 1 = shortest job prio (2.3); 2 = long tail distribution (2.4); 3 = deterministic
    experiments = [0,1,2,3]
    #experiments=[0]
    for exp in experiments:
        if exp == 0:
            N = [1,2,4]
        else:
            N = [1]

        for n in N:
            file = "../data/exp"+ str(exp)+ "_mm" + str(n)  + "_results.csv"
            df = pd.read_csv(file)
            df.columns=["rho","waiting_time"]

            # For each unique rho value
            #rhos = df.rho.unique().tolist()
            rhos=[0.9]

            for rho in rhos:
                this_data = df.loc[df['rho'] == rho]
                #print(this_data["waiting_time"])
                #sns.distplot(waiting_time, norm_hist=True)#, hist=True, kde=False)
                sns.kdeplot(this_data["waiting_time"],shade=True)
    title = "density plot of waiting times for rho = 0.9"
    plt.title(title)
    plt.xlabel("waiting time")
    plt.ylabel("density")
    plt.xlim([0,None])
    plt.ylim([0,None])
    plt.legend(["M/M/1", "M/M/2","M/M/4","M/M/1, priority", "M/H/1","M/D/1"])
    plt.savefig("../plots/density_rho=0.9.jpg", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
