import numpy as np

from Cadena.link import Link
from Cadena.render import PandaRender
from direct.task import Task

# Constantes
dt = 0.01
g = [0.0, 0.0, -9.8]

# Links

link1 = Link([0, 0, 2], [0, 0, 0], m=1.0)  # Link fijo (sin padre)
link2 = Link([0, 1, 1], [0, 0, 0], m=1.0, padre=link1)
link3 = Link([2, 0, 0], [0, 0, 0], m=1.0, padre=link2)

# Create renderer
renderer = PandaRender()
renderer.setup_camera_controls()

# Add objects to renderer with different colors
renderer.add_object(link1, color=(1, 0, 0, 1))
renderer.add_object(link2, color=(1, 0, 0, 1))
renderer.add_object(link3, color=(1, 0, 0, 1))

# Task to update object positions
def move_objects(task):
    # El primer link podría estar fijo
    # link1.paso(dt)  # Comentado si queremos que esté fijo
    
    link2.paso(dt, k=200, damping=1.0, gravedad=np.array(g))
    link3.paso(dt, k=200, damping=1.0, gravedad=np.array(g))
    return Task.cont

renderer.taskMgr.add(move_objects, "MoveObjectsTask")

# Run the application
renderer.run()