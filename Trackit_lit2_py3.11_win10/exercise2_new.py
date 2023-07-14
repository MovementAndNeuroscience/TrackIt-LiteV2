from __future__ import division
import pygame
import os
import shutil
import datetime
import tools2
import json
import time
import numpy as np
### !!!!!!!!!!!!!! UNCOMMENT THE FOLLOWING BLOCK OF CODE WHEN USING DAQ !!!!!!!!!!!!!!!!!!!!!!!!
# import daqmxlib
# import PyDAQmx
# from PyDAQmx import Task

# def send_trigger(trigger_mode):
#     # Actuate a single digital pulse (period between 1 and 2 ms) on a desired port, depending on trigger mode value.
#     # trigger_mode: either "random" or "series"
#      print ("Sending TMS trigger signal... mode = %s" % trigger_mode)
    #  dev_port_line = "1"
    #  if trigger_mode == "random":
    #      dev_port_line = "/Dev1/port1/line3"  ### THERE MAY BE OTHER DEV NUMBER!
    #  elif trigger_mode == "series":
    #      dev_port_line = "/Dev1/port1/line2"  ### THERE MAY BE OTHER DEV NUMBER!
    #  print (dev_port_line)
    #  task = Task()
    #  task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    #  task.StartTask()
    #  task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([1], dtype=np.uint8), None, None)
    #  task.StopTask()
    #  task = Task()
    #  task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    #  task.StartTask()
    #  task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([0], dtype=np.uint8), None, None)
    #  task.StopTask()
### !!!!!!!!!!!!!! UNCOMMENT THE ABOVE BLOCK OF CODE WHEN USING DAQ !!!!!!!!!!!!!!!!!!!!!!!!
### !!!!!!!!!!!!!! COMMENT THE FOLLOWING BLOCK OF CODE WHEN USING DAQ !!!!!!!!!!!!!!!!!!!!!!!!    
def send_trigger(trigger_mode):
    print( "PUFF! trigger mode: {}".format(trigger_mode))
### !!!!!!!!!!!!!! COMMENT THE ABOVE BLOCK OF CODE WHEN USING DAQ !!!!!!!!!!!!!!!!!!!!!!!!

def UseDAQToUpdateCursor(moving_avg_samples, center_pos):

    ########## USE THE FOLLOWING LINE WHEN USING DAQ ############################
    # for i in range(len(moving_avg_samples) - 1):
    #     moving_avg_samples[i + 1] = moving_avg_samples[i]
    #     moving_avg_samples[0] = tools2.get_px_from_voltage(reader.read()[0], -2.0)
    #     moving_avg_samples[0] = tools2.get_px_from_voltage(0, -2.0)
    # center_pos = [int(500 + size[1] * 0.5), int(np.mean(moving_avg_samples))] # note the first argument within [] is encompassed with int()
    # print ("Sample: {}, moving avg: {}".format(moving_avg_samples[0], int(np.mean(moving_avg_samples))))
    return center_pos

def HasUserLeftPreviousRect(rect_h, rect_h0s, exit_time_ref, is_rect_now, cur_rect, exit_times, center_pos):
    if is_rect_now and cur_rect > 0:
        if rect_h0s[cur_rect - 1] <= center_pos[1] <= rect_h0s[cur_rect - 1] + rect_h:
            exit_times[cur_rect - 1] = time.time() - exit_time_ref
    return exit_times


def IsUserOnTarget(rect_h, rect_h0, time_ref, time_on_target, trace_size, screen, already_on_target, is_rect_now, cur_rect, b, r, entry_times, samples_px, center_pos, was_on_target, exit_time_ref, time_on_target_ref):
    currently_on_target = is_rect_now and rect_h0 <= center_pos[1] <= rect_h0 + rect_h
    if currently_on_target:
        pygame.draw.circle(screen, b, center_pos, trace_size)
        if not already_on_target: # so we enter the rectangle for the first time
           entry_times[cur_rect] = time.time() - time_ref
           already_on_target = True
           time_on_target_ref = time.time()
           was_on_target = True
        if not was_on_target: # we re-enter the rectangle
           time_on_target_ref = time.time()
           was_on_target = True
        exit_time_ref = time.time()
    else:
       pygame.draw.circle(screen, r, center_pos, trace_size)
       if was_on_target:  # stop the time on target stopwatch, add the most recent time that was spent inside the rectangle
           time_on_target += time.time() - time_on_target_ref 
           print("time on target : " + str(time_on_target))
           was_on_target = False
			   #draw an appropriate rectangle
    if is_rect_now:
        samples_px[cur_rect].append(center_pos[1])

    return time_on_target, already_on_target, entry_times, was_on_target, exit_time_ref, time_on_target_ref, samples_px

    

