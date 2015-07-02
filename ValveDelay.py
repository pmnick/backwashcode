import RPi.GPIO as GPIO
from time import sleep
from Tkinter import *
import thread
import math
import time
import numpy as np
import spidev
from datetime import datetime, timedelta
import sys
import smtplib
import email                                                                                                                                                                                                                      

print("start")
#Setting up Spi to read ADC
spi_0 = spidev.SpiDev()
spi_0.open(0, 0) 

#Setting up Global Variables
ForwardPumpTarget=15
BackwashPumpTarget=40
ForwardFlowCount = 0.0
oldForwardFlowCount= 0.0
backwashflow=0.0
forwardflow = 0.0
FlowTarget = 1.0 #lpm
PumpThreshold = 1 #psi
StartTime = datetime.now()
samplePeriod = 10  #milliseconds
destination = "/home/pi/Desktop/Data/DelayData %s.txt" %str(StartTime)
a=open(destination,'w') 
Average= 3 
flowshow = 0.0
backshow = 0.0
FPshow = ForwardPumpTarget
BPshow = BackwashPumpTarget
Diffshow= ForwardPumpTarget
TimestampB=datetime.now()
Timestamp=datetime.now()

root = Tk()
root.geometry('880x700+150+150')
root.title("Delay Control")

#----initializing GUI------------------
background_image = PhotoImage(file='/home/pi/Desktop/Code/background.gif')
w=background_image.width()
h=background_image.height() 
C = Canvas(root, bg='#333',height=(h+5),width=(w+5))
C.focus_set() # Sets the keyboard focus to the canvas
bg_label = Label(C , image=background_image)
bg_label.pack()
Ftank_text = Label(C, text='psi:', padx=5)
Ftank_text.place(x=320,y=41)
Btank_text = Label(C, text='psi:', padx=5)
Btank_text.place(x=318,y=338)
FTL= StringVar()
FTL.set('0')
forward_tank_label = Label(C, textvariable=FTL, padx=5)
forward_tank_label.place(x=350,y=41)
BTL= StringVar()
BTL.set('0')
back_tank_label = Label(C, textvariable=BTL, padx=5)
back_tank_label.place(x=350,y=338)
DL= StringVar()
DL.set('0')
differential_label = Label(C, textvariable=DL, padx=5)
differential_label.place(x=400,y=200)
Flowrate_text = Label(C, text='Flow Rate:', padx=5,pady=3)
Flowrate_text.place(x=418,y=89)
Flowrate_text2 = Label(C, text='Flow Rate:', padx=5,pady=3)
Flowrate_text2.place(x=418,y=274)
FRL= StringVar()
FRL.set('0')
Flowrate_label = Label(C, textvariable=FRL,pady=3)
Flowrate_label.place(x=489,y=89)
BFL= StringVar()
BFL.set('0')
BackFlowrate_label = Label(C, textvariable=BFL,pady=3)
BackFlowrate_label.place(x=489,y=274)
Cycle_text = Label(C,text='Cycles:', padx=5,pady=3)
Cycle_text.place(x=605,y=182)
CY= StringVar()
CY.set('0')
Cycle_label = Label(C, textvariable=CY, padx=5,pady=3)
Cycle_label.place(x=655,y=182)
Concentrate_text = Label(C,text='Liters:', padx=5)
Concentrate_text.place(x=760,y=145)
CL= StringVar()
CL.set('0')
Concentrate_label = Label(C, textvariable=CL, padx=5)
Concentrate_label.place(x=805,y=145)
Filtrate_text = Label(C,text='Liters:', padx=5)
Filtrate_text.place(x=760,y=320)
FL= StringVar()
FL.set('0')
Filtrate_label = Label(C, textvariable=FL, padx=5)
Filtrate_label.place(x=805,y=320)
frame=Frame(root)
frame.pack(anchor=NW)


#----Threshold set up-----------------
Controls= LabelFrame(root,text='Controls',height=270,width=w-450)
Controls.pack_propagate(False)
Controls.place(x=0,y=0)


