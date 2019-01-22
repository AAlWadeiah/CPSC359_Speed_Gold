#C functions that will be used are imported from "smbus.c"
cdef extern from "smbus.c":
  #void writeI2CBlockData(int address, char cmd, int data)
  #long readI2CBlockData(int address, char cmd)
	int readByteData(int address, char cmd)
	int writeByteData(int address, char cmd, char value)

#function definitions
def write_i2c_block_data(int address, char cmd, int data[]):
	print("It works!!!")
	cdef unsigned char r[256]
	#call C function
	for i in range(data.length):
		writeByteData(address, cmd, data[i])

cpdef read_i2c_block_data(int address, char cmd, int length):
	cdef unsigned char r[256]
	#call C function

	data = []
	for i in range(length):
		data.append(r[i])
	return data

cpdef read_byte_data(int address, char cmd):
	return readByteData(address, cmd)

cpdef write_byte_data(int address, char cmd, char value):
	return writeByteData(address, cmd, value)
