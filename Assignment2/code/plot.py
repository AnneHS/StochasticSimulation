import sys
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

experiments = [0, 2, 3]
server_count = [1]

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
    #print(stdevs)

    # plot
    for i in range(len(server_count)):
        if exp == 0:
            system_name = 'M/M/' + str(server_count[i]) + ' FIFO'
        elif exp == 1:
            system_name = 'M/M/' + str(server_count[i]) + ' Priority'
        elif exp == 2:
            system_name = 'M/H/' + str(server_count[i])
        elif exp == 3:

            system_name = 'M/D/' + str(server_count[i])

        mean = means[i]
        stdev = stdevs[i]

        print(server_count[i])
        print(mean)
        print(stdev)
        print()

        plt.plot(mean, label=system_name)
        plt.fill_between(rhos, mean-stdev, mean+stdev,alpha=.1,)
        plt.yscale('log')
        plt.legend()
        plt.xlabel(r'$\rho$')
        plt.ylabel('Average waiting time')
        #plt.show()

fig_name = '../plots/exp0123_means_std' #.format(exp)
plt.savefig(fig_name,dpi=300)
plt.show()
