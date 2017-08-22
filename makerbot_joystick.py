#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import makerbot_driver, serial, threading, time
port = '/dev/ttyACM0'
print('Connecting to serial port '+port)
r = makerbot_driver.s3g()
file = serial.Serial(port, 115200, timeout=1)
r.writer = makerbot_driver.Writer.StreamWriter(file, threading.Condition())
print('Connected to MakerBot successfully!')

xBegin = -10000
xEnd   = 10000

yBegin = -5000
yEnd   = 5000

axes = r.get_extended_position()[0]
x_pos = axes[0]
y_pos = axes[1]

r.queue_extended_point([xBegin, yBegin, 0, 0, 0], 400, 0, 0)

home = False

while not home:
	time.sleep(0.2)
	axes = r.get_extended_position()[0]
	x_pos = axes[0]
	y_pos = axes[1]
	if x_pos == xBegin and y_pos == yBegin:
		home = True

print "Device Initialized, ready to play..."

def move(x,y):
	axes = r.get_extended_position()[0]
	x_pos = axes[0]
	y_pos = axes[1]
	print "x_pos: " + str(x_pos) + " y_pos: " + str(y_pos)
	x_goal = x_pos + x
	y_goal = y_pos + y
	x_goal = x_pos + x
	y_goal = y_pos + y
	if y_goal <= yBegin:
		y_goal = yBegin
	if y_goal >= yEnd:
		y_goal = yEnd
	if x_goal <= xBegin:
		x_goal = xBegin
	if x_goal >= xEnd:
		x_goal = xEnd
	print "x_goal: " + str(x_goal) + " y_goal: " + str(y_goal)
	print "--------------"
	r.queue_extended_point([x_goal, y_goal, 0, 0, 0], 1000, 0, 0)

def callback(data):
	#print data
	x = -1*data.axes[0]
	y = data.axes[1]
	x *= 500
	y *= 500
	print "X: " + str(x) + " Y: " + str(y)
	move(int(x),int(y))	

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