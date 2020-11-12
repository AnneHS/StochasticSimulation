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


T = 10000 #number of points
N = 10 # number of iterations per point

#real = np.linspace(-2, 2, 1000)
#imag = np.linspace(-1, 1, 1000)
#x_axis = []
#y_axis = []
#max_iter = 10

def mandelIter(c, max_iter):
    '''
    Iterates max_iter times over the F(Z) function.
    '''
    z = 0
    for i in range(0, max_iter):
        z = z**2 + c
    return z

def randomComplex():
    x,y = np.random.uniform(-2, 2, 2)
    c = complex(x+y*((-1)**(-1/2)))
    return c,x,y

'''
def orthogonal(min, max, N):
    r = max - min

    sample_x=[]
    sample_y=[]
    for i in range(N):
        x_sub = [(min + i * r/N), (min + i+1 * r/N)]

        for j in range(N):
            y_sub = [(min + i * r/N), (min + i+1 * r/N)]

            x_point = np.random.uniform(x_sub[0], x_sub[1], 1)[0]
            y_point = np.random.uniform(y_sub[0], y_sub[1], 1)[0]

            sample_x.append(x_point)
            sample_y.append(y_point)

    return sample_x, sample_y
'''

def orthogonal(min, max, N):

    samples = N*N
    r = max - min

    scale = r/samples

    xlist = [[0 for i in range(N)] for j in range(N)]
    ylist = [[0 for i in range(N)] for j in range(N)]
    print(xlist)
    print(ylist)

    m=0
    for i in range(N):
        for j in range(N):
            xlist[i][j] = ylist[i][j] = m
            m+=1

    np.random.shuffle(xlist)
    np.random.shuffle(ylist)
    print(xlist)
    print(ylist)

    xvalues=[]
    yvalues=[]
    count=0
    for i in range(N):
        for j in range(N):
            count+=1
            print(min, scale, xlist[i][j])
            xvalues.append( min + (scale * (xlist[i][j])) + (np.random.uniform()*scale) )
            yvalues.append( min + (scale * (ylist[j][i])) +  (np.random.uniform()*scale) )

    print(count)
    return xvalues, yvalues


    '''
    lim = [min_v, max_v]
    r = max_v - min_v
    res = []
    for i in range(N):
        x_lim = [
            lim[0] + i * r/N,
            lim[0] + (i+1) * r/N
        ]
        for j in range(N):
            y_lim = [
                lim[0] + j * r/N,
                lim[0] + (j+1) * r/N
            ]
            res.append([
                np.random.uniform(x_lim[0], x_lim[1], 1)[0],
                np.random.uniform(y_lim[0], y_lim[1], 1)[0]
            ])
    return res
    '''

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
        if abs(m) < 2: #is part of the mandelbrotset
            mandelset_x.append(x)
            mandelset_y.append(y)
            mandel_area += 1
    mandel_area = (mandel_area*16)/T
    return (mandelset_x, mandelset_y, mandel_area)

N = 10
min=-2
max=2
x, y = orthogonal(min, max, N)
plt.scatter(x, y)

r = max - min
scale = r/N
sections=[]
m=1
for i in range(N):
    sections.append(min+ m*scale)
    m+=1

for i in sections:
    plt.plot([i, i], [-3, 3], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    #pass
for i in sections:
    #plt.plot([-3, -3], [i, i], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.hlines(i, min, max, colors='k', linestyle='--', linewidth=0.5, alpha=0.5)
'''
for i in [-1, 0, 1]:
    plt.plot([i, i], [-3, 3], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
for i in [-1, 0, 1]:
    plt.plot([-3, 3], [i, i], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
'''
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()

'''
x, y =orthogonal(-2, 2, 4)
plt.scatter(x, y)
for i in [-1, 0, 1]:
    plt.plot([i, i], [-3, 3], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
for i in [-1, 0, 1]:
    plt.plot([-3, 3], [i, i], color='k', linestyle='--', linewidth=0.5, alpha=0.5)
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()
'''
#mandelset = mandel_set(T, N)
#print(mandelset[2])
#plt.scatter(mandelset[0], mandelset[1])
#plt.show()
