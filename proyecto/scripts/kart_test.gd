extends VehicleBody3D

############################################################
# behaviour values

var max_rpm = 100
var max_torque = 20
var max_linear_speed = 20.0  # Velocidad máxima deseada en unidades por segundo

############################################################
# Input
func _ready():
	connect("_change_color_car", Callable(self, "_on_change_color_car"))

func _physics_process(delta):
	steering = lerp(steering, Input.get_axis("right", "left") * 0.6, 5 * delta)
	var acceleration = Input.get_axis("back", "forward") * 10

	# Calcula la velocidad angular promedio de las ruedas
	var rpm_average = ($back_left.get_rpm() + $back_right.get_rpm()) / 2.0
	var angular_speed_average = rpm_average * 2 * PI / 60.0  # Convertir RPM a velocidad angular en radianes por segundo

	# Calcula la velocidad lineal aproximada del vehículo
	var wheel_radius = 0.5  # Ajusta el radio de la rueda según tu modelo
	var linear_speed = angular_speed_average * wheel_radius

	# Limitar la velocidad máxima
	if linear_speed > max_linear_speed:
		var reduction_factor = max_linear_speed / linear_speed
		acceleration *= reduction_factor

	var rpm_factor = (max_rpm - rpm_average) / max_rpm  # Ajusta según el RPM de las ruedas para controlar la fuerza de motor
	var engine_force = acceleration * max_torque * rpm_factor

	$back_left.engine_force = engine_force
	$back_right.engine_force = engine_force

	print("Velocidad del kart:", linear_speed)
