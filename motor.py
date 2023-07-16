import time
import board
import RPi.GPIO as GPIO

### Fields
# Important variables
penDelay = 0.5
stepSize = 1
xStep = 0
yStep = 0

# Pen GPIO pin
PEN = 4

# X-axis stepper GPIO pins
XA1 = 17
XA2 = 27
XB1 = 22
XB2 = 23

# Y-axis stepper GPIO pins
YA1 = 5
YA2 = 6
YB1 = 13
YB2 = 12


### Pen direct functions
# Push pen into drawing surface
def penDown():
   GPIO.output(PEN, 1)


# Retract pen from drawing surface
def penUp():
   GPIO.output(PEN, 0)


# Create a dot on the drawing surface
def dot():
   penDown()
   time.sleep(penDelay)
   penUp()


### Motor functions
# Release all motors
def releaseAll():
   releaseX()
   releaseY()


# Release X-axis stepper
def releaseX():
   GPIO.output(XA1, 0)
   GPIO.output(XA2, 0)
   GPIO.output(XB1, 0)
   GPIO.output(XB2, 0)


# Release Y-axis stepper
def releaseY():
   GPIO.output(YA1, 0)
   GPIO.output(YA2, 0)
   GPIO.output(YB1, 0)
   GPIO.output(YB2, 0)


# Step motor in direction in full steps
def step(axis, direction):
   global xStep, yStep
   a1, a2, b1, b2 = redefine(axis)

   # Set step based on working axis
   if axis: 
      step = xStep
   else: 
      step = yStep

   # Check step is not illegal
   if step >= 4 and direction: # redundant but protects from errors
      step = 0
   elif step < 0 and not direction:
      step = 3
   
   # Move the poles depending on the current step
   if step == 0:
      GPIO.output(a1, 1)
      GPIO.output(a2, 0)
      GPIO.output(b1, 0)
      GPIO.output(b2, 1)
      iterateStep(axis, direction)

   elif step == 1:
      GPIO.output(a1, 1)
      GPIO.output(a2, 1)
      GPIO.output(b1, 0)
      GPIO.output(b2, 0)
      iterateStep(axis, direction)
   
   elif step == 2:
      GPIO.output(a1, 0)
      GPIO.output(a2, 1)
      GPIO.output(b1, 1)
      GPIO.output(b2, 0)
      iterateStep(axis, direction)

   elif step == 3:
      GPIO.output(a1, 0)
      GPIO.output(a2, 0)
      GPIO.output(b1, 1)
      GPIO.output(b2, 1)
      iterateStep(axis, direction)

   else:
      if axis:
         print("X-axis overstep error. xStep = %s" % xStep)
      else:
         print("Y-axis overstep error. yStep = %s" % yStep)


# Step motor in direction in half steps
def halfStep(axis, direction):
   global xStep, yStep
   a1, a2, b1, b2 = redefine(axis)

   # Set step based on working axis
   if axis: 
      step = xStep
   else: 
      step = yStep

   # Check step is not illegal
   if step >= 8 and direction: # redundant but protects from errors
      step = 0
   elif step < 0 and not direction:
      step = 7
   
   # Move the poles depending on the current step
   if step == 0:
      GPIO.output(a1, 1)
      GPIO.output(a2, 0)
      GPIO.output(b1, 0)
      GPIO.output(b2, 0)
      iterateHalfStep(axis, direction)

   elif step == 1:
      GPIO.output(a1, 1)
      GPIO.output(a2, 1)
      GPIO.output(b1, 0)
      GPIO.output(b2, 0)
      iterateHalfStep(axis, direction)

   elif step == 2:
      GPIO.output(a1, 0)
      GPIO.output(a2, 1)
      GPIO.output(b1, 0)
      GPIO.output(b2, 0)
      iterateHalfStep(axis, direction)

   elif step == 3:
      GPIO.output(a1, 0)
      GPIO.output(a2, 1)
      GPIO.output(b1, 1)
      GPIO.output(b2, 0)
      iterateHalfStep(axis, direction)
   
   elif step == 4:
      GPIO.output(a1, 0)
      GPIO.output(a2, 0)
      GPIO.output(b1, 1)
      GPIO.output(b2, 0)
      iterateHalfStep(axis, direction)

   elif step == 5:
      GPIO.output(a1, 0)
      GPIO.output(a2, 0)
      GPIO.output(b1, 1)
      GPIO.output(b2, 1)
      iterateHalfStep(axis, direction)

   elif step == 6:
      GPIO.output(a1, 0)
      GPIO.output(a2, 0)
      GPIO.output(b1, 0)
      GPIO.output(b2, 1)
      iterateHalfStep(axis, direction)

   elif step == 7:
      GPIO.output(a1, 1)
      GPIO.output(a2, 0)
      GPIO.output(b1, 0)
      GPIO.output(b2, 1)
      iterateHalfStep(axis, direction)

   else:
      if axis:
         print("X-axis overstep error. xStep = %s" % xStep)
      else:
         print("Y-axis overstep error. yStep = %s" % yStep)


# Iterates motor step by 1 (not interchangable to prevent stuttering)
def iterateStep(axis, direction):
   global xStep, yStep

   if axis:
      if direction:
         xStep += 1
      else:
         xStep -= 1
   else:
      if direction:
         yStep += 1
      else:
         yStep -= 1

   # check for illegal state
   if xStep >= 4:
      xStep = 0

   if xStep < 0:
      xStep = 3

   if yStep >= 4:
      yStep = 0

   if yStep < 0:
      yStep = 3


# Iterates motor half step by 1 (not interchangable to prevent stuttering)
def iterateHalfStep(axis, direction):
   global xStep, yStep

   if axis:
      if direction:
         xStep += 1
      else:
         xStep -= 1
   else:
      if direction:
         yStep += 1
      else:
         yStep -= 1

   if xStep >= 8:
      xStep = 0

   if xStep < 0:
      xStep = 7

   if yStep >= 8:
      yStep = 0

   if yStep < 0:
      yStep = 7


# Helper function to redefine motors
def redefine(axis):
   if axis:
      a1 = XA1
      a2 = XA2
      b1 = XB1
      b2 = XB2

   else:
      a1 = YA1
      a2 = YA2
      b1 = YB1
      b2 = YB2
   
   return a1, a2, b1, b2


### Initializer function
def init(penDelayIn, stepSizeIn):
   global penDelay, stepSize
   penDelay = penDelayIn
   stepSize = stepSizeIn
   
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
   GPIO.setup(PEN, GPIO.OUT)

   GPIO.setup(XA1, GPIO.OUT)
   GPIO.setup(XA2, GPIO.OUT)
   GPIO.setup(XB1, GPIO.OUT)
   GPIO.setup(XB2, GPIO.OUT)

   GPIO.setup(YA1, GPIO.OUT)
   GPIO.setup(YA2, GPIO.OUT)
   GPIO.setup(YB1, GPIO.OUT)
   GPIO.setup(YB2, GPIO.OUT)
