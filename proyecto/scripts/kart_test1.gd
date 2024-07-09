extends VehicleBody3D

signal _change_color_car(color: Color)
signal game_start
############################################################
# behaviour values

const MAX_ENGINE_FORCE: float = 700.0
const  MAX_BRAKE_FORCE: float = 10.0
const  MAX_STEER_ANGLE: float = 0.6
const  steer_speed: float = 20.0

var steer_target: float = 0.0
var steer_angle: float = 0.0
var can_move = false

############################################################
# Input

# Define los identificadores para los ejes del joystick
const JOY_ANALOG_LX: int = 0
const JOY_ANALOG_R2: int = 5
const JOY_ANALOG_L2: int = 4


func _ready():
	connect("_change_color_car", Callable(self, "_on_change_color_car"))
	get_parent().get_parent().connect("game_start", Callable(self, "_on_game_start"))
	
func _on_game_start():
	can_move = true


func _physics_process(delta: float) -> void:
	if can_move:
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
		#print(speed)
		
		if brake_val > 0.0:
			if speed > 10.0:
				brake = min(brake_val * MAX_BRAKE_FORCE, speed * 0.5)
			else:
				brake = brake_val * MAX_BRAKE_FORCE
		else:
			brake = 0.1  # Suaviza la desaceleración
		
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
	var material_1 = $PorDentro.mesh.surface_get_material(1)
	if material_1:
		material_1.albedo_color = color
	var material_2 = $AleronDelantero.mesh.surface_get_material(0)
	if material_2:
		material_2.albedo_color = color
	var material_3 = $"Aleron Lat".mesh.surface_get_material(0)
	if material_3:
		material_3.albedo_color = color
	
	