def DrawContentOnScreen():
    screen.fill(f) # make the screen black
    pygame.draw.rect(screen, white, [500, 1, size[0], size[1]], 0)
    if is_rect_now:
        pygame.draw.rect(screen, eval(cur_event[-1]), [500, rect_h0, size[1], rect_h], 4)

        
def ShowFeedbackOnScreen(time_rect_s, show_fb_time, font, screen, b, times_on_target):
    if show_fb_time > 0.0:
        screen.blit(font.render('Score: {0:.1f}%'.format(np.mean([t / time_rect_s for t in times_on_target]) * 100), True, b), (1100, 400))
    show_fb_time_ref = time.time()
    return show_fb_time_ref


def ListenToKeyEvents(beep, center_pos, time_ref, exit_time_ref, ready):
    for event in pygame.event.get():  # This enables clicking "X" to close the window (and the exercise programme)
        if event.type == pygame.QUIT:
            should_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                beep.play(maxtime=200)
                pygame.time.delay(400)  # because beep returns immediately!
                ready = True
                time_ref = exit_time_ref = time.time()
            elif event.key == pygame.K_i:
                center_pos[1] -= 20
            elif event.key == pygame.K_k:
                center_pos[1] += 20
    return time_ref,exit_time_ref,ready, center_pos

def SaveResultsAndConfInFiles(total_num_rects, entry_times, times_on_target, stddevs, inaccuracies, exit_times):
    date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    with open('q_{}.txt'.format(date_str), 'w') as r:
        r.write("Rect_no\tEntry_time (s)\tTime_on_target (s)\tSD (px)\tInaccuracy (px)\tExit_time(s)\n")
        for i in range(total_num_rects):
            r.write("{i}\t{et}\t{tot}\t{sd}\t{inac}\t{ext}\n".format(i=i, et=entry_times[i], tot=times_on_target[i], sd=stddevs[i], inac=inaccuracies[i], ext=exit_times[i]))
    try:
        dump_dir_name = 'quest_{}'.format(date_str)
        new_dir = os.path.join(os.getcwd(), dump_dir_name)
        os.mkdir(new_dir)
        shutil.copyfile('conf.cfg', os.path.join(new_dir, 'conf.cfg'))
        shutil.copyfile('q_{}.txt'.format(date_str), os.path.join(new_dir, 'q_{}.txt'.format(date_str)))
        print ('Results saved in the following folder: {}'.format(dump_dir_name))
    except Exception as e:
        print (e.message)
        raise

def ExitTheLastRectPrepareForNewRect(was_on_target, cur_event, time_on_target, time_on_target_ref, exit_times, exit_time_ref, times_on_target):
    if cur_event != "" and cur_event[0] == "R": # not the beginning
        if was_on_target:  # stop the time on target stopwatch, as we finished this rectangle
            time_on_target += time.time() - time_on_target_ref
                # the exit time is the time since last moment on target till the end of the rectangle
            was_on_target = False 
                # COMMENTED we were on target till the last moment, so we start counting the exit time
                # exit_time_ref = time.time()

        exit_times[cur_rect] =  exit_time_ref - time.time()
        times_on_target[cur_rect] = time_on_target
        time_on_target = 0
    return was_on_target, time_on_target, exit_times, times_on_target

