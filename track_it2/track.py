from __future__ import division
from Tkinter import *
import datetime
import shutil
from tkMessageBox import *
import webbrowser
import json
import os


def get_appropriate_text():
    if os.path.isfile('track_results.json'):
        with open('track_results.json') as tr:
            return tr.read()
    else:
        return 'Welcome. Start the exercise and view the results here.'


def track_once(duration, num_rects, post_fb, pre_fb, fb_time, rectangle_height, feedback, spawn_mode, max_v):
    num_reps = int(repsChoice.get())
    config = {
        "fb_time": int(fb_time),
        "time_post_fb": int(post_fb),
        "num_rectangles": int(num_rects),
        "with_fb": int(feedback),
        "time_to_fb": int(pre_fb),
        "duration": int(duration),
        "rect_height": int(rectangle_height),
        "num_reps": num_reps,
        "max_voltage": max_v
    }
    if spawn_mode == "Last setting":
        with open('saved_series.txt') as s:
            config["series"] = s.read()
    elif spawn_mode == "Custom":
        config["series"] = stationary_series.get()
    with open('config.cfg', 'w') as cfg:
        cfg.write(json.dumps(config, indent=4))
    os.system('python exercise.py')
    #     showerror('Error', 'You have not chosen all the parameters correctly!')
    #     return


def clear_results():
    with open('track_results.json', 'w') as tr:
        tr.write('')
    plot_path = os.path.join(os.getcwd(), 'plots')
    for plot in os.listdir(plot_path):
        os.remove(os.path.join(plot_path, plot))
    samples_path = os.path.join(os.getcwd(), 'raw_samples')
    for samples_file in os.listdir(samples_path):
        os.remove(os.path.join(samples_path, samples_file))
    os.remove('results_excel.txt')


def view_web():
    webbrowser.open("http://127.0.0.1:8000/index", new=1, autoraise=True)


# def update():
#     text.delete("1.0", END)
#     text.insert(END, get_appropriate_text())


def save_all():
    try:
        dump_dir_name = 'tracking_{}'.format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        new_dir = os.path.join(os.getcwd(), dump_dir_name)
        os.mkdir(new_dir)
        shutil.copyfile('track_results.json', os.path.join(new_dir, 'track_results.json'))
        shutil.copyfile('results_excel.txt', os.path.join(new_dir, 'results_excel.txt'))
        shutil.copyfile('results_quest_excel.txt', os.path.join(new_dir, 'results_quest_excel.txt'))
        shutil.copytree(os.path.join(os.getcwd(), 'plots'), os.path.join(new_dir, 'plots'))
        shutil.copytree(os.path.join(os.getcwd(), 'raw_samples'), os.path.join(new_dir, 'raw_samples'))
        showinfo("Saving successful!",
                 message='Saving succeed! Data saved in a new folder named: {}'.format(dump_dir_name))
    except Exception, e:
        showerror(title="Oj!", message="The following problem occured: {}".format(e.message))
        raise


def run_server():
    try:
        os.system("start runserver.bat")
        showinfo(title="Server up!", message="Sever set up successfully!")
    except OSError, e:
        showerror(title="Oj!", message="Server could not start due to: {}".format(e.message))


def view_help():
    try:
        os.system("start help.txt")
    except OSError, e:
        showerror(title="Oj!", message="Help could not be displayed because of: {}".format(e.message))


def view_about():
    showinfo(title='About', message='TRACK IT! v.1.0\nAuthor: Krzysztof Malarski')


def start_quest(series, quest, rect_width, rect_height, max_v):
    res_path = 'q_{}.txt'.format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    config2 = {
        "rect_height": int(rect_height),
        "rect_width": int(rect_width),
        "series": [num for num in series.split()],  # store strings, so that the colours can also be decoded
        "quest": quest,
        "res_path": res_path,
        "max_voltage": max_v
    }
    with open('config2.cfg', 'w') as cfg:
        cfg.write(json.dumps(config2, indent=4))
    with open(res_path, "w") as q:
        q.write("series:\t{}\n".format(series))
        q.write("exercise:\t{}\n".format(quest.replace("s", series)))
    os.system('python exercise2.py')


