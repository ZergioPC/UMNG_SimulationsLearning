import numpy as np
from typing import Optional

class Link:
    def __init__(self, pos:list[float,float,float], vel:list[float,float,float], m:float, padre:Optional['Link'] = None):
        """
        Clase que representa el Link de una cadena

        Args:
            - pos (list[float, float, float]) : Posicion inicial
            - vel (list[float, float, float]) : Velocidad inicial
            - m (float) : Masa
            - padre (None | Link) : Referencia al Link padre
        """
        self.x = np.array(pos, dtype=float) # Posición como array de numpy
        self.v = np.array(vel, dtype=float) # Velocidad como array
        self.F = np.array([0.0, 0.0, 0.0])       # Fuerza acumulada
        self.masa = m
        self.parent = padre if padre else None
        
        # Parámetros para la conexión con el padre
        if self.parent is not None:
            # Distancia de equilibrio entre este link y su padre
            self.longitud_equilibrio = np.linalg.norm(self.x - self.parent.x)
        else:
            self.longitud_equilibrio = None
    
    def sumar_fuerzas(self, fuerzas: list[np.ndarray]):
        """Suma todas las fuerzas externas aplicadas al link"""
        self.F = np.sum(fuerzas, axis=0) if fuerzas else np.array([0.0, 0.0, 0.0])
    
    def calcular_fuerza_resorte(self, k: float = 100.0, damping: float = 0.5):
        """Calcula la fuerza del resorte con el link padre"""
        if self.parent is None:
            return np.array([0.0, 0.0, 0.0])
        
        # Vector dirección del padre a este link
        direccion = self.x - self.parent.x
        distancia_actual = np.linalg.norm(direccion)
        
        # Evitar división por cero
        if distancia_actual < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # Vector unitario
        u = direccion / distancia_actual
        
        # Fuerza del resorte (Ley de Hooke)
        elongacion = distancia_actual - self.longitud_equilibrio
        fuerza_resorte = -k * elongacion * u
        
        # Fuerza de amortiguamiento
        velocidad_relativa = self.v - self.parent.v
        fuerza_damping = -damping * velocidad_relativa
        
        return fuerza_resorte + fuerza_damping
    
    def paso(self, dt: float, k: float = 100.0, damping: float = 0.5, gravedad: np.ndarray = np.array([0.0, -9.81, 0.0])):
        """Actualiza posición y velocidad usando integración de Verlet o Euler"""
        
        # Fuerza de la gravedad
        F_gravedad = self.masa * gravedad
        
        # Fuerza del resorte con el padre
        F_resorte = self.calcular_fuerza_resorte(k, damping)
        
        # Fuerza total
        F_total = self.F + F_gravedad + F_resorte
        
        # Aceleración (F = ma)
        a = F_total / self.masa
        
        # Integración de Euler (puedes mejorar con Verlet o RK4)
        self.v = self.v + a * dt
        self.x = self.x + self.v * dt
        
        # Resetear fuerzas acumuladas para el siguiente paso
        self.F = np.array([0.0, 0.0, 0.0])