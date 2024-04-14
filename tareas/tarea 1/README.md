# README

### Monserrat Montero Troncoso

He decidido modelar mi libélula, llamada Tomás, con una cabeza (un circulo), su cuerpo (una figura personalizada) y 4 alas independientes (triangulos). De manera que Tomás tiene tres tipos de movimientos:

- Movimiento de las alas: Las cuatro se mueven diferente en tiempo real, dependiendo de si una corresponde a la ala superiore/inferiore o del frente/fondo. 
- Movimiento horizontal: Se mueve en linea recta a velocidad constante. Cuando Tomás está por salir de la escena, vuelve a parecer al otro lado, simulando un seguimiento de cámara.
- Movimiento vertical: Se mueve de forma sinusoidal

He inspirado (fuertemente) mi codigo en auxiliares y el proyecto "butterffly_moving". Me ha servido para entender como funciona OpenGL y la creación/transformación de objetos.

Se ha revisado ademas que cada parte de Tomás está en su capa correspondiente (profundidad), poniendolas en el orden correcto en la función "on_draw"

He dejado, ademas, la imagenes que he utilizado de referencia para el modelado del cuerpo de Tomás y la función que le he pedido a una inteligencia artificial para conseguir un circulo tan bacán como la cabeza de Tomás.