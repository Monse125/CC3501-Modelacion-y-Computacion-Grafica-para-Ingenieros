extends Control

@onready var morado: CheckButton = $VBoxContainer/VBoxContainer/Colores/Morado
@onready var azul: CheckButton = $VBoxContainer/VBoxContainer/Colores/Azul
@onready var blanco: CheckButton = $VBoxContainer/VBoxContainer/Colores/Blanco
@onready var rosado: CheckButton = $VBoxContainer/VBoxContainer/Colores/Rosado
@onready var rojo: CheckButton = $VBoxContainer/VBoxContainer/Colores/Rojo
@onready var verde_fofo: CheckButton = $"VBoxContainer/VBoxContainer/Colores2/Verde Fofo"
@onready var papaya: CheckButton = $VBoxContainer/VBoxContainer/Colores2/Papaya


@onready var libre: CheckButton = $VBoxContainer/VBoxContainer2/HBoxContainer2/Libre
@onready var vuelta_rapida: CheckButton = $VBoxContainer/VBoxContainer2/HBoxContainer2/Vuelta_Rapida

@onready var colors = ButtonGroup.new()
@onready var mode = ButtonGroup.new()

@onready var play: Button = $HBoxContainer/Play
@onready var menu: Button = $VBoxContainer2/Menu

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	morado.button_group = colors
	azul.button_group = colors
	blanco.button_group = colors
	rosado.button_group = colors
	rojo.button_group = colors
	verde_fofo.button_group = colors
	papaya.button_group = colors
	
	blanco.button_pressed = true
	
	libre.button_group = mode
	vuelta_rapida.button_group = mode
	
	libre.button_pressed = true
	
	# Conectar señales de los botones de color
	papaya.connect("pressed", Callable(self, "_on_color_button_pressed"))
	morado.connect("pressed", Callable(self, "_on_color_button_pressed"))
	azul.connect("pressed", Callable(self, "_on_color_button_pressed"))
	blanco.connect("pressed", Callable(self, "_on_color_button_pressed"))
	rosado.connect("pressed", Callable(self, "_on_color_button_pressed"))
	rojo.connect("pressed", Callable(self, "_on_color_button_pressed"))
	verde_fofo.connect("pressed", Callable(self, "_on_color_button_pressed"))
	# Conectar señales de los botones de modo
	libre.connect("pressed",Callable(self, "_on_mode_button_pressed"))
	vuelta_rapida.connect("pressed", Callable(self, "_on_mode_button_pressed"))
	# Conectar señal del botón de jugar (asumiendo que tienes un botón llamado 'play_button')
	play.connect("pressed", Callable(self, "_on_play_pressed"))
	menu.connect("pressed", Callable(self, "_on_menu_pressed"))
	

# Función para manejar la selección de botones de color
func _on_color_button_pressed(button: CheckButton) -> void:
	# Desactivar todos los botones del grupo excepto el seleccionado
	for child in $VBoxContainer/VBoxContainer/Colores.get_children():
		if child is CheckButton and child.group == button.group:
			child.pressed = (child == button)

# Función para manejar la selección de modos
func _on_mode_button_pressed(button: CheckButton) -> void:
	# Desactivar todos los botones del grupo excepto el seleccionado
	for child in $VBoxContainer/VBoxContainer2/HBoxContainer2.get_children():
		if child is CheckButton and child.group == button.group:
			child.pressed = (child == button)

# Función para iniciar el juego
func _on_play_pressed() -> void:
	var color_selected: Color = Color(1, 1, 1)  # Color por defecto si no se encuentra ninguno seleccionado
	var mode_selected = ""
	
	# Determinar qué color está seleccionado
	var boton_color = colors.get_pressed_button()
	color_selected = boton_color.modulate
	
	var kart_scene = preload("res://scenes/karts/kart_test_3.tscn").instantiate()
	# Agregar la escena del kart a la escena actual antes de emitir la señal
	add_child(kart_scene)
	kart_scene.emit_signal("_change_color_car", color_selected)
	
	var boton_mode = mode.get_pressed_button()
	mode_selected = boton_mode.text
	
	
	# Realizar acciones basadas en el color y el modo seleccionados
	if mode_selected == "Practica Libre":
		print(color_selected,mode_selected)
		get_tree().change_scene_to_file("res://scenes/game_menus/practica_libre.tscn")
	else:
		print(color_selected,mode_selected)
		
func _on_menu_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game_menus/main_menu.tscn")
