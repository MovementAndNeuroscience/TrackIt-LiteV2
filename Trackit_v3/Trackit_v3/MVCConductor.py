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

def RunMVC(dpg, smoothingFilter):

    pygame.init()
    #Setup calibration space and such 
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Maximum Voluntary Contraction Test')

    bl = (0,0,0)
    w = (255,255,255)
    r = (255,0,0)
    g = (0,255,0)
    b = (0,0,255)

    clock = pygame.time.Clock()
    serialObj = serial.Serial() 
    inputMode = dpg.get_value("device")
    forceDirection = dpg.get_value("forceDirection")
    maxVoltage = dpg.get_value("maxVoltage")
    minVoltage = dpg.get_value("minVoltage")
    neutralVal = dpg.get_value("neutralNIDAQval")
    percentageOfMaxVoltage = dpg.get_value("percentOfMaxCal")
    absOrRelvoltage = "Absolute"
    comport = dpg.get_value("comport")
    absoluteMaxVoltage = 7.0
    minIsoCalibrationValue = dpg.get_value("minIsometricCaliVal")
    pushPull = dpg.get_value("pushPull")
    setupConnection = True
    mvcCounter = 0
    reader = 0
    feedbackVoltage = 0 
    startMVCTime = 3000
    stopMVCTime = 12000
    maxMvcinTiem = 0
    maxMvcinY = 0
    maxMvcinVoltage = 0 
    serialConnection = 0
    vToNCoefficient= dpg.get_value("vToNCoefficient")
    mvcFound = False
    mvcStarted = False
    experimentalMode = dpg.get_value("experimentMode")
    nidaqCh = dpg.get_value("nidaqCh")
    linearLog = dpg.get_value("linearLog")
    playerposX = []
    playerposY = []
    voltagelist = []

    if inputMode == "NIDAQ":
        reader = daqmxlib.Reader({nidaqCh:1})

    if inputMode == "USB/ADAM":
        if setupConnection == True:
            serialObj = SerialBoardAPI.SetupSerialCommuniation(comport)
            serialObj = SerialBoardAPI.testCommunication(serialObj)
            SerialBoardAPI.OpenCommunication(serialObj)
            if experimentalMode == "Dynamic":
                SerialBoardAPI.EnableDynamicMeasurement(serialObj)
                reader = SerialBoardAPI.GetPotValue(serialObj)
            if experimentalMode == "Isometric":
                SerialBoardAPI.EnableIsomeetricMeasurement(serialObj)
                ##SerialBoardAPI.OffsetLoadCell(serialObj)
                reader = SerialBoardAPI.GetLoaValue(serialObj)
            setupConnection = False

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start MVC', True, w)
    text_1 = font.render('1', True, w)
    text_2 = font.render('2', True, w)
    text_3 = font.render('3', True, w)
    text_start = font.render('GIVE IT ALL!', True, w)
    text_motivation = font.render('FULL THROTTLE!', True, w)
    text_done = font.render('DONE!', True, w)
    text_feedback = font.render(str(feedbackVoltage), True, w)

    textRect = introText.get_rect()
    text_1_Rect = text_1.get_rect()
    text_2_Rect = text_2.get_rect()
    text_3_Rect = text_3.get_rect()
    text_start_rect = text_start.get_rect()
    text_moti_rect = text_motivation.get_rect()
    text_done_rect = text_done.get_rect()
    text_feedback_rect = text_feedback.get_rect()

    textpos = (GetSystemMetrics(0) // 2 ,GetSystemMetrics(1) //20 )
    feedbackPos = ((GetSystemMetrics(0) // 2)-200 ,GetSystemMetrics(1) //12 )
    textRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    text_1_Rect.center = textpos
    text_2_Rect.center = textpos
    text_3_Rect.center = textpos
    text_start_rect.center = textpos
    text_moti_rect.center = textpos
    text_done_rect.center = textpos
    text_feedback_rect.center = feedbackPos

    def drawPlayer(playerposX, playerposY):
        for posx, posy in zip(playerposX, playerposY):
            pygame.draw.circle(gameDisplay, r, (posx, posy), 6)

    def DrawAxis(minTime, maxTime, maxVoltage):
        fifthTime = (maxTime - minTime)/5
        fifthScreen = GetSystemMetrics(0) / 5

        tenthNewton = round((absoluteMaxVoltage*vToNCoefficient)/10)
        tenthScreenHeight = GetSystemMetrics(1) / 10 

        #X AXIS Line
        pygame.draw.line(gameDisplay,w,(0,GetSystemMetrics(1) - 45), (GetSystemMetrics(0), GetSystemMetrics(1)-45),2)
        # Y AXIS LINE 
        pygame.draw.line(gameDisplay,w,(130,0), (130, GetSystemMetrics(1)),2)

        # X AXIS
        time_0 = font.render('0 s', True, w)

        time_tik_1 = str(fifthTime/1000 )+ ' s'
        time_1 = font.render(time_tik_1, True, w)

        time_tik_2 = str((fifthTime + fifthTime)/1000) + ' s'
        time_2 = font.render(time_tik_2, True, w)

        time_tik_3 = str((fifthTime + fifthTime + fifthTime)/1000) + ' s'
        time_3 = font.render(time_tik_3, True, w)

        time_tik_4 = str((fifthTime + fifthTime + fifthTime + fifthTime)/1000) + ' s'
        time_4 = font.render(time_tik_4, True, w)

        time_tik_5 = str((fifthTime + fifthTime + fifthTime + fifthTime + fifthTime)/1000) + ' s'
        time_5 = font.render(time_tik_5, True, w)
        
        time_0_Rect = time_0.get_rect()
        time_1_Rect = time_1.get_rect()
        time_2_Rect = time_2.get_rect()
        time_3_Rect = time_3.get_rect()
        time_4_Rect = time_4.get_rect()
        time_5_Rect = time_5.get_rect()

        moveToLeftpx = 45 
        time_0_Rect.center = (85, GetSystemMetrics(1) - 20)
        time_1_Rect.center = (fifthScreen - moveToLeftpx, GetSystemMetrics(1) - 20)
        time_2_Rect.center = (fifthScreen * 2 -moveToLeftpx, GetSystemMetrics(1) - 20)
        time_3_Rect.center = (fifthScreen * 3 -moveToLeftpx, GetSystemMetrics(1) - 20)
        time_4_Rect.center = (fifthScreen * 4 -moveToLeftpx, GetSystemMetrics(1) - 20)
        time_5_Rect.center = (fifthScreen * 5 -moveToLeftpx, GetSystemMetrics(1) - 20)

        gameDisplay.blit(time_0, time_0_Rect)
        gameDisplay.blit(time_1, time_1_Rect)
        gameDisplay.blit(time_2, time_2_Rect)
        gameDisplay.blit(time_3, time_3_Rect)
        gameDisplay.blit(time_4, time_4_Rect)
        gameDisplay.blit(time_5, time_5_Rect)


        # Y AXIS 
        newton_0 = font.render('0 N', True, w)

        newton_tik_1 = str(tenthNewton )+ ' N'
        newton_1 = font.render(newton_tik_1, True, w)

        newton_tik_2 = str(tenthNewton*2 )+ ' N'
        newton_2 = font.render(newton_tik_2, True, w)

        newton_tik_3 = str(tenthNewton*3 )+ ' N'
        newton_3 = font.render(newton_tik_3, True, w)

        newton_tik_4 = str(tenthNewton*4 )+ ' N'
        newton_4 = font.render(newton_tik_4, True, w)

        newton_tik_5 = str(tenthNewton*5 )+ ' N'
        newton_5 = font.render(newton_tik_5, True, w)

        newton_tik_6 = str(tenthNewton*6 )+ ' N'
        newton_6 = font.render(newton_tik_6, True, w)

        newton_tik_7 = str(tenthNewton*7 )+ ' N'
        newton_7 = font.render(newton_tik_7, True, w)

        newton_tik_8 = str(tenthNewton*8 )+ ' N'
        newton_8 = font.render(newton_tik_8, True, w)

        newton_tik_9 = str(tenthNewton*9 )+ ' N'
        newton_9 = font.render(newton_tik_9, True, w)

        newton_tik_10 = str(tenthNewton*10 )+ ' N'
        newton_10 = font.render(newton_tik_10, True, w)

        newton_0_Rect = newton_0.get_rect()
        newton_1_Rect = newton_1.get_rect()
        newton_2_Rect = newton_2.get_rect()
        newton_3_Rect = newton_3.get_rect()
        newton_4_Rect = newton_4.get_rect()
        newton_5_Rect = newton_5.get_rect()
        newton_6_Rect = newton_6.get_rect()
        newton_7_Rect = newton_7.get_rect()
        newton_8_Rect = newton_8.get_rect()
        newton_9_Rect = newton_9.get_rect()
        newton_10_Rect = newton_10.get_rect()

        moveToRightpx = 70 
        newton_0_Rect.center = (moveToRightpx + 20, GetSystemMetrics(1) - 60)
        newton_1_Rect.center = (moveToRightpx + 10, GetSystemMetrics(1) - tenthScreenHeight)
        newton_2_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*2)
        newton_3_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*3)
        newton_4_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*4)
        newton_5_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*5)
        newton_6_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*6)
        newton_7_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*7)
        newton_8_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*8)
        newton_9_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*9)
        newton_10_Rect.center = (moveToRightpx, GetSystemMetrics(1) - tenthScreenHeight*9.8)

        gameDisplay.blit(newton_0, newton_0_Rect)
        gameDisplay.blit(newton_1, newton_1_Rect)
        gameDisplay.blit(newton_2, newton_2_Rect)
        gameDisplay.blit(newton_3, newton_3_Rect)
        gameDisplay.blit(newton_4, newton_4_Rect)
        gameDisplay.blit(newton_5, newton_5_Rect)
        gameDisplay.blit(newton_6, newton_6_Rect)
        gameDisplay.blit(newton_7, newton_7_Rect)
        gameDisplay.blit(newton_8, newton_8_Rect)
        gameDisplay.blit(newton_9, newton_9_Rect)
        gameDisplay.blit(newton_10, newton_10_Rect)

    #running MVC
    while not mvcFound:

        if(mvcStarted == True):
        #resets image
            mvcCounter += clock.get_time()
            gameDisplay.fill(bl)

            feedbackVoltage, ypos = inRep.InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader, smoothingFilter, pushPull, linearLog, neutralVal)
            feedbackVoltage = feedbackVoltage*vToNCoefficient
            if(mvcCounter > startMVCTime ):
                relativeMaxTime = stopMVCTime - startMVCTime
                timerOffset = mvcCounter - startMVCTime
                percentOfrelativeMaxTime = timerOffset / (relativeMaxTime)
                playerposX.append(GetSystemMetrics(0) * percentOfrelativeMaxTime)
                playerposY.append(ypos)
                voltagelist.append(feedbackVoltage)
                drawPlayer(playerposX, playerposY)
            
            if(mvcCounter > stopMVCTime):
                tempY = 0
                tempX = 0
                tempVoltage = 0
                for xpos, ypos, voltage in zip(playerposX, playerposY, voltagelist):
                    if voltage > tempVoltage:
                        tempY = ypos
                        tempX = xpos
                        tempVoltage = voltage
                maxMvcinTiem = tempX
                maxMvcinVoltage = tempVoltage
                maxMvcinY = tempY

            if(mvcCounter < 1000):
                gameDisplay.blit(text_3, text_3_Rect)
            elif(mvcCounter < 2000):
                gameDisplay.blit(text_2, text_2_Rect)
            elif(mvcCounter < startMVCTime):
                gameDisplay.blit(text_1, text_1_Rect)
            elif(mvcCounter < 4000):
                gameDisplay.blit(text_start, text_start_rect)
                text_feedback = font.render(str(feedbackVoltage), True, w)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(mvcCounter < stopMVCTime):
                gameDisplay.blit(text_motivation, text_moti_rect)
                text_feedback = font.render(str(feedbackVoltage), True, w)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(mvcCounter < 16000):
                pygame.draw.line(gameDisplay,g,(maxMvcinTiem,0.0),(maxMvcinTiem,GetSystemMetrics(1)),3)
                gameDisplay.blit(text_done, text_done_rect)
                text_feedback = font.render(str(maxMvcinVoltage), True, w)
                gameDisplay.blit(text_feedback, text_feedback_rect)
            elif(mvcCounter < 18000):
                dpg.set_value("maxMvc", maxMvcinVoltage)

                mvcFound = True                     

            DrawAxis(startMVCTime, stopMVCTime, maxVoltage)

        else:
            gameDisplay.blit(introText, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mvcFound = True
                smoothingFilter.ResetFilter()
                SerialBoardAPI.CloseCommunication(serialObj)
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    smoothingFilter.ResetFilter()
                    SerialBoardAPI.CloseCommunication(serialObj)
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    mvcStarted = True

        pygame.display.update()
        clock.tick(120)
    smoothingFilter.ResetFilter()
    SerialBoardAPI.CloseCommunication(serialObj)
    pygame.quit()
