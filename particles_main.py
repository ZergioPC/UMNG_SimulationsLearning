import os
import numpy as np

from ParticleSimulation.Particle import Particula

def simpleSimulation():
    END = 10.0
    time = 0.0
    h = 0.1

    x0 = np.array([0.0, 100.0, 0.0])
    v0 = np.array([0.0, 0.0, 0.0])

    test = Particula(x0,v0,1.0,h)
    gravedad = np.array([0.0, -9.8, 0.0])

    while(time <= END):
        test.forcesSum([gravedad])
        test.step()
        print(test)
        time += h

if __name__ == "__main__":
    simpleSimulation()