app = Tk()
app.title("TRACK IT!")
# Auxiliary variables' declarations
samples = IntVar()
rects = IntVar()
pause_duration = IntVar()
is_repetitive = IntVar()
is_feedback = IntVar()
labelText = StringVar()
controlText = StringVar()
informText = StringVar()
informText.set("Stationary exercise parameters:")
stationary_series = StringVar()
stationary_series.set("250 500 250 500")
series = StringVar()
series.set("100v 400f")
quest = StringVar()
quest.set("400 300 s 240 100 s 500")
series_first = IntVar()
repeat = IntVar()
max_voltage = StringVar()
max_voltage.set("-2.5")
# This dictionary will be passed to tracking class
param_dict = {}

topFrame = Frame(app)
topFrame.pack()
radioFrame = Frame(app)
radioFrame.pack()
othersFrame = Frame(app)
othersFrame.pack()
buttonsFrame = Frame(app)
buttonsFrame.pack()

labelText.set("CONFIGURE PARAMETERS AND START YOUR FAVOURITE EXCITING EXERCISE!")
label1 = Label(topFrame, textvariable=labelText).grid(row=0, column=0, columnspan=4)

controlText.set('If you are not sure how to work with the programme please click "View help" button!')
controlLabel = Label(topFrame, textvariable=controlText).grid(row=1, column=0, columnspan=4)

informLabel = Label(topFrame, textvariable=informText).grid(row=2, column=0, columnspan=4)

repsLabel = Label(topFrame, text='Number of repetitions:').grid(row=3, column=0)
repsChoice = Spinbox(topFrame, from_=1, to=10)
repsChoice.grid(row=3, column=1)
repetitiveChoice = Checkbutton(topFrame, text="Multi-run?", variable=is_repetitive, onvalue=1, offvalue=0, height=5,
                               width=20).grid(row=3, column=2)
feedbackChoice = Checkbutton(topFrame, text="Feedback?", variable=is_feedback, onvalue=1, offvalue=0).grid(row=3,
                                                                                                           column=3)
modeLabel = Label(topFrame, text='Spawn mode:').grid(row=4, column=0)
modeBox = Spinbox(topFrame, values=("Random", "Last setting", "Custom"), wrap=True)
modeBox.grid(row=4, column=1)
heightLabel = Label(topFrame, text='Rectangle  height:').grid(row=4, column=2)
yourHeightChoice = Spinbox(topFrame, from_=1, to=999, wrap=True)
yourHeightChoice.grid(row=4, column=3)

rectLabel = Label(topFrame, text='Number of random rectangles:').grid(row=5, column=0)
rectChoice = Spinbox(topFrame, from_=1, to=10, wrap=True)
rectChoice.grid(row=5, column=1)
statSeriesLabel = Label(topFrame, text='Type series values (space-separated):').grid(row=5, column=2)
statSeriesField = Entry(topFrame, textvariable=stationary_series).grid(row=5, column=3)

preFbLabel = Label(topFrame, text='Time to fb (seconds):').grid(row=6, column=0, sticky=W)
preFbChoice = Spinbox(topFrame, from_=1, to=10, wrap=True)
preFbChoice.grid(row=6, column=1)
FbLabel = Label(topFrame, text='Fb time (seconds):').grid(row=6, column=2, sticky=W)
fbChoice = Spinbox(topFrame, from_=1, to=10, wrap=True)
fbChoice.grid(row=6, column=3)
postFbLabel = Label(topFrame, text='Time after fb (seconds):').grid(row=7, column=0, sticky=W)
postFbChoice = Spinbox(topFrame, from_=1, to=10, wrap=True)
postFbChoice.grid(row=7, column=1)
lengthLabel = Label(topFrame, text='Length of the exercise (seconds):').grid(row=7, column=2, sticky=W)
lengthChoice = Spinbox(topFrame, from_=1, to=12, wrap=True)
lengthChoice.grid(row=7, column=3)
maxVoltageLabel = Label(topFrame, text='A PARAMETER FOR WHATEVER MODE:').grid(row=8, columnspan=4)
maxVolatgeText = Label(topFrame, text='Maximum input voltage (in volts):').grid(row=9, column=0, columnspan=2)
maxVoltageField = Entry(topFrame, textvariable=max_voltage).grid(row=9, column=2, columnspan=2)

