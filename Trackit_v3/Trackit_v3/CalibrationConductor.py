#CalibrationConductor
#runs the calibration game and stores the calibration value 
import pygame 
from win32api import GetSystemMetrics
import dearpygui.dearpygui as dpg
import SerialBoardAPI
import VoltageConverter
import daqmxlib
import serial
import numpy as np
import InputRepository as inRep

def RunCalibration(dpg, calibrationDataClass):

    pygame.init()
    #Setup calibration space and such 
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Calibration')

    bl = (0,0,0)
    w = (255,255,255)
    r = (255,0,0)
    g = (0,255,0)
    b = (0,0,255)

    clock = pygame.time.Clock()
    serialObj = serial.Serial() 
    inputMode = dpg.get_value("device")
    forcedirection = dpg.get_value("forceDirection")
    comport = dpg.get_value("comport")
    calibrated = False
    calibrationStarted = False
    setupConnection = True
    calibrationCounter = 0
    reader = 0
    feedbackVoltage = 0 
    serialConnection = 0
    experimentalMode = dpg.get_value("experimentMode")
    nidaqCh = dpg.get_value("nidaqCh")
    if inputMode == "NIDAQ":
        reader = daqmxlib.Reader({nidaqCh:1})

    if inputMode == "USB/ADAM":
        if setupConnection == True:
            serialObj = SerialBoardAPI.SetupSerialCommuniation(comport)
            serialObj = SerialBoardAPI.testCommunication(serialObj)
            SerialBoardAPI.OpenCommunication(serialObj)
            reader = SerialBoardAPI.GetValueFromA0(serialObj)
            setupConnection = False

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start Calibration', True, w)
    text_1 = font.render('1', True, w)
    text_2 = font.render('2', True, w)
    text_3 = font.render('3', True, w)
    text_calibrate = font.render('CALIBRATE!', True, w)
    text_motivation = font.render('FULL THROTTLE!', True, w)
    text_done = font.render('DONE!', True, w)
    text_feedback = font.render(str(feedbackVoltage), True, w)

    textRect = introText.get_rect()
    text_1_Rect = text_1.get_rect()
    text_2_Rect = text_2.get_rect()
    text_3_Rect = text_3.get_rect()
    text_cali_rect = text_calibrate.get_rect()
    text_moti_rect = text_motivation.get_rect()
    text_done_rect = text_done.get_rect()
    text_feedback_rect = text_feedback.get_rect()

    textpos = (GetSystemMetrics(0) // 2 ,GetSystemMetrics(1) //20 )
    feedbackPos = ((GetSystemMetrics(0) // 2)-200 ,GetSystemMetrics(1) //12 )
    textRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    text_1_Rect.center = textpos
    text_2_Rect.center = textpos
    text_3_Rect.center = textpos
    text_cali_rect.center = textpos
    text_moti_rect.center = textpos
    text_done_rect.center = textpos
    text_feedback_rect.center = feedbackPos

    def drawPlayer(ypos):
        pygame.draw.circle(gameDisplay, r, (GetSystemMetrics(0)/2, ypos), 5)

    #running calibtation
    while not calibrated:

        if(calibrationStarted == True):
        #resets image
            calibrationCounter += clock.get_time()
            gameDisplay.fill(bl)

            ypos, calibrationDataClass, feedbackVoltage = inRep.CalibrationInputCalculations(inputMode, serialObj, calibrationDataClass, experimentalMode, forcedirection, reader)
            drawPlayer(ypos)

            if(calibrationCounter < 1000):
                gameDisplay.blit(text_3, text_3_Rect)
            elif(calibrationCounter < 2000):
                gameDisplay.blit(text_2, text_2_Rect)
            elif(calibrationCounter < 3000):
                gameDisplay.blit(text_1, text_1_Rect)
            elif(calibrationCounter < 5000):
                gameDisplay.blit(text_calibrate, text_cali_rect)
                text_feedback = font.render(str(feedbackVoltage), True, w)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(calibrationCounter < 6000):
                gameDisplay.blit(text_motivation, text_moti_rect)
                text_feedback = font.render(str(feedbackVoltage), True, w)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(calibrationCounter < 8000):
                gameDisplay.blit(text_done, text_done_rect)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(calibrationCounter < 8500):
                calibrated = True                     

        else:
            gameDisplay.blit(introText, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calibrated = True
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    calibrationStarted = True

        pygame.display.update()
        clock.tick(120)
    pygame.quit()
