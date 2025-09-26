import numpy as np

class Particula:
    """
    Clase Partícula para simulación
    """
    def __init__(self, x0:np.array, v0:np.array, masa:float, h:float):
        """        
        Clase Partícula para simulación

        Args:
           - x0 (np.Array)  : Posición inicial
           - v0 (np.Array)  : Velocidad inicial
           - masa (float)   : Masa del objeto
           - h (float)      : Delta de tiempo en la operación
        """
        self.y = np.concat((x0,v0))     # [x, y, z, vx, vy, vz]
        self.m = masa
        self.F = np.array([0.0, 0.0, 0.0])
        self.dt = h
    
    def __str__(self):
        return f"Partícula: <{self.y[0]}, {self.y[1]}, {self.y[2]}>"
    
    def forcesSum(self, forces:np.array):
        """
        Suma todas las fuerzas que afectan sobre la partícula
        
        Args:
           - forces (np.Array) Lista de fuerzas que afectan a la partícula
        """
        self.F = np.sum(forces, axis=0)
    
    def step(self):
        """
        Solucionador de la velocidad y la posición de la partícula según
        la fuerza obtenida
        """
        x = self.y[:3]   # posición
        v = self.y[3:]   # velocidad

        a = self.F / self.m

        # Update
        v_new = v + a * self.dt
        x_new = x + v_new * self.dt

        # Save back
        self.y[:3] = x_new
        self.y[3:] = v_new