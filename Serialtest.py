import serial
import time
from datetime import datetime, timedelta

StartTime = datetime.now()
destination = "/home/pi/Desktop/Data/Particledata%s.txt" %str(StartTime)
a=open(destination,'w') #a means append to existing file, w means overwrite old

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

trash = ''

ser.write('U')
time.sleep(.5)
while ser.inWaiting() > 0:
        trash += ser.read(1)
ser.write('c')
time.sleep(.5)
while ser.inWaiting() > 0:
        trash += ser.read(1)
        
count = 0
while count < 200:
        ser.write('e')
        time.sleep(.5)
        while ser.inWaiting() > 0:
                trash += ser.read(1)
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
        ser.write('A')
        time.sleep(.5)
        trash = ser.read(1)
        status =ser.read(1)
        if status == " ":
            status = 'No alarms'
        elif status == "!":
            status = 'Sensor Fail'
        elif status == "$":
            status = "Count Alarm"
        else:
            status = status
        trash += ser.read(24)
        um1 = ser.read(6)
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
        ser.write('c')
        time.sleep(.5)
        while ser.inWaiting() > 0:
                trash += ser.read(1)
        data = str(count)+'\t'+ str(status)+'\t'+str(um1)+'\t'+str(um3)+'\t'+str(um5)+'\t'+str(um10)+'\t'+str(um15)+'\t'+str(um25)+'\t'+str(um50)+'\t'+str(um100)
        a.write("\n"+ str(datetime.now()) + "\t" + str(data))
        ser.write('c')
        time.sleep(.5)
        while ser.inWaiting() > 0:
                trash += ser.read(1)
        time.sleep(9.5)
        count += 1
        print count

print 'exited sucsessfully;'
ser.write('e')
time.sleep(.5)
while ser.inWaiting() > 0:
        trash += ser.read(1)
        #print um5
##	#get keyboard input
##	input = raw_input("<< ")
##	if input == 'exit' :
##		ser.close()
##		exit()
##	else:
##	#send character to the device
##		ser.write(input)# may need \r or\n or \r\n to respond correctly
##                trash = ''
##                time.sleep(1)
##                while ser.inWaiting() > 0:
##                        trash += ser.read(1)
##
##                if trash != '':
##                        print ">>"+trash
