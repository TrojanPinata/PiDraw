import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Globals - while I don't like them, this is a exception case
kit = MotorKit(i2c=board.I2C())

F = stepper.FORWARD
R = stepper.BACKWARD
MS = stepper.MICROSTEP
SS = stepper.SINGLE
DS = stepper.DOUBLE
PEN = 4

x = 0;
y = 0;
xDirection = F
yDirection = F
penDelay = 0.5
xLim = 150
yLim = 150

# Allow the motors to cool down by releasing the coils
def cooldown():
   kit.stepper1.release()
   kit.stepper2.release()

# Activate solenoid
def penDown():
   GPIO.output(PEN, 1)

# Activate solenoid
def penUp():
   GPIO.output(PEN, 0)

# Find given point
def findPoint(xMod, yMod):
   xInit = x
   yInit = y
   if (xInit - xMod < 0):
      xDirection = R
   else:
      xDirection = F
   if (yInit - yMod < 0):
      yDirection = R
   else: 
      yDirection = F

   for i in range(abs(xInit - xMod)):
      time.sleep(0.02)
      kit.stepper1.onestep(direction=xDirection, style=MS)
      updatePos()

   for j in range(abs(yInit - yMod)):
      time.sleep(0.02)
      kit.stepper2.onestep(direction=yDirection, style=MS)
      updatePos()

# Set current point to zero
def setZero():
   x = 0
   y = 0

# Actuate solenoid
def dot():
   penDown()
   time.sleep(penDelay)
   penUp()

# Initialize motors
def initMotors():
   kit.stepper1.release()
   kit.stepper2.release()
   f = input("Press any key when motors are at in initial positions.")
   setZero()

# Initialize solenoid and motor
def init():
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
   GPIO.setup(PEN, GPIO.OUT)
   initMotors()

# Find given point moving directly there (via diagonal)
def smoothFind(xMod, yMod):
   xInit = x
   yInit = y
   if (xInit - xMod < 0):
      xDirection = R
   else:
      xDirection = F
   if (yInit - yMod < 0):
      yDirection = R
   else: 
      yDirection = F

   for i in range(yInit, yMod):
      for j in range(xInit, xMod):
         j = (j - yInit)*(xMod - xInit)/(yMod - yInit)+xInit
         for r in range(x, j):
            if (r < 0):
               kit.stepper1.onestep(direction=R, style=MS)
            else:
               kit.stepper1.onestep(direction=F, style=MS)
            updatePos()

         for s in range(y, i):
            if (s < 0):
               kit.stepper2.onestep(direction=R, style=MS)
            else:
               kit.stepper2.onestep(direction=F, style=MS)
            updatePos()
   
# Updates global position values
def updatePos():
   if (xDirection == F):
      x += 1
   else:
      x -= 1

   if (yDirection == F):
      y += 1
   else:
      y -= 1

def iterateX():
   x += 1
   kit.stepper1.onestep(direction=F, style=MS)

def iterateY():
   y += 1
   kit.stepper2.onestep(direction=F, style=MS)

def main():
   init()
   
def __init__():
   main()