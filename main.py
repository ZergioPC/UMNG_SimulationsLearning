import numpy as np
import matplotlib.pyplot as plt

def fwd_euler_while(f, a, b, y0, h):
    t = a
    y = y0
    tvals = [t]
    yvals = [y]
    while t < b - 1e-12:
        y += h*f(t, y)
        t += h
        tvals.append(t)
        yvals.append(y)
    return tvals, yvals

def fwd_for(f, a, b, y0, h):
    n = round((b-a)/h)
    h = (b-a)/n # fix if (b-a)/h
    t = [0]*(n+1) # was not an int
    y = [0]*(n+1)
    t[0] = a
    y[0] = y0
    for k in range(0, n):
        y[k+1] = y[k] + h*f(t[k],y[k])
        t[k+1] = t[k] + h
    return t, y

def edo1(t,y):
    salida=-2*t*y
    return salida

def sol1(t):
    y=np.exp(-t**2)
    return y

#t=np.arange(0,5,0.3)
t2=np.linspace(0,4,101)
yexacta= sol1(t2)

taprox, yaprox=fwd_euler_while(edo1, 0, 4, 1, 0.3)

plt.plot(t2,yexacta)
plt.plot(taprox,yaprox,'*-')

#plt.title("hola")
plt.show()