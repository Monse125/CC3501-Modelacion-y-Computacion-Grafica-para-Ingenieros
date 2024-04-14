# coding=utf-8
"""Código de Ejemplo Auxiliar 2"""

import pyglet
from OpenGL.GL import *

from math import cos, sin

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica import basic_shapes as bs
from grafica import easy_shaders as es
from grafica import transformations as tr
from shapes_utils import HighLevelGPUShape, createGPUShape

class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Pyglet window"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.pipeline = None
        self.repeats = 0

# Controlador que permite comunicarse con la ventana de pyglet
class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Auxiliar 2"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.pipeline = None
        self.repeats = 0
        self.triangleSpeed = 0
        self.trianglePosX = 0

# Se asigna el ancho y alto de la ventana y se crea.
WIDTH, HEIGHT = 1280, 800
controller = Controller(width=WIDTH, height=HEIGHT)
# Se asigna el color de fondo de la ventana
glClearColor(0.15, 0.15, 0.15, 1.0)

# Se configura el pipeline y se le dice a OpenGL que utilice ese shader
pipeline = es.SimpleTransformShaderProgram()
controller.pipeline = pipeline
glUseProgram(pipeline.shaderProgram)

# Se crea una figura GPU para luego dibujarla.
gpuTriangle = HighLevelGPUShape(pipeline, bs.createRainbowTriangle())

# Función que dibuja un triángulo con shearing
def draw_shearing_triangle(controller: Controller):
    gpuTriangle._transform = tr.matmul([
        tr.translate(controller.trianglePosX, -0.5, 0),
        tr.shearing(0.3 * sin(controller.total_time), 0, 0, 0, 0, 0),
        tr.uniformScale(0.7)
    ])
    gpuTriangle.draw(controller.pipeline)

# Función que dibuja un triángulo rotando
def draw_rotating_triangle(controller: Controller):
    gpuTriangle._transform = tr.identity()  # Make the transform neutral again
    gpuTriangle.rotation = tr.rotationZ(controller.total_time)
    gpuTriangle.translation = tr.translate(-0.5 * cos(controller.total_time), 0.5 * sin(controller.total_time), 0.0)
    gpuTriangle.scale = tr.uniformScale(0.3)
    gpuTriangle.draw(controller.pipeline)

# El controlador puede recibir inputs del usuario. Estas funciones define cómo manejarlos.
@controller.event
def on_key_press(symbol, modifiers):
    controller.triangleSpeed = 0

    if symbol == pyglet.window.key.SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()
    
    elif symbol == pyglet.window.key.LEFT:
        controller.triangleSpeed -= 1

    elif symbol == pyglet.window.key.RIGHT:
        controller.triangleSpeed += 1

@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.LEFT:
        controller.triangleSpeed = 0

    elif symbol == pyglet.window.key.RIGHT:
        controller.triangleSpeed = 0

# Esta función se ejecuta aproximadamente 60 veces por segundo, dt es el tiempo entre la última
# ejecución y ahora
def update(dt, controller):
    controller.total_time += dt
    controller.trianglePosX += controller.triangleSpeed * dt

# Cada vez que se llama update(), se llama esta función también
@controller.event
def on_draw():
    controller.clear()

    # Si el controller está en modo fillPolygon, dibuja polígonos. Si no, líneas.
    if controller.fillPolygon:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    # Dibuja las figuras
    draw_shearing_triangle(controller)
    draw_rotating_triangle(controller)

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()
