import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np

'''
For cooling schedule comparison x=iterations, y=length
'''
problem = 'a280'
cooling_schedules = ['linear'] #, 'exponential', 'log', 'quadratic']

for schedule in cooling_schedules:
    file_name = '../results/single_run/{}_{}.csv'.format(problem, schedule)
    df = pd.read_csv(file_name)

    means = df.mean(axis=0).to_numpy()
    stdev = df.std(axis=0).to_numpy()
    iterations = np.linspace(0, 6001, 6002) # 6002 = length means

    plt.plot(iterations, means)
    plt.fill_between(iterations, means-stdev, means+stdev,alpha=.1,)
    plt.xlabel('iteration')
    plt.ylabel('length')
    plt.show()


def plot_markov():
    problem = 'a280'
    cooling_schedules = ['linear']
    for schedule in cooling_schedules:
        file_name = '../results/{}_{}.csv'.format(problem, schedule)
        df = pd.read_csv(file_name)
        df.columns = ['schedule', 'markov', 'iterations', 'best_route_length']
        print(df)

plot_markov()
