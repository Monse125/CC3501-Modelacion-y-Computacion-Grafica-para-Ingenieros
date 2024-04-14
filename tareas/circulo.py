import numpy as np

# Definir el número de segmentos del círculo
num_segments = 36
theta = np.linspace(0, 2 * np.pi, num_segments)

# Definir los datos del círculo
circle_position = []
circle_indices = []
circle_color = []

# Agregar los puntos del círculo
for i in range(num_segments):
    x = np.cos(theta[i])
    y = np.sin(theta[i])
    circle_position.extend([x, y, 0.0])
    circle_color.extend([1, 0.5, 1])  # Color rosa para el círculo

# Agregar los índices para dibujar el círculo
for i in range(1, num_segments - 1):
    circle_indices.extend([0, i, i + 1])

# Último triángulo para cerrar el círculo
circle_indices.extend([0, num_segments - 1, 1])

# Convertir a arrays numpy
circle_position = np.array(circle_position, dtype=np.float32)
circle_indices = np.array(circle_indices, dtype=np.uint32)
circle_color = np.array(circle_color, dtype=np.float32)

# Crear un diccionario con los datos del círculo
Circle = {
    'position': circle_position,
    'indices': circle_indices,
    'color': circle_color
}

print(Circle)
print(np.size(Circle['position']))