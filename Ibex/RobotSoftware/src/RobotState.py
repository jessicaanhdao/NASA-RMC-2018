class RobotState:

	#self.currentState = None
	#self.lastState = None

	def __init__(self):
		self.currentState = "OFF"
		self.lastState = None

	def getState(self):
		return self.currentState

	def getLastState(self):
		return self.lastState

	def setState(self, state):
		self.lastState = self.currentState
		self.currentState = state

STATES = ["MSG_STOP",
		  "MSG_DRIVE_TIME",
		  "MSG_DRIVE_DISTANCE",
		  "MSG_ROTATE_TIME",
		  "MSG_SCOOP_TIME",
		  "MSG_SCOOP_DISTANCE",
		  "MSG_DEPTH_TIME",
		  "MSG_DEPTH_DISTANCE",
		  "MSG_ROTATE_TO_CENTER",
		  "MSG_BUCKET_DISTANCE",
		  "MSG_GET_TARGET",
		  "MSG_STOP_TIME",
		  "MSG_MOTOR_VALUES",
		  "MSG_ROTATE_TO_PERPENDICULAR"]
