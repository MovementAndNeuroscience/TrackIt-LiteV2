from __future__ import division
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
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


# from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage


class Tracking:
    """
    This class provides functions realising tracking exercises.
    """
    number_samples = None
    number_rectangles = None
    # height of the rectangle
    height = None
    # voltage bounds (defines screen scale). Voltage bounds estimated basing on fixed full-screen Y resolution: 927px
    min_voltage = None
    max_voltage = None
    repetitions = None
    post_fb = None
    pre_fb = None
    fb_time = None
    # strongman mode
    strongman = None
    # should one see the feedback
    feedback = None
    # Those above are set at initialisation from GUI!
    # This variable stores rectangle info
    rectangles = None
    # This array stores timestamps for raw samples
    # samples_timestamps = [datetime.datetime.now()]
    # empirically estimated data acquisition rate: 45 (90 now!!! for some reason) samples/s
    # current monitor's resolution dpi = 96
    # the length of one animation iteration, used for determining the pause between consecutive runs (in seconds)
    iter_duration = 0.055
    # global variable counting how many samples was in "good" range. It has to be set to 0 after each result dump!
    points = 0
    # artificial timer, expressed in number of refresh_figure() iterations,
    # referring to the time interval from feedback drawal to next tracking initiation. Used also for initial delay.
    iters_post_fb = 0
    # as above, but referring to the time inteval between the last sample capture and feedback drawing.
    iters_pre_fb = 0
    # as above, determining how long the feedback should be presented.
    iters_fb = 0
    # a flag triggering the function which makes a screenshot of the plot.
    run_print_save_figure = True
    # the lists carrying X and Y axes of the plot.
    xs = [1]
    samples = [0]
    # offset needed for strongman
    offset = 0
    # background image with rectangles drawn
    img = None

    def __init__(self, **kwargs):

        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        # set repetitions to one, if no number specified so far
        if self.repetitions is None:
            self.repetitions = 1

        self.rectangles = tools.generate_rectangle_info(self.number_rectangles, self.height)
        self.samples = [0]
        self.xs = [1]
        self.reader = daqmxlib.Reader()
        self.tmp = 0
        self.run_start = False

    def evaluate_sample(self, num, val):
        """
        A simple mechanism, which checks if the sample fits the appropriate rectangle. If yes then it counts a point.
        :param num: number of sample
        :param val: value of a sample described by num
        :return: 1 when point is granted, 0 otherwise
        """
        cur_pixel = tools.sample_to_px(num, self.number_samples)
        rect_width = self.rectangles[1][2] - self.rectangles[1][0]
        cur_rectangle = min(tools.find_rect(cur_pixel, rect_width), self.number_rectangles)
        result = tools.voltage_to_px(voltage=val, max_value=self.max_voltage, min_value=self.min_voltage)
        if self.rectangles[cur_rectangle][1] <= result <= self.rectangles[cur_rectangle][3]:
            return 1
        else:
            return 0

    def capture_from_daq(self, real=True):
        """
        This function, run in parallel thread, captures the voltage samples from DAQ. After collecting the agreed number
        of samples it terminates automatically. If mocking mode (real = False) set, it generates random numbers within
        the Y range.
        :param real: True - capture from real device, False - generate mock data
        :return:
        """
        game_over = False
        sample_num = 2
        millis = int(round(time.time() * 1000))
        if real:
            my_reader = daqmxlib.Reader()  # ({"ai0": 1})
        while sample_num <= self.number_samples:
            if real:
                if self.strongman:
                    sample_val = my_reader.read()[0] + self.offset
                    if sample_val > self.max_voltage:
                        sample_val = self.max_voltage
                    self.offset += 0.005
                else:
                    sample_val = my_reader.read()[0]
            else:
                sample_val = random.uniform(self.min_voltage, self.max_voltage)
                time.sleep(0.01)
            self.xs.append(sample_num)
            self.samples.append(sample_val)
            # self.samples_timestamps.append(datetime.datetime.now())
            if self.strongman:
                if not self.evaluate_sample(sample_num, sample_val):
                    game_over = True
                if not game_over:
                    self.points += self.evaluate_sample(sample_num, sample_val)
            else:
                self.points += self.evaluate_sample(sample_num, sample_val)
            sample_num += 1
        print 'Data acquisition of {} samples took {} milis.'.format(self.number_samples,
                                                                     int(round(time.time() * 1000)) - millis)
        with open('raw_samples\samples_{}.txt'.format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")),
                  'w+') as raw:
            for i in range(len(self.samples)):
                raw.write("{}\n".format(self.samples[i]))
                # raw.write("{} {}\n".format(samples[i], samples_timestamps[i]))
        print 'Capturing thread is now terminating...'

    def capture2(self, smpls=1000):
        while smpls > 0:
            smpls -= 1
            yield self.reader.read()[0]

    def draw_last_and_feedback(self, run, axis, fb=False):
        if run:
            axis.plot(np.array((self.xs + [self.xs[-1] + 1])), np.array((self.samples + [self.samples[-1]])))
            plt.draw()
        score = 100 * (self.points / self.number_samples)
        if fb and self.feedback == 1:
            plt.text(0.5, 0.5, s='Your score is: {}'.format(score),
                     fontdict=dict(size=45, weight='bold'), bbox=dict(facecolor='green'))
            plt.draw()

    def print_save_results(self, run):
        """
        From here all the results analyses are invoked. Also plots are dumped.
        :param run: The flag saying whether the function has been already called for the particular exercise (True) or
        not (False). Thanks to that one avoids saving the same data more than once.
        :return:
        """
        if run:
            # stuff connected directly to the animation
            score = 100 * (self.points / self.number_samples)
            self.repetitions -= 1
            # analytical stuff and saving image
            if not self.strongman:
                deviations, inaccuracy = tools.compute_stddev_accuracy(self.number_rectangles, self.samples,
                                                                       self.max_voltage,
                                                                       self.min_voltage,
                                                                       self.height)
                duration = self.number_samples / 90
                data = {
                    "DATE": datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
                    "NUM_RECTS": self.number_rectangles,
                    "DURATION": "{0:.2f}s".format(duration),
                    "CORRECT": score,  # "{0:.2f}".format(100 * (points / number_samples)),
                    "STDDEV_BY_RECT": deviations,
                    "SLEW_RATE_BY_RECT": tools.compute_slew_rates(self.number_rectangles, self.samples,
                                                                  self.max_voltage, self.min_voltage,
                                                                  self.height),
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
                if self.samples == 1280:
                    length = 'long'
                elif self.samples == 640:
                    length = 'medium'
                elif self.samples == 512:
                    length = 'short'
                elif self.samples == 320:
                    length = 'veryshort'

                    # for displayNumber, rect in enumerate(getDisplayRects(), 1):
                    #     im_display = getRectAsImage(rect)
                    #     im_display.save('plots\exercise{}_{}_{}.png'.format(length, self.number_rectangles,
                    #                                                         datetime.datetime.now().strftime(
                    #                                                             "%Y_%m_%d_%H_%M_%S"), ), format='png')
                    #     break

    def refresh_figure(self, ax1, timer):
        """
        This function is responsible for graphical representation of tracking line. Depending on the state it sets the
        figure and starts capturing or (when invoked later) it prints a new sample on the plot. When the exercise is
        done it calls data saving and analysis and then it becomes idle.
        :param ax1: matplotlib axis
        :param timer: timer instance (used to stop it, when necessary)
        :return:
        """
        if not self.run_start:
            pre_fb_tmp = datetime.datetime.now()
            pre_delta = pre_fb_tmp - self.tmp
            if pre_delta.total_seconds() < self.post_fb:
                pass
            else:
                self.run_start = True
                plt.cla()
                ax1.set_xlim(left=0, right=self.number_samples)
                ax1.set_ylim(bottom=self.min_voltage, top=self.max_voltage)
                ax1.set_position([0, 0, 1, 1])  # the values are (0,1) !
                ax1.patch.set_alpha(0)  # total transparency, otherwise background rectangles are shadowed
                winsound.Beep(442, 500)
                plt.draw()
                t = TrackThread(self)
                t.run()
        else:
            if len(self.xs) == self.number_samples:
                if self.run_print_save_figure:  # save results, set fb timers
                    self.print_save_results(self.run_print_save_figure)
                    self.draw_last_and_feedback(self.run_print_save_figure, ax1, fb=False)
                    self.run_print_save_figure = False
                    self.tmp = datetime.datetime.now()
                else:
                    fb_tmp = datetime.datetime.now()
                    delta = fb_tmp - self.tmp
                    if delta.total_seconds() < self.pre_fb:  # waiting for fb
                        pass
                    else:
                        if delta.total_seconds() < self.pre_fb + self.fb_time:  # fb option
                            print "Pre_fb trwalo {}".format(fb_tmp - self.tmp)
                            self.draw_last_and_feedback(False, ax1, fb=True)
                        else:  # tear down and prepare the next run/exit exercise
                            if self.repetitions > 0:  # This should happen after fb
                                print "Koniec fb! W czasie {}".format(fb_tmp - self.tmp)
                                plt.cla()
                                self.points = 0
                                self.tmp = datetime.datetime.now()
                                self.samples = [0]
                                self.xs = [1]
                                self.run_print_save_figure = True
                                self.run_start = False
                                plt.draw()
                            else:  # end of the exercise
                                # plt.annotate(xy=(200, 200), xytext=(200, 200), s='Finished! Close the figure!')
                                timer.remove_callback(self.refresh_figure)
                                self.samples = [0]
                                self.xs = [1]
                                plt.cla()
                                plt.draw()
            else:
                ax1.plot(np.array(self.xs), np.array(self.samples))
                plt.draw()

    # def draw_init(self):
    #     img = mpimg.imread('exercise.png')  # this png contains the generated rectangles
    #     self.ax.set_xlim(left=0, right=self.number_samples)
    #     self.ax.set_ylim(bottom=self.min_voltage, top=self.max_voltage)
    #     self.ax.set_position([0, 0, 1, 1])  # the values are (0,1) !
    #     plt.figimage(img)
    #     self.ax.patch.set_alpha(0.1)  # total transparency, otherwise background rectangles are shadowed
    #     mng = plt.get_current_fig_manager()
    #     mng.resize(*mng.window.maxsize())
    #     self.line.set_data(self.xs, self.samples)
    #     return self.line,
    #
    # def draw_new(self, data):
    #     new_val = data
    #     self.samples.append(new_val)
    #     self.xs.append(self.xs[-1] + 1)
    #     self.line.set_data(self.xs, self.samples)
    #     return self.line,
    #     # print new_val
    #
    # def init_tracking(self):
    #     ani = animation.FuncAnimation(fig=self.fig, func=self.draw_new, frames=self.capture2, blit=False, interval=15,
    #                                   repeat=False, init_func=self.draw_init)
    #     plt.show()

    def run_tracking(self):
        """
        This function initialises the plot and controls the tracking exercise.
        :return:
        """
        fig, ax1 = plt.subplots()
        cycler = mpl.cycler(color=['r'])
        mpl.rcParams['lines.linewidth'] = 2.0
        mpl.rcParams['axes.prop_cycle'] = cycler  # this gives an uniform colour of the line
        img = mpimg.imread('exercise.png')  # this png contains the generated rectangles
        print self.number_samples
        ax1.set_xlim(left=0, right=self.number_samples)
        ax1.set_ylim(bottom=self.min_voltage, top=self.max_voltage)
        ax1.set_position([0, 0, 0.1, 0.1])  # the values are (0,1) !
        plt.figimage(img)
        ax1.patch.set_alpha(0.1)  # total transparency, otherwise background rectangles are shadowed
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())  # kinda maximising the window, not totally though...
        self.tmp = datetime.datetime.now()
        timer = fig.canvas.new_timer(interval=10)
        timer.add_callback(self.refresh_figure, ax1=ax1, timer=timer)
        plt.draw()
        timer.start()
        plt.show()


class TrackThread(object):
    """
    An auxiliary class of daemon threads for data acquisition. Needed for repetitive runs of exercises.
    """

    def __init__(self, tracking_object):
        self.thread = threading.Thread(target=tracking_object.capture_from_daq, kwargs={'real': True})
        self.thread.daemon = True

    def run(self):
        self.thread.start()
