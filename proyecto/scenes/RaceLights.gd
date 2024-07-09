extends CanvasLayer

signal tween_all_completed

var light_index = 0
var lights = []

func _ready():
	lights = [$L0,$L1,$L2,$L3,$L4,$L5]
	for light in lights:
		light.visible = false

func start():
	light_index = 0
	_next_light()

func _next_light():
	if light_index < lights.size():
		lights[light_index].visible = true
		var timer = Timer.new()
		timer.wait_time = 1.0
		timer.one_shot = true
		timer.connect("timeout", Callable(self, "_next_light"))
		add_child(timer)
		timer.start()
		light_index += 1
	else:
		emit_signal("tween_all_completed")