#----Manual control switchs----------------
Switch=StringVar()
Switch.set('Forward')
ManualSwitch = Checkbutton(Controls,indicatoron=0,textvariable=Switch)
ManualSwitch.pack()
FP_ison = IntVar()
FT_ison = IntVar()
BP_ison = IntVar()
BT_ison = IntVar()
FPSwitch = Checkbutton(Controls,onvalue=1,offvalue=0,variable=FP_ison)
FTSwitch = Checkbutton(Controls,onvalue=1,offvalue=0,variable=FT_ison)
BPSwitch = Checkbutton(Controls,onvalue=1,offvalue=0,variable=BP_ison)
BTSwitch = Checkbutton(Controls,onvalue=1,offvalue=0,variable=BT_ison)
FPSwitch.pack() 
FTSwitch.pack()
BPSwitch.pack()
BTSwitch.pack()
#--- Graph settings
screenWidth = 450
resolution = 1 #number of pixels between data points, for visual purposes only
timeRange = .5 #minutes
baseTime = int(timeRange*60*1000/screenWidth)
x0Coords = []
y0Coords = []
xy0Coords = []
FlowrateAvg = []
BackflowAvg = []
FPumpAvg = []
BPumpAvg = []
DiffAvg = []

coordLength = int(screenWidth/resolution)
#---initiation of lists
for i in range(0,coordLength):
    x0Coords.append(i*resolution)
    y0Coords.append(249)
    xy0Coords.append(0)
    xy0Coords.append(0)
for i in range(0,Average):
    FlowrateAvg.append(FlowTarget)
    BackflowAvg.append(0)
    FPumpAvg.append(ForwardPumpTarget)
    BPumpAvg.append(BackwashPumpTarget)
    DiffAvg.append(0)
    
#putting X and Y corrdinites in a list
def coordinate():
    global x0Coords, y0Coords, xy0Coords
    for i in range(0,coordLength*2,2):
        xy0Coords[i] = x0Coords[i/2]
        xy0Coords[i+1] = y0Coords[i/2]
#---End initiation of lists

Graph= LabelFrame(root, text="Flow Graph",height=250,width=screenWidth)
Graph.place(x=(w-screenWidth)+2,y=0)

GraphC=Canvas(Graph, bg = "gray", height = 249, width = screenWidth-1)
c0 = GraphC.create_rectangle(0,0,20,50)
cl0 = GraphC.create_line(xy0Coords,smooth=True)
ctar = GraphC.create_line(0,(249-FlowTarget*20),450,(249-FlowTarget*20), fill='red')

