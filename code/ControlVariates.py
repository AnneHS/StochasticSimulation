## control variates
import numpy as np
import csv
from sampling import random_sampling
from sampling import orthogonal_sampling
from sampling import LHS_sampling
import os
import math
import matplotlib.pyplot as plt

def inControlVariate(x,y,control_area):
    #is the point in an circle with area of 1.5
    R_2 = (math.sqrt(control_area/math.pi))**2
    if (x**2 + y**2) < (R_2):
        return True
    return False

def main():
    '''
    Choose: experiment type (fixed i/s), sampling method, mandelbrot iterations,
    sample sizes and number of simulations.

    Results are in ../results
    i, s, area
    '''

    # params
    type_experiment = "Fixedi" #"CVs_Fixeds" #"CVs_Fixedi"
    sampling_method_all = [random_sampling, LHS_sampling, orthogonal_sampling]
    mandelbrot_iterations = [1000] #np.arange(100,10001,100)#[1000]
    sample_sizes = np.arange(100, 10001, 100) #[1000] #np.arange(100, 10001, 100)
    number_of_sims = 100
    control_area = 1.5

    # sample area
    min = -2
    max = 2
    total_area = (max - min)*(max - min)
    l = 1.96 #lambda for p = 95%

    # set seeed
    np.random.seed(1)

    a_vals = [] #empty list to store the a values

    for sampling_method in sampling_method_all:
        # csv with mandelbrot results
        file_name_mandelbrot = "../results/" + type_experiment + '_' + sampling_method.__name__ + ".csv"
        #extract the mandelbrot results:
        results = []
        with open(file_name_mandelbrot, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if len(row) > 0:
                    results.append(row)
        results = np.asarray(results) #for better handling
        results = results.astype(np.float)

        Y_area = []
        #generate control variate Y
        for i in mandelbrot_iterations:
            for s in sample_sizes:
                for n in range(number_of_sims):
                    x_list, y_list = sampling_method(min, max, s) # SAMPLING s * (x, y)

                    control_Y = 0
                    for x, y in zip(x_list, y_list):
                        #estimate the control variate area (1.5)
                        in_control = inControlVariate(x,y,control_area)
                        if in_control:
                            control_Y +=1
                    control_Y = (control_Y/s)*total_area
                    Y_area.append(control_Y)

        #new file for CI results
        file_name_CV = "../results/" + "CV_" + type_experiment + '_' + sampling_method.__name__ + ".csv"
        if not os.path.isfile(file_name_CV):
            open(file_name_CV, "x")

        #calculate the new area with the control variate and the confidence intervals
        #lists for plots
        sample_mean = []
        upper_bound = []
        lower_bound = []
        a_method = []
        Y_area = np.asarray(Y_area)

        #calculate confidence interval for each interval and sample sizes
        for i in np.unique(results[:,0]): #go through all different amounts of iterations
            index_i = np.where(results[:,0]==i)
            for j in np.unique(results[index_i,1]): #go through all different amount of sample sizes
                #get all area values of the iteration i and sample size j
                if type_experiment == "Fixedi":
                    index_j = np.where(results[:,1]==j)
                elif type_experiment == "Fixeds":
                    index_j = index_i
                areas_X = results[index_j,2]
                areas_X = np.asarray(areas_X[0])
                areas_Y = Y_area[index_j]

                #calculate the new area estimate with the control variate
                mean_X = sum(areas_X/len(areas_X))
                mean_Y = sum(areas_Y/len(areas_Y))
                c = -1*(sum((areas_X-mean_X)*(areas_Y-mean_Y))/(sum((areas_Y-mean_Y)**2)))
                #print(areas_X,c,areas_Y)
                areas_CV = areas_X + c*(areas_Y + control_area)

                #calculate confidence interval
                n = len(areas_CV)
                mean = sum(areas_CV/len(areas_CV))
                sample_mean.append(mean)
                sample_variance = (sum((areas_CV-mean)**2))/(n-1)
                a = (l*sample_variance)/math.sqrt(n)
                lower_a = mean - a
                lower_bound.append(lower_a)
                upper_a = mean + a
                upper_bound.append(upper_a)
                a_method.append(a)

                # Save results
                with open(file_name_CV, 'a') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow([i, j, mean, lower_a, upper_a, a])

        a_vals.append(a_method)

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
        print(x)
        #plt.xlim(min(x),max(x))
        plt.legend()
        title = "method: " + sampling_method.__name__
        plt.title(title)
        save_title = "../results/" + "CV_" + type_experiment + "_" + sampling_method.__name__ + ".png"
        plt.savefig(save_title,dpi=300)
        plt.show()

        #make plot that compares all a values (with and without control variates)
    for sampling_method in sampling_method_all:
        #file with results
        file_name_a = "../results/"+ "CI_" + type_experiment + '_' + sampling_method.__name__ + ".csv"

        #read in results
        results_a = []
        with open(file_name_a, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if len(row) > 0:
                    results_a.append(row)

        results_a = np.asarray(results_a) #for better handling
        results_a = results_a.astype(np.float)

        #extract the a-values per method
        a_vals = results_a[:,-1]
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
    plt.plot(x, a[0], 'b', label = 'random sampling & control variate')
    plt.plot(x, a[1], 'r', label = 'latin hypercube sampling & control variate')
    plt.plot(x, a[2], 'g', label = 'orthogonal sampling & control variate')
    plt.plot(x, a[3], 'c', label = 'random sampling')
    plt.plot(x, a[4], 'm', label = 'latin hypercube sampling')
    plt.plot(x, a[5], 'y', label = 'orthogonal sampling')
    plt.xlabel(xlab)
    plt.ylabel("a")
    #plt.xlim(min(x),max(x))
    plt.legend()
    title = "a-values for fixed " + fixed
    plt.title(title)
    save_title = "../results/" + "CV_aValues_" + type_experiment + ".png"
    plt.savefig(save_title,dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
