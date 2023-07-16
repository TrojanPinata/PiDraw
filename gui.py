from tkinter import *
from tkinter import filedialog
import os
import picture, dot

filepath = ''

root = Tk()
root.geometry("500x600")
root.title("PyDraw v1.1")

def returnHome(frame):
    clearFrame(frame)
    frontPage()

def clearFrame(frame):
    frame.pack_forget()
    frame.destroy()

def buildFrame(frame=None):
    if frame != None:
        return Frame(frame)
    else:
        return Frame(root)

def chooseFile(frame):
    global filepath
    filepath = filedialog.askopenfilename()
    clearFrame(frame)
    frontPage(frame)

def optionsCheck(colorCheck, scaleField, thresholdField):
    global filepath
    if not (filepath.endswith(".png") or filepath.endswith(".jpg") or filepath.endswith(".bmp")):
        messagebox.showerror(title="Illegal file type", message="Make sure the image you are trying to use is a image file")
        return False
    elif scaleField > 10:
        messagebox.showerror(title="Illegal scale value", message="Scale is too large")
        return False
    elif scaleField < 1:
        messagebox.showerror(title="Illegal scale value", message="Scale is too small")
        return False
    elif thresholdField > 255:
        messagebox.showerror(title="Illegal threshold value", message="Threshold is too high")
        return False
    elif thresholdField < 0:
        messagebox.showerror(title="Illegal threshold value", message="Threshold is too low")
        return False
    else:
        return True
    return False

def runPicture(frame, colorCheck, scaleField, thresholdField, drawCheck, invertCheck):
    if not optionsCheck(colorCheck, scaleField, thresholdField):
        frontPage(frame)
    else:
        if drawCheck:
            picture.bezierConversion(filepath, scaleField)
        else:
            picture.processPrint(filepath, colorCheck, thresholdField, scaleField, invertCheck)

def frontPage(frame0=None):
    global filepath
    dot.init()
    if frame0 != None:
        clearFrame(frame0)
    frame = buildFrame()
    frame.pack()

    headerText = Label(frame, text="PyDraw", font=("IBM Plex Sans",20))
    browseBtn = Button(frame, text="File to Print", bd="5", command=lambda: chooseFile(frame))

    if filepath == "":
        fileText = Label(frame, text="No File Selected...", font=("IBM Plex Sans", 10, "bold"))
    else:
        fileText = Label(frame, text=filepath, font=("IBM Plex Sans", 10, "bold"))
    
    scaleField = 1
    thresholdField = 128
    drawCheck = False
    colorCheck = False
    invertCheck = False

    colorCheckText = Label(frame, text="Color", font=("IBM Plex Sans", 10))
    colorEntry = Checkbutton(frame, text="", variable=colorCheck, onvalue=True, offvalue=False)
    invertCheckText = Label(frame, text="Invert", font=("IBM Plex Sans", 10))
    invertEntry = Checkbutton(frame, text="", variable=invertCheck, onvalue=True, offvalue=False)
    scaleFieldText = Label(frame, text="Scale (1 - 10)", font=("IBM Plex Sans", 10))
    scaleEntry = Entry(frame, textvariable=scaleField, width=10)
    thresholdFieldText = Label(frame, text="Threshold (0 - 255)", font=("IBM Plex Sans", 10))
    thresholdEntry = Entry(frame, textvariable=thresholdField, width=10)
    drawText = Label(frame, text="Draw", font=("IBM Plex Sans", 10))
    drawEntry = Checkbutton(frame, text="", variable=drawCheck, onvalue=True, offvalue=False)
    debugBtn = Button(frame, text="Debug", bd="5", command=lambda: dot.debug())
    exitBtn = Button(frame, text="Exit", bd="5", command=lambda: cleanExit())
    submitBtn = Button(frame, text="Print", bd="5", command=lambda: runPicture(frame, colorCheck, scaleField, thresholdField, drawCheck, invertCheck))

    headerText.grid(row = 0, column = 0, pady=(15,15))
    browseBtn.grid(row = 1, column = 0, pady=(15,15))
    fileText.grid(row = 1, column = 1, pady=(15,15))
    drawText.grid(row = 2, column = 0, pady=(15,15))
    drawEntry.grid(row = 2, column = 1, pady=(15,15))
    colorCheckText.grid(row = 3, column = 0, pady=(15,15))
    colorEntry.grid(row = 3, column = 1, pady=(15,15))
    invertCheckText.grid(row = 4, column = 0, pady=(15,15))
    invertEntry.grid(row = 4, column = 1, pady=(15,15))
    scaleFieldText.grid(row = 5, column = 0, pady=(15,15))
    scaleEntry.grid(row = 5, column = 1, pady=(15,15))
    thresholdFieldText.grid(row = 6, column = 0, pady=(15,15))
    thresholdEntry.grid(row = 6, column = 1, pady=(15,15))
    submitBtn.grid(row = 7, column = 0, pady=(15,15))
    debugBtn.grid(row = 8, column = 0, pady=(15,15))
    exitBtn.grid(row = 8, column = 1, pady=(15,15))

def cleanExit():
    dot.releaseAll()
    exit()

def main():
    frontPage()
    root.mainloop()

if __name__=="__main__":
    main()
