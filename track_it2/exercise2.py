from __future__ import division
import pygame
import daqmxlib
import os
import tools2
import json
import time
import numpy as np
import PyDAQmx
from PyDAQmx import Task


def send_trigger(trigger_mode):
    # Actuate a single digital pulse (period between 1 and 2 ms) on a desired port, depending on trigger mode value.
    # trigger_mode: either "random" or "series"
    print "Sending TMS trigger signal... mode = %s" % trigger_mode
    dev_port_line = ""
    if trigger_mode == "random":
        dev_port_line = "/Dev1/port1/line3"
    elif trigger_mode == "series":
        dev_port_line = "/Dev1/port1/line2"
    print dev_port_line
    task = Task()
    task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    task.StartTask()
    task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([1], dtype=np.uint8), None, None)
    task.StopTask()
    task = Task()
    task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
    task.StartTask()
    task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([0], dtype=np.uint8), None, None)
    task.StopTask()


# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1300, 100)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1, 20)
with open('config2.cfg', 'r') as cfg:
    conf_dict = json.loads(cfg.read())

# num_rectangles = conf_dict["num_rectangles"]
# rectangles_to_go = num_rectangles
rect_h = conf_dict["rect_height"]
rect_w = conf_dict["rect_width"]
RECT_W = rect_w
res_path = conf_dict["res_path"]
# num_series = conf_dict["num_series"]
# remaining_series = num_series
series = conf_dict["series"]
raw_quest = conf_dict["quest"]
max_voltage = float(conf_dict["max_voltage"])
quest = raw_quest.split()
total_num_rects = len(quest) + quest.count("s") * (len(series) - 1)  # all random plus all series rectangles
# series_first = conf_dict["series_first"]
# Initialize the game engine and the daq
pygame.init()
reader = daqmxlib.Reader()
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
pygame.display.set_caption("Quest mode")
font = pygame.font.SysFont('Arial', 25)
should_quit = False
size = [rect_w + 1100, 1000]
size_disp = [2549, 1400]
screen = pygame.display.set_mode(size_disp)
# rect params: [width0, height0, delta_w, delta_h], optional: thickness, otherwise filled rect
# trace params below
previous_pos = [0, 0]
center_pos = []
trace_size = 4
to_save_series = []
tmp_position = 0
is_series = False
was_score_in_rect = False
currently_on_target = False
not_sent = True
triggers = [0 for _ in range(total_num_rects)]
gaps = []
temp_iter = -1
for item in range(len(quest)):
    temp_iter += 1
    if quest[item] == "s":  # starting point for series
        triggers[temp_iter] = 1
        temp_iter += len(series) - 1
    elif quest[item] == "b":
        gaps.append(temp_iter)
    else:
        if item == 0 or quest[item - 1] == "s":
            triggers[temp_iter] = 2  # starting trigger
# print triggers
# print gaps
# print len(triggers), total_num_rects
# if series_first > 0 and len(series) > 0:
#     tmp_position = int(series[0])
#     rect_list = [[int(size[0] * 0.5), tmp_position, rect_w, rect_h]]
#     cur_ser_elem = 1  # it determines which element of the series should be drawn at will
# else:
#     tmp_position = random.randint(0, 899)
#     rect_list = [[int(size[0] * 0.5), tmp_position, rect_w, rect_h]]
#     rectangles_to_go -= 1
#     cur_ser_elem = 0
if quest[0] == "s":
    is_series = True
    tmp_position = int(series[0][:-1])  # because the last character is the colour
    cur_ser_elem = 1
    cur_q_elem = 0
elif quest[0] == "b":  # blank rectangle at the beginning
    tmp_position = 500
    cur_q_elem = 1
    cur_ser_elem = 0
else:
    tmp_position = int(quest[0])
    cur_ser_elem = 0
    cur_q_elem = 1

cur_rect_index = 0
# rect_list = [[int(size[0]), tmp_position, rect_w, rect_h]]
rect_list = [[int(size[0]), tmp_position, 1, rect_h, cur_rect_index]]
cur_rect_index += 1
old_rect_index = -1  # will be used to detect a new rectangle passing over the trace
rect_px_cnt = 0
to_save_series.append(tmp_position)
shift_cnt = 0
# score_s = 0
# score_q = 0
scores = [0 for _ in range(total_num_rects)]
inaccuracies = [[] for _ in range(total_num_rects)]
inacs = [0 for _ in range(total_num_rects)]
stddevs = [0 for _ in range(total_num_rects)]
slew_rates = [0 for _ in range(total_num_rects)]
exit_rates = [0 for _ in range(total_num_rects)]
# inaccuracies_s = []
# inaccuracies_q = []
samples = [[] for _ in range(total_num_rects)]

# print scores, inaccuracies, inacs, stddevs, samples
# for rect in range(total_num_rects):
#     samples[rect] = []
#     scores[rect] = 0
#     inaccuracies[rect] = []
#     inacs = 0
#     stddevs[rect] = 0

