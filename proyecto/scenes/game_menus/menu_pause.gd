extends MarginContainer

@onready var reanudar: Button = $PanelContainer/MarginContainer/VBoxContainer/Reanudar

@onready var menu: Button = $PanelContainer/MarginContainer/VBoxContainer/Menu

# Called when the node enters the scene tree for the first time.
func _ready():
	hide()
	reanudar.connect("pressed", Callable(self, "_on_resume_pressed"))
	menu.connect("pressed", Callable(self, "_on_menu_pressed"))
	


func _input(event):
	if event.is_action_pressed("pause"):
		if visible:
			_resume_game()
		else:
			_pause_game()

func _pause_game() -> void:
	visible = true
	get_tree().paused = true
	
func _resume_game() -> void:
	visible = false
	get_tree().paused = false
	
func _on_menu_pressed():
	get_tree().change_scene_to_file("res://scenes/game_menus/main_menu.tscn")
	get_tree().paused = false

func _on_resume_pressed() -> void:
	_resume_game()
	
