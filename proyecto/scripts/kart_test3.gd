extends VehicleBody3D

############################################################
# Valores de comportamiento

const MAX_ENGINE_FORCE: float = 500.0
const MAX_BRAKE_FORCE: float = 10.0
const MAX_STEER_ANGLE: float = 0.6

const steer_speed: float = 30.0

var steer_target: float = 0.0
var steer_angle: float = 0.0

var friction: float = 0.5  # Ajusta la fricción para simular el deslizamiento

############################################################
# Entrada

# Define los identificadores para los ejes del joystick
const JOY_ANALOG_LX: int = 0
const JOY_ANALOG_R2: int = 5
const JOY_ANALOG_L2: int = 4

func _ready():
	# Llamado cada vez que el nodo se agrega a la escena.
	# Inicialización aquí
	pass

func _physics_process(delta: float) -> void:
	var steer_val: float = 0.0
	var throttle_val: float = 0.0
	var brake_val: float = 0.0
	
	# Sobrescribe para teclado
	if Input.is_action_pressed("forward"):
		throttle_val = 1.0
	if Input.is_action_pressed("back"):
		brake_val = 1.0
	if Input.is_action_pressed("left"):
		steer_val = 1.0
	elif Input.is_action_pressed("right"):
		steer_val = -1.0
	
	engine_force = throttle_val * MAX_ENGINE_FORCE
	brake = brake_val * MAX_BRAKE_FORCE
	
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
	
	# Aplicar fricción para simular deslizamiento
	apply_friction()

func apply_friction():
	# Ajustar fricción para simular deslizamiento
	var linear_velocity = get_linear_velocity()
	linear_velocity *= (1 - friction)
	set_linear_velocity(linear_velocity)
