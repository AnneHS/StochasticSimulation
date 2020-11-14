import numpy as np
import math
from pyDOE import *
from scipy.stats.distributions import uniform, norm

def random_sampling(min, max, s):
    s = int(s)
    x = np.empty(shape=(s, 1))
    y = np.empty(shape=(s, 1))
    #c = []

    for point in range(s):
        x[point], y[point] =  np.random.uniform(min, max, 2)
        #c.append(complex(x_p, y_p))  #complex(x[point]+y[point]*((-1)**(-1/2)))

    return x,y


def LHS_sampling(min, max, s):
    s = int(s)
    latin_x = lhs(int(math.sqrt(s)))#, samples = 2)
    latin_y = lhs(int(math.sqrt(s)))#, samples = 2)
    latin_x = np.asarray(latin_x).reshape(-1) #make the matrix 1D
    latin_y = np.asarray(latin_y).reshape(-1) #make the matrix 1D
    #uniform(loc = -2, scale = 4).ppf(latin)
    latin_x = uniform(loc = min, scale = (max-min)).ppf(latin_x)
    latin_y = uniform(loc = min, scale = (max-min)).ppf(latin_y)
    x,y = latin_x,latin_y
    np.random.shuffle(y)

    return x, y

def orthogonal_sampling(min, max, s):

    N = int(math.sqrt(s))
    samples = s
    r = max - min

    scale = r/samples

    xlist = [[0 for i in range(N)] for j in range(N)]
    ylist = [[0 for i in range(N)] for j in range(N)]
    #print(xlist)
    #print(ylist)

    m=0
    for i in range(N):
        for j in range(N):
            xlist[i][j] = ylist[i][j] = m
            m+=1

    np.random.shuffle(xlist)
    np.random.shuffle(ylist)

    xvalues=[]
    yvalues=[]
    count=0
    for i in range(N):
        for j in range(N):
            count+=1
            #print(min, scale, xlist[i][j])
            xvalues.append( min + (scale * (xlist[i][j])) + (np.random.uniform()*scale) )
            yvalues.append( min + (scale * (ylist[j][i])) +  (np.random.uniform()*scale) )

    return xvalues, yvalues
