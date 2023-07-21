import dot
import os
import potrace
import cv2
import numpy as np
from datetime import datetime
import time

CYAN = 3
MAGENTA = 2
YELLOW = 1
BLACK = 0

# Read image from file and split into layers
def readImage(filename):
   image = cv2.imread(filename)
   bgr = image.astype(np.float)/255

   with np.errstate(invalid='ignore',divide='ignore'):
      K = 1 - np.max(bgr, axis=2)
      C = (1-bgr[...,2] - K)/(1-K)
      M = (1-bgr[...,1] - K)/(1-K)
      Y = (1-bgr[...,0] - K)/(1-K)
   CMYK = (C, M, Y, K)
   return image, CMYK


# gets size of image
def getSize(image):
   height, width, channels = image.shape
   return height, width


# takes in inupt parameters in order to start plotting image
def processPrint(filename, color, threshold, scale, invert):
   image, CMYK = readImage(filename)
   height, width = getSize(image)

   if (color):
      for i in CMYK:
         dot.findPoint(0,0)
         printImage(i, width, height, threshold, scale, invert)
   else:
      printImage(CMYK[3], width, height, threshold, scale, invert)


# print image as dot matrix
def printImage(layer, width, height, threshold, scale, invert):
   startTime = datetime.now()
   cx = 0
   cy = 0
   print()

   if not invert:
      for y in range(height):
         print()
         penState = False
         x = 0
         line = []
         for o in range(width):
            line.append("\u001B[37m" + u"\u2588"+ u"\u2588")
   
         for x in range(width):
            if y%2 == 0:
               dot.findPoint(x*scale, y*scale)
               if (layer[y][x]*256)-1 > threshold:
                  line[x] = "\u001B[30m" + u"\u2588" + u"\u2588"
                  print("".join(line), end="\r")
                  if x + 1 < width:
                     if (layer[y][x+1]*256)-1 > threshold:
                        dot.dot()
                        time.sleep(0.2)
                     else:
                        dot.dot()
                        #dot.penDown()
                        time.sleep(0.2)
                  else:
                     dot.penUp()
                     time.sleep(0.2)
               else:
                  print("".join(line), end="\r")
   
            else:
               dot.findPoint((width-x-1)*scale,y*scale)
               if (layer[y][width-x-1]*256)-1 > threshold:
                  line[width-x-1] = "\u001B[30m" + u"\u2588"+ u"\u2588"
                  print("".join(line), end="\r")
                  if x - 1 >= 0:
                     if (layer[y][width-x-2]*256)-1 > threshold:
                        dot.dot()
                        #dot.penDown()
                        time.sleep(0.2)
                     else:
                        dot.dot()
                        time.sleep(0.2)
                  else:
                     dot.penUp()
                     time.sleep(0.2)
               else:
                  print("".join(line), end="\r")

   else:
      for y in range(height):
         print()
         penState = False
         x = 0
         line = []
         for o in range(width):
            line.append("\u001B[30m" + u"\u2588"+ u"\u2588")

         for x in range(width):
            if y%2 == 0:
               dot.findPoint(x*scale, y*scale)
               if (layer[y][x]*256)-1 < threshold:
                  line[x] = "\u001B[37m" + u"\u2588" + u"\u2588"
                  print("".join(line), end="\r")
                  if x + 1 < width:
                     if (layer[y][x+1]*256)-1 < threshold:
                        dot.dot()
                        #dot.penDown()
                        time.sleep(0.2)
                     else:
                        dot.dot()
                        time.sleep(0.2)
                  else:
                     dot.penUp()
                     time.sleep(0.2)
               else:
                  print("".join(line), end="\r")

            else:
               dot.findPoint((width-x-1)*scale,y*scale)
               if (layer[y][width-x-1]*256)-1 < threshold:
                  line[width-x-1] = "\u001B[37m" + u"\u2588"+ u"\u2588"
                  print("".join(line), end="\r")
                  if x - 1 >= 0:
                     if (layer[y][width-x-2]*256)-1 < threshold:
                        dot.dot()
                        #dot.penDown()
                        time.sleep(0.2)
                     else:
                        dot.dot()
                        time.sleep(0.2)
                  else:
                     dot.penUp()
                     time.sleep(0.2)
               else:
                  print("".join(line), end="\r")

   # copy entire thing down and flip inequalities for color inversion

   print("\n")
   print("Print complete. " + str(width) + "x" + str(height) + " - ", end="")
   print(datetime.now()-startTime)
   dot.findPoint(0,0)
   dot.releaseAll()


# draw inputted bezier curve
def drawCurve(bezier, scale):
   points = bezier.points
   dot.penUp()
   dot.findPoint(points[0].x * scale, points[0].y * scale)
   dot.penDown()
   dot.findPoint(points[3].x * scale, points[3].y * scale)


