# README
## Tarea 3: "El vuelo de una libélula en 3D, con fondo, iluminación y otros"
### Monserrat Montero Troncoso

Este proyecto se basa en un código original de Daniel Calderon, licenciado bajo la licencia MIT. Puedes encontrar el código original [https://github.com/ivansipiran/grafica]

He inspirado (fuertemente) mi codigo en auxiliares y el proyecto "ex_scene_graph_3dcars".


#### Instrucciones de la tarea:

Hay que implementar una libélula 3D que se mueva (ya sea por cuenta propia o por el imput de un usuario).
- La libélula tiene todas sus partes. [CHECK]
- El movimiento debe tener: trasladar y rotar.[CHECK]
- Las transformaciones deben estar hechas en base a matrices. [CHECK]
- La camara debe moverse, ya sea siguiendo una trayectoria o a través de un input del usuario [CHECK]
- El entorno debe estar decorado y coloreado :D [CHECK]
- Hay que trabajar la iluminación
- Hay que aplicar texturas a almenos dos objetos de la escena. [CHECK]


#### Acerca del código:

Al ejecutar 'Tarea.py' debería funcionar correctamente. Sin embargo, genero MUCHOS elementos (ramitas y flores) de forma aleatoria. Realicé varios test para encontrar la configuración más estética, pero me di cuenta (sin juzgar) de que no todos los computadores tienen las mismas capacidades que el mío. Por eso, limité considerablemente la cantidad de elementos generados. En caso de necesitar limitar aún más la cantidad para poder corregir correctamente, solo es necesario disminuir el valor de la variable al inicio del código (aproximadamente en la línea 25)

Ademas, en honor al tiempo disponible, el algoritmo que genera los elementos de forma aleatoria no es para nada el mas eficiente así que podría demorar un poquito (unos segundos) el arranque de la visualización.

##### Tomás, la libélula

Al igual que en mi tarea 2, Tomás (la libélula) está formado por: una cabeza (una esfera), su cuerpo (otra esfera), su cola (un cubo) y 4 alas independientes (triangulos). De manera que Tomás tiene tres tipos de movimiento:

- Movimiento de las alas: Las cuatro se mueven diferente en tiempo real, dependiendo de si una corresponde a la ala superior/inferior o de la derecha/izquierda.
- Movimiento horizontal: Se ha mejorado el movimiento de Tomás, de manera que ahora recorre dos curvas de Bézier a velocidad constante (una cuando el tiempo retrocede y otra cuando este avanza) y rota mirando hacia adelante.
- Movimiento vertical: Se mueve de forma sinusoidal

##### Escenario

El escenario está formado por diversas ramitas verdad. Las mas cercanas a Tomás están puestas por mi, sin embargo el resto se ponen de forma al azar al rededor de la escena principal (para que no parezca tan vacio).

He añadido lavandas porque me dijeron que a las libelulas les gustan y quería que Tomás se sintiese a gusto en su bucle temporal. De manera que, tanto las lavandas (tallo y flor) como el suelo poseen texturas.

##### Camara

He arreglado la cámara del proyecto respecto a mi tarea 2, enderezándola. Además, he mejorado mi manejo de estas, ahora manipulando también el punto focal.

Por ello, he decidido aprender cómo hacer una especie de cinemática en lugar de simplemente usar 'keys' para cambiar el POV. De esta manera, la cámara ahora sigue a Tomás automáticamente."

##### Iluminación



#### Funciones que arreglar/agregar:

- Ver lo de la iluminación


