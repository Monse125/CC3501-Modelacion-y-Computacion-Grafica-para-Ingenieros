extends Control

@onready var play: Button = $VBoxContainer/Play
@onready var salir: Button = $VBoxContainer/Salir


# Called when the node enters the scene tree for the first time.
func _ready():
	play.connect("pressed", Callable(self, "_on_play_pressed"))
	salir.connect("pressed", Callable(self, "_on_exit_pressed"))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_play_pressed()-> void:
	get_tree().change_scene_to_file("res://scenes/game_menus/play_settings.tscn")
	
func _on_exit_pressed()-> void:
	get_tree().quit()
	
	
