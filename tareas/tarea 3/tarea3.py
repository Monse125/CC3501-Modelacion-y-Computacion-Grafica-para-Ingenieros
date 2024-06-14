# coding=utf-8
"""Tarea 3
Monserrat Montero Troncoso
21.090.341-0
"""

import glfw
from OpenGL.GL import *
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

cant_random = 40
dis_gen = 25
LIGHT_FLAT    = 0
LIGHT_GOURAUD = 1
LIGHT_PHONG   = 2

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([dis_gen*1.2,dis_gen/2,dis_gen/3])
        self.camUp = np.array([0, 0, 1])
        self.focusPoint = np.array([0, 0, 0])
        self.distance = 20


controller = Controller()

def bezierCurve(t, P0, P1, P2, P3):
    return P0 * pow(1-t, 3) + P1 * 3 * t * pow(1-t, 2) + P2 * 3 * pow(t, 2) * (1-t) + P3 * pow(t, 3)


def setPlot(texPipeline,pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

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

def setView(texPipeline,pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            controller.focusPoint,
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Fill Polygon")

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis
        print("Show Axis")

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        print("ByeBye")

 
    else:
        print('Unknown key')
    

def createOFFShape(pipeline, filename, r,g, b):
    shape = readOFF(getAssetPath(filename), (r, g, b))
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices,3), dtype=np.float32)
        print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  
        #print(faces)
        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        



        return bs.Shape(vertexDataF, indices)

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

def createTexturedArc(d):
    vertices = [d, 0.0, 0.0, 0.0, 0.0,
                d+1.0, 0.0, 0.0, 1.0, 0.0]
    
    currentIndex1 = 0
    currentIndex2 = 1

    indices = []

    cont = 1
    cont2 = 1

    for angle in range(4, 185, 5):
        angle = np.radians(angle)
        rot = tr.rotationY(angle)
        p1 = rot.dot(np.array([[d],[0],[0],[1]]))
        p2 = rot.dot(np.array([[d+1],[0],[0],[1]]))

        p1 = np.squeeze(p1)
        p2 = np.squeeze(p2)
        
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])
        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        
        indices.extend([currentIndex1, currentIndex2, currentIndex2+1])
        indices.extend([currentIndex2+1, currentIndex2+2, currentIndex1])

        if cont > 4:
            cont = 0


        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])

        currentIndex1 = currentIndex1 + 4
        currentIndex2 = currentIndex2 + 4
        cont2 = cont2 + 1
        cont = cont + 1

    return bs.Shape(vertices, indices)

def createTiledFloor(dim):
    vert = np.array([[-0.5,0.5,0.5,-0.5],[-0.5,-0.5,0.5,0.5],[0.0,0.0,0.0,0.0],[1.0,1.0,1.0,1.0]], np.float32)
    rot = tr.rotationX(-np.pi/2)
    vert = rot.dot(vert)

    indices = [
         0, 1, 2,
         2, 3, 0]

    vertFinal = []
    indexFinal = []
    cont = 0

    for i in range(-dim,dim,1):
        for j in range(-dim,dim,1):
            tra = tr.translate(i,0.0,j)
            newVert = tra.dot(vert)

            v = newVert[:,0][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 1])
            v = newVert[:,1][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 1])
            v = newVert[:,2][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 0])
            v = newVert[:,3][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 0])
            
            ind = [elem + cont for elem in indices]
            indexFinal.extend(ind)
            cont = cont + 4

    return bs.Shape(vertFinal, indexFinal)


