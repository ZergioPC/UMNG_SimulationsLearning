import numpy as np
from random import randint as rng
from random import random as rngf

from ParticleSimulation.Particle import Particula
from ParticleSimulation.Solvers import Solvers
from ParticleSimulation.System import System
from ParticleSimulation.Render import Render

from Terminal import print_wasd, print_banner

def auxSelectMetodo(n):
    match n:
        case 1:
            return Solvers.euler
        case 2:
            return Solvers.runge_kutta_4
        case 3:
            return Solvers.verlet

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

def newSimulation_1(n:int, delta:float, nParticles:float):
    METODO = auxSelectMetodo(n)
    DT = delta

    limites = [-1000, 1000, -1000, 1000, -1000, 1000]
    gravedad = [0.0, -98000, 0.0]

    sistema = System(METODO, DT, limites)
    
    x0 = np.array([20, 0, 20])

    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([rng(0,400), rng(0,200), 0])
        
        color_val = rngf() * 0.7 + 0.3
        color = [0.0, color_val, 0.0]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)
    
    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([-rng(0,400), rng(0,200), 0])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, 0.0, 0.0]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)

    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([0.0, rng(0,200), rng(0,100)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, color_val, color_val]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)
        
    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([0.0, rng(0,200), -rng(0,100)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val*0.3, color_val*0.3, color_val]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)

    sistema.aplicar_posiciones()
    
    render = Render(sistema, ancho=800, alto=600)
    render.inicializar()

    # Bucle principal controlado manualmente
    while True:
        #print(sistema.time)
        #sistema.time_tic()

        # Aplica fuerzas y actualiza el sistema
        fuerzas = np.array([gravedad])  # gravedad
        sistema.aplicar_fuerzas(fuerzas)
        sistema.aplicar_posiciones()
        
        # Actualiza la visualización
        render.actualizar_frame()

