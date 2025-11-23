import numpy as np

from Cadena.link import Link
from Cadena.render import PandaRender
from direct.task import Task

# Constantes
dt = 0.01
g = [0.0, 0.0, -9.8]

# Links
linkPin1 = Link([ 1, 0, 2], [0, 0, 0], m=1.0)  # Link fijo (sin padre)
linkPin2 = Link([-1, 0, 2], [0, 0, 0], m=1.0)  # Link fijo (sin padre)

link1 = Link([ 0.5, 0, 1], [0, 0, 0], m=1.0, padre1=linkPin1)
link2 = Link([-0.5, 0, 1], [0, 0, 0], m=1.0, padre1=linkPin2)
link3 = Link([ 0, 1, 0], [0, 0, 0], m=1.0, padre1=link1, padre2=link2)

# Create renderer
renderer = PandaRender()
renderer.setup_camera_controls()

# Add objects to renderer with different colors
renderer.add_object(linkPin1, color=(0, 1, 0, 1))
renderer.add_object(linkPin2, color=(0, 1, 0, 1))
renderer.add_object(link1, color=(1, 0, 0, 1))
renderer.add_object(link2, color=(1, 0, 0, 1))
renderer.add_object(link3, color=(1, 0, 0, 1))

# Calcular Fuerzas
def sim_fuerzas():
    """
    Función encargada de sumar las fuerzas que
    interactuan en cada objeto
    """
    t = renderer.getTime()
    ruido =  renderer.getNoise(0.0)
    wind = np.array([np.sin(ruido), np.cos(ruido), np.sin(ruido)])

    link1.sumar_fuerzas([wind*10])

# Actualizar Posiciones
def sim_posiciones():
    """
    Función encargada de actualizar las posiciones
    de cada objeto
    """
    linkPin1.paso(dt, k=0, damping=1.0)

    link1.paso(dt, k=200, damping=1.0, gravedad=np.array(g))
    link2.paso(dt, k=200, damping=1.0, gravedad=np.array(g))
    link3.paso(dt, k=200, damping=1.0, gravedad=np.array(g))

# Bucle while
def simulacion(task):
    """
    Ciclo de simulación para Panda3D
    """
    sim_fuerzas()
    sim_posiciones()
    return Task.cont

renderer.taskMgr.add(simulacion, "MoveObjectsTask")

# Run the application
renderer.run()