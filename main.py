import os
import numpy as np

from ParticleSimulation.Particle import Particula

def simpleSimulation():
    x0 = np.array([0.0, 1.0, 0.0])
    v0 = np.array([0.0, 0.5, 0.0])

    test = Particula(x0,v0,1.0)
    
    while(True):
        print("xd")

if __name__ == "__main__":
    simpleSimulation() 