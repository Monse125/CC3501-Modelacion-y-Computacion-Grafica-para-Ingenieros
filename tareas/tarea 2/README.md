# README
## Tarea 2: "El vuelo de una libélula en 3D, simple"
### Monserrat Montero Troncoso

Le he preguntado a ChatGPT como hacer correctamente uso de un código que presenta una licencia, cualquier comentario acerca de esto será bien recibido para saber como proceder en el futuro. Este proyecto se basa en un código original de Daniel Calderon, licenciado bajo la licencia MIT. Puedes encontrar el código original [https://github.com/ivansipiran/grafica]

#### Decisiones de desarrollo:

Con ejecutar "Tarea.py" debería funcionar.

Está vez mi libelula, recuerdar que se llama Tomás, posee una cabeza (una esfera), su cuerpo (otra esfera), su cola (un cubo) y 4 alas independientes (triangulos). De manera que Tomás tiene tres tipos de movimiento:

- Movimiento de las alas: Las cuatro se mueven diferente en tiempo real, dependiendo de si una corresponde a la ala superior/inferior o de la derecha/izquierda.
- Movimiento horizontal: Se mueve según una linea de bezier velocidad constante. Está vez se encuentra en una paradoja temporal así que cuando está por salir de la escena se retrocede el tiempo.
- Movimiento vertical: Se mueve de forma sinusoidal

He inspirado (fuertemente) mi codigo en auxiliares y el proyecto "ex_scene_graph_3dcars".

No he logrado ajustar correctamente la camara para que esté derecha.