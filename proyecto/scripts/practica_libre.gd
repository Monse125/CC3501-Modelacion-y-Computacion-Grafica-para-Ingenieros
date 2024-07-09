extends Node3D

var race_started = false

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$StartMsg.visible = true


func _input(event):
	if Input.is_action_pressed("start") and !race_started:
		$StartMsg.visible = false
		$car/kart_test3._on_game_start()
		$car/kart_test3.freeze = false
		
