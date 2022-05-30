from __future__ import division
import random
from PIL import Image, ImageDraw
import math
import numpy as np
import datetime
import os
import json
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage

# import daqmxlib
#import PyDAQmx
#from PyDAQmx import Task

# def send_trigger(trigger_mode):
    #Actuate a single digital pulse (period between 1 and 2 ms) on a desired port, depending on trigger mode value.
    #trigger_mode: either "random" or "series"
    # print "Sending TMS trigger signal... mode = %s" % trigger_mode
    # dev_port_line = ""
    # if trigger_mode == "random":
        # dev_port_line = "/Dev1/port1/line3"
    # elif trigger_mode == "series":
        # dev_port_line = "/Dev1/port1/line2"
    # print dev_port_line
    # task = Task()
    # task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    # task.StartTask()
    # task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([1], dtype=np.uint8), None, None)
    # task.StopTask()
    # task = Task()
    # task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    # task.StartTask()
    # task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([0], dtype=np.uint8), None, None)
    # task.StopTask()

def get_px_from_voltage(voltage, max_voltage):
    if voltage >= 0:
        result = 1000
    elif voltage <= max_voltage:
        result = 0
    else:
        result = 1000 - int(voltage / (max_voltage * 0.001))
    # print max_voltage * 0.001, voltage, result
    return result

