#!/usr/bin/env python

import makerbot_driver, serial, threading, time
port = '/dev/ttyACM0'
print('Connecting to serial port '+port)
r = makerbot_driver.s3g()
file = serial.Serial(port, 115200, timeout=1)
r.writer = makerbot_driver.Writer.StreamWriter(file, threading.Condition())
print('Connected to MakerBot successfully!')

# queue_extended_point([X, Y, Z, A, B], rate, 0, 0)

# X from -10000 to +10000 (left to right)
# Y from  -5000 to  +5000 (front to rear)
# Z from      0 to -48000 (bottom to top, almost touch extruder)

#xBegin = -10000
#xEnd   = 10000
xBegin = -8000
xEnd   = 8000
xStep  = 1000

yBegin = -5000
yEnd   = 5000
yStep  = 1000

zBegin = 0
zEnd   = 14000
zStep  = -1000

print('Go to initial position ...')
#r.queue_extended_point([xBegin, yBegin, 0, 0, 0], 400, 0, 0)
#r.queue_extended_point([xBegin, yBegin, -48000, 0, 0], 400, 0, 0)
# Some time to go to initial position
#time.sleep(10)

#r.queue_extended_point([xBegin, yBegin, 1000, 0, 0], 400, 0, 0)
#test = r.get_extended_position()
#r.queue_extended_point([0, 0, 0, 0, -2000], 400, 0, 0)
#r.queue_extended_point([0, 0, 0, 0, -27000], 50, 0, 0)
#r.queue_extended_point([0, 0, -30000, -700, 0], 400, 0, 0)
r.queue_extended_point([-8000, -5000, 0, 0, 0], 400, 0, 0)
while True:
	print r.get_extended_position()[0]
	time.sleep(0.2)
#r.queue_extended_point([0, 0, 0, 0, 0], 400, 0, 0)

"""
#test = r.get_extended_position()
#print test
"""