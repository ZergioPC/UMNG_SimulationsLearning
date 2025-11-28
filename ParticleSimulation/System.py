import numpy as np
from ParticleSimulation.Particle import Particula

class System:
    """
    Clase para gestionar un sistema de múltiples partículas
    """
    def __init__(self, solver:callable, dt:float, limites=None|list):
        """
        Inicializa el sistema de partículas con una lista vacía

        Args:
            - metodo_numerico (function) : Función que implementa un método numérico.
                                           Debe recibir (derivada, y, dt) y retornar el nuevo estado
            - limites (np.array) : Lista de los limites del mundo 
                                   [xmin, xmax, ymin, ymax, zmin, zmax]
            - dt (float) : Delta de tiempo
        """
        self.solver = solver
        self.dt = dt
        self.limites:list = limites
        self.particulas:list[Particula] = []
        self.time = 0.00
    
    def agregar_particula(self, particula: Particula):
        """
        Agrega una partícula al sistema
        
        Args:
            - particula (Particula): Objeto de tipo Particula a agregar
        """
        self.particulas.append(particula)
    
    def aplicar_fuerzas(self, fuerzas: np.array):
        """
        Aplica un array de fuerzas a cada partícula del sistema
        
        Args:
            - fuerzas (np.array): Array de fuerzas de forma (n_particulas, 3)
                                  donde cada fila corresponde a la fuerza [Fx, Fy, Fz]
                                  que actúa sobre cada partícula
        """
        for particula in self.particulas:
            particula.forcesSum(fuerzas)

    def aplicar_posiciones(self):
        """
        Calcula las posiciones con un metodo de integración definido
        """
        for particula in self.particulas:
            particula.step(self.solver, self.limites, self.dt)

    def time_tic(self):
        self.time += self.dt