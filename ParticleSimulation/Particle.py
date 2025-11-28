import numpy as np
from random import random as rng

class Particula:
    """
    Clase Partícula para simulación
    """
    def __init__(
            self, 
            x0:np.array, 
            v0:np.array, 
            masa:float, 
            coef_restitucion:float=1.0,
            color:list=[1.0, 1.0, 1.0] 
            ):
        """        
        Clase Partícula para simulación

        Args:
        - x0 (np.array)  : Posición inicial
        - v0 (np.array)  : Velocidad inicial
        - masa (float)   : Masa del objeto
        - color (list)   : Color del objeto
        - coef_restitucion (float) : Coeficiente de restitución (0.0 a 1.0)
        """
        self.y = np.concatenate((x0,v0))     # [x, y, z, vx, vy, vz]
        self.m = masa
        self.F = np.array([0.0, 0.0, 0.0])
        self.e = coef_restitucion  # Coeficiente de restitución
        self.color = color
    
    def __str__(self):
        return f"Partícula: <{self.y[0]}, {self.y[1]}, {self.y[2]}>"

    def _frontera(self, limites:np.array):
        """
        Calcula los limites de frontera del mundo y aplica la colisión

        Args:
            - limites (np.array) : Lista de los limites del mundo 
                                [xmin, xmax, ymin, ymax, zmin, zmax]
        """
        x, y, z, vx, vy, vz = self.y
        xmin, xmax, ymin, ymax, zmin, zmax = limites
        
        # Eje X
        if x < xmin:
            x = xmin
            vx *= -self.e
            vx = vx + (20 * rng() - 10.0 )
        elif x > xmax:
            x = xmax
            vx *= -self.e
            vx = vx + (20 * rng() - 10.0 )

        # Eje Y
        if y < ymin:
            y = ymin
            vy *= -self.e
            vy = vy + (20 * rng() - 10.0 )
        elif y > ymax:
            y = ymax
            vy *= -self.e
            vy = vy + (20 * rng() - 10.0 )
        
        # Eje Z
        if z < zmin:
            z = zmin
            vz *= -self.e
            vz = vz + (20 * rng() - 10.0 )
        elif z > zmax:
            z = zmax
            vz *= -self.e
            vz = vz + (20 * rng() - 10.0 )
        
        self.y = np.array([x,y,z,vx,vy,vz])

    def _derivada(self, y):
        """
        Calcula la derivada del estado [x, y, z, vx, vy, vz]
        
        Args:
           - y (np.array): Estado actual [x, y, z, vx, vy, vz]
           
        Returns:
           - np.array: Derivada [vx, vy, vz, ax, ay, az]
        """
        v = np.array([y[3], y[4], y[5]])
        v = np.round(v, decimals=2)
        a = self.F / self.m  # aceleración
        return np.concatenate((v,a))
    
    def forcesSum(self, forces:np.array):
        """
        Suma todas las fuerzas que afectan sobre la partícula
        
        Args:
        - forces (np.array) Lista de fuerzas que afectan a la partícula
        """
        self.F = np.sum(forces, axis=0)
    
    def step(self, metodo_numerico:callable, limites:np.array, dt:float):
        """
        Solucionador de la velocidad y la posición de la partícula según
        la fuerza obtenida y el método numérico proporcionado
        
        Args:
            - metodo_numerico (function) : Función que implementa un método numérico.
                                           Debe recibir (y, dt) y retornar el nuevo estado
            - limites (np.array) : Lista de los limites del mundo 
                                   [xmin, xmax, ymin, ymax, zmin, zmax]
            - dt (float) : Delta de tiempo
        """
        
        self.y = metodo_numerico(self._derivada, self.y, dt)
        self.F = np.array([0.0, 0.0, 0.0])
        
        if limites is not None:
            self._frontera(limites)

        self.y = np.round(self.y, decimals=2)