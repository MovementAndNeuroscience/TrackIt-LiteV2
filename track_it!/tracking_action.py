# coding: utf-8
from __future__ import division
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.image as mpimg
import numpy as np
import threading
import time
import json
import daqmxlib
import datetime
import tools
import winsound
import os
import random
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage

# empirically estimated data acquisition rate: 45 (90 now!!! for some reason) samples/s
# current monitor's resolution
DPI = 96
# voltage bounds have been estimated basing on fixed full-screen Y resolution: 927px
# lower voltage bound in volts (determines Y axis in the plot)
MIN_VOLTAGE = -2.5
# upper voltage bound in volts
MAX_VOLTAGE = 0.281
# the length of one animation iteration, used for determining the pause between consecutive runs (in seconds)
ITER_DURATION = 0.055
# global variable counting how many samples was in "good" range. It has to be set to 0 after each result dump!
points = 0
# artificial timer, postponing the start of capturing. One unit is about 60 ms.
iters_to_remove_or_close = 0
# a flag triggering the function which makes a screenshot of the plot.
run_print_save_figure = True
# the lists carrying X and Y axes of the plot.
xs = [1]
samples = [0]
# how many reps
repetitions = 0
# strongman option
strong_man = False
offset = 0
feedback = 1
img = None


def track_it(number_samples, number_rectangles, height, min_v, max_v, reps=1, pause_len=5, strongman=False, fb=1):
    """
    Performs a tracking exercise customised by the following parameters:
    :param number_samples: how many voltage samples will be captured (length of the exercise)
    :param number_rectangles:
    :param height: height of a single rectangle
    :param min_v: lower voltage bound (Y axis)
    :param max_v: upper voltage bound (Y axis)
    :param reps: number of repetitions (multiple exercise if more than 1)
    :param pause_len: length (in seconds) of pause separating consecutive runs of the exercise
    :param strongman: if selected, an insane mode of strongman will be run!
    :return:
    """
    global points, iters_to_remove_or_close, run_print_save_figure, repetitions, MIN_VOLTAGE, MAX_VOLTAGE, strong_man, \
        offset, feedback, img  # this have to be done in order to handle those quantities in nested functions
    print reps
    MIN_VOLTAGE = min_v
    MAX_VOLTAGE = max_v
    repetitions = int(reps)
    iters_to_remove_or_close = int(int(pause_len) / ITER_DURATION)  # animation iterations, determining pauses' lengths
    points = 0
    offset = 0  # used only for strongman case!
    strong_man = strongman
    feedback = fb
    run_print_save_figure = True  # this flag makes the saving process be executed only once after exercise is finished
    # initialise the figure
    matplotlib.use('TkAgg')
    fig, ax1 = plt.subplots()
    img = mpimg.imread('exercise.png')  # this png contains the generated rectangles
    ax1.set_xlim(left=0, right=number_samples)
    ax1.set_ylim(bottom=MIN_VOLTAGE, top=MAX_VOLTAGE)
    ax1.set_position([0, 0, 1, 1])  # the values are (0,1) !
    plt.figimage(img)
    ax1.patch.set_alpha(0)  # total transparency, otherwise background rectangles are shadowed
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())  # kinda maximising the window, not totally though...
    rectangles = tools.generate_rectangle_info(number_rectangles, height)  # used for results evaluation
    samples_timestamps = [datetime.datetime.now()]

    def evaluate_sample(num, val):
        """
        A simple mechanism, which checks if the sample fits the appropriate rectangle. If yes then it counts a point.
        :param num: number of sample
        :param val: value of a sample described by num
        :return: 1 when point is granted, 0 otherwise
        """
        cur_pixel = tools.sample_to_px(num, number_samples)
        rect_width = rectangles[1][2] - rectangles[1][0]
        cur_rectangle = tools.find_rect(cur_pixel, rect_width)
        result = tools.voltage_to_px(voltage=val, max_value=MAX_VOLTAGE, min_value=MIN_VOLTAGE)
        if rectangles[cur_rectangle][1] <= result <= rectangles[cur_rectangle][3]:
            return 1
        else:
            return 0

    def capture_from_daq(real=True):
        """
        This function, run in parallel thread, captures the voltage samples from DAQ. After collecting the agreed number
        of samples it terminates automatically. If mocking mode (real = False) set, it generates random numbers within
        the Y range.
        :param real: True - capture from real device, False - generate mock data
        :return:
        """
        global points, offset, strong_man
        sample_num = 2
        millis = int(round(time.time() * 1000))
        if real:
            my_reader = daqmxlib.Reader({"ai0": 1})
        while sample_num <= number_samples:
            if real:
                if strong_man:
                    sample_val = my_reader.read()[0] + offset
                    if sample_val > max_v:
                        sample_val = max_v
                    offset += 0.005
                else:
                    sample_val = my_reader.read()[0]
            else:
                sample_val = random.uniform(MIN_VOLTAGE, MAX_VOLTAGE)
                time.sleep(0.01)
            xs.append(sample_num)
            samples.append(sample_val)
            samples_timestamps.append(datetime.datetime.now())
            if strong_man:
                game_over = True if not evaluate_sample(sample_num, sample_val) else False
                if not game_over:
                    points += evaluate_sample(sample_num, sample_val)
            else:
                points += evaluate_sample(sample_num, sample_val)
            sample_num += 1
        print 'Data acquisition took {} milis.'.format(int(round(time.time() * 1000)) - millis)
        with open('raw_samples\samples_{}.txt'.format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")),
                  'w+') as raw:
            for i in range(len(samples)):
                raw.write("{}\n".format(samples[i]))
                # raw.write("{} {}\n".format(samples[i], samples_timestamps[i]))
        print 'Capturing thread is now terminating...'

    class TrackThread(object):
        """
        An auxiliary class of daemon threads for data acquisition. Needed for repetitive runs of exercises.
        """

        def __init__(self):
            self.thread = threading.Thread(target=capture_from_daq, kwargs={'real': False})
            self.thread.daemon = True

        def run(self):
            self.thread.start()

    def draw_last_and_feedback(run):
        global points, feedback
        if run:
            ax1.plot(np.array((xs + [xs[-1] + 1])), np.array((samples + [samples[-1]])))
            score = 100 * (points / number_samples)
            if feedback == 1:
                plt.text(0, 0, s='Your score is: {}'.format(score),
                         fontdict=dict(name='Courier', weight='bold'), bbox=dict(facecolor='green'))
            plt.draw()

    def print_save_results(run):
        """
        From here all the results analyses are invoked. Also plots are dumped.
        :param run: The flag saying whether the function has been already called for the particular exercise (True) or
        not (False). Thanks to that one avoids saving the same data more than once.
        :return:
        """
        if run:
            global points, repetitions, strong_man
            # stuff connected directly to the animation
            score = 100 * (points / number_samples)
            repetitions -= 1
            # analytical stuff and saving image
            if not strong_man:
                deviations, inaccuracy = tools.compute_stddev_accuracy(number_rectangles, samples, MAX_VOLTAGE,
                                                                       MIN_VOLTAGE,
                                                                       height)
                duration = number_samples / 90
                data = {
                    "DATE": datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
                    "NUM_RECTS": number_rectangles,
                    "DURATION": "{0:.2f}s".format(duration),
                    "CORRECT": score,  # "{0:.2f}".format(100 * (points / number_samples)),
                    "STDDEV_BY_RECT": deviations,
                    "SLEW_RATE_BY_RECT": tools.compute_slew_rates(number_rectangles, samples, MAX_VOLTAGE, MIN_VOLTAGE,
                                                                  height),
                    "INACCURACY_BY_RECT": inaccuracy
                }
                # save in excel-ready format - LOT OF MAGIC NUMBERS HERE, BEWARE!
                if not os.path.isfile('results_excel.txt') or os.stat('results_excel.txt').st_size == 0:
                    with open('results_excel.txt', 'w+') as excel_f:
                        excel_f.write("Date\tNumber of rectangles\tDuration\tCorrect\t"
                                      "Stddev by rect:\t1\t2\t3\t4\t5\t6\t7\t8\t"
                                      "Inaccuracy by rect:\t1\t2\t3\t4\t5\t6\t7\t8\t"
                                      "Slew rate by rect:\t 1-2\t 2-3\t 3-4\t 4-5\t 5-6\t 6-7\t 7-8\t")
                        # the apostrophes above prevent Excel from converting the entries to dates!
                        # excel_f.close()

                def wr(x, category):
                    return " " if x not in data[category] else data[category][x]

                with open('results_excel.txt', 'a') as excel_f:
                    excel_f.write("\n{}\t{}\t{}\t{}\t".format(data["DATE"], data["NUM_RECTS"], data["DURATION"],
                                                              data["CORRECT"]))
                    for i in range(1, 9):
                        excel_f.write("\t{}".format(wr(i, "STDDEV_BY_RECT")))
                    excel_f.write("\t")
                    for i in range(1, 9):
                        excel_f.write("\t{}".format(wr(i, "INACCURACY_BY_RECT")))
                    excel_f.write("\t")
                    levels = ['1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8']
                    for i in levels:
                        excel_f.write("\t{}".format(wr(i, "SLEW_RATE_BY_RECT")))

                if os.stat('track_results.json').st_size == 0:
                    with open('track_results.json', 'w') as tr:
                        tr.write(json.dumps([data], indent=4))
                elif os.stat('track_results.json').st_size > 0:
                    with open('track_results.json', 'r') as tr:
                        file_content = json.loads(tr.read())
                    file_content.append(data)
                    with open('track_results.json', 'w') as tr:
                        tr.write(json.dumps(file_content, indent=4))
                length = ''
                if samples == 1280:
                    length = 'long'
                elif samples == 640:
                    length = 'medium'
                elif samples == 512:
                    length = 'short'
                elif samples == 320:
                    length = 'veryshort'

                for displayNumber, rect in enumerate(getDisplayRects(), 1):
                    im_display = getRectAsImage(rect)
                    im_display.save('plots\exercise{}_{}_{}.png'.format(length, number_rectangles,
                                                                        datetime.datetime.now().strftime(
                                                                            "%Y_%m_%d_%H_%M_%S"), ), format='png')
                    break  # since we want to dump only display 1 (in lab 3)

                    # img_grab.grab_to_file('plots\exercise{}_{}_{}.png'.format(length, number_rectangles,
                    #                                                           datetime.datetime.now().strftime(
                    #                                                               "%Y_%m_%d_%H_%M_%S")))

    def refresh_figure():
        """
        This function is responsible for graphical representation of tracking line. Depending on the state it sets the
        figure and starts capturing or (when invoked later) it prints a new sample on the plot. When the exercise is
        done it calls data saving and analysis and then it becomes idle.
        :return:
        """
        global iters_to_remove_or_close, img
        if iters_to_remove_or_close > 0:
            iters_to_remove_or_close -= 1
            if iters_to_remove_or_close == 0:
                plt.cla()
                # plt.grid(True)
                # image = mpimg.imread('exercise.png')
                #  plt.figimage(img)  # possibly resize=True
                ax1.set_xlim(left=0, right=number_samples)
                ax1.set_ylim(bottom=MIN_VOLTAGE, top=MAX_VOLTAGE)
                ax1.set_position([0, 0, 1, 1])  # the values are (0,1) !

                ax1.patch.set_alpha(0)  # total transparency, otherwise background rectangles are shadowed
                print datetime.datetime.now()
                winsound.Beep(442, 500)
                plt.draw()
                t = TrackThread()
                t.run()

        else:
            global points, xs, samples, run_print_save_figure, repetitions
            if len(xs) == number_samples:
                draw_last_and_feedback(run_print_save_figure)
                print_save_results(run_print_save_figure)
                points = 0
                run_print_save_figure = False
                if repetitions > 0:
                    iters_to_remove_or_close = int(int(pause_len) / ITER_DURATION)
                    samples = [0]
                    xs = [1]
                    run_print_save_figure = True
                else:
                    plt.annotate(xy=(200, 200), xytext=(200, 200), s='Finished! Close the figure!')
                    timer.remove_callback(refresh_figure)
                    samples = [0]
                    xs = [1]
                    plt.draw()
            else:
                ax1.plot(np.array(xs), np.array(samples))
                plt.draw()

    plt.text(x=0, y=0,
             s='Maximise the window! The exercise starts in {} seconds! Wait for the beep!'.format(int(pause_len)))
    print datetime.datetime.now()
    timer = fig.canvas.new_timer(interval=25)
    timer.add_callback(refresh_figure)
    plt.draw()
    timer.start()
    plt.show()
