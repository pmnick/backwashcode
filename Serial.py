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
		um1 = ''
                um3 = ''
                um5 = ''
                um10 = ''
                um15 = ''
                um25 = ''
                um50 = ''
                um100 = ''
                trash = ''
                status = ''
		if input =="A":
                        time.sleep(.3)
                        trash = ser.read(1)
                        status +=ser.read(1)
                        if status == " ":
                                status = 'No alarms'
                        elif status == "!":
                                status = 'Sensor Fail'
                        elif status == "$":
                                status = "Count Alarm"
                        else:
                                status = "?"
                        print 'Status is :' + status
                        trash += ser.read(24)
                        um1 = ser.read(6)
                        print um1
                        trash += ser.read(5)
                        um3 = ser.read(6)
                        trash += ser.read(5)
                        um5 = ser.read(6)
                        trash += ser.read(5)
                        um10 = ser.read(6)
                        trash += ser.read(5)
                        um15 = ser.read(6)
                        trash += ser.read(5)
                        um25 = ser.read(6)
                        trash += ser.read(5)
                        um50 = ser.read(6)
                        trash += ser.read(5)
                        um100 = ser.read(6)
                        while ser.inWaiting() > 0:
                                trash += ser.read(1)

                        if trash != '':
                                print ">>"+trash

		else :
                        time.sleep(.3)
                        while ser.inWaiting() > 0:
                                trash += ser.read(1)

                        if trash != '':
                                print ">>"+trash
