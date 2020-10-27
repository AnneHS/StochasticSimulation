import matplotlib.pyplot as plt
import numpy as np

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

real = np.linspace(-2, 2, 1000)
imag = np.linspace(-1, 1, 1000)
x_axis = []
y_axis = []
max_iter = 10

def mandel(c, max_iter):
    '''
    Iterates max_iter times over the F(Z) function.
    '''
    z = 0
    for i in range(0, max_iter):
        z = z**2 + c

    return z

def mandel_set(x, y, max_iter):
    '''
    The distance to 0 must be <2 for any point in the Mandelbrot set. The
    distance is the absolute alue or modulus of complex number c.
        c = a +bi
    Where a is the real part (x-axis) and b is the imaginary part (y-axis)
    '''
    for i in x:
        for z in y:
            a = complex(i+z*((-1)**(-1/2)))
            m = mandel(a, max_iter)
            if abs(m) < 2:
                x_axis.append(i)
                y_axis.append(z)

mandel_set(real, imag, max_iter)

plt.scatter(x_axis, y_axis)
plt.show()
