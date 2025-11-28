import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ParticleSimulation.System import System

class Render:
    """
    Clase para visualizar la simulación de partículas usando OpenGL
    """
    def __init__(self, sistema:System, ancho=800, alto=600):
        """
        Inicializa el renderizador OpenGL
        
        Args:
            - sistema (System): Sistema de partículas a visualizar
            - ancho (int): Ancho de la ventana
            - alto (int): Alto de la ventana
        """
        self.sistema = sistema
        self.ancho = ancho
        self.alto = alto
        self.angulo_x = 0
        self.angulo_y = 0
        
    def inicializar(self):
        """
        Inicializa GLUT y configura OpenGL
        """
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.ancho, self.alto)
        glutCreateWindow(b"Simulacion de Particulas")
        
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        glutDisplayFunc(self.dibujar)
        glutIdleFunc(None)
        glutKeyboardFunc(self.teclado)
        
    def configurar_camara(self):
        """
        Configura la cámara y la proyección
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.ancho / self.alto, 1.0, 6000.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 4000, 0, 0, 0, 0, 1, 0)
        
        glRotatef(self.angulo_x, 1, 0, 0)
        glRotatef(self.angulo_y, 0, 1, 0)
    
    def dibujar_caja(self):
        """
        Dibuja los límites del mundo si están definidos
        """
        if self.sistema.limites is None:
            return
            
        xmin, xmax, ymin, ymax, zmin, zmax = self.sistema.limites
        
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        
        # Aristas inferiores
        glVertex3f(xmin, ymin, zmin)
        glVertex3f(xmax, ymin, zmin)
        
        glVertex3f(xmax, ymin, zmin)
        glVertex3f(xmax, ymax, zmin)
        
        glVertex3f(xmax, ymax, zmin)
        glVertex3f(xmin, ymax, zmin)
        
        glVertex3f(xmin, ymax, zmin)
        glVertex3f(xmin, ymin, zmin)
        
        # Aristas superiores
        glVertex3f(xmin, ymin, zmax)
        glVertex3f(xmax, ymin, zmax)
        
        glVertex3f(xmax, ymin, zmax)
        glVertex3f(xmax, ymax, zmax)
        
        glVertex3f(xmax, ymax, zmax)
        glVertex3f(xmin, ymax, zmax)
        
        glVertex3f(xmin, ymax, zmax)
        glVertex3f(xmin, ymin, zmax)
        
        # Aristas verticales
        glVertex3f(xmin, ymin, zmin)
        glVertex3f(xmin, ymin, zmax)
        
        glVertex3f(xmax, ymin, zmin)
        glVertex3f(xmax, ymin, zmax)
        
        glVertex3f(xmax, ymax, zmin)
        glVertex3f(xmax, ymax, zmax)
        
        glVertex3f(xmin, ymax, zmin)
        glVertex3f(xmin, ymax, zmax)
        
        glEnd()
    
    def dibujar_particula(self, particula):
        """
        Dibuja una partícula como una esfera
        
        Args:
            - particula (Particula): Partícula a dibujar
        """
        x, y, z = particula.y[:3]
        
        # Radio proporcional a la masa (radio = masa^(1/3) * factor_escala)
        radio = (particula.m ** (1.0/3.0)) * 2.0
        
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(particula.color[0], particula.color[1], particula.color[2])
        
        # Dibuja esfera usando cuadriláteros
        quadric = gluNewQuadric()
        gluSphere(quadric, radio, 20, 20)
        gluDeleteQuadric(quadric)
        
        glPopMatrix()

    def dibujar_texto(self, x, y, texto):
        """
        Dibuja texto en coordenadas de pantalla 2D
        
        Args:
            - x (int): Posición x en pantalla
            - y (int): Posición y en pantalla
            - texto (str): Texto a dibujar
        """
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.ancho, 0, self.alto)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(x, y)
        
        for caracter in texto:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(caracter))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def dibujar(self):
        """
        Función de renderizado principal
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.configurar_camara()
        self.dibujar_caja()
        
        for particula in self.sistema.particulas:
            self.dibujar_particula(particula)
        
        self.dibujar_texto(10, self.alto - 30, "Hecho por:")
        self.dibujar_texto(20, self.alto - 60, "Sofia Marin")
        self.dibujar_texto(20, self.alto - 90, "Sergio Mendez")
        self.dibujar_texto(20, self.alto - 120, "Sergio Palacios")
        self.dibujar_texto(10, 10, "Mover la camara con W-A-S-D")
        glutSwapBuffers()
    
    def teclado(self, key, x, y):
        """
        Maneja eventos del teclado
        
        Args:
            - key (bytes): Tecla presionada
            - x (int): Posición x del mouse
            - y (int): Posición y del mouse
        """
        if key == b'q' or key == b'\x1b':  # 'q' o ESC
            glutLeaveMainLoop()
        elif key == b'w':
            self.angulo_x += 5
        elif key == b's':
            self.angulo_x -= 5
        elif key == b'a':
            self.angulo_y -= 5
        elif key == b'd':
            self.angulo_y += 5
    
    def actualizar_frame(self):
        """
        Actualiza un frame de la visualización
        Debe ser llamado desde un bucle externo
        """
        glutMainLoopEvent()
        glutPostRedisplay()