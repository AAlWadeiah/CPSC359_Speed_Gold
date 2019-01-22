import smbus

def init():
	"""Initialize bus object and set up registers for reading accelerometer position"""
	add = 0x53
	reg = 0x32
	power_ctl = 0x2d
	bus = smbus.SMBus()
	bus.open(1)
	power = bus.read_byte_data(add, power_ctl)
	#0000 1000
	measure_on = power | 0x8
	bus.write_byte_data(add, power_ctl, measure_on)

def getX():
	position = bus.read_i2c_block_data(add, reg, 6)
	x0 = position[0]
	x1 = position[1]

	xPos = x1 << 8
	xPos = xPos | x0

	xPos = xPos ^ 0x8000
	xPos -= 0x8000

	return xPos

def getY():
	position = bus.read_i2c_block_data(add, reg, 6)
	y0 = position[2]
	y1 = position[3]

	yPos = y1 << 8
	yPos = yPos | y0

	yPos = yPos ^ 0x8000
	yPos -= 0x8000

	return yPos

def getZ():
	position = bus.read_i2c_block_data(add, reg, 6)
	z0 = position[4]
	z1 = position[5]

	zPos = z1 << 8
	zPos = zPos | z0

	zPos = zPos ^ 0x8000
	zPos -= 0x8000

	return zPos

def closeBus():
	bus.close()

# def getAccValues():
# 	"""Function that retrieves x, y, and z positions of the accelerometer."""
# 	# add = 0x53
# 	# reg = 0x32
# 	# power_ctl = 0x2d
# 	# bus = smbus.SMBus()
# 	# bus.open(1)
# 	# power = bus.read_byte_data(add, power_ctl)
# 	# #0000 1000
# 	# measure_on = power | 0x8
# 	# bus.write_byte_data(add, power_ctl, measure_on)
# 	# maxX, minX, maxY, minY, maxZ, minZ = (0, 0, 0, 0, 0, 0)
# 	position = bus.read_i2c_block_data(add, reg, 6)
# 	# x0 = position[0]
# 	# x1 = position[1]
# 	y0 = position[2]
# 	y1 = position[3]
# 	z0 = position[4]
# 	z1 = position[5]
#
# 	# xPos = x1 << 8
# 	# xPos = xPos | x0
# 	yPos = y1 << 8
# 	yPos = yPos | y0
# 	zPos = z1 << 8
# 	zPos = zPos | z0
#
# 	# xPos = xPos ^ 0x8000
# 	# xPos -= 0x8000
#
# 	yPos = yPos ^ 0x8000
# 	yPos -= 0x8000
#
# 	zPos = zPos ^ 0x8000
# 	zPos -= 0x8000
#
# 	return xPos, yPos, zPos
