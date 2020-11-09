import matplotlib.pyplot as plt
import numpy as np
from pyDOE import *
from scipy.stats.distributions import uniform, norm
import random

'''

The Mandelbrot Set
Set of complex numbers for which the function:

F(Z) = Z**2 + c

remains bounded to an absolute value (the entire set is contained in a distance
or radius 2 around the origin) and where complex number c can be written

c = a + bi

where a is the real part and b is the imaginary part.

A point (x,y) on the plane belongs to the Mandelbrot Set iff the modulus or
absolute value of the complex number c is never larger than 2, no matter how
many iterations we do.

https://diegosalinas-47084.medium.com/plot-the-mandelbrot-set-with-matplotlib-c941450c80f2
'''


T = 500000 #number of points
N = 100 #number of iterations per point

def mandelIter(c, max_iter):
    '''
    Iterates max_iter times over the F(Z) function.
    '''
    z = 0
    for i in range(0, max_iter):
        z = z**2 + c
        if abs(z) > 2:
            return False
    return True

def randomComplex():
    x,y = np.random.uniform(-2, 2, 2)
    c = complex(x,y)
    return c,x,y

def mandel_set_random(T, N): #uses random uniform drawn points
    '''
    The distance to 0 must be <2 for any point in the Mandelbrot set. The
    distance is the absolute alue or modulus of complex number c.
        c = a +bi
    Where a is the real part (x-axis) and b is the imaginary part (y-axis)
    '''
    mandel_area = 0
    mandelset_x = []
    mandelset_y = [] #list of the points that belong to the mandelbrot set

    for i in range(T):
        c,x,y = randomComplex()
        m = mandelIter(c, N)
        if m == True: #is part of the mandelbrotset
            mandelset_x.append(x)
            mandelset_y.append(y)
            mandel_area += 1
    mandel_area = (mandel_area/T)*16
    return (mandelset_x, mandelset_y, mandel_area)

def LHSrandom(T): #latin hypercube
    latin = lhs(T, samples = 2)
    latin = uniform(loc = -2, scale = 4).ppf(latin)
    x,y = latin
    random.shuffle(y)
    c = []
    for i in range(len(x)):
        num = complex(x[i],y[i])
        c.append(num)
    return c,x,y

def mandel_set_latin(T, N): #uses latin hypercube drawn points for mandelbrotset
    '''
    The distance to 0 must be <2 for any point in the Mandelbrot set. The
    distance is the absolute alue or modulus of complex number c.
        c = a +bi
    Where a is the real part (x-axis) and b is the imaginary part (y-axis)
    '''
    mandel_area = 0
    mandelset_x = []
    mandelset_y = [] #list of the points that belong to the mandelbrot set
    c,x,y = LHSrandom(T)

    for i in range(T):
        m = mandelIter(c[i], N)
        if m == True: #is part of the mandelbrotset
            mandelset_x.append(x[i])
            mandelset_y.append(y[i])
            mandel_area += 1
    mandel_area = (mandel_area/T)*16
    return (mandelset_x, mandelset_y, mandel_area)

mandelarea_random = []

for i in range(N): #computes mandelbrot area for each iteration j < N
    mandelset = mandel_set_random(T, i)
    mandelarea_random.append(mandelset[2]) #for random uniform drawn points

    """
    mandelset = mandel_set_latin(T, i)
    mandelarea_latin.append(mandelset[2]) #for latin hypercube
    """


mandelset = mandel_set_random(T, N)
mandelarea_random = np.array(mandelarea_random)
mandelarea_random = mandelarea_random - mandelset[2]
#mandelarea_latin = np.array(mandelarea_latin)
#mandelarea_latin = mandelarea_latin - mandelset[2]

#plt.scatter(mandelset[0], mandelset[1])
#plt.show()

plt.plot(mandelarea_random, label = "random")
#plt.plot(mandelarea_latin, label = "lhs")
plt.xlabel("iterations")
plt.ylabel("area")
plt.title("convergence of mandelbrot area with pure random sampling")
#plt.hlines(0,1,N-1)
#plt.legend()
plt.show()
