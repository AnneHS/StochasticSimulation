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
        df.columns = ['rho', 'waiting_time'] #, 'length_queue']
        rhos =df.rho.unique().tolist()

        #= [0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]

        means.append(df.groupby('rho')['waiting_time'].mean())
        stdevs.append(df.groupby('rho')['waiting_time'].std())

    for i in range(len(server_count)):
        system_name = 'M/M/' + str(server_count[i])
        mean = means[i]
        stdev = stdevs[i]
        plt.plot(mean, label=system_name)
        plt.fill_between(rhos, mean+stdev,alpha=.1,)
        #plt.fill_between(rhos, means-stdevs,means+stdevs,alpha=.1,)
        plt.legend()
        plt.xlabel('Rho')
        plt.ylabel('Average waiting time')
    plt.show()
'''
print('jo')
means=[]
stdevs=[]
for rho in rhos:
    print(rho)
    mean = df[(df['rho']==rho)]['waiting_time'].mean()
    stdev = df[(df['rho']==rho)]['waiting_time'].std()

    means.append(mean)
    stdevs.append(stdevs)

print('jojo')
#means = np.asarray(means)
#stdevs = np.asarray(stdevs)
plt.plot(rhos, means)
plt.fill_between(rhos, means-stdevs,means+stdevs,alpha=.1)
plt.xlabel('rho')
plt.ylabel('waiting time')
plt.show()
'''
