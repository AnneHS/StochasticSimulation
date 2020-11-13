##compare a-values of fixed interval with each other and fixed samples with each other
import numpy as np
import csv
import os
import math
import matplotlib.pyplot as plt

def main():
    #set experiment type and method over which confidence interval is calculated
    type_experiment = "Fixeds" #"Fixeds" #"Fixedi"
    sampling_method = ["random_sampling", "LHS_sampling", "orthogonal_sampling"]

    a = [] #empty list to store the a values

    for method in sampling_method:
        #file with results
        file_name = "../results/"+ "CI_" + type_experiment + '_' + method + ".csv"

        #read in results
        results = []
        with open(file_name, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if len(row) > 0:
                    results.append(row)

        results = np.asarray(results) #for better handling
        results = results.astype(np.float)

        #extract the a-values per method
        a_vals = results[:,-1]
        a.append(a_vals)

    #plot the confidence intervals and the sample mean
    if type_experiment == "Fixedi":
        x = np.unique(results[:,1])
        xlab = "samples"
        fixed = "iterations"
    elif type_experiment == "Fixeds":
        x = np.unique(results[:,0])
        xlab = "iterations"
        fixed = "samples"
    plt.plot(x, a[0], 'c', label = 'random sampling')
    plt.plot(x, a[1], 'm', label = 'latin hypercube sampling')
    plt.plot(x, a[2], 'y', label = 'orthogonal sampling')
    plt.xlabel(xlab)
    plt.ylabel("a")
    plt.xlim(min(x),max(x))
    plt.legend()
    title = "a-values for fixed " + fixed
    plt.title(title)
    save_title = "../results/" + "aValues_" + type_experiment + ".png"
    plt.savefig(save_title,dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
