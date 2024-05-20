# coding=utf-8
"""Tarea 2
Monserrat Montero Troncoso
21.090.341-0
"""

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
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath
import random

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# puntos de control
P = [[-5, -7], [-10, 2.5], [5, 0], [5, 7]]

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([20,20,20])
        self.camUp = np.array([0, 1, 0])
        self.distance = 20


controller = Controller()

def bezierCurve(t, P0, P1, P2, P3):
    return P0 * pow(1-t, 3) + P1 * 3 * t * pow(1-t, 2) + P2 * 3 * pow(t, 2) * (1-t) + P3 * pow(t, 3)


def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

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
    
    elif key == glfw.KEY_1:
        controller.viewPos = np.array([controller.distance,controller.distance,controller.distance]) #Vista diagonal 1
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0,0,controller.distance]) #Vista frontal
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance,0,0]) #Vista lateral
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0,controller.distance,0]) #Vista superior
        controller.camUp = np.array([0,0,1])
    
    elif key == glfw.KEY_5:
        controller.viewPos = np.array([-controller.distance,controller.distance,controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    else:
        print('Unknown key')

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

"""------------------ Funciónes para crear los elementos de escena -------------------"""
#NOTA: Aqui creas tu escena. En escencia, sólo tendrías que modificar esta función.
def createLibelula(pipeline, colores):
    rBody,gBody,bBody = colores[0]
    rWinsSup,gWingsSup,bWingsSup = colores[1]
    rWinsInf,gWingsSInf,bWingsInf = colores[2]
    # Creating shapes on GPU memory

    wingSupTriangle = bs.createColorTriangle(rWinsSup,gWingsSup,bWingsSup)
    gpuWingSupTriangle = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWingSupTriangle)
    gpuWingSupTriangle.fillBuffers(wingSupTriangle.vertices, wingSupTriangle.indices, GL_STATIC_DRAW)

    wingInfTriangle = bs.createColorTriangleEsc(rWinsInf,gWingsSInf,bWingsInf)
    gpuWingInfTriangle = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWingInfTriangle)
    gpuWingInfTriangle.fillBuffers(wingInfTriangle.vertices, wingInfTriangle.indices, GL_STATIC_DRAW)

    bodySphere = bs.createColorSphereTarea2(rBody,gBody,bBody)
    gpuBodySphere = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBodySphere)
    gpuBodySphere.fillBuffers(bodySphere.vertices, bodySphere.indices, GL_STATIC_DRAW)
    
    tailCube = bs.createColorCube(rBody,gBody,bBody)
    gpuTailCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTailCube)
    gpuTailCube.fillBuffers(tailCube.vertices, tailCube.indices, GL_STATIC_DRAW)

    # Idear un ala superior
    wingSup = sg.SceneGraphNode("wing")
    wingSup.transform = tr.scale(-1, -2, 0)
    wingSup.childs += [gpuWingSupTriangle]

    # Idear un ala inferior
    wingInf = sg.SceneGraphNode("wing")
    wingInf.transform = tr.scale(-1, -2, 0)
    wingInf.childs += [gpuWingInfTriangle]


    # Instanciating 2 wings superiores
    supWing1 = sg.SceneGraphNode("SupWing1")
    supWing1.transform = tr.matmul([
            tr.translate(0.1,0.2,0.4),
            tr.rotationZ((np.pi/180)*20),
            tr.rotationX((np.pi/180)*12),
            tr.rotationY((np.pi/180)*90)
            
    ])
    supWing1.childs += [wingSup]

    supWing2 = sg.SceneGraphNode("SupWing2")
    supWing2.transform = tr.matmul([
            tr.translate(-0.1,0.2,0.4),
            tr.rotationY((np.pi/180)*90),
            tr.rotationZ((np.pi/180)*20),
            tr.rotationX((np.pi/180)*-12)
            
    ])
    supWing2.childs += [wingSup]

    # Instanciating 2 wings inferiores
    infWing1 = sg.SceneGraphNode("InfWing1")
    infWing1.transform = tr.matmul([
            tr.translate(-0.38,0.5,0),
            tr.rotationY((np.pi/180)*-90),
            #tr.rotationZ((np.pi/180)*20),
            #tr.rotationX((np.pi/180)*-12)
            
    ])
    infWing1.childs += [wingInf]

    infWing2 = sg.SceneGraphNode("InfWing2")
    infWing2.transform = tr.matmul([
            tr.translate(0.38,0.5,0),
            tr.rotationY((np.pi/180)*-90),
            #tr.rotationZ((np.pi/180)*20),
            #tr.rotationX((np.pi/180)*12)
            
    ])
    infWing2.childs += [wingInf]
    
    # Creating the body
    body = sg.SceneGraphNode("Body")
    body.transform = tr.matmul([
            tr.rotationX((np.pi/180)*-5),
            tr.scale(0.38,0.75,0.5)
            
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
    libelula.childs += [supWing2]
    libelula.childs += [infWing1]
    libelula.childs += [infWing2]
    return libelula

def crearSuelo(pipeline):
    cuadradoCafe = bs.createColorCube(58/255, 53/255, 5/255)
    gpuCuadradoCafe = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCuadradoCafe)
    gpuCuadradoCafe.fillBuffers(cuadradoCafe.vertices, cuadradoCafe.indices, GL_STATIC_DRAW)

    #suelo
    suelo = sg.SceneGraphNode("suelo")
    suelo.transform= tr.matmul([
        tr.translate(0,0,-50),
        tr.scale(100,100,100)])
    
    
    suelo.childs = [gpuCuadradoCafe]

    suelofinal = sg.SceneGraphNode("suelofinal")
    suelofinal.childs += [suelo]

    return suelofinal

def crearRamitas(pipeline):
    cilindrosVerdes = bs.createColorCylinderTarea2(71/255,146/255,31/255)
    gpuCilindrosVerdes = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCilindrosVerdes)
    gpuCilindrosVerdes.fillBuffers(cilindrosVerdes.vertices,cilindrosVerdes.indices,GL_STATIC_DRAW)

    esferasRojas = bs.createColorSphereTarea2(198/255,48/255,48/255)
    gpuEsferasRojas = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEsferasRojas)
    gpuEsferasRojas.fillBuffers(esferasRojas.vertices,esferasRojas.indices,GL_STATIC_DRAW)

    #Ramita Principal
    ramitaPrincipal = sg.SceneGraphNode("ramitaPrincipal")
    ramitaPrincipal.transform = tr.matmul([
        tr.translate(0,0,1),
        tr.rotationX((np.pi/180)*90),
        tr.scale(0.2,5,0.2)
    ])
    ramitaPrincipal.childs += [gpuCilindrosVerdes]

    #RamitasHijas y sus flores
    ramitaHija1 = sg.SceneGraphNode("ramitaPrincipal")
    ramitaHija1.transform = tr.matmul([
        tr.translate(0,1.3,1),
        tr.rotationX((np.pi/180)*25),
        tr.scale(0.15,1.4,0.15)
    ])
    ramitaHija1.childs += [gpuCilindrosVerdes]

    ramitaHija2 = sg.SceneGraphNode("ramitaPrincipal")
    ramitaHija2.transform = tr.matmul([
        tr.translate(-1.3,0,1),
        tr.rotationZ((np.pi/180)*90),
        tr.rotationX((np.pi/180)*25),
        tr.scale(0.15,1.4,0.15)
    ])
    ramitaHija2.childs += [gpuCilindrosVerdes]

    ramitaHija3 = sg.SceneGraphNode("ramitaPrincipal")
    ramitaHija3.transform = tr.matmul([
        tr.translate(0,-1.3,1),
        tr.rotationX((np.pi/180)*-25),
        tr.scale(0.15,1.4,0.15)
    ])
    ramitaHija3.childs += [gpuCilindrosVerdes]


    ramitaHija4 = sg.SceneGraphNode("ramitaPrincipal")
    ramitaHija4.transform = tr.matmul([
        tr.translate(1.3,0,1),
        tr.rotationZ((np.pi/180)*90),
        tr.rotationX((np.pi/180)*-25),
        tr.scale(0.15,1.4,0.15)
    ])
    ramitaHija4.childs += [gpuCilindrosVerdes]

    conjuntoRamitas = sg.SceneGraphNode("conjuntoRamitas")
    conjuntoRamitas.childs += [ramitaHija1]
    conjuntoRamitas.childs += [ramitaHija2]
    conjuntoRamitas.childs += [ramitaHija3]
    conjuntoRamitas.childs += [ramitaHija4]

    #Conjunto de ramitas
    c1 = sg.SceneGraphNode("c1")
    c1.childs +=  [conjuntoRamitas]

    c2 = sg.SceneGraphNode("c2")
    c2.transform = tr.translate(0,0,2.25)
    c2.childs +=  [conjuntoRamitas]

    c3 = sg.SceneGraphNode("c3")
    c3.transform = tr.translate(0,0,4.5)
    c3.childs +=  [conjuntoRamitas]


    ramitaFinal = sg.SceneGraphNode("ramitaFinal")
    ramitaFinal.childs += [ramitaPrincipal]
    ramitaFinal.childs += [c1]
    ramitaFinal.childs += [c2]
    ramitaFinal.childs += [c3]
    

    return ramitaFinal




