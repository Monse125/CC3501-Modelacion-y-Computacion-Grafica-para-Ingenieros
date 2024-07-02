extends Control

@onready var play: Button = $VBoxContainer/Play
# Called when the node enters the scene tree for the first time.
func _ready():
	play.connect("pressed", Callable(self, "_on_play_pressed"))


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_play_pressed():
	get_tree().change_scene_to_file("res://scenes/game_menus/play_settings.tscn")
	
func _on_settings_pressed():
	pass
	
	