# QUEST PART
questLabel = Label(othersFrame, text='Parameters for quest mode:').grid(row=0)
# lastQuestChoice = Checkbutton(othersFrame, text='Last settings?', variable=repeat, onvalue=1, offvalue=0).grid(
#     row=1, column=0)
# numSeriesLabel = Label(othersFrame, text='Number of series:').grid(row=2, column=0)
# # text = Text(othersFrame)
# # text.insert(INSERT, get_appropriate_text())
# # text.config(height=20, width=40)
# # text.grid(row=1, column=1, rowspan=12)
# numSeriesChoice = Spinbox(othersFrame, from_=0, to=100, wrap=True)
# numSeriesChoice.grid(row=3, column=0)
# seriesLabel = Label(othersFrame, text='Type series values (space-separated):').grid(row=4, column=0)
# seriesField = Entry(othersFrame, textvariable=series).grid(row=5, column=0)
# seriesFirstChoice = Checkbutton(othersFrame, text='Series first?', variable=series_first, onvalue=1, offvalue=0).grid(
#     row=6, column=0)
# numRandomLabel = Label(othersFrame, text='Number of random rectangles:').grid(row=7, column=0)
# numRandom = Spinbox(othersFrame, from_=0, to=100, wrap=True)
# numRandom.grid(row=8, column=0)
# rectWidthLabel = Label(othersFrame, text='Rectangle width:').grid(row=9, column=0)
# rectWidthChoice = Spinbox(othersFrame, from_=1, to=499, wrap=True)
# rectWidthChoice.grid(row=10, column=0)
# rectHeightLabel = Label(othersFrame, text='Rectangle height:').grid(row=11, column=0)
# rectHeightChoice = Spinbox(othersFrame, from_=1, to=999, wrap=True)
# rectHeightChoice.grid(row=12, column=0)

# HERE YOU CAN CHANGE COLOUR HELP TEXT
colourLabel = Label(othersFrame, text='b=blue, g=green, y=yellow, v=violet, r=red, p=pink, c=cyan, f=black').grid(row=1)
seriesLabel = Label(othersFrame, text='Type series values (space-separated):').grid(row=2, column=0)
seriesField = Entry(othersFrame, textvariable=series).grid(row=2, column=1)
questRunLabel = Label(othersFrame, text='Type quest values: random and series (space-separated):').grid(row=3, column=0)
questField = Entry(othersFrame, textvariable=quest).grid(row=3, column=1)
rectWidthLabel = Label(othersFrame, text='Rectangle width:').grid(row=4, column=0)
rectWidthChoice = Spinbox(othersFrame, from_=1, to=499, wrap=True)
rectWidthChoice.grid(row=4, column=1)
rectHeightLabel = Label(othersFrame, text='Rectangle height:').grid(row=5, column=0)
rectHeightChoice = Spinbox(othersFrame, from_=1, to=999, wrap=True)
rectHeightChoice.grid(row=5, column=1)

start_one_button = Button(buttonsFrame, text="Start normal exercise",
                          command=lambda: track_once(duration=lengthChoice.get(), num_rects=rectChoice.get(),
                                                     post_fb=postFbChoice.get(),
                                                     pre_fb=preFbChoice.get(),
                                                     fb_time=fbChoice.get(),
                                                     rectangle_height=yourHeightChoice.get(),
                                                     feedback=is_feedback.get(),
                                                     spawn_mode=modeBox.get(),
                                                     max_v=max_voltage.get()))

start_one_button.pack(side=LEFT)
strongman_button = Button(buttonsFrame, text='Start quest exercise',
                           command=lambda: start_quest(series=series.get(),
                                                       quest=quest.get(),
                                                       rect_width=rectWidthChoice.get(),
                                                       rect_height=rectHeightChoice.get(),
                                                       max_v=max_voltage.get())).pack(side=LEFT)
# updateButton = Button(buttonsFrame, text='Update results', command=update).pack(side=LEFT)
saveButton = Button(buttonsFrame, text='Save data', command=save_all).pack(side=LEFT)
clear_button = Button(buttonsFrame, text="Clear data", command=clear_results).pack(side=LEFT)
run_web_button = Button(buttonsFrame, text='Run Webserver', command=run_server).pack(side=LEFT)
web_button = Button(buttonsFrame, text="View the Website", command=view_web).pack(side=LEFT)
help_button = Button(buttonsFrame, text='View help', command=view_help).pack(side=LEFT)
about_button = Button(buttonsFrame, text='About', command=view_about).pack(side=LEFT)

app.mainloop()
