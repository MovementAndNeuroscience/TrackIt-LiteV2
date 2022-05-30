from __future__ import division
from PIL import Image, ImageDraw
import math
import numpy as np
import os

SCREEN_WIDTH_PX = 1280
MPL_GENERATED_SCREEN_HEIGHT_PX = 927
PROGRAM_MAIN_DIR = os.path.dirname(os.path.realpath(__file__))


def safe_boundaries(h):
        return h if h < MPL_GENERATED_SCREEN_HEIGHT_PX else MPL_GENERATED_SCREEN_HEIGHT_PX


# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def prepare_background(num_rectangles, height):
    im = Image.new('RGB', (1280, 927), (255, 255, 255))

    draw = ImageDraw.Draw(im)

    if num_rectangles == 4:
        draw.rectangle(xy=[0, 150, 320, safe_boundaries(150 + height)], outline=(255, 0, 0))  # fill=(255, 0, 0)
        draw.rectangle(xy=[320, 300, 640, safe_boundaries(300 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[640, 450, 960, safe_boundaries(450 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[960, 100, 1279, safe_boundaries(100 + height)], outline=(255, 0, 0))
    elif num_rectangles == 6:
        draw.rectangle(xy=[0, 150, 213, safe_boundaries(150 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[213, 300, 426, safe_boundaries(300 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[426, 450, 639, safe_boundaries(450 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[639, 100, 852, safe_boundaries(100 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[852, 350, 1065, safe_boundaries(350 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[1065, 200, 1279, safe_boundaries(200 + height)], outline=(255, 0, 0))
    elif num_rectangles == 8:
        draw.rectangle(xy=[0, 150, 160, safe_boundaries(150 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[160, 300, 320, safe_boundaries(300 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[320, 450, 480, safe_boundaries(450 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[480, 100, 640, safe_boundaries(100 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[640, 350, 800, safe_boundaries(350 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[800, 200, 960, safe_boundaries(200 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[960, 600, 1120, safe_boundaries(600 + height)], outline=(255, 0, 0))
        draw.rectangle(xy=[1120, 150, 1279, safe_boundaries(150 + height)], outline=(255, 0, 0))
    elif num_rectangles == 1:
        draw.rectangle(xy=[0, 50, 1279,  safe_boundaries(50 + height)], outline=(255, 0, 0), fill=(255, 0, 0))
    else:
        raise NotImplementedError('Only 4, 6, 8 squares are possible!')
    del draw
    im.save('exercise.png', 'PNG')


# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def generate_rectangle_info(num_rectangles, height):
    if num_rectangles == 4:
        return {
            1: (0, 150, 320, safe_boundaries(150 + height)),
            2: (320, 300, 640, safe_boundaries(300 + height)),
            3: (640, 450, 960, safe_boundaries(450 + height)),
            4: (960, 100, 1279, safe_boundaries(100 + height))
        }
    elif num_rectangles == 6:
        return {
            1: (0, 150, 213, safe_boundaries(150 + height)),
            2: (213, 300, 426, safe_boundaries(300 + height)),
            3: (426, 450, 639, safe_boundaries(450 + height)),
            4: (639, 100, 852, safe_boundaries(100 + height)),
            5: (852, 350, 1065, safe_boundaries(350 + height)),
            6: (1065, 200, 1279, safe_boundaries(200 + height))
        }
    elif num_rectangles == 8:
        return {
            1: (0, 150, 160, safe_boundaries(150 + height)),
            2: (160, 300, 320, safe_boundaries(300 + height)),
            3: (320, 450, 480, safe_boundaries(450 + height)),
            4: (480, 100, 640, safe_boundaries(100 + height)),
            5: (640, 350, 800, safe_boundaries(350 + height)),
            6: (800, 200, 960, safe_boundaries(200 + height)),
            7: (960, 600, 1120, safe_boundaries(600 + height)),
            8: (1120, 150, 1279, safe_boundaries(150 + height))
        }
    elif num_rectangles == 1:
        return {
            1: (0, 50, 1279, safe_boundaries(50 + height))
        }
    else:
        raise NotImplementedError('Only 4, 6, 8 rectangles are available!')


def find_rect(point, rect_width):
    rect = 0
    while point >= rect_width:
        point -= rect_width
        rect += 1
    if point > 0:
        rect += 1
    return rect


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.
    :param values: numpy ndarray
    :param weights: numpy ndarray (the same shape as values)
    """
    average = np.average(values, weights=weights)
    variance = np.average((values - average) ** 2, weights=weights)  # Fast and numerically precise
    return math.sqrt(variance)


def compute_stddev_accuracy(num_rects, values_list, max_voltage, min_voltage, height):
    """
    Provides the user with standard deviations calculated in rectangle-wise manner.
    :param num_rects: number of rectangles
    :param values_list: voltages read
    :param max_voltage: upper voltage range
    :param min_voltage: lower voltage range
    :param height: height of the rectangle in px
    :return: stddevs per rectangle in a form of list
    """
    deviations = {}
    inaccuracy = {}
    num_samples = len(values_list)
    rect_info = generate_rectangle_info(num_rects, height=height)
    rect_w_px = rect_info[2][0]
    #rect_h_px = rect_info[1][3] - rect_info[1][1]
    for rect in range(num_rects):
        target = int((rect_info[rect + 1][1] + rect_info[rect + 1][3]) / 2)
        start = px_to_sample(rect * rect_w_px, num_samples)
        stop = px_to_sample((rect + 1) * rect_w_px, num_samples)
        vals_px = [voltage_to_px(values_list[i], max_voltage, min_voltage) for i in range(start, stop)]
        deviations[rect + 1] = "{0:.2f}%".format(
                100 * np.mean(weighted_avg_and_std(values=vals_px, weights=None)) / height)
        diffs_px = [math.fabs(vals_px[j] - target) for j in range(len(vals_px))]
        inaccuracy[rect + 1] = "{0:.2f}%".format(100 * np.average(diffs_px) / height * 0.5)

    return deviations, inaccuracy


def compute_slew_rates(num_rects, values_list, max_voltage, min_voltage, height):
    """
    Calculates how quick did the object manage to reach the next rectangle from the previous one.
    :param num_rects: number of rectangles
    :param values_list: voltages read
    :param max_voltage:
    :param min_voltage:
    :param height: height of the rectangle in px
    :return:
    """
    slew_rates = {}
    rect_info = generate_rectangle_info(num_rects, height=height)
    num_samples = len(values_list)
    rect_w_px = rect_info[2][0]
    cur_rect = 2
    slew_cnt = 0
    cur_px = rect_w_px  # beginning of the second rect
    while cur_rect <= num_rects:
        if rect_info[cur_rect][1] <= voltage_to_px(values_list[px_to_sample(cur_px, num_samples)], max_voltage,
                                                   min_voltage) <= rect_info[cur_rect][3]:
            slew_rates['{}-{}'.format(cur_rect - 1, cur_rect)] = '{0:.2f}%'.format(slew_cnt / rect_w_px * 100)  # %
            slew_cnt = 0
            cur_px = cur_rect * rect_w_px
            cur_rect += 1
            continue
        else:
            if slew_cnt == rect_w_px - 1:  # slew rate reaches rectangle width!
                slew_rates['{}-{}'.format(cur_rect - 1, cur_rect)] = '{0:.2f}%'.format(slew_cnt / rect_w_px * 100)  # %
                slew_cnt = 0
                cur_px += 1
                cur_rect += 1
                continue
            slew_cnt += 1  # SCREEN_WIDTH_PX / num_samples  # slew_cnt in px
            cur_px += 1
    return slew_rates


# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def sample_to_px(sample_num, num_samples):
    resolution = SCREEN_WIDTH_PX / num_samples  # how many px per sample
    return (sample_num - 1) * resolution


# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def px_to_sample(px_num, num_samples):
    resolution = SCREEN_WIDTH_PX / num_samples
    value = int(math.ceil(px_num / resolution))
    return num_samples - 1 if value > num_samples - 1 else value


# THIS FUNCTION OUGHT TO BE MODIFIED SHOULD THE SCREEN RESOLUTION CHANGE!!!
def voltage_to_px(voltage, max_value, min_value):
    if voltage > max_value:
        return 0
    elif voltage < min_value:
        return MPL_GENERATED_SCREEN_HEIGHT_PX
    else:
        return int(
                round(MPL_GENERATED_SCREEN_HEIGHT_PX - (
                    voltage - min_value) / 0.003))  # MIN_VOLTAGE = 927px, 1px = 0.003V <- this works under the
# assumption that the voltage range is 2.781V!!!