"""------------------ ------------------- ------------------- -------------------"""

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "tarea 2"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(214/255, 225/255, 105/255, 1.0)

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
    redCarNode.transform = tr.matmul([
        tr.translate(0,0,2)
    ])
    sueloNode = crearSuelo(mvpPipeline)
    ramita1Node = crearRamitas(mvpPipeline)
    ramita1Node.transform = tr.matmul([
        tr.translate(-3,-4,-0.5),
        tr.scale(0.4,0.4,1)
    ])

    ramita2Node = crearRamitas(mvpPipeline)
    ramita2Node.transform = tr.matmul([
        tr.translate(-5,5,1),
        tr.scale(0.4,0.4,1)
    ])
    ramita3Node = crearRamitas(mvpPipeline)
    ramita3Node.transform = tr.matmul([
        tr.translate(2,-2,-0.5),
        tr.scale(0.4,0.4,1)
    ])
    ramita4Node = crearRamitas(mvpPipeline)
    ramita4Node.transform = tr.matmul([
        tr.translate(0,6,1),
        tr.scale(0.4,0.4,1)
    ])

    ramita5Node = crearRamitas(mvpPipeline)
    ramita5Node.transform = tr.matmul([
        tr.translate(0,-8,1),
        tr.scale(0.4,0.4,1)
    ])

    ramita6Node = crearRamitas(mvpPipeline)
    ramita6Node.transform = tr.matmul([
        tr.translate(-8,3,1),
        tr.scale(0.4,0.4,1)
    ])

    ramita7Node = crearRamitas(mvpPipeline)
    ramita7Node.transform = tr.matmul([
        tr.translate(3,7,1),
        tr.scale(0.4,0.4,1)
    ])

    ramita8Node = crearRamitas(mvpPipeline)
    ramita8Node.transform = tr.matmul([
        tr.translate(4,-7,1),
        tr.scale(0.4,0.4,1)
    ])

    ramita9Node = crearRamitas(mvpPipeline)
    ramita9Node.transform = tr.matmul([
        tr.translate(4,-3,1),
        tr.scale(0.4,0.4,1)
    ])

    # Función para crear ramitas en posiciones aleatorias fuera del rango [-7, 7]
    def crearRamitasAleatorias(mvpPipeline, num_ramitas, min_val=-10, max_val=10, exclusion_range=7):
        ramitas = []
        for _ in range(num_ramitas):
            while True:
                x = random.uniform(min_val, max_val)
                y = random.uniform(min_val, max_val)
                # Asegurarse de que la ramita esté fuera del cuadrado [-7, 7]
                if abs(x) > exclusion_range or abs(y) > exclusion_range:
                    break
            ramitaNode = crearRamitas(mvpPipeline)
            ramitaNode.transform = tr.matmul([
                tr.translate(x, y, 1),
                tr.scale(0.4, 0.4, 1)
            ])
            ramitas.append(ramitaNode)
        return ramitas

    # Crear 10 ramitas adicionales fuera del rango [-7, 7]
    ramitasAdicionales = crearRamitasAleatorias(mvpPipeline, 10)

    

    """------------------ ------------------- ------------------- -------------------"""

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        deltaTime = perfMonitor.getDeltaTime()
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

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)
        
        
        """------------------ Movimiento de la libelula -------------------"""
        
        # oscila entre 0 y 1
        t = np.sin(glfw.get_time())*0.5 + 0.5

        LibX = bezierCurve(t,P[0][0], P[1][0], P[2][0], P[3][0])
        LibY = bezierCurve(t, P[0][1], P[1][1], P[2][1], P[3][1])
        LibZ = (np.sin(glfw.get_time() * 2)*0.5) + 2

        redCarNode.transform = tr.translate(LibX,LibY,LibZ)
        print(LibZ)

        wingSup1MoveNode = sg.findNode(redCarNode,"SupWing1")
        wingSup1MoveNode.transform = tr.matmul([
                            tr.translate(0.1,0.2,0.4),
                            tr.rotationZ((np.pi/180)*-20),
                            tr.rotationX((np.pi/180)*12),
                            tr.rotationY(np.sin(t*40) + (np.pi/180)*90)
                            
                            
                    ])
        
        wingSup2MoveNode = sg.findNode(redCarNode,"SupWing2")
        wingSup2MoveNode.transform = tr.matmul([
                            tr.translate(-0.1,0.2,0.4),
                            tr.rotationZ((np.pi/180)*20),
                            tr.rotationX((np.pi/180)*12),
                            tr.rotationY(-np.sin(t*40) + (np.pi/180)*90)
                            
                    ])
        
        wingInf1MoveNode = sg.findNode(redCarNode,"InfWing1")
        wingInf1MoveNode.transform = tr.matmul([
                            #tr.translate(0,0,0),
                            tr.translate(-0.38,0.5,0),
                            #tr.rotationX((np.pi/180)*-12),
                            #tr.rotationZ((np.pi/180)*20),
                            tr.rotationY(-np.sin(t*60)*1.3 + (np.pi/180)*-25),   
                    ])
        
        wingInf2MoveNode = sg.findNode(redCarNode,"InfWing2")
        wingInf2MoveNode.transform = tr.matmul([
                            #tr.translate(0,0,0),
                            tr.translate(0.38,0.5,0),
                            #tr.rotationX((np.pi/180)*-12),
                            #tr.rotationZ((np.pi/180)*20),
                            tr.rotationY(np.sin(t*60)*1.3 + (np.pi/180)*-155),   
                    ])
        


                
        """------------------ ------------------- ------------------- -------------------"""

        # Drawing the Car
        sg.drawSceneGraphNode(redCarNode, mvpPipeline, "model")
        sg.drawSceneGraphNode(ramita1Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita2Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita3Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita4Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita5Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita6Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita7Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita8Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(ramita9Node,mvpPipeline,"model")
        sg.drawSceneGraphNode(sueloNode,mvpPipeline,"model")
        

        # Agregar las nuevas ramitas a la escena o a la estructura de datos correspondiente
        for ramita in ramitasAdicionales:
            sg.drawSceneGraphNode(ramita,mvpPipeline,"model")
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    redCarNode.clear()
    

    glfw.terminate()