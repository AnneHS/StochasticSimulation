import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np

'''
For cooling schedule comparison x=iterations, y=length
'''
problem = 'eil51'
cooling_schedules = ['linear', 'exponential', 'log', 'quadratic']

for schedule in cooling_schedules:
    file_name = '../results/single_run/{}_{}.csv'.format(problem, schedule)

    df = pd.read_csv(file_name).to_numpy() #read in data
    n = len(df)
    print(n)
    means = np.mean(df,axis=0) #means
    df = df.T

    iterations = np.arange(1, len(means)+1, 1) #x-axis

    #calculate cofidence interval:
    l = 1.96 #for a CI of 95%
    numerator = []
    for i in range(len(means)):
        numerator.append(sum((df[i]-means[i])**2))
    sample_variance = np.array(numerator)/(n-1)
    a = (l*sample_variance)/np.sqrt(n)

    plt.plot(iterations, means, label = schedule)
    plt.fill_between(iterations, means-a, means+a, alpha=.2,)

plt.xlabel('iteration')
plt.ylabel('length')
plt.legend()
title = "problem: " + problem
plt.title(title)
savefig = "../figures/coolingSchedules_" + problem + ".jpg"
plt.savefig(savefig, dpi=300)
plt.show()

"""
def plot_markov():
    problem = 'a280'
    cooling_schedules = ['linear']
    for schedule in cooling_schedules:
        file_name = '../results/{}_{}.csv'.format(problem, schedule)
        df = pd.read_csv(file_name)
        df.columns = ['schedule', 'markov', 'iterations', 'best_route_length']
        print(df)

plot_markov()
"""
