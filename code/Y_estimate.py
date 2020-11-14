##Generate Y estimate for control variates
import numpy as np
import csv
from sampling import random_sampling
from sampling import orthogonal_sampling
from sampling import LHS_sampling
import os
import math

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

    for sampling_method in sampling_method_all:
        # csv with mandelbrot results
        file_name = "../results/" + "Y_" + type_experiment + '_' + sampling_method.__name__ + ".csv"
        if not os.path.isfile(file_name):
            open(file_name, "x")

        Y_area = []
        #generate control variate Y
        for i in mandelbrot_iterations:
            print("i: ", i)
            for s in sample_sizes:
                print("s: ", s)
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

                    # Save results
                    with open(file_name, 'a') as file:
                        writer = csv.writer(file, delimiter=',')
                        writer.writerow([i, s, Y_area])

if __name__ == "__main__":
    main()
