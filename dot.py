import time
import board
import RPi.GPIO as GPIO
import motor

### Fields
xDirection = False
yDirection = False
x = 0
y = 0
xLim = 150
yLim = 150
penDelay = 0.2
stepDelay = 0.07


# Set positions to zero
def setZero():
   global x, y
   x = 0
   y = 0


# Return to (0,0)
def returnHome():
   findPoint(0, 0)


# Find given point moving directly there (via diagonal)
def smoothFind(xMod, yMod):
   xAxis = False
   yAxis = True
   xInit = x
   yInit = y

   for i in range(yInit, yMod):
      for j in range(xInit, xMod):
         j = (j - yInit)*(xMod - xInit)/(yMod - yInit)+xInit
         for r in range(x, j):
            if (r < 0):
               motor.step(xAxis, True)
            else:
               motor.step(xAxis, False)
            updatePos(xDirection)

         for s in range(y, i):
            if (s < 0):
               motor.step(yAxis, True)
            else:
               motor.step(yAxis, False)
            updatePos(yDirection)


# Find given point
def findPoint(xMod, yMod):
   xInit = x
   yInit = abs(y)

   if (xInit - xMod < 0):
      xDirection = False
   else:
      xDirection = True
   if (yInit - yMod < 0):
      yDirection = True
   else: 
      yDirection = False

   for i in range(abs(abs(xInit) - abs(xMod))):
      time.sleep(stepDelay)
      motor.halfStep(True, xDirection)
      #print("x = " + str(x))       # these have been so helpful
      updatePos(True, xDirection)

   for j in range(abs(abs(yInit) - abs(yMod))):
      time.sleep(stepDelay)
      motor.halfStep(False, yDirection)
      #print("y = " + str(y))
      updatePos(False, yDirection)


# Updates global position values
def updatePos(axis, direction):
   global x, y
   if axis:
      if direction:
         x -= 1
      else:
         x += 1
   else:
      if direction:
         y -= 1
      else:
         y += 1


def iterateX():
   x += 1
   motor.step(True, False)


def iterateY():
   y += 1
   motor.step(False, False)


### Interface with motor.py
def dot():
   motor.dot()


def penUp():
   motor.penUp()


def penDown():
   motor.penDown()


def releaseAll():
   motor.releaseAll()


def releaseX():
   motor.releaseX()


def releaseY():
   motor.releaseY()


def init():
   motor.init(penDelay, 1)


# main function to do all of the things main does
def main():
   init()
   z = 0
   c = True
   v = True
   print("Key | Command\n====================\n f  | fowrard\n r  | reverse\n x  | x-axis\n y  | y-axis\n n  | go to (100,100)\n a  | diagonal to (100,100)\n h  | return to (0,0)\n t  | run test drawing\n d  | dot\n p  | pen down\n u  | pen up\n c  | release motors\n q  | release motors and quit\n")
   while(True):
      f = input()
      if f == "q":
         motor.releaseAll()
         penUp()
         break
      elif f == "f":
         v = True
      elif f == "r":
         v = False
      elif f == "x":
         c = True
      elif f == "y":
         c = False
      elif f == "d":
         dot()
      elif f == "p":
         penDown()
      elif f == "u":
         penUp()
      elif f == "h":
         returnHome()
         releaseAll()
      elif f == "n":
         findPoint(100, 100)
         releaseAll()
      elif f == "a":
         for i in range(100):
            findPoint(i,i)
         releaseAll()
      elif f == "t":
         returnHome()
         penDown()
         findPoint(100,0)
         findPoint(100,100)
         findPoint(0,100)
         findPoint(0,0)
         findPoint(50,0)
         for i in range(50):
            findPoint(i+50, i)
         for i in range(50):
            findPoint(100-i, i+50)
         for i in range(50):
            findPoint(50-i, 100-i)
         for i in range(50):
            findPoint(i, 50-i)
         penUp()
         findPoint(50,50)
         dot()
         penUp()
         returnHome()
         releaseAll()
      elif f == "c":
         releaseAll()
      else:
         motor.step(c, v)
         z += 1
         print(z)


if __name__=="__main__":
   main()
