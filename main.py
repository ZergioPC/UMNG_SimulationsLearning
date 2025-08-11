import numpy as np

def function1(x,y):
    return (x-np.exp(-x))*y

def fwd_euler(f, a, b, y0, n):
    h = (b-a)/n
    print(h)
    t = [a]
    y = [y0]

    # Usando For
    for k in range(0, n):
        y.append(y[k] + h*f(t[k],y[k]))
        t.append(t[k] + h)
    
    """
    # Usando While
    yaux = y0
    taux = a
    while (t < b):
        yaux += h*f(t, y)
        taux += h
        y.append(yaux)
        t.append(taux)
    """

    return t, y

X,Y = fwd_euler(function1, 0, 2, 2, 200)
