import numpy as np
import csv
from sampling import random_sampling
from sampling import orthogonal_sampling
from sampling import LHS_sampling
import os

def mandel_iter(c, max_iter):
    '''
    Iterates max_iter times over the F(Z) function.
    '''
    z = 0
    for i in range(0, max_iter):
        z = z**2 + c
        if abs(z) > 2:
            return False
    return True


def main():
    '''
    Choose: experiment type (fixed i/s), sampling method, mandelbrot iterations,
    sample sizes and number of simulations.

    Results are in ../results
    i, s, area 
    '''

    # params
    type_experiment = "Fixeds" #"fixed s"
    sampling_method = LHS_sampling # random_sampling # LHS_sampling
    mandelbrot_iterations = [1000]
    sample_sizes = np.arange(100, 10000, 100)
    number_of_sims = 10

    # create csv for results
    file_name = "../results/"+ type_experiment + '_' + sampling_method.__name__ + ".csv"
    if not os.path.isfile(file_name):
        open(file_name, "x")


    # sample area
    min = -2
    max = 2
    total_area = (max - min)*(max - min)

    for i in mandelbrot_iterations:
        for s in sample_sizes:
            for n in range(number_of_sims):
                x_list, y_list = sampling_method(min, max, s) # SAMPLING s * (x, y)
                mandel_area=0
                mandelset_x=[]
                mandelset_y=[]

                for x, y in zip(x_list, y_list):
                    c = complex(x, y)
                    in_mandel = mandel_iter(c, i) #MANDEL_ITER
                    if in_mandel:
                        mandelset_x.append(x)
                        mandelset_y.append(y)
                        mandel_area+=1
                mandel_area = (mandel_area/s)*total_area

                # Save results
                with open(file_name, 'a') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow([i, s, mandel_area])


if __name__ == "__main__":
    main()