#setting up GPIO pins
ForwardTankValve = 14
ForwardPump = 15
BackwashPump = 18
ForwardPumpValve = 23
BackwashTankValve = 24
BackwashPumpValve = 25                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
ForwardFlow = 22
BackwashFlow = 17
on = GPIO.LOW
off = GPIO.HIGH
vopen = GPIO.LOW
vclose = GPIO.HIGH
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ForwardTankValve, GPIO.OUT)
GPIO.setup(ForwardPumpValve, GPIO.OUT)
GPIO.setup(ForwardPump, GPIO.OUT)
GPIO.setup(BackwashTankValve, GPIO.OUT)
GPIO.setup(BackwashPumpValve, GPIO.OUT)
GPIO.setup(BackwashPump, GPIO.OUT)
GPIO.setup(ForwardFlow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BackwashFlow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#----------------------Function Definitons--------------------------------

def readadc_0(adcnum_0): #this fucntion can be used to find out the ADC value on ADC 0
    if adcnum_0 > 7 or adcnum_0 < 0:
        return -1
    r_0 = spi_0.xfer2([1, 8 + adcnum_0 << 4, 0]) #start bit, Single/Differential mode, Don't care bit OR
    adcout_0 = ((r_0[1] & 3) << 8) + r_0[2]
    return adcout_0

def callback_fflow(ForwardFlow):
    global ForwardFlowCount
    ForwardFlowCount+=1  

def writeData(): 
    global destination,cycles,Diffshow,passes,switched,Switch,backwash,switched,samplePeriod,Timestamp,TimestampB,ForwardFlowCount,oldForwardFlowCount,BackwashFlowCount,oldBackwashFlowCount,forwardflow,backwashflow,FlowrateAvg,flowshow

    ##Calibration of sensor: Real Pressure = reading-(-1.06+.1007xreading)
    Reading=(3.3*float(readadc_0(3)-readadc_0(0))/1023)*100
    ForwardPumpActual=round(Reading-(-1.06+.1007*Reading),1)
    FPumpAvg.pop(0)
    FPumpAvg.append(ForwardPumpActual)
    FPshow=np.mean(FPumpAvg)
    FTL.set(str(round(FPshow,1)))
    if ForwardPumpActual-FPshow > PumpThreshold/2:#if ForwardPumpTarget-FPshow > float(PTdisplay.get())/2:
         GPIO.output(ForwardPump,on)
    if FPshow-ForwardPumpActual > PumpThreshold/2:#if FPshow-ForwardPumpTarget > float(PTdisplay.get())/2:
        GPIO.output(ForwardPump,off)

    Reading=(3.3*float(readadc_0(1)-readadc_0(0))/1023)*100
    BackwashPumpActual=round(Reading-(-1.06+.1007*Reading),1)
    BPumpAvg.pop(0)
    BPumpAvg.append(BackwashPumpActual)
    BPshow=np.mean(BPumpAvg)
    BTL.set(str(round(BPshow,1)))
    if BackwashPumpActual-BackwashPumpActual > PumpThreshold/2:#if BackwashPumpTarget-BackwashPumpActual > float(PTdisplay.get())/2:
        GPIO.output(BackwashPump, on)
    if BackwashPumpActual - BackwashPumpActual > PumpThreshold/2:#if BackwashPumpActual - BackwashPumpTarget > float(PTdisplay.get())/2:
        GPIO.output(BackwashPump, off)

    forwardflow=((ForwardFlowCount-oldForwardFlowCount)/samplePeriod)*60 #60 is a conversion factor to convert the flowrate from pulses per 100miliseconds to liters per minute
    FlowrateAvg.pop(0)
    FlowrateAvg.append(forwardflow)
    flowshow = np.mean(FlowrateAvg)
    FRL.set(str(round(flowshow,1)))
    
    data = str(round(Diffshow,1)) + "\t" + str(round(flowshow,1)) + "\t" +str(round(backwashflow,1)) + "\t" +str(round(FPshow,1))+ "\t" +str(round(BPshow,1))#Writing averaged data
    #data = str(round(Diffshow,1)) + "\t" + str(round(forwardflow,1)) + "\t" +str(round(backwashflow,1)) + "\t" +str(round(ForwardPumpActual,1))+ "\t" +str(round(BackwashPumpActual,1))+'\t'+str(cycles)+'\t'+str(backwash) # writng actual data
    a.write("\n"+ str(datetime.now()) + "\t" + str(data))
    oldForwardFlowCount=ForwardFlowCount
   

    Timestamp=datetime.now()

    if FP_ison.get():
        GPIO.output(ForwardPumpValve,vopen)
    else:
        GPIO.output(ForwardPumpValve,vclose)

    if FT_ison.get():
        GPIO.output(ForwardTankValve,vopen)
    else:
        GPIO.output(ForwardTankValve,vclose)

    if BP_ison.get():
        GPIO.output(BackwashPumpValve, vopen)
    else:
        GPIO.output(BackwashPumpValve, vclose)

    if BT_ison.get():
        GPIO.output(BackwashTankValve, vopen)
    else:
        GPIO.output(BackwashTankValve, vclose)

    root.after(samplePeriod,writeData)

def callback_end(event):
    global FlowCount, StartTime
    GPIO.output(ForwardPump, off)
    GPIO.output(BackwashPump, off)
    GPIO.output(ForwardPumpValve, vclose)#Keeps pressure in the tank
    GPIO.output(BackwashPumpValve, vclose)
    GPIO.output(ForwardTankValve, vopen)#lets pressure out into the tank
    GPIO.output(BackwashTankValve, vopen)
    time.sleep(10)
    GPIO.output(BackwashTankValve, vclose)
    GPIO.output(ForwardTankValve, vclose)
    spi_0.close()
    a.close()
    quit()

#Setting up event detection
GPIO.add_event_detect(ForwardFlow, GPIO.RISING, callback=callback_fflow)

#----------------------------------Main loop----------------------------------------

C.bind("<End>",callback_end)
C.place(x=10,y=280)
GraphC.pack(anchor=CENTER)
root.after(samplePeriod,writeData)
root.mainloop()
