from Tkinter import *
import json
import os

def start_ex():
    config = {
        "raw_rects_pauses_str": str(exercise.get()),
        "time_rect_s": str(rectTime.get()),
        "rect_h": str(rectHeight.get()),
        "triggers": str(triggers.get()),
        "show_fb_time": str(show_fb_time.get())
    }
    print config
    with open('conf.cfg', 'w') as c:
        c.write(json.dumps(config, indent=4))
    os.system('python exercise2_new.py') # this line works on win 7 

app = Tk()
app.title("TRACK IT Lite")

exercise = StringVar()
exercise.set("R800r P200 R400r P200 R400r P200 R400r P200")
rectTime = StringVar()
rectTime.set("2")
rectHeight = StringVar()
rectHeight.set("30")
labelText = StringVar()
labelText.set("CONFIGURE PARAMETERS CAREFULLY!")
triggers = StringVar()
triggers.set("1")
show_fb_time = StringVar()
show_fb_time.set("2")

topFrame = Frame(app)
topFrame.pack()


label1 = Label(topFrame, textvariable=labelText).grid(row=0, column=0, columnspan=4)

colourLabel = Label(topFrame, text='R=rectangle, P=pause, b=blue, g=green, y=yellow, v=violet, r=red, p=pink, c=cyan, f=black').grid(row=1)

inputLabel = Label(topFrame, text='Exercise events (space-separated):').grid(row=2, column=0, columnspan=4)
inputField = Entry(topFrame, textvariable=exercise).grid(row=3, column=0, columnspan=4)

rectTimeLabel = Label(topFrame, text='Rectangle display time (seconds):').grid(row=4, column=0, columnspan=2)
rectTimeField = Entry(topFrame, text=rectTime).grid(row=4, column=2, columnspan=2)

rectHeightLabel = Label(topFrame, text='Rectangle height (px):').grid(row=5, column=0, columnspan=2)
rectHeightField = Entry(topFrame, text=rectHeight).grid(row=5, column=2, columnspan=2)

triggersLabel = Label(topFrame, text='Trigger rectangle indices (space-separated):').grid(row=6, column=0, columnspan=2)
triggersField = Entry(topFrame, text=triggers).grid(row=6, column=2, columnspan=2)

fbTimeLabel = Label(topFrame, text='Feedback display time in seconds (0 means no display):').grid(row=7, column=0, columnspan=2)
fbTimeField = Entry(topFrame, text=show_fb_time).grid(row=7, column=2, columnspan=2)

startButton = Button(topFrame, text='Start', command=lambda: start_ex()).grid(row=8, column=0, columnspan=4)


app.mainloop()
