extends VehicleBody3D

signal _change_color_car(color: Color)
############################################################
# behaviour values

const MAX_ENGINE_FORCE: float = 650.0
const  MAX_BRAKE_FORCE: float = 10.0
const  MAX_STEER_ANGLE: float = 0.6

const  steer_speed: float = 28.0

var steer_target: float = 0.0
var steer_angle: float = 0.0

############################################################
# Input

# Define los identificadores para los ejes del joystick
const JOY_ANALOG_LX: int = 0
const JOY_ANALOG_R2: int = 5
const JOY_ANALOG_L2: int = 4


func _ready():
	connect("_change_color_car", Callable(self, "_on_change_color_car"))
	


func _physics_process(delta: float) -> void:
	var steer_val: float 
	var throttle_val: float 
	var brake_val: float 
	
	# Overrules for keyboard
	if Input.is_action_pressed("forward"):
		throttle_val = 1.0
	if Input.is_action_pressed("back"):
		brake_val = 1.0
	if Input.is_action_pressed("left"):
		steer_val = 1.0
	elif Input.is_action_pressed("right"):
		steer_val = -1.0
	
	engine_force = throttle_val * MAX_ENGINE_FORCE
	
	# Calcula la velocidad actual del vehículo
	var speed = linear_velocity.length()
	print(speed)
	# Implementa un simulador de ABS para evitar el bloqueo de las ruedas
	if brake_val > 0.0:
		if speed > 10.0:  # Ajusta el umbral de velocidad según sea necesario
			brake = min(brake_val * MAX_BRAKE_FORCE, speed * 0.5)
		else:
			brake = brake_val * MAX_BRAKE_FORCE
	else:
		brake = 0.0
	
	steer_target = steer_val * MAX_STEER_ANGLE
	if steer_target < steer_angle:
		steer_angle -= steer_speed * delta
		if steer_target > steer_angle:
			steer_angle = steer_target
	elif steer_target > steer_angle:
		steer_angle += steer_speed * delta
		if steer_target < steer_angle:
			steer_angle = steer_target
	
	steering = steer_angle
	
	# Añade una fuerza hacia abajo para mejorar la adherencia
	#self.apply_central_force(Vector3(0, -, 0))
	
func _on_change_color_car(color: Color) -> void:
	# Aquí puedes usar el color para lo que necesites
	print("Color recibido:", color)
	"""
	# Ejemplo: Cambiar el color del material del kart
	var dentro_material = $PorDentro.material_override
	if dentro_material:
		dentro_material.albedo_color = color
	var aleron_lat_material = $"Aleron Lat".material_override
	if aleron_lat_material:
		aleron_lat_material.albedo_color = color
	var aleron_del_material = $AleronDelantero.material_override
	if aleron_del_material:
		aleron_del_material.albedo_color = color
	"""
