extends Node3D

signal game_start

var race_started = false

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$StartMsg.visible = true
	$RaceLights.visible = false
	$Timer.visible = false
	set_process_input(true)

func _input(event):
	if Input.is_action_pressed("start") and !race_started:
		$StartMsg.visible = false
		$RaceLights.visible = true
		_start_race_lights()

func _start_race_lights():
	$RaceLights.start()
	await $RaceLights.tween_all_completed()
	race_started = true
	$Timer.start()
	emit_signal("game_start")
