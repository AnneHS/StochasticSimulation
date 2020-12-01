import sys
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

experiments = [0]
server_count = [1, 2, 4]

for exp in experiments:
    means = []
    stdevs = []
    for n in server_count:

        fileName = '../data/exp' + str(exp) + '_mm' + str(n) + '_results.csv'
        df = pd.read_csv(fileName)
        df.columns = ['rho', 'waiting_time']
        rhos =df.rho.unique().tolist()

        means.append(df.groupby('rho')['waiting_time'].mean())
        stdevs.append(df.groupby('rho')['waiting_time'].std())

    # plot
    for i in range(len(server_count)):
        system_name = 'M/M/' + str(server_count[i])
        mean = means[i]
        stdev = stdevs[i]

        plt.plot(mean, label=system_name)
        plt.fill_between(rhos, mean+stdev,alpha=.1,)
        plt.yscale('log')
        plt.legend()
        plt.xlabel(r'$\rho$')
        plt.ylabel('Average waiting time')

    fig_name = '../plots/exp{}_means_std'.format(exp)
    plt.savefig(fig_name,dpi=300)
    plt.show()
