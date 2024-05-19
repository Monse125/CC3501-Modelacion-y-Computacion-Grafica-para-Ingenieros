"""
Monserrat Montero Troncoso
21.090.341-0
monserrat.montero@ug.uchile.cl

"""

# coding=utf-8
"""Drawing 3D cars via scene graph"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.performance_monitor as pm

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')

"""------------------ Funciónes para crear los elementos de escena -------------------"""
def createLibelula(pipeline, colores):
    rBody,gBody,bBody = colores[0]
    rWinsSup,gWingsSup,bWingsSup = colores[1]
    rWinsInf,gWingsSInf,bWingsInf = colores[1]
    # Creating shapes on GPU memory
    wingTriangle = bs.createColorTriangle(rWinsSup,gWingsSup,bWingsSup)
    gpuWingTriangle = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWingTriangle)
    gpuWingTriangle.fillBuffers(wingTriangle.vertices, wingTriangle.indices, GL_STATIC_DRAW)

    bodySphere = bs.createColorSphereTarea2(rBody,gBody,bBody)
    gpuBodySphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBodySphere)
    gpuBodySphere.fillBuffers(bodySphere.vertices, bodySphere.indices, GL_STATIC_DRAW)
    
    tailCube = bs.createColorCube(rBody,gBody,bBody)
    gpuTailCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTailCube)
    gpuTailCube.fillBuffers(tailCube.vertices, tailCube.indices, GL_STATIC_DRAW)

    # Idear un ala superior
    wing = sg.SceneGraphNode("wing")
    wing.transform = tr.scale(0.17, 0.33, 0)
    wing.childs += [gpuWingTriangle]

    wingMoving = sg.SceneGraphNode("wingMoving")
    wingMoving.childs += [wing]


    # Instanciating 4 wings
    supWing1 = sg.SceneGraphNode("SupWing1")
    supWing1.transform = tr.translate(0.3,0,-0.3)
    supWing1.childs += [wingMoving]

    SupWing2 = sg.SceneGraphNode("SupWing2")
    SupWing2.transform = tr.translate(0.3,0,-0.3)
    SupWing2.childs += [wingMoving]

    infWing1 = sg.SceneGraphNode("InfWing1")
    infWing1.transform = tr.translate(-0.3,0,-0.3)
    infWing1.childs += [wingMoving]

    infWing2 = sg.SceneGraphNode("InfWing2")
    infWing2.transform = tr.translate(-0.3,0,-0.3)
    infWing2.childs += [wingMoving]
    
    # Creating the body
    body = sg.SceneGraphNode("Body")
    body.transform = tr.matmul([
            tr.rotationX((np.pi/180)*-5),
            tr.scale(0.5,0.75,0.5)
            
    ])
    body.childs += [gpuBodySphere]

    # Creating the head
    head = sg.SceneGraphNode("Head")
    head.transform = tr.matmul([
            tr.scale(0.40,0.40,0.50),
            tr.translate(0,-2.5,0.5)
    ])
    head.childs += [gpuBodySphere]

    # Creating the tail
    tail = sg.SceneGraphNode("Tail")
    tail.transform = tr.matmul([
            tr.translate(0,1.8,-0.2),
            tr.rotationX((np.pi/180)*-10),
            tr.scale(0.2,2.4,0.2)
            
    ])
    tail.childs += [gpuTailCube]

    # All pieces together
    libelula = sg.SceneGraphNode("libelula")
    libelula.childs += [body]
    libelula.childs += [head]
    libelula.childs += [tail]
    libelula.childs += [supWing1]
    return libelula






"""------------------ ------------------- ------------------- -------------------"""

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600
    title = "3D cars via scene graph"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    """------------------ Colores de las partes de la libélula -------------------"""
    
    color_alas_fondo_pequeñas = [125/255, 51/255, 181/255]
    color_alas_frente_pequeñas = [181/255, 83/255, 255/255]
    color_alas_frente_grandes = [255/255, 83/255, 228/255]
    color_alas_fondo_grandes = [182/255, 67/255, 164/255]
    color_body = [53/255, 199/255, 255/255]

    colores_libelula = [color_body, color_alas_frente_grandes, color_alas_frente_pequeñas]

    """------------------ Instancia de libelula -------------------"""
    redCarNode = createLibelula(mvpPipeline, colores_libelula)



    """------------------ ------------------- ------------------- -------------------"""
    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    view = tr.lookAt(
            np.array([5,5,7]),
            np.array([0,0,0]),
            np.array([0,0,1])
        )
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        """------------------ Movimiento de la libelula -------------------"""
        """
        # Moving the red car and rotating its wheels
        redCarNode.transform = tr.translate(3 * np.sin( glfw.get_time() ),0,0.5)
        redWheelRotationNode = sg.findNode(redCarNode, "wheelRotation")
        redWheelRotationNode.transform = tr.rotationY(-10 * glfw.get_time())

        # Uncomment to print the red car position on every iteration
        #print(sg.findPosition(redCarNode, "car"))"""
        """------------------ ------------------- ------------------- -------------------"""
        # Drawing the Car
        sg.drawSceneGraphNode(redCarNode, mvpPipeline, "model")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    redCarNode.clear()

    glfw.terminate()