#for the mandelbrot figures without the monte carlo method, to save time
import numpy as np
import matplotlib.pyplot as plt

N = 45
T = 2000
x = np.linspace(-2,2,T)
y = np.linspace(-2,2,T)

def mandel(c,N):
    z = 0
    for i in range(0,N):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return True

def mandel_set(x,y,N):
    x_axis = []
    y_axis = []
    for i in x:
        for z in y:
            a = complex(i,z)
            m = mandel(a,N)
            if m == True:
                x_axis.append(i)
                y_axis.append(z)
    return x_axis,y_axis

for i in range(N):
    x_ax,y_ax = mandel_set(x,y,i)
    plt.scatter(x_ax,y_ax, s = 0.1)
    print(i)

#plt.xlim(0.3,0.5)
#plt.ylim(0.1,0.3)
plt.savefig("intro_iterations4.png",dpi=300)
plt.show()