def IsItTheEndOfStimuli(time_ref, cur_event, is_rect_now, rect_h0, time_pause_s, already_on_target, cur_rect, was_on_target, time_on_target, time_on_target_ref, exit_time_ref, rects_pauses_list, exit_times, times_on_target):
    if cur_event == "" or is_rect_now and time.time() - time_ref >= time_rect_s or not is_rect_now and time.time() - time_ref >= time_pause_s:
        # switch to the next event from the list
        was_on_target, time_on_target, exit_times, times_on_target = ExitTheLastRectPrepareForNewRect(was_on_target, cur_event, time_on_target, time_on_target_ref, exit_times, exit_time_ref, times_on_target)

        cur_event = rects_pauses_list.pop(0)
        is_rect_now, cur_rect, rect_h0, time_pause_s, time_ref, already_on_target, was_on_target = IsItRectOrPause(cur_event, is_rect_now, cur_rect, rect_h0, triggers, time_pause_s, time_ref, already_on_target, was_on_target)
    return time_ref, cur_event, is_rect_now, rect_h0, time_pause_s, already_on_target, cur_rect, was_on_target, time_on_target, time_on_target_ref, exit_time_ref, rects_pauses_list

def IsItRectOrPause(cur_event, is_rect_now, cur_rect, rect_h0, triggers, time_pause_s, time_ref, already_on_target, was_on_target):
    if cur_event[0] == "R":
        is_rect_now = True
        cur_rect += 1
        rect_h0 = int(cur_event[1:-1])
        if (cur_rect + 1) in triggers:
            send_trigger("series")
    elif cur_event[0] == "P":
        is_rect_now = False
        time_pause_s = int(cur_event[1:]) * 0.001
    time_ref = time.time()
    already_on_target = False
    was_on_target = False
    return  is_rect_now, cur_rect, rect_h0, time_pause_s, time_ref, already_on_target, was_on_target

def FeedbackAndResults( rect_h, time_rect_s, show_fb_time, rect_h0s, total_num_rects, show_fb_time_ref, font, screen, b, entry_times, times_on_target, samples_px, stddevs, inaccuracies, exit_times):
    if show_fb_time_ref == 0:
                # derive the missing quantities
        for i in range(total_num_rects):
            stddevs[i] = np.std(samples_px[i])
            inaccuracies[i] = np.mean([np.abs(sample - (rect_h0s[i] + 0.5 * rect_h)) for sample in samples_px[i]])
                # print len(samples_px[i])
                #print the results in the cmd  
        print (entry_times)
        print (times_on_target)
        print (stddevs)
        print (inaccuracies)
                # display average time on target on the screen
        show_fb_time_ref = ShowFeedbackOnScreen(time_rect_s, show_fb_time, font, screen, b, times_on_target)

        SaveResultsAndConfInFiles(total_num_rects, entry_times, times_on_target, stddevs, inaccuracies, exit_times)
    return show_fb_time_ref



with open('conf.cfg', 'r') as cfg:
    conf_dict = json.loads(cfg.read())

rect_h = int(conf_dict["rect_h"]) #rect_h = 100
raw_rects_pauses_str = conf_dict["raw_rects_pauses_str"] # raw_rects_pauses_str = "R500b P3000 R450v P600 R400p P1000 R400f P100 R400v P800 R400p P1000"
time_rect_s = int(conf_dict["time_rect_s"])# time_rect_s = 1  # time the rectangle is displayed
triggers = [int(trig) for trig in conf_dict["triggers"].split()] # triggers expressed as rect indices
show_fb_time = float(conf_dict["show_fb_time"])
rect_h0 = 0  # will be retrieved from the list!
rects_pauses_list = raw_rects_pauses_str.split()

def filterForR(wordList):
    list = []
    for word in wordList:
        if word.startswith("R"):
            list.append(word)
    return list

rects_list = filterForR(rects_pauses_list)
rect_h0s = [int(r_str[1:4]) for r_str in rects_list]
total_num_rects = len(rects_list)

time_pause_s = 0 # it will be retrieved from the list!
time_ref = 0 # time used to reference when changing rectangles
time_on_target_ref = 0  # used to calculate time on target
time_on_target = 0
exit_time_ref = 0
show_fb_time_ref = 0 # a reference time to control feedback display time
####### MOVING AVERAGE PARAMETER (SMOOTHENING)
x_point_avg = 5 # moving average of samples will be containing x_point_avg points
#######
moving_avg_samples = [0 for _ in range(x_point_avg)]  # 5-point sample set for moving average
# Initialize the graphical engine and the daq
pygame.init()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!! UNCOMMENT THE FOLLOWING LINE WHEN USING DAQ !!!!!!!!!!!!!!!!!!!!!!!!!!
#reader = daqmxlib.Reader()

