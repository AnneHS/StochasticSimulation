import matplotlib.pyplot as plt
import numpy as np
#from pyDOE import *

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


T = 100000 #number of points
N = 75 #number of iterations per point

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

def mandel_set(T, N):
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

mandelarea = []
np.array(mandelarea)
for i in range(N):
    mandelset = mandel_set(T, i)
    mandelarea.append(mandelset[2])

mandelset = mandel_set(T, N)
mandelarea = np.array(mandelarea)
mandelarea = mandelarea - mandelset[2]
#mandelarea.append(mandelset[2])
#print(mandelset[2])
print(mandelarea)
plt.plot(mandelarea)
plt.xlabel("iterations")
plt.ylabel("area")
plt.title("convergence of mandelbrot area")
plt.hlines(0,1,N-1)
plt.show()