"""------------------ Funciónes para crear los elementos de escena -------------------"""
#NOTA: Aqui creas tu escena. En escencia, sólo tendrías que modificar esta función.
def createLibelula(pipeline, colores):
    rBody,gBody,bBody = colores[0]
    rWinsSup,gWingsSup,bWingsSup = colores[1]
    rWinsInf,gWingsSInf,bWingsInf = colores[2]
    # Creating shapes on GPU memory

    wingSupTriangle = bs.createColorTriangle(rWinsSup,gWingsSup,bWingsSup)
    gpuWingSupTriangle = createGPUShape(pipeline,wingSupTriangle)

    wingInfTriangle = bs.createColorTriangleEsc(rWinsInf,gWingsSInf,bWingsInf)
    gpuWingInfTriangle = createGPUShape(pipeline,wingInfTriangle)

    bodySphere = bs.createColorSphereTarea2(rBody,gBody,bBody)
    gpuBodySphere = createGPUShape(pipeline,bodySphere)
    
    tailCube = bs.createColorCube(rBody,gBody,bBody)
    gpuTailCube = createGPUShape(pipeline,tailCube)

    # Idear un ala superior
    wingSup = sg.SceneGraphNode("wingS")
    wingSup.transform = tr.scale(-1, -2, 0)
    wingSup.childs += [gpuWingSupTriangle]

    # Idear un ala inferior
    wingInf = sg.SceneGraphNode("wingI")
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
    ##### CODIGO DEL SUELO #### 
    sandBaseShape = createGPUShape(pipeline, createTiledFloor(50))
    sandBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("suelo.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    sueloHorizontal = sg.SceneGraphNode('sueloH')
    sueloHorizontal.transform = tr.rotationX(np.pi/2)
    sueloHorizontal.childs += [sandBaseShape]

    sueloNode = sg.SceneGraphNode('suelo')
    sueloNode.childs += [sueloHorizontal]
    return sueloNode

def crearRamitas(pipeline):
    cilindrosVerdes = bs.createColorCylinderTarea2(71/255,146/255,31/255)
    gpuCilindrosVerdes = createGPUShape(pipeline,cilindrosVerdes)

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

def crearFlor(pipeline):
    gpuTalloVerde = createGPUShape(pipeline,bs.createTextureCube())
    gpuTalloVerde.texture = es.textureSimpleSetup(
        getAssetPath("tallo.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    gpuLavandas = createGPUShape(pipeline,bs.createTextureCube())
    gpuLavandas.texture = es.textureSimpleSetup(
        getAssetPath("lavanda.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)


    #Tallo
    tallo = sg.SceneGraphNode("tallo")
    tallo.transform = tr.matmul([
        tr.translate(0,0,1),
        tr.rotationX((np.pi/180)*90),
        tr.scale(0.1,6,0.1)
    ])
    tallo.childs += [gpuTalloVerde]

    #Flor
    flor = sg.SceneGraphNode("flor")
    flor.transform = tr.matmul([
        tr.translate(0,0,5),
        tr.rotationX((np.pi/180)*90),
        tr.scale(0.3,4,0.3)
    ])
    flor.childs += [gpuLavandas]

    lavandaFinal = sg.SceneGraphNode("lavandaFinal")
    lavandaFinal.childs += [tallo]
    lavandaFinal.childs += [flor]
    return lavandaFinal

def generarPosicionesPasto(num_pasto, min_val, max_val):
    posiciones = []
    while len(posiciones) < num_pasto:
        x = random.uniform(-max_val, max_val)
        y = random.uniform(-max_val, max_val)
        z = random.uniform(-1, 1)

        # Excluir el cuadrado central
        if not (min_val < abs(x) < max_val and min_val < abs(y) < max_val):
            posiciones.append((x, y, z))

    return posiciones

def crearColoredScene(pipeline):
    scene = sg.SceneGraphNode('ColoredSystem')  

    pos_ramitas= [(-3,-4,-0.5),(-5,5,1),(2,-2,-0.5),(0,6,1),(0,-8,1),(-8,3,1),(3,7,1),(4,-7,1),(4,-3,1)]
    nuevas_posiciones = generarPosicionesPasto(cant_random/0.75, 20, 30)
    pos_ramitas.extend(nuevas_posiciones)
    nuevas_posiciones = generarPosicionesPasto(cant_random, 30, 40)
    pos_ramitas.extend(nuevas_posiciones)
    for pos in pos_ramitas:
        ramitaNode = crearRamitas(pipeline)
        ramitaNode.transform = tr.matmul([
        tr.translate(pos[0],pos[1],pos[2]),
        tr.scale(0.4,0.4,1)
        ])
        scene.childs += [ramitaNode]
    return scene

def crearTexturedScene(pipeline):
    scene = sg.SceneGraphNode('TexturedSystem')

    pos_lavandas = [(3,10,0),(5,0,0),(1, 2, 0),(-4, -6, 0),(8, -3, 0),(-7, 5, 0),(0, -8, 0),(-10,-2,0),(-3,-15,0)]
    for pos in pos_lavandas:
        lavandaNode = crearFlor(pipeline)
        lavandaNode.transform = tr.matmul([
            tr.translate(pos[0],pos[1],pos[2])
        ])
        scene.childs += [lavandaNode]

    sueloNode = crearSuelo(pipeline)
    scene.childs += [sueloNode]

    return scene

    

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
    texPipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    
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
        tr.translate(0,0,4)
    ])
    escena_color= crearColoredScene(mvpPipeline)
    escena_textura = crearTexturedScene(texPipeline)

    

    

    """------------------ ------------------- ------------------- -------------------"""

    setPlot(texPipeline,pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    time_anterior = 0
    frente = False

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

        setView(texPipeline,pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)
        
        
        """------------------ Movimiento de la libelula -------------------"""
        """------------------ Setting camaras cinematic -------------------"""

        # puntos de control
        punto_cero = [-9, -11]
        punto_uno =  [9, 13]

        P1 = [punto_cero, [10, -2.5], [5, -0], punto_uno]

        P2 = [punto_cero, [-5, 3], [-4, 3],punto_uno]

    
        # oscila entre 0 y 1
        time = glfw.get_time()
        t = np.sin(glfw.get_time())*0.5 + 0.5
        LibZ = (np.sin(glfw.get_time() * 2)*0.5) + 2
        
        if time_anterior > t: #fase 1
            LibX = bezierCurve(t,P1[0][0], P1[1][0], P1[2][0], P1[3][0])
            LibY = bezierCurve(t, P1[0][1], P1[1][1], P1[2][1], P1[3][1]) 
            if t < 0.1: #c5
                controller.viewPos = np.array([-controller.distance,-controller.distance/2,controller.distance]) #Vista diagonal 2
                controller.camUp = np.array([0,0,1])
                controller.focusPoint = np.array([0, -1, 0])
            elif t < 0.7 and t > 0.1: #c3
                controller.viewPos = np.array([controller.distance,-1,5]) 
                controller.camUp = np.array([0,0,1])
                controller.focusPoint = np.array([0, 0, 0])
            else:
                controller.viewPos = np.array([controller.distance,controller.distance/2,controller.distance/2]) #Vista diagonal 1
                controller.camUp = np.array([0,0,1])
                controller.focusPoint = np.array([0, 8, 0]) #c1
            

        else: #fase 2
            #print("fase 2")
            LibX = bezierCurve(t,P2[0][0], P2[1][0], P2[2][0], P2[3][0])
            LibY = bezierCurve(t, P2[0][1], P2[1][1], P2[2][1], P2[3][1])
            if t < 0.4: #c5
                controller.viewPos = np.array([-controller.distance,-controller.distance/2,controller.distance]) #Vista diagonal 2
                controller.camUp = np.array([0,0,1])
                controller.focusPoint = np.array([0, -1, 0])#c5
            else:
                controller.viewPos = np.array([controller.distance,controller.distance/2,controller.distance/2]) #Vista diagonal 1
                controller.camUp = np.array([0,0,1])
                controller.focusPoint = np.array([0, 8, 0]) #c1


        
        redCarNode.transform = tr.matmul([
            tr.translate(LibX,LibY,LibZ),
            tr.rotationZ(-time-10)
            ])
        time_anterior = t

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
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(escena_textura,texPipeline,"model")
        

        glUseProgram(mvpPipeline.shaderProgram)
        sg.drawSceneGraphNode(redCarNode, mvpPipeline, "model")
        sg.drawSceneGraphNode(escena_color, mvpPipeline, "model")
        
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    redCarNode.clear()
    escena_color.clear()
    escena_textura.clear()
    

    glfw.terminate()