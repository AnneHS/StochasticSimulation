import numpy as np
import csv
import os
import math
import matplotlib.pyplot as plt

def main():
    #set experiment type and method over which confidence interval is calculated
    type_experiment = "Fixeds" #"Fixeds" #"Fixedi"
    sampling_method = "LHS_sampling" #"orthogonal_sampling" #"LHS_sampling" # random_sampling

    #file with results
    file_name = "../results/"+ type_experiment + '_' + sampling_method+ ".csv"

    #read in results
    results = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if len(row) > 0:
                results.append(row)
    #del(results[0]) #delete header
    results = np.asarray(results) #for better handling
    results = results.astype(np.float)

    #new file for CI results
    file_name_CI = "../results/" + "CI_" + type_experiment + '_' + sampling_method + ".csv"
    if not os.path.isfile(file_name_CI):
        open(file_name_CI, "x")

    l = 1.96 #lambda for p = 95%

    #lists for plots
    sample_mean = []
    upper_bound = []
    lower_bound = []

    #calculate confidence interval for each interval and sample sizes
    for i in np.unique(results[:,0]): #go through all different amounts of iterations
        index_i = np.where(results[:,0]==i)
        for j in np.unique(results[index_i,1]): #go through all different amount of sample sizes
            #get all area values of the iteration i and sample size j
            if type_experiment == "Fixedi":
                index_j = np.where(results[:,1]==j)
            elif type_experiment == "Fixeds":
                index_j = index_i
            areas = results[index_j,2]
            areas = np.asarray(areas[0])

            #calculate confidence interval
            n = len(areas)
            mean = sum(areas/len(areas))
            sample_mean.append(mean)
            sample_variance = (sum((areas-mean)**2))/(n-1)
            a = (l*sample_variance)/math.sqrt(n)
            lower_a = mean - a
            lower_bound.append(lower_a)
            upper_a = mean + a
            upper_bound.append(upper_a)

            # Save results
            with open(file_name_CI, 'a') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow([i, j, mean, lower_a, upper_a, a])

    sample_mean = np.asarray(sample_mean)
    lower_bound = np.asarray(lower_bound)
    upper_bound = np.asarray(upper_bound)

    #plot the confidence intervals and the sample mean
    if type_experiment == "Fixedi":
        x = np.unique(results[:,1])
        xlab = "samples"
    elif type_experiment == "Fixeds":
        x = np.unique(results[:,0])
        xlab = "iterations"
    plt.plot(x, lower_bound, 'pink', label = '95% confidence interval')
    plt.plot(x, upper_bound, 'pink')
    plt.plot(x, sample_mean,'k',label = 'sample mean', linewidth = 0.5)
    plt.fill_between(x,lower_bound, upper_bound, color = 'pink')
    plt.xlabel(xlab)
    plt.ylabel("area")
    plt.xlim(min(x),max(x))
    plt.legend()
    title = "method: " + sampling_method
    plt.title(title)
    save_title = "../results/" + "CI_" + type_experiment + "_" + sampling_method + ".png"
    plt.savefig(save_title,dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
