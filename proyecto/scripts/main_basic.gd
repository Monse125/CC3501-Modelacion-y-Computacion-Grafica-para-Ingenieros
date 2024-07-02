extends Node3D

func _ready():
	pass
	# Aquí puedes usar el color para lo que necesites


func _process(delta):
	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().quit()