def newSimulation_2(n:int, delta:float, nParticles:float):
    METODO = auxSelectMetodo(n)
    DT = delta

    limites = [-1000, 1000, -1000, 1000, -1000, 1000]
    gravedad = [0.0, -98000, 0.0]

    sistema = System(METODO, DT, limites)
    
    x0 = np.array([20, 0, 20])

    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([rng(0,200), rng(0,200), rng(0,200)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [0.0, color_val, 0.0]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)
    
    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([-rng(0,100), rng(0,200), rng(0,100)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, 0.0, 0.0]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)

    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([-rng(0,200), rng(0,200), rng(0,200)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, color_val, color_val]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)
        
    for _ in range(int(np.round(250 * nParticles, decimals=0))):
        m = rng(1,1000)
        v0 = np.array([rng(0,100), rng(0,200), -rng(0,100)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val*0.3, color_val*0.3, color_val]

        p = Particula(x0, v0, m, 1.0, color)
        sistema.agregar_particula(p)

    sistema.aplicar_posiciones()
    
    render = Render(sistema, ancho=800, alto=600)
    render.inicializar()

    # Bucle principal controlado manualmente
    while True:
        #print(sistema.time)
        #sistema.time_tic()

        # Aplica fuerzas y actualiza el sistema
        fuerzas = np.array([gravedad])  # gravedad
        sistema.aplicar_fuerzas(fuerzas)
        sistema.aplicar_posiciones()
        
        # Actualiza la visualización
        render.actualizar_frame()

def newSimulation_3(n:int, delta:float, nParticles:float):
    METODO = auxSelectMetodo(n)
    DT = delta

    limites = [-1000, 1000, -1000, 1000, -1000, 1000]
    gravedad = [0.0, -98000, 0.0]

    sistema = System(METODO, DT, limites)
    
    for _ in range(int(np.round(100 * nParticles, decimals=0))):
        m = rng(1,1000)
        x0 = np.array([-100, 500, -100])
        v0 = np.array([0,0,0])
        
        color_val = rngf() * 0.7 + 0.3
        color = [0.0, color_val, 0.0]

        coef_res = rngf() * 0.5 +0.5

        p = Particula(x0, v0, m, coef_res, color)
        sistema.agregar_particula(p)
    
    for _ in range(int(np.round(300 * nParticles, decimals=0))):
        m = rng(1,1000)
        x0 = np.array([0, 0, 0])
        v0 = np.array([rng(0,400) - 200, rng(0,1000), rng(0,800)-400])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, 0.0, 0.0]

        coef_res = rngf() * 0.5

        p = Particula(x0, v0, m, coef_res, color)
        sistema.agregar_particula(p)

    for _ in range(int(np.round(300 * nParticles, decimals=0))):
        m = rng(1,1000)
        x0 = np.array([100, 0, 100])
        v0 = np.array([-rng(0,200), rng(0,100), rng(0,200)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val, color_val, color_val]

        coef_res = 0.5

        p = Particula(x0, v0, m, coef_res, color)
        sistema.agregar_particula(p)
        
    for _ in range(int(np.round(300 * nParticles, decimals=0))):
        m = rng(1,1000)
        x0 = np.array([0, 0, 100])
        v0 = np.array([rng(0,200), rng(0,100), rng(0,200)])
        
        color_val = rngf() * 0.7 + 0.3
        color = [color_val*0.3, color_val*0.3, color_val]

        coef_res = 0.5

        p = Particula(x0, v0, m, coef_res, color)
        sistema.agregar_particula(p)

    sistema.aplicar_posiciones()
    
    render = Render(sistema, ancho=800, alto=600)
    render.inicializar()

    # Bucle principal controlado manualmente
    while True:
        #print(sistema.time)
        #sistema.time_tic()

        # Aplica fuerzas y actualiza el sistema
        fuerzas = np.array([gravedad])  # gravedad
        sistema.aplicar_fuerzas(fuerzas)
        sistema.aplicar_posiciones()
        
        # Actualiza la visualización
        render.actualizar_frame()

if __name__ == "__main__":
    titulo = " Práctica ejercicios de Sistema de partículas "
    texto = """ Integrantes
    Sofía Marín : Sergio Méndez : Sergio Palacios 
    """
    print_banner(texto, padding=2, border_char="═", corner_char="╔", title=titulo, align="center", color="bright_cyan")
    print("\n\n")
    print_wasd("Mover la camara:")
    print("\n\n")

    try:
        print("Simulaciones")
        print("1. Ejemplo 1 \n2. Ejemplo 2 \n3. Ejemplo 3 \n")

        simulacion = int(input("Simulacion seleccionada: "))
        if (not isinstance(simulacion, int)) or (simulacion > 3) or (simulacion < 1):
            raise ValueError("Opcion no disponible")
        
        print("\n\n")
        print("Metodo Numerico")
        print("1. Euler \n2. Runge Kutta  \n3. Verlet \n")
        
        metodo = int(input("Metodo seleccionado: "))
        if (not isinstance(metodo, int)) or (metodo > 3) or (metodo < 1):
            raise ValueError("Opcion no disponible")
        
        print("\n\n")
        print("Cantidad de particulas")
        print("Aumentar la cantidad de particulas que aparecen en pantalla")
        print("siendo 1.0 son 1000 particulas")
        
        particulas = float(input("Aumento de particulas x"))
        if (particulas < 0.0):
            raise ValueError("Valor fuera del rango esperado")
        
        print("\n\n")
        print("Delta de Tiempo")
        print("Debe ser mayor a cero y menor a 1")
        
        dt = float(input("Paso: "))
        if (dt >= 1) or (dt <= 0):
            raise ValueError("Valor fuera del rango esperado")
        
        match simulacion:
            case 1:
                newSimulation_1(metodo, dt, particulas)
            case 2:
                newSimulation_2(metodo, dt, particulas)
            case 3:
                newSimulation_3(metodo, dt, particulas)

    except ValueError as e:
        print(f"Error detectado: {e}")