#LEGACY FUNCTIONS
	
	
# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def prepare_background(screen_w, screen_h, num_rectangles, height, series=None):
    im = Image.new('RGB', (screen_w, screen_h), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    num_rects = num_rectangles if series is None else len(series.split())
    rect_w = math.floor(screen_w / num_rects)  # just in case
    rect_info = {}

    for i in range(num_rects):
        x0 = i * rect_w
        x = x0 + rect_w
        y0 = random.randint(0, screen_h - height - 1) if series is None else int(series.split()[i])
        y = y0 + height
        # draw 4 lines, because draw.rect does not have adjustable width parameter
        red = (255, 0, 0)
        draw.line(xy=[x0, y0, x0, y], fill=red, width=4)
        draw.line(xy=[x0, y0, x, y0], fill=red, width=4)
        draw.line(xy=[x, y0, x, y], fill=red, width=4)
        draw.line(xy=[x0, y, x, y], fill=red, width=4)
        # draw.rectangle(xy=[x0, y0, x, y], outline=(255, 0, 0))
        rect_info[i] = (x0, y0, x, y)
    del draw
    im.save('exercise.png', 'PNG')
    return rect_info, rect_w


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.
    :param values: numpy ndarray
    :param weights: numpy ndarray (the same shape as values)
    """
    average = np.average(values, weights=weights)
    variance = np.average((values - average) ** 2, weights=weights)  # Fast and numerically precise
    return math.sqrt(variance)


def store_raw(samples):
    with open('raw_samples\\samples_{}.txt'.format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")), 'w+') as rw:
        for i in range(len(samples)):
            rw.write("{}\n".format(samples[i]))


def save_quest_data(raw_data, score, inaccuracy, stddev):
    store_raw(raw_data)
    with open('config2.cfg') as cfg:
        param_dict = json.loads(cfg.read())
    if not os.path.isfile('results_quest_excel.txt') or os.stat('results_quest_excel.txt').st_size == 0:
        header = "Date\tRandom rectangles\tNumber of series\tSeries\tOrder\tScore\tStddev\tInaccuracy"
        with open('results_quest_excel.txt', 'w+') as excel_f:
            excel_f.write(header)
    date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    order = "ran/ser" if param_dict["series_first"] == 0 else "ser/ran"
    with open('results_quest_excel.txt', 'a') as excel_f:
        excel_f.write("\n{date}\t{num_ran}\t{num_ser}\t{ser}\t{ord}\t{sc}\t{stddev}\t{inac}"
                            .format(date=date, num_ran=param_dict["num_rectangles"], num_ser=param_dict["num_series"],
                                    ser=param_dict["series"], ord=order, sc=score, stddev=stddev, inac=inaccuracy))


def save_quest_settings(to_save_series):
    # with open("config2.cfg", "r") as used_conf, open("saved_quest.cfg", "w") as to:
    #     to.write(json.dumps(json.loads(used_conf.read()), indent=4))
    to_save = ""
    for num in to_save_series:
        to_save += "{} ".format(num)
    with open('saved_quest.txt', 'w') as save:
        print to_save
        save.write(to_save)


class ResultAnalyser:
    """
    A class for analysing the object's performance.
    Planned functions: calculate score, stddev, inaccuracy, slew rates
    """
    points = None
    rectangles_dict = None
    num_rects = None
    rect_w = None
    rect_h = None
    screen_w = None
    num_samples = None
    score = None
    deviations = None
    inaccuracy = None
    slew_rates = None

    def __init__(self, points, rects, screen_w):
        self.points = points
        self.rectangles_dict = rects
        self.num_rects = len(self.rectangles_dict)
        self.rect_w = math.floor(screen_w / self.num_rects)
        self.rect_h = self.rectangles_dict[0][3] - self.rectangles_dict[0][1]
        self.screen_w = screen_w
        self.num_samples = len(self.points)

    def __evaluate_point(self, point):
        rect = int(point[0] / self.rect_w)
        return 1 if self.rectangles_dict[rect][1] <= point[1] <= self.rectangles_dict[rect][3] else 0

    def __px_to_sample(self, px_num):
        resolution = self.screen_w / self.num_samples
        value = int(math.ceil(px_num / resolution))
        return self.num_samples - 1 if value > self.num_samples - 1 else value

    def get_score(self):
        score = 0
        for point in self.points:
            score += self.__evaluate_point(point)
        self.score = float(score / len(self.points))
        return float(score / len(self.points))

    def compute_stddev_accuracy(self):
        """
        Provides the user with standard deviations calculated in rectangle-wise manner.
        :return: stddevs per rectangle in a form of list
        """
        deviations = {}
        inaccuracy = {}
        for rect in range(self.num_rects):
            target = int((self.rectangles_dict[rect][1] + self.rectangles_dict[rect][3]) / 2)  # the middle of the rect
            start = self.__px_to_sample(rect * self.rect_w)
            stop = self.__px_to_sample((rect + 1) * self.rect_w)
            vals_px = [self.points[i][1] for i in range(start, stop)]
            deviations[rect + 1] = "{0:.2f}%".format(
                100 * np.mean(weighted_avg_and_std(values=vals_px, weights=None)) / self.rect_h)
            diffs_px = [math.fabs(vals_px[j] - target) for j in range(len(vals_px))]
            inaccuracy[rect + 1] = "{0:.2f}%".format(100 * np.average(diffs_px) / self.rect_h)
        self.deviations = deviations
        self.inaccuracy = inaccuracy
        return deviations, inaccuracy

    def compute_slew_rates(self):
        """
        Calculates how quick did the object manage to reach the next rectangle from the previous one.
        :return:
        """
        slew_rates = {}
        cur_rect = 1
        slew_cnt = 0
        cur_px = self.rectangles_dict[1][0]  # beginning of the second rect
        while cur_rect < self.num_rects:
            if self.rectangles_dict[cur_rect][1] <= self.points[self.__px_to_sample(cur_px)][1] <= \
                    self.rectangles_dict[cur_rect][3]:
                slew_rates['{}-{}'.format(cur_rect, cur_rect + 1)] = '{0:.2f}%'.format(
                    slew_cnt / self.rect_w * 100)  # %
                slew_cnt = 0
                cur_px = cur_rect * self.rect_w
                cur_rect += 1
                continue
            else:
                if slew_cnt == self.rect_w - 1:  # slew rate reaches rectangle width!
                    slew_rates['{}-{}'.format(cur_rect, cur_rect + 1)] = '{0:.2f}%'.format(
                        slew_cnt / self.rect_w * 100)  # %
                    slew_cnt = 0
                    cur_px += 1
                    cur_rect += 1
                    continue
                slew_cnt += 1  # SCREEN_WIDTH_PX / num_samples  # slew_cnt in px
                cur_px += 1
        self.slew_rates = slew_rates
        return slew_rates

    def store_results(self, duration, raw_samples, stop_date):
        """
        Saves all the analytic data, as well as raw samples and screenshots.
        :param duration: experiment duration in seconds
        :param raw_samples: a list of voltage measurements taken
        :param stop_date: time of finishing the exercise
        :return:
        """
        # First store raw samples
        store_raw(raw_samples)
        # Then prepare a JSON with the data
        data = {
            "DATE": stop_date,
            "NUM_RECTS": self.num_rects,
            "DURATION": "{0:.2f}s".format(duration),
            "CORRECT": self.score,  # "{0:.2f}".format(100 * (points / number_samples)),
            "STDDEV_BY_RECT": self.deviations,
            "SLEW_RATE_BY_RECT": self.slew_rates,
            "INACCURACY_BY_RECT": self.inaccuracy
        }
        # save in excel-ready format - LOT OF MAGIC NUMBERS HERE, BEWARE!
        if not os.path.isfile('results_excel.txt') or os.stat('results_excel.txt').st_size == 0:
            header = "Date\tNumber of rectangles\tDuration\tCorrect\t"
            header += "Stddev by rect:\t"
            for r in range(self.num_rects):
                header += "{}\t".format(r + 1)
            header += "Inaccuracy by rect:\t"
            for r in range(self.num_rects):
                header += "{}\t".format(r + 1)
            header += "Slew rate by rect:\t"
            for r in range(1, self.num_rects):
                header += " {}-{}\t".format(r, r + 1)
            with open('results_excel.txt', 'w+') as excel_f:
                excel_f.write(header)

        with open('results_excel.txt', 'a') as excel_f:
            excel_f.write("\n{}\t{}\t{}\t{}\t".format(data["DATE"], data["NUM_RECTS"], data["DURATION"],
                                                      data["CORRECT"]))
            for r in range(self.num_rects):
                excel_f.write("\t{}".format(data["STDDEV_BY_RECT"][r + 1]))
            excel_f.write("\t")
            for r in range(self.num_rects):
                excel_f.write("\t{}".format(data["INACCURACY_BY_RECT"][r + 1]))
            excel_f.write("\t")
            for r in range(1, self.num_rects):
                excel_f.write("\t{}".format(data["SLEW_RATE_BY_RECT"]["{}-{}".format(r, r + 1)]))

        if os.stat('track_results.json').st_size == 0:
            with open('track_results.json', 'w') as tr:
                tr.write(json.dumps([data], indent=4))
        elif os.stat('track_results.json').st_size > 0:
            with open('track_results.json', 'r') as tr:
                file_content = json.loads(tr.read())
            file_content.append(data)
            with open('track_results.json', 'w') as tr:
                tr.write(json.dumps(file_content, indent=4))

        for displayNumber, rect in enumerate(getDisplayRects(), 1): # dump the secondary monitors
            im_display = getRectAsImage(rect)
            im_display.save('plots\exercise{0:.2f}sec_{rects}_{date}.png'
                            .format(duration, rects=self.num_rects,
                                    date=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")), format='png')
            break

    def save_series(self):
        to_save = ""
        for i in range(len(self.rectangles_dict)):
            to_save += "{} ".format(self.rectangles_dict[i][1])
        with open('saved_series.txt', 'w') as s:
            # print to_save
            s.write(to_save)