# convert image to set of bezier curves
def bezierConversion(filename, scale):
   image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
   binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
   bitmap = potrace.Bitmap(binary)
   path = bitmap.trace()

   f = input("Pen Ready? (Press any key to continue)")

   for curve in path:
      bezier = curve.to_bezier()
      for b in bezier:
         drawCurve(b, scale)


# does the things main does (mostly getting information from user)
def main():
   print('''
          _____                    _____                            _____                    _____                    _____                    _____          
         /\    \                  /\    \                          /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                        /::\    \                /::\    \                /::\    \                /::\____\        
       /::::\    \               \:::\    \                      /::::\    \              /::::\    \              /::::\    \              /:::/    /        
      /::::::\    \               \:::\    \                    /::::::\    \            /::::::\    \            /::::::\    \            /:::/   _/___      
     /:::/\:::\    \               \:::\    \                  /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/   /\    \     
    /:::/__\:::\    \               \:::\    \                /:::/  \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/   /::\____\    
   /::::\   \:::\    \              /::::\    \              /:::/    \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /:::/   /:::/    /    
  /::::::\   \:::\    \    ____    /::::::\    \            /:::/    / \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/   /:::/   _/___  
 /:::/\:::\   \:::\____\  /\   \  /:::/\:::\    \          /:::/    /   \:::\ ___\  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /:::/___/:::/   /\    \ 
/:::/  \:::\   \:::|    |/::\   \/:::/  \:::\____\        /:::/____/     \:::|    |/:::/  \:::\   \:::|    |/:::/  \:::\   \:::\____\|:::|   /:::/   /::\____\\
\::/    \:::\  /:::|____|\:::\  /:::/    \::/    /        \:::\    \     /:::|____|\::/   |::::\  /:::|____|\::/    \:::\  /:::/    /|:::|__/:::/   /:::/    /
 \/_____/\:::\/:::/    /  \:::\/:::/    / \/____/          \:::\    \   /:::/    /  \/____|:::::\/:::/    /  \/____/ \:::\/:::/    /  \:::\/:::/   /:::/    / 
          \::::::/    /    \::::::/    /                    \:::\    \ /:::/    /         |:::::::::/    /            \::::::/    /    \::::::/   /:::/    /  
           \::::/    /      \::::/____/                      \:::\    /:::/    /          |::|\::::/    /              \::::/    /      \::::/___/:::/    /   
            \::/____/        \:::\    \                       \:::\  /:::/    /           |::| \::/____/               /:::/    /        \:::\__/:::/    /    
             ~~               \:::\    \                       \:::\/:::/    /            |::|  ~|                    /:::/    /          \::::::::/    /     
                               \:::\    \                       \::::::/    /             |::|   |                   /:::/    /            \::::::/    /      
                                \:::\____\                       \::::/    /              \::|   |                  /:::/    /              \::::/    /       
                                 \::/    /                        \::/____/                \:|   |                  \::/    /                \::/____/        
                                  \/____/                          ~~                       \|___|                   \/____/                  ~~              
''')
   print("Brian Hill 2023")
   print("https://github.com/TrojanPinata/PiDraw")
   f = input("Press d to enter debug or anything else to continue normally.")
   if f == "d":
      debug()
      
   dot.init()
   filename = input("What file do you want to print? ")
   if not os.path.isfile(filename):
       print("File not found. Exiting.")
       exit()

   draw = input("Draw image? (0 or 1) ")
   if (draw == "1"):
      scale = input("what image scaling should be applied (1 - 10) ")
      if (scale != ""):
         scale = int(scale)
         if (scale > 10 or scale < 1):
            scale = 4
         else: 
            scale = int(scale)
      else:
         scale = 4
      f = input("Pen ready? (Press any key to continue)")
      bezierConversion(filename, scale)

   else:
      color = input("B/W or Color? (0 or 1) ")
      if (color == "1"):
         color = True
         invert = False
      else:
         color = False
         invert = input("Invert colors? (0 or 1) ")
         if invert == "1":
            invert = True
         else:
            invert = False
      threshold = input("What is the threshold to print at? (0-255) ")
      if (threshold != ""): # why did I write this?
         threshold = int(threshold)
         if (threshold > 255 or threshold < 0):
            threshold = 127
         else:
            threshold = int(threshold)
      else:
         threshold = 127
      scale = input("What image scaling should be applied? (1 - 10) ")
      if (scale != ""):
         scale = int(scale)
         if (scale > 10 or scale < 1):
            scale = 4
         else: 
            scale = int(scale)
      else:
         scale = 4

      f = input("Pen ready? (Press any key to continue)")
      processPrint(filename, color, threshold, scale, invert)


# just in case you wantted to see the limits of each axis
def debug():
   dot.init()
   x = 0
   y = 0
   while(True):
      f = input("(x stat) press any key until no space left (q to quit)")
      if (f == "q"):
         break
      dot.iterateX()
      x += 1

   while(True):
      f = input("(y stat) press any key until no space left (q to quit)")
      if (f == "q"):
         break
      dot.iterateY()
      y += 1

   print("plate size: " + x + ", " + y)


if __name__=="__main__":
   main()
