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

def fwd_euler_for(f, a, b, y0, h):
    n = round((b-a)/h)
    h = (b-a)/n         # fix if (b-a)/h was not an int
    t = [0]*(n+1)           
    y = [0]*(n+1)
    t[0] = a
    y[0] = y0
    for k in range(0, n):
        y[k+1] = y[k] + h*f(t[k],y[k])
        t[k+1] = t[k] + h
    return t, y

def fwd_runge_kutta_algoritm(f, a, b, x0, n):
    h = round((b-a)/n)
    t = np.linspace(a, b, np.floor((b-a)*h))
    x = [x0]

    for k in range(len(t-1)):
        a = f(t[k],x[k])
        b = f(t[k] + h/2, x[k] + a*h/2)
        print(b)
        c = f(t[k] + h/2, x[k] + b*h/2)
        print(c)
        d = f(t[k] + h, x[k] + h*c)
        x.append(x[k] + h/6 * (a + 2*b + 2*c + d))

    return t, x

def edo1(t,y):
    salida=-2*t*y
    return salida

def sol1(t):
    y=np.exp(-t**2)
    return y

#t=np.arange(0,5,0.3)
t2=np.linspace(0,4,101)
yexacta= sol1(t2)

#taprox, yaprox=fwd_euler_while(edo1, 0, 4, 1, 0.3)
taprox, yaprox=fwd_runge_kutta_algoritm(edo1, 0, 4, 1, 0.3)

#plt.plot(t2,yexacta)
#plt.plot(taprox,yaprox,'*-')

#plt.title("hola")
#plt.show()

print(len(taprox), len(yaprox))