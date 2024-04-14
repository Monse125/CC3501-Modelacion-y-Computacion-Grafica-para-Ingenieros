"""
Monserrat Montero Troncoso
21.090.341-0
monserrat.montero@ug.uchile.cl

"""


import pyglet
from OpenGL import GL
import numpy as np
import utils.shapes as shapes
import utils.transformations as tr
import os

from pathlib import Path

WIDTH = 1000
HEIGHT = 700
TIME = 0

#Se define el controlador de la ventana pyglet
class Controller(pyglet.window.Window):
    def __init__(self, title, *args, **kargs):
        super().__init__(*args, **kargs)
        # Evita error cuando se redimensiona a 0
        self.set_minimum_size(240, 240)
        self.set_caption(title)

    def update(self, dt):
        pass

#Clase que nos ayudará a dibujar 
class Model():
    def __init__(self, position_data, color_data, index_data=None):
        self.position_data = position_data
        self.color_data = color_data

        self.index_data = index_data
        if index_data is not None:
            self.index_data = np.array(index_data, dtype=np.uint32)

        self.gpu_data = None

        # Calcular el centro de la libélula
        min_x = min(self.position_data[::3])
        max_x = max(self.position_data[::3])
        min_y = min(self.position_data[1::3])
        max_y = max(self.position_data[1::3])
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        # Establecer la posición en el centro de la libélula
        self.position = np.array([center_x, center_y, 0], dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)
        self.scale = np.array([1, 1, 1], dtype=np.float32)

    def init_gpu_data(self, pipeline):
        if self.index_data is not None:
            self.gpu_data = pipeline.vertex_list_indexed(
                len(self.position_data) // 3, GL.GL_TRIANGLES, self.index_data)
        else:
            self.gpu_data = pipeline.vertex_list(
                len(self.position_data) // 3, GL.GL_TRIANGLES)

        self.gpu_data.position[:] = self.position_data
        self.gpu_data.color[:] = self.color_data

    def draw(self, mode=GL.GL_TRIANGLES):
        self.gpu_data.draw(mode)

    def get_transform(self):
        translation_matrix = tr.translate(
            self.position[0], self.position[1], self.position[2])
        rotation_matrix = tr.rotationX(
            self.rotation[0]) @ tr.rotationY(self.rotation[1]) @ tr.rotationZ(self.rotation[2])
        scale_matrix = tr.scale(self.scale[0], self.scale[1], self.scale[2])
        transformation = translation_matrix @ rotation_matrix @ scale_matrix
        return np.reshape(transformation, (16, 1), order="F")





# programa principal
if __name__ == "__main__":

    """------------------ Preparación para la construcción -------------------"""
    # creamos una instancia del controlador
    controller = Controller("Libélula en Movimiento", width=WIDTH,
                            height=HEIGHT, resizable=True)
    
    with open(Path(os.path.dirname(__file__)) / "shaders/transform.vert") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "shaders/color.frag") as f:
        fragment_source_code = f.read()

    # Compilación de shaders
    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(
        fragment_source_code, "fragment")
    # Creación del pipeline
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    """------------------ Colores de las partes de la libélula -------------------"""
    
    color_alas_fondo = [61/255, 199/255, 203/255]
    color_alas_frente = [64/255, 252/255, 255/255]
    colors_body = [60/255, 0/255, 255/255]


    intensities_body = [1]*10
    

    """------------------ Creación de las partes de la libélula -------------------"""
    body = Model(shapes.Body['position'], colors_body* 10, shapes.Body['index'])
    body.init_gpu_data(pipeline)
    body.scale = np.array([1/24, 1/24, 1/24], dtype=np.float32)
    body.position = np.array([0+1,0,0], dtype=np.float32)

    cabeza = Model(
        shapes.Circle["position"], colors_body* 36, shapes.Circle['indices'])
    cabeza.init_gpu_data(pipeline)
    cabeza.scale = np.array([1/18, 1/18, 1/18], dtype=np.float32)
    cabeza.position = np.array([-0.32+1, 0.08, 0], dtype=np.float32)

    #Alas pequeñas
    ala_pequeña_frente = Model(shapes.Triangle["position"], color_alas_frente*3)
    ala_pequeña_frente.init_gpu_data(pipeline)
    ala_pequeña_frente.scale = np.array([0.17, 0.33, 0], dtype=np.float32)
    ala_pequeña_frente.rotation[2] = (np.pi/180) * 122
    ala_pequeña_frente.position = np.array([-0.18+1, 0.07, 0], dtype=np.float32)

    ala_pequeña_fondo = Model(shapes.Triangle["position"], color_alas_fondo*3)
    ala_pequeña_fondo.init_gpu_data(pipeline)
    ala_pequeña_fondo.scale = np.array([0.15, 0.33, 0], dtype=np.float32)
    ala_pequeña_fondo.rotation[2] = (np.pi/180) * 130
    ala_pequeña_fondo.position = np.array([-0.18+1, 0.07, 0], dtype=np.float32)

    #Alas grandes
    ala_grande_frente = Model(shapes.TriangleEsc["position"], color_alas_frente*3)
    ala_grande_frente.init_gpu_data(pipeline)
    ala_grande_frente.scale = np.array([0.3, 0.15, 0], dtype=np.float32)
    ala_grande_frente.rotation[2] = (np.pi/180) * 10
    ala_grande_frente.position = np.array([-0.15+1, 0.01, 0], dtype=np.float32)

    
    ala_grande_fondo = Model(shapes.TriangleEsc["position"], color_alas_fondo*3)
    ala_grande_fondo.init_gpu_data(pipeline)
    ala_grande_fondo.scale = np.array([0.3, 0.15, 0], dtype=np.float32)
    ala_grande_fondo.rotation[2] = (np.pi/180) * 10
    ala_grande_fondo.position = np.array([-0.15+1, 0.01, 0], dtype=np.float32)


    """------------------ Definición del movimiento de la libélula y sus partes -------------------"""
    def update(dt):
        global TIME
        TIME += dt

        #Movimiento Alas pequeñas:
        ala_pequeña_fondo.rotation[0] = np.sin(4*TIME+0.3)*0.7 + np.pi/4
        ala_pequeña_frente.rotation[0] = np.sin(4*TIME)*0.7 - (3*np.pi)/4
        #Movimiento Alas grandes
        ala_grande_frente.rotation[0] = np.sin(4*TIME+0.3)*0.7 + np.pi/4
        ala_grande_fondo.rotation[0] = np.sin(4*TIME)*0.7 - (3*np.pi)/4

        #Movimiento horizontal
        if cabeza.position[0] <= -1.5:
            cabeza.position[0] += 2.5
            body.position[0] += 2.5
            ala_grande_frente.position[0] += 2.5
            ala_grande_fondo.position[0] += 2.5
            ala_pequeña_fondo.position[0] += 2.5
            ala_pequeña_frente.position[0] += 2.5
        cabeza.position[0] -= 0.004
        body.position[0] -= 0.004
        ala_grande_frente.position[0] -= 0.004
        ala_grande_fondo.position[0] -= 0.004
        ala_pequeña_fondo.position[0] -= 0.004
        ala_pequeña_frente.position[0] -= 0.004

        #Movimiento vertical
        body.position[1] = np.sin(TIME*2)/2
        cabeza.position[1]= np.sin(TIME*2)/2+0.08
        ala_grande_fondo.position[1]= np.sin(TIME*2)/2+0.01
        ala_grande_frente.position[1]= np.sin(TIME*2)/2+0.01
        ala_pequeña_fondo.position[1]= np.sin(TIME*2)/2+ 0.07
        ala_pequeña_frente.position[1]= np.sin(TIME*2)/2+ 0.07
              
        


    """------------------ Llamada del controlador -------------------"""
    @controller.event
    def on_draw():
        # color de fondo al limpiar un frame (0,0,0) es negro
        GL.glClearColor(147/255, 255/255, 132/255, 1.0)
        # si hay algo dibujado se limpia del frame
        controller.clear()
        # se le dice al pipeline que se va a usar
        pipeline.use()

        pipeline["u_transform"] = ala_pequeña_fondo.get_transform()
        ala_pequeña_fondo.draw()

        pipeline["u_transform"] = ala_grande_fondo.get_transform()
        ala_grande_fondo.draw()

        pipeline["u_transform"] = body.get_transform()
        body.draw(GL.GL_TRIANGLES)

        pipeline["u_transform"] = cabeza.get_transform()
        cabeza.draw(GL.GL_TRIANGLES)

        pipeline["u_transform"] = ala_pequeña_frente.get_transform()
        ala_pequeña_frente.draw()

        pipeline["u_transform"] = ala_grande_frente.get_transform()
        ala_grande_frente.draw()


    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()

    


    