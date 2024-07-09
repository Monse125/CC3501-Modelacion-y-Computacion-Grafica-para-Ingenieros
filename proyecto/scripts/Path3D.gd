extends Path3D

# PathFollow3D node reference
@onready var path_follow: PathFollow3D = $PathFollow3D
# Load the StaticBody3D scenes
var static_body_scene_1: PackedScene = preload("res://scenes/track promps/pila_neumaticos_blanca.tscn")
var static_body_scene_2: PackedScene = preload("res://scenes/track promps/pila_neumaticos_roja.tscn")
var step_size = 2.4 # Distancia entre cada StaticBody3D
var scale_factor = Vector3(0.2, 0.2, 0.2) # Factor de escala para ajustar el tamaño de las instancias


func _ready():
	print("Path3D ready")
	_instantiate_objects()

func _instantiate_objects():
	print("aa")
	# Obtiene la longitud de la curva
	var path_length = self.curve.get_baked_length()
	
	# Calcula el número de instancias necesarias basado en la longitud del camino y el tamaño del paso
	var num_instances = int(path_length / step_size)
	
	# Loop a través del camino y instancia StaticBody3Ds
	for i in range(num_instances):
		# Alterna entre las dos escenas
		var instance
		if i % 2 == 0:
			instance = static_body_scene_1.instantiate()
		else:
			instance = static_body_scene_2.instantiate()
			
		# Ajusta la escala de la instancia
		instance.scale = scale_factor
		
		# Calcula la posición a lo largo del camino
		var t = float(i) / num_instances
		path_follow.progress_ratio = t
		
		# Asegura que la instancia tenga la misma transformación global que el PathFollow3D
		instance.global_transform = path_follow.global_transform
		
		# Añade la instancia a la escena
		add_child(instance)
		
