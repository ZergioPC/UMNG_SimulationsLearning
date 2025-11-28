import numpy as np

class Solvers:
    """
    Clase para gestionar los metodos numéricos
    """
    @staticmethod
    def euler(derivada:callable, y:np.array, dt:float):
        """
        Metodo Numerico de Euler

        Args:
            - derivada (function) : Funcion que calcula la derivada
            - y (np.array) :        Estado actual [x, y, z, vx, vy, vz]
            - dt (float) :          Delta de tiempo

        Returns:
        - np.array: Posiciones y velocidades [x, y, z, vx, vy, vz]
        """
        y_diff = derivada(y)
        y_diff = np.round(y_diff, decimals=2)
        y_new = y + y_diff * dt

        return y_new

    @staticmethod
    def runge_kutta_4(derivada:callable, y:np.array, dt:float):
        """
        Metodo Numerico de Runge Kutta 4

        Args:
            - derivada (function) : Funcion que calcula la derivada
            - y (np.array) :        Estado actual [x, y, z, vx, vy, vz]
            - dt (float) :          Delta de tiempo
            
        Returns:
            - np.array: Posiciones y velocidades [x, y, z, vx, vy, vz
        """

        k1 = np.round(derivada(y), decimals=2)
        k2 = np.round(derivada(y + k1 * dt / 2), decimals=2)
        k3 = np.round(derivada(y + k2 * dt / 2), decimals=2)
        k4 = np.round(derivada(y + k3 * dt), decimals=2)
        y_new =  y + (k1 + 2*k2 + 2*k3 + k4) * dt / 6
        
        return y_new
    
    @staticmethod
    def verlet(derivada, y, dt):
        """
        Método Numérico de Verlet (Velocity Verlet)

        Args:
            - derivada (function): Función que calcula la derivada
            - y (np.array):        Estado actual [x, y, z, vx, vy, vz]
            - dt (float):          Delta de tiempo

        Returns:
            - np.array: Nuevo estado [x, y, z, vx, vy, vz]
        """
        # Extraemos velocidad y aceleración actuales
        v = y[3:]
        a = derivada(y)[3:]   # aceleración actual
        
        # Paso de posición
        x_new = y[:3] + v * dt + 0.5 * a * dt**2

        # Estado provisional para recalcular aceleración
        y_temp = np.concatenate((x_new, v))
        a_new = derivada(y_temp)[3:]  # nueva aceleración
        
        # Paso de velocidad
        v_new = v + 0.5 * (a + a_new) * dt

        # Nuevo estado completo
        return np.concatenate((x_new, v_new))