import numpy as np

class Particula:
    def __init__(self, x0:np.array, v0:np.array, masa:float):
        y = np.concat((x0,v0))
        m = masa
        forces = []

    def forceSolver(forces:np.array):
        return np.sum(forces)
