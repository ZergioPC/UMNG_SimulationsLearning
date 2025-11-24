import numpy as np
from typing import Optional

import numpy as np
from typing import Optional

class Link:
    def __init__(
            self,
            pos:list[float,float,float], 
            vel:list[float,float,float], 
            m:float, 
            name:str = "Link", 
            padre1:Optional['Link'] = None,
            padre2:Optional['Link'] = None
            ):
        """
        Clase que representa el Link de una cadena

        Args:
            - pos (list[float, float, float]) : Posicion inicial
            - vel (list[float, float, float]) : Velocidad inicial
            - m (float) : Masa
            - name (str) : Nombre identificador
            - padre1 (None | Link) : Referencia al Link padre1
            - padre2 (None | Link) : Referencia al Link padre2
        """
        self.x = np.array(pos, dtype=float) # Posición como array de numpy
        self.v = np.array(vel, dtype=float) # Velocidad como array
        self.F = np.array([0.0, 0.0, 0.0])       # Fuerza acumulada
        self.masa = m
        self.parent1 = padre1 if padre1 else None
        self.parent2 = padre2 if padre2 else None
        
        # Parámetros para la conexión con padre1
        if self.parent1 is not None:
            self.longitud_equilibrio1 = np.linalg.norm(self.x - self.parent1.x)
        else:
            self.longitud_equilibrio1 = None
        
        # Parámetros para la conexión con padre2
        if self.parent2 is not None:
            self.longitud_equilibrio2 = np.linalg.norm(self.x - self.parent2.x)
        else:
            self.longitud_equilibrio2 = None
    
    def sumar_fuerzas(self, fuerzas: list[np.ndarray]):
        """
        Suma todas las fuerzas externas aplicadas al link y actualiza `self.F`.

        Args:
            fuerzas (list[np.ndarray]): Lista (o iterable) de vectores de fuerza
                (cada uno un array de 3 elementos) aplicados sobre este link.

        Returns:
            None: Actualiza la fuerza acumulada en `self.F`. Si `fuerzas` está
            vacío o es `None`, `self.F` se establece en un vector cero.
        """
        self.F = np.sum(fuerzas, axis=0) if fuerzas else np.array([0.0, 0.0, 0.0])
    
    def calcular_fuerza_resorte_padre(self, padre: 'Link', longitud_eq: float, k: float, damping: float):
        """
        Calcula la fuerza ejercida por el resorte que conecta este `Link`
        con un `padre` concreto, incluyendo un término de amortiguamiento.

        La fuerza total devuelta es la suma de la componente elástica (Ley de
        Hooke) y la componente viscosa (amortiguamiento proporcional a la
        velocidad relativa).

        Args:
            padre (Link): El `Link` padre al que está conectado este enlace.
            longitud_eq (float): Longitud de equilibrio (longitud natural) del
                resorte entre los dos enlaces.
            k (float): Constante del resorte (rigidez).
            damping (float): Coeficiente de amortiguamiento (viscoso).

        Returns:
            np.ndarray: Vector de 3 componentes con la fuerza aplicada sobre
            este `Link` por el resorte y el amortiguador (en newtons).

        Notas:
            - Si `padre` o `longitud_eq` es `None`, o la distancia actual entre
              los nodos es (prácticamente) cero, devuelve un vector cero para
              evitar divisiones por cero.
            - La dirección positiva del vector de fuerza está definida como la
              fuerza que actúa sobre este `Link` (no sobre el padre).
        """
        if padre is None or longitud_eq is None:
            return np.array([0.0, 0.0, 0.0])
        
        # Vector dirección del padre a este link
        direccion = self.x - padre.x
        distancia_actual = np.linalg.norm(direccion)
        
        # Evitar división por cero
        if distancia_actual < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # Vector unitario
        u = direccion / distancia_actual
        
        # Fuerza del resorte (Ley de Hooke)
        elongacion = distancia_actual - longitud_eq
        fuerza_resorte = -k * elongacion * u
        
        # Fuerza de amortiguamiento
        velocidad_relativa = self.v - padre.v
        fuerza_damping = -damping * velocidad_relativa
        
        return fuerza_resorte + fuerza_damping
    
    def calcular_fuerza_resorte(self, k: float = 100.0, damping: float = 0.5):
        """
        Calcula y devuelve la fuerza resultante de las conexiones tipo resorte
        con `parent1` y `parent2` (si existen).

        Args:
            k (float): Constante de rigidez de los resortes (por defecto 100.0).
            damping (float): Coeficiente de amortiguamiento (por defecto 0.5).

        Returns:
            np.ndarray: Vector de 3 componentes con la fuerza total debida a los
            resortes que actúan sobre este `Link`.
        """
        fuerza_total = np.array([0.0, 0.0, 0.0])
        
        # Fuerza del padre1
        if self.parent1 is not None:
            fuerza_total += self.calcular_fuerza_resorte_padre(
                self.parent1, self.longitud_equilibrio1, k, damping
            )
        
        # Fuerza del padre2
        if self.parent2 is not None:
            fuerza_total += self.calcular_fuerza_resorte_padre(
                self.parent2, self.longitud_equilibrio2, k, damping
            )
        
        return fuerza_total
    
    def paso(
            self, 
            dt: float, 
            k: float = 100.0, 
            damping: float = 0.5, 
            gravedad: np.ndarray = np.array([0.0, 0.0, 0.0])
            ):
        """
        Realiza un paso de integración explícita (Euler) para actualizar la
        velocidad y posición del `Link` durante un intervalo de tiempo `dt`.

        El método combina las fuerzas acumuladas en `self.F`, la gravedad y las
        fuerzas elásticas de los resortes con los padres para calcular la
        aceleración y luego integra la velocidad y la posición.

        Args:
            dt (float): Paso de tiempo (segundos).
            k (float): Constante de rigidez para las fuerzas de resorte.
            damping (float): Coeficiente de amortiguamiento para los resortes.
            gravedad (np.ndarray): Vector de gravedad (por defecto [0,-9.81,0]).

        Returns:
            None: Actualiza `self.v`, `self.x` y reinicia `self.F` (fuerzas
            acumuladas) a cero para el siguiente paso.
        """

        # Fuerza de la gravedad
        F_gravedad = self.masa * gravedad
        
        # Fuerza del resorte con ambos padres
        F_resorte = self.calcular_fuerza_resorte(k, damping)
        
        # Fuerza total
        F_total = self.F + F_gravedad + F_resorte
        
        # Aceleración (F = ma)
        a = F_total / self.masa
        
        # Integración de Euler
        self.v = self.v + a * dt
        self.x = self.x + self.v * dt
        
        # Resetear fuerzas acumuladas para el siguiente paso
        self.F = np.array([0.0, 0.0, 0.0])