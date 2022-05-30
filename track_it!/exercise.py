import pygame
import daqmxlib
import tools2
import os
import datetime
import json
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 100)
with open('config.cfg', 'r') as cfg:
    conf_dict = json.loads(cfg.read())
series = None if 'series' not in conf_dict else conf_dict['series']
num_rectangles = conf_dict["num_rectangles"]
rect_height = conf_dict["rect_height"]
duration = conf_dict["duration"]
with_fb = (conf_dict["with_fb"] == 1)
time_to_fb = conf_dict["time_to_fb"]
fb_time = conf_dict["fb_time"]
time_post_fb = conf_dict["time_post_fb"]
num_reps = conf_dict["num_reps"]
max_voltage = float(conf_dict["max_voltage"])
# Initialize the game engine and the daq
pygame.init()
reader = daqmxlib.Reader()
actuator = daqmxlib.Actuator(physical_channels=["ao1"])
# Define the colors we will use in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
samples_for_durations = (800, 800, 960, 960, 800, 960, 1120, 1280, 720, 800, 880, 960)
px_per_sample = samples_for_durations[duration - 1] / (80 * duration)
# The width is adjusted to the length of the run
size = [samples_for_durations[duration - 1], 1000]
screen = pygame.display.set_mode(size)
rect_info, rect_width = tools2.prepare_background(size[0], size[1], num_rectangles, rect_height, series)
img = pygame.image.load('exercise.png')
pygame.display.set_caption("Exercise")
font = pygame.font.SysFont('Arial', 25)
should_quit = False
# Unfortunately it must be here alone, and later called by prepare function.
screen.blit(img, [0, 0])
done = 0
x0 = 0
raw = reader.read()[0]
y0 = tools2.get_px_from_voltage(raw, max_voltage)
x = 0
points = [(x0, y0), ]
raw_samples = [raw]
pygame.display.update()
ready = False
beep = pygame.mixer.Sound('beep.wav')


def prepare(repetitions):
    """
    Do the above inits when more repetitions are scheduled.
    :param repetitions: do inits only if there are any left
    :return:
    """
    global done, x0, raw, y0, x, points, raw_samples, start_time
    if repetitions:
        screen.blit(img, [0, 0])
        done = 0
        x0 = 0
        raw = reader.read()[0]
        y0 = tools2.get_px_from_voltage(raw, max_voltage)
        x = 0
        points = [(x0, y0), ]
        raw_samples = [raw]
        pygame.display.update()
        pygame.time.delay(time_post_fb * 1000)
        beep.play(maxtime=200)
        # pygame.time.delay(400)
        actuator.execute_task("Start", 10000, 5, auto_start=1, timeout=50)
        start_time = datetime.datetime.now()


def draw_new(new_x):
    r = reader.read()[0]
    y2 = tools2.get_px_from_voltage(r, max_voltage)
    points.append((new_x, y2))
    raw_samples.append(r)
    pygame.draw.line(screen, blue, [points[-2][0], points[-2][1]], [points[-1][0], points[-1][1]], 2)
while not should_quit and num_reps > 0:
    for event in pygame.event.get():  # This enables clicking "X" to close the window (and the exercise programme)
        if event.type == pygame.QUIT:
            should_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.time.delay(time_post_fb * 1000)
                beep.play(maxtime=200)
                pygame.time.delay(400)  # because beep returns immediately!
                start_time = datetime.datetime.now()
                ready = True
    if not ready:
        pygame.time.delay(100)
    else:
        if len(rect_info) * rect_width - 1 - x < px_per_sample and done == 0:
            stop_date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            done = 1
            stop_time = datetime.datetime.now() - start_time
            print "Taking {} samples took {}.".format(len(points), stop_time.total_seconds())
        if done == 2:  # ultimate freeze - after all the repetitions
            if with_fb:
                pygame.time.delay(fb_time * 1000)  # time of fb
            screen.fill(white)
            num_reps -= 1
            prepare(num_reps)
        elif done == 1:  # print feedback with appropriate delays
            ra = tools2.ResultAnalyser(points, rect_info, size[0])
            prec, inac = ra.compute_stddev_accuracy()
            sr = ra.compute_slew_rates()
            sc = ra.get_score()
            ra.store_results(stop_time.total_seconds(), raw_samples, stop_date)
            ra.save_series()
            # TODO make these pulses and test them in the lab!
            actuator.execute_task("End", 10000, 5, auto_start=1, timeout=50)
            pygame.time.delay(time_to_fb * 1000)  # time to fb
            if with_fb:
                screen.blit(font.render('Score: {}!'.format(sc), True, blue), (size[0] - 200, size[1] - 100))
            done = 2
            x += px_per_sample
        elif done == 0:
            x += px_per_sample
            draw_new(x)
        pygame.display.update()
pygame.quit()
