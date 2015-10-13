import serial
import time

ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

try:
	ser.open()
except Exception, e:
	print "Error: Cannot open serial port: " + str(e)
	exit()

if ser.isOpen():
	print ser.portstr
	try:#flush input and output buffers that could be halting comunication
		ser.flushInput()
		ser.flushOutput()
	except Exception, e1:
		print "error communicating...: " + str(e1)

print 'enter your commands below. \r\nInsert "exit" to leave the aplication'

input = 1
while 1:
	#get keyboard input
	input = raw_input("<< ")
	if input == 'exit' :
		ser.close()
		exit()
	else:
	#send character to the device
		ser.write(input)# may need \r or\n or \r\n to respond correctly
                trash = ''
                time.sleep(1)
                while ser.inWaiting() > 0:
                        trash += ser.read(1)

                if trash != '':
                        print ">>"+trash
