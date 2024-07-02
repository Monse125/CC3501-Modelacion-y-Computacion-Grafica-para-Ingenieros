extends Path3D

# PathFollow3D node reference
@onready var path_follow: PathFollow3D = $PathFollow3D
# Load the StaticBody3D scene
var static_body_scene: PackedScene = preload("res://scenes/track promps/barrera_2.tscn")

var step_size = 3.0 # Distancia entre cada StaticBody3D

func _ready():
	# Usa await para esperar un frame antes de continuar
	await get_tree().process_frame
	
	# Obtiene la longitud de la curva
	var curve = self.curve
	var path_length = curve.get_baked_length()
	
	# Calcula el número de instancias necesarias basado en la longitud del camino y el tamaño del paso
	var num_instances = int(path_length / step_size)
	
	# Loop a través del camino y instancia StaticBody3Ds
	for i in range(num_instances):
		var instance = static_body_scene.instantiate()
		
		# Calcula la posición a lo largo del camino
		var t = float(i) / num_instances
		path_follow.progress_ratio = t
		
		# Posiciona la instancia
		instance.global_transform.origin = path_follow.global_transform.origin
		
		# Añade la instancia a la escena
		add_child(instance)
