extends CanvasLayer

var timer = 0.0
var running = false

func _ready():
	$TimerLabel.text = str(timer)

func start():
	running = true
	set_process(true)

func _process(delta):
	if running:
		timer += delta
		$TimerLabel.text = str(round(timer * 100) / 100.0)
