"""
Monserrat Montero Troncoso
21.090.341-0
monserrat.montero@ug.uchile.cl

"""
import pyglet
from OpenGL.GL import *
import numpy as np
from shaders import easy_shaders as es
from shaders import lighting_shaders as ls
from shaders import basic_shapes as bs
from shaders import transformations as tr


WIDTH = 1000
HEIGHT = 700
TIME = 0

class Controller(pyglet.window.Window):
    def __init__(self, width, height, title="Tarea 2: Super Libelula"):
        super().__init__(width, height, title)
        self.set_minimum_size(240, 240)
        self.set_caption(title)
        self.fillPolygon = True
        self.showAxis = True
        self.camera_position_index = 0  # Índice para rastrear la posición actual de la cámara
        self.camera_positions = [
            np.array([6, 6, 7]),  # Posición original de la cámara
            np.array([0, 10, 10])  # Nueva posición de la cámara
        ]
        self.camera_position = self.camera_positions[self.camera_position_index]
        self.pipeline = None
        self.axis = None
        self.scene = None

        # Definir las coordenadas de los ejes
        self.axis_coords = {
            'x': (np.array([-10, 0, 0]), np.array([10, 0, 0])),
            'y': (np.array([0, -10, 0]), np.array([0, 10, 0])),
            'z': (np.array([0, 0, -10]), np.array([0, 0, 10]))
        }

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.camera_position_index = (self.camera_position_index + 1) % len(self.camera_positions)
            self.camera_position = self.camera_positions[self.camera_position_index]
            print("Cámara cambiada a posición:", self.camera_position)
        elif symbol == pyglet.window.key.LSHIFT:
            self.showAxis = not self.showAxis
            print("Show axis")
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()
            print("ByeBye")
        else:
            print('Unknown key')
    
    def draw_axis(self):
        glLineWidth(2)  # Establecer el ancho de la línea

        # Dibujar ejes X, Y y Z en rojo, verde y azul respectivamente
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)  # Rojo para el eje X
        glVertex3fv(self.axis_coords['x'][0])
        glVertex3fv(self.axis_coords['x'][1])

        glColor3f(0, 1, 0)  # Verde para el eje Y
        glVertex3fv(self.axis_coords['y'][0])
        glVertex3fv(self.axis_coords['y'][1])

        glColor3f(0, 0, 1)  # Azul para el eje Z
        glVertex3fv(self.axis_coords['z'][0])
        glVertex3fv(self.axis_coords['z'][1])
        glEnd()


if __name__ == "__main__":
    """------------------ Preparación para la construcción -------------------"""
    controller = Controller(width=WIDTH, height=HEIGHT)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()

    # Como trabajamos en 3D, necesitamos chequear cuáles objetos están en frente, y cuáles detrás.
    glEnable(GL_DEPTH_TEST)

    """------------------ Colores de los elementos en la escena -------------------"""


    """------------------ Creación de elementos en la escena -------------------"""


    """------------------ Definición del movimiento de la libélula y sus partes -------------------"""
    def update(dt):
        global TIME
        TIME += dt

    """------------------ Llamada del controlador -------------------"""
    @controller.event
    def on_draw():
        # color de fondo al limpiar un frame (0,0,0) es negro
        glClearColor(122/255, 226/255, 229/255, 1.0)
        # si hay algo dibujado se limpia del frame
        controller.clear()
        if controller.showAxis:
            controller.draw_axis()

    # Iniciar el bucle de la aplicación con actualizaciones regulares
    pyglet.clock.schedule_interval(controller.update, 1/60.0)
    pyglet.app.run()