ready = False
beep = pygame.mixer.Sound('beep.wav')


def draw_from_list(chosen_list):
    colour = r
    for i, rect_pos in enumerate(chosen_list):
        # if rect_pos[0] == 0:  # if it reached left border ...
        if rect_pos[0] == 1100:  # if it reached left border ...
            if rect_pos[2] == 0:  # ... and has already shrunk to nothing
                chosen_list.remove(rect_pos)  # get rid of it
            else:  # shrink it more
                rect_pos[2] -= 1
        else:  # shift to the left
            rect_pos[0] -= 1
            if rect_pos[2] < rect_w:  # so it just need to stretch at the right border
                rect_pos[2] += 1
        colour = eval(rect_pos[-1]) if len(rect_pos) == 6 else r  # now series elements have colour attribute at the end
        pygame.draw.rect(screen, colour, rect_pos[:4], 3) if rect_pos[-1] not in gaps else pygame.draw.rect(screen, white, rect_pos[:4], 1)
    return chosen_list


def refresh_background_series(a_list):
    global shift_cnt, cur_q_elem, cur_ser_elem, is_series, cur_rect_index
    # screen.fill(white)
    screen.fill(f)
    pygame.draw.rect(screen, white, [1100, 1, rect_w, 1000], 0)
    # if remaining_series > 0:
    #     if shift_cnt == rect_w:  # last one shifted the whole width - render a new rectangle...
    #         tmp = int(series[cur_ser_elem])
    #         a_list.append([size[0], tmp, 1, rect_h])  # ... of initial width from series list
    #         to_save_series.append(tmp)
    #         cur_ser_elem += 1
    #         if cur_ser_elem == len(series):
    #             cur_ser_elem = 0
    #             remaining_series -= 1
    #         shift_cnt = 0
    #     else:  # last one still needs to shift more
    #         shift_cnt += 1
    if shift_cnt == rect_w:
        tmp = int(series[cur_ser_elem][:-1])
        a_list.append([size[0], tmp, 1, rect_h, cur_rect_index, series[cur_ser_elem][-1]])  # ... of initial width from series list (now with colours at the end)
        cur_rect_index += 1
        to_save_series.append(tmp)
        cur_ser_elem += 1
        if cur_ser_elem == len(series):
            cur_ser_elem = 0
            cur_q_elem += 1
            is_series = False
            if cur_q_elem < len(quest):
                if quest[cur_q_elem] == "s":
                    is_series = True
        shift_cnt = 0
    else:  # last one still needs to shift more
        shift_cnt += 1
    return draw_from_list(a_list)


def refresh_background_random(a_list):
    global shift_cnt, cur_q_elem, is_series, cur_rect_index
    # screen.fill(white)
    screen.fill(f)
    pygame.draw.rect(screen, white, [1100, 1, rect_w, 1000], 0)
    # if rectangles_to_go > 0:  # because one is already in the list!
    #     if shift_cnt == rect_w:
    #         tmp = random.randint(0, 899)
    #         a_list.append([size[0], tmp, 1, rect_h])
    #         to_save_series.append(tmp)
    #         rectangles_to_go -= 1
    #         shift_cnt = 0
    #     else:
    #         shift_cnt += 1
    if cur_q_elem < len(quest):
        if shift_cnt == rect_w:
            if quest[cur_q_elem] == "s":  # when we still slide the last quest one, but the next one is from series
                tmp = int(series[0])
            elif quest[cur_q_elem] == "b":  # a gap!
                tmp = 500
            else:
                tmp = int(quest[cur_q_elem])
            a_list.append([size[0], tmp, 1, rect_h, cur_rect_index])
            cur_rect_index += 1
            to_save_series.append(tmp)
            cur_q_elem += 1
            if cur_q_elem < len(quest):
                if quest[cur_q_elem] == "s":
                    is_series = True
            shift_cnt = 0
        else:
            shift_cnt += 1
    return draw_from_list(a_list)


def refresh_background():
    global shift_cnt, cur_q_elem, is_series
    # if series_first > 0:
    #     if remaining_series > 0:
    #         return refresh_background_series(rect_list)
    #     else:
    #         return refresh_background_random(rect_list)
    # else:
    #     if rectangles_to_go > 0:
    #         return refresh_background_random(rect_list)
    #     else:
    #         return refresh_background_series(rect_list)
    # if cur_q_elem == "s":
    #     is_series = True
    #     print "Hey, now series!"
    # else:
    #     is_series = False

    if is_series:
        return refresh_background_series(rect_list)
    else:
        return refresh_background_random(rect_list)


while not should_quit:
    for event in pygame.event.get():  # This enables clicking "X" to close the window (and the exercise programme)
        if event.type == pygame.QUIT:
            should_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                beep.play(maxtime=200)
                pygame.time.delay(400)  # because beep returns immediately!
                ready = True
    if not ready:
        pygame.time.delay(100)
    else:
        if rect_list:
            # print rect_list
            refresh_background()
            # center_pos = [int(size[0] * 0.5), tools2.get_px_from_voltage(samples[-1])]
            raw_sample = reader.read()[0]
            center_pos = [int(1100 + RECT_W * 0.5), tools2.get_px_from_voltage(raw_sample, max_voltage)]
            if currently_on_target:
                pygame.draw.circle(screen, b, center_pos, trace_size)
            else:
                pygame.draw.circle(screen, r, center_pos, trace_size)
            for rect in rect_list:
                if rect[0] <= center_pos[0] <= rect[0] + rect[2]:  # only evaluate the proper rectangle
                    # the appropriate samples and scores lists should be updated
                    rect_index = rect[4]
                    # print rect_index, old_rect_index
                    if rect_index != old_rect_index:  # we have changed an "active" rectangle
                        not_sent = True
                        was_score_in_rect = False  # useful for computing slew rates
                        old_rect_index = rect_index
                        rect_px_cnt = 0
                        if not_sent:
                            if triggers[rect_index] == 1:
                                print "Series trigger"
                                send_trigger("series")
                                not_sent = False
                            elif triggers[rect_index] == 2:
                                print "Random trigger"
                                send_trigger("random")
                                not_sent = False
                    # print rect_index
                    if rect_index not in gaps:  # calculate scores only for non-blank rectangles!
                        rect_w = RECT_W #!!!!!!!!!!!!!!!!!!!!!!
                        rect_px_cnt += 1
                        # print rect_px_cnt
                        samples[rect_index].append(raw_sample)
                        inaccuracies[rect_index].append(abs(center_pos[1] - ((rect[1] + (rect[1] + rect[3])) / 2)))
                        if rect[1] <= center_pos[1] <= rect[1] + rect[3]:
                            scores[rect_index] += 1
                            currently_on_target = True
                            was_score_in_rect = True
                            exit_rates[rect_index] = rect_px_cnt
                        else:
                            currently_on_target = False
                            if not was_score_in_rect:
                                slew_rates[rect_index] += 1
                    else: # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        rect_w = 20
                    # if is_series:
                    #     inaccuracies_s.append(abs(center_pos[1] - ((rect[1] + (rect[1] + rect[3])) / 2)))
                    # else:
                    #     inaccuracies_q.append(abs(center_pos[1] - ((rect[1] + (rect[1] + rect[3])) / 2)))
                    # evaluate(center_pos)
                    break

        else:
            # score = (score / (rect_w * (num_rectangles + num_series * len(series)) + 1))
            # print "SERIES: {} {}".format(score_s, quest.count("s") * len(series))
            # print "REST: {} {}".format(score_q, len(raw_quest.replace("s", "").split()))
            # score_s = (score_s / (rect_w * quest.count("s") * len(series)))
            # score_q = (score_q / (rect_w * len(raw_quest.replace("s", "").split())))
            # inaccuracy_s = average(inaccuracies_s)
            # inaccuracy_q = average(inaccuracies_q)
            # inaccuracy = average(inaccuracies)
            # calculate stddev for each rectangle
            for temp in range(total_num_rects):
                samples_px = [tools2.get_px_from_voltage(samples[temp][j], max_voltage) for j in
                              range(len(samples[temp]))]
                stddevs[temp] = tools2.weighted_avg_and_std(samples_px, None)
                inacs[temp] = np.average(inaccuracies[temp])
            final_score_avg = sum(scores) / (rect_w * total_num_rects)
            screen.blit(font.render(
                '{0:.2f}%'.format(final_score_avg * 100), True, b), (1100, 400))
            # screen.blit(font.render('INACCURACY: {inac}'.format(inac=inaccuracy), True, blue), (100, 400))
            # screen.blit(font.render('STDDEV: {stddev}'.format(stddev=stddev), True, blue), (100, 800))
            pygame.display.update()
            # tools2.save_quest_data(samples, score, inaccuracy, stddev)
            with open(res_path, "a") as results:
                results.write(
                    "Score (% of rect width)\tInaccuracy (% of half of rect height)\tStddev (% of rect height)"
                    "\tEntry (% of rect width)\tExit (% of rect width)\n")
                for temp in range(total_num_rects):
                    results.write(
                        "{s}\t{i}\t{d}\t{sr}\t{er}\n".format(s=(scores[temp] / rect_w), i=(inacs[temp] / (rect_h * 0.5)),
                                                       d=(stddevs[temp] / rect_h), sr=(slew_rates[temp] / rect_w), er=(exit_rates[temp] / rect_w)))
                    # results.write("Score_s\tScore_r\tInaccuracy_s\tInaccuracy_r\tStddev\n")
                    # results.write(
                    #     "{ss}\t{sq}\t{inacs}\t{inacq}\t{stddev}\n".format(ss=score_s, sq=score_q, inacs=inaccuracy_s,
                    #                                                       inacq=inaccuracy_q, stddev=stddev))
            tools2.save_quest_settings(to_save_series)
            time.sleep(1)
            should_quit = True
        pygame.display.update()
pygame.quit()