pygame.display.set_caption("Quest mode")
font = pygame.font.SysFont('Arial', 35)
trace_size = 4
ready = False  # a flag for starting after pressing ENTER`
beep = pygame.mixer.Sound('beep.wav')
should_quit = False  # a flag for enabling quitting the game before the natural end

### ~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
size = [1000, 1000] # CHANGE FOR THE DESIRED SCREEN RESOLUTION
size_disp = [1920, 1080] #[2549, 1400] was the resolution in the lab
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

screen = pygame.display.set_mode(size_disp)
currently_on_target = False  # to alternate trace colours
already_on_target = False  # to detect when the user reaches the new rectangle for the first time
was_on_target = False # for a stopwatch counting time on target
is_rect_now = False # if not then we have a pause
cur_event = ""  # a string from the rectangle list
cur_rect = -1  # will iterate through a list, so it will start from 0 
# Define the colors we will use in RGB format
white = (255, 255, 255)
b = (0, 0, 255)  # blue
r = (255, 0, 0)  # red
f = (0, 0, 0)  # black
g = (0, 255, 0)  # green
y = (255, 255, 0)  # yellow
v = (148, 0, 211)  # violet
c = (0, 255, 255)  # cyan
p = (255, 20, 147)  # pink
# define the structures for the results
entry_times = [0 for _ in range(total_num_rects)]
times_on_target = [0 for _ in range(total_num_rects)]	
samples_px = [[] for _ in range(total_num_rects)]
stddevs = [0 for _ in range(total_num_rects)]
inaccuracies = [0 for _ in range(total_num_rects)]
exit_times = [0 for _ in range(total_num_rects)]
	

########## USE THE FOLLOWING LINE WHEN NOT USING DAQ ############################
center_pos = [1000, 500]

center_pos = UseDAQToUpdateCursor(moving_avg_samples, center_pos)

while not should_quit:
    
    time_ref, exit_time_ref, ready, center_pos = ListenToKeyEvents(beep, center_pos, time_ref, exit_time_ref, ready)

    if not ready:  # wait until ENTER pressed
        pygame.time.delay(100)
    else:	# the game is running
        if len(rects_pauses_list) > 0:
            # if beginning or current rect/pause time is over
            # if there is nothing in the current event or 
            # (there is a rectacle and the time has passed beyond time of the rectancle) or 
            # (if there was no rectacle and the time has passed beyond the time of the pause)
            time_ref, cur_event, is_rect_now, rect_h0, time_pause_s, already_on_target, cur_rect, was_on_target, time_on_target, time_on_target_ref, exit_time_ref, rects_pauses_list = IsItTheEndOfStimuli(time_ref, cur_event, is_rect_now, rect_h0, time_pause_s, already_on_target, cur_rect, was_on_target, time_on_target, time_on_target_ref, exit_time_ref, rects_pauses_list, exit_times,times_on_target)
            # anyways draw what should be drawn
            DrawContentOnScreen()

            center_pos = UseDAQToUpdateCursor(moving_avg_samples, center_pos)
            # first check if left the previous rectangle zone; if so, then update the exit time
            exit_times = HasUserLeftPreviousRect(rect_h, rect_h0s, exit_time_ref, is_rect_now, cur_rect, exit_times, center_pos)

            time_on_target, already_on_target, entry_times, was_on_target, exit_time_ref, time_on_target_ref, samples_px = IsUserOnTarget(rect_h, rect_h0, time_ref, time_on_target, trace_size, screen, already_on_target, is_rect_now, cur_rect, b, r, entry_times, samples_px, center_pos, was_on_target, exit_time_ref, time_on_target_ref)
            
        else:
            show_fb_time_ref = FeedbackAndResults( rect_h, time_rect_s, show_fb_time, rect_h0s, total_num_rects, show_fb_time_ref, font, screen, b, entry_times, times_on_target, samples_px, stddevs, inaccuracies, exit_times)
            
            should_quit = (float(time.time() - show_fb_time_ref) > show_fb_time)            
        pygame.display.update()
pygame.quit()
