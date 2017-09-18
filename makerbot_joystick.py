#!/usr/bin/env python


# Make sure to set the following:
#	WHEN MACHINE BOOTS, COORDINATES ARE SET TO 0,0. Either move to 0,0 before closing, or figure it out again as you go along
#
#
#	rosparam set /autorepeat_rate 5.0
#	rosparam set /coalesce_interval 0.2
#
import rospy
from sensor_msgs.msg import Joy
import makerbot_driver, serial, threading, time
port = '/dev/ttyACM0'
print('Connecting to serial port '+port)
r = makerbot_driver.s3g()
file = serial.Serial(port, 115200, timeout=1)
r.writer = makerbot_driver.Writer.StreamWriter(file, threading.Condition())
print('Connected to MakerBot successfully!')

xBegin = 0
xEnd   = 24100

yBegin = 0
yEnd   = 10500

zBegin = 0
zEnd   = 26000

clawBegin = 0
clawEnd = -29000

axes = r.get_extended_position()[0]
x_pos = axes[0]
y_pos = axes[1]
z_pos = axes[3]
claw_pos = axes[4]

r.queue_extended_point([xBegin, yBegin, 0, zBegin, clawBegin], 400, 0, 0)

home = False

while not home:
	time.sleep(0.2)
	axes = r.get_extended_position()[0]
	x_pos = axes[0]
	y_pos = axes[1]
	z_pos = axes[3]
	claw_pos = axes[4]
	if x_pos == xBegin and y_pos == yBegin and z_pos == zBegin and claw_pos == clawBegin:
		home = True

print "Device Initialized, ready to play..."

z_goal = 0

def move(x,y,z,claw,speed):
	axes = r.get_extended_position()[0]
	x_pos = axes[0]
	y_pos = axes[1]
	z_pos = axes[3]
	claw_pos = axes[4]
	print "x_pos: " + str(x_pos) + " y_pos: " + str(y_pos) + " z_pos: " + str(z_pos) + " claw_pos: " + str(claw_pos)
	x_goal = x_pos + x
	y_goal = y_pos + y
	z_goal = z_pos + z
	claw_goal = claw_pos + claw
	if y_goal <= yBegin:
		y_goal = yBegin
	if y_goal >= yEnd:
		y_goal = yEnd
	if x_goal <= xBegin:
		x_goal = xBegin
	if x_goal >= xEnd:
		x_goal = xEnd
	if z_goal >= zEnd:
		z_goal = zEnd
	if z_goal <= zBegin:
		z_goal = zBegin
	if claw_goal >= clawBegin:
		claw_goal = clawBegin
	if claw_goal <= clawEnd:
		claw_goal = clawEnd
	print "x_goal: " + str(x_goal) + " y_goal: " + str(y_goal) + " z_goal: " + str(z_goal) + " claw_goal: " + str(claw_goal)
	print "--------------"
	r.queue_extended_point([x_goal, y_goal, 0, z_goal, claw_goal], speed, 0, 0)
	#r.queue_extended_point([x_goal, y_goal, 0, z_goal, 0], speed, 0, 0)
def callback(data):
	#print data
	#speed = 400
	x = -1*data.axes[0]
	y = data.axes[1]
	x *= 600
	y *= 600
	speed_val = max(abs(x),abs(y))
	speed = 800-int(400*speed_val/600)
	if abs(x)<=350 and abs(y)<=350:
		speed = 750
	z = 0
	claw = 0
	if data.buttons[4] == 1 and x==0 and y==0:
		speed = 1
		z = -600
		x = 0
		y = 0
	if data.buttons[2] == 1 and x==0 and y ==0:
		speed = 1
		z = 600
		x = 0
		y = 0
	if data.buttons[1] == 1 and x==0 and y==0:
		speed = 1
		x = 0
		y = 0
		claw = -600
	if data.buttons[3] == 1 and x==0 and y==0:
		speed = 1
		x = 0
		y = 0
		claw = 600
	print "X: " + str(x) + " Y: " + str(y)
	move(int(x),int(y),z,claw,speed)	

def joystick_listener():

	rospy.init_node("makerbot_controller")
	rospy.Subscriber("joy", Joy, callback)
	rospy.spin()

joystick_listener()
"""
import makerbot_driver, serial, threading, time
port = '/dev/ttyACM0'
print('Connecting to serial port '+port)
r = makerbot_driver.s3g()
file = serial.Serial(port, 115200, timeout=1)
r.writer = makerbot_driver.Writer.StreamWriter(file, threading.Condition())
print('Connected to MakerBot successfully!')
"""