import dearpygui.dearpygui as dpg
import Eventsdata
import EventData 
import InputData
import InputDatas
import TriggerSender
import numpy as np
import pygame 
from win32api import GetSystemMetrics
import SaveDataFiles as SaveFiles
import TrackItStatistics as statistics
import VoltageConverter
import daqmxlib
import serial
import SerialBoardAPI
import InputRepository as inRep
import HighscoreRepository as highRep
import random
 
def RunGame(dpg, eventsData, smoothingFilter):

    pygame.init()
    #Setup calibration space and such 
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Track-it V3')

    inputMode = dpg.get_value("device")
    forceDirection = dpg.get_value("forceDirection")
    useSustain = dpg.get_value("TargetSustain")
    minSustainTime = dpg.get_value("sustainOnTarget")
    maxVoltage = dpg.get_value("maxVoltage")
    minVoltage = dpg.get_value("minVoltage")
    percentageOfMaxVoltage = dpg.get_value("percentOfMaxCal")
    absOrRelvoltage = dpg.get_value("absOrRelVoltage")
    absoluteMaxVoltage = dpg.get_value("absMaxVoltage")
    comport = dpg.get_value("comport")
    bioComport = dpg.get_value("biosemiComport")
    biosemi = dpg.get_value("Biosemi")
    experimentalMode = dpg.get_value("experimentMode")
    nidaqCh = dpg.get_value("nidaqCh")
    level = dpg.get_value("playerLevel")
    coinEnabled = dpg.get_value("coinRew")
    SoundEnabled = dpg.get_value("soundRew")
    pushPull = dpg.get_value("pushPull")

    gameStarted = False
    countdownStarted = False
    gameOver = False
    endOfFeedback = False
    gameTimeCounter = 0
    countDownCounter = 0 
    eventIndex = 0
    eventVisibleTime = 0 
    collisionDetected = False
    firstEvent = True
    reacted = False 
    eventTriggerSend = False
    tempPos = 0
    reader = 0
    score = 0
    setupConnection = True
    setupBioConnection = True
    rectBorderWidth = 2

    coinImg = None
    coinRect = None
    imgAlpha = 255
    coinpos = 0
    imgWidth = 0
    towardsMinus = True
    plingSound1 = None
    plingSound2 = None
    plingSound3 = None
    plingSound4 = None
    plingSound5 = None
    playsound = True


    serialObj = serial.Serial() 
    inputs = InputDatas.InputDatas()
    events = eventsData.eventDatas
    
    bl = (0,0,0)
    f = (0,0,0)
    w = (255,255,255)
    r = (255,0,0)
    g = (0,255,0) # bright green
    h = (0,128,0) # dark green
    b = (0,0,255) # bright blue
    d = (0,0,128) # dark blue
    y = (255, 255, 0)  # yellow
    v = (148, 0, 211)  # violet
    c = (0, 255, 255)  # cyan
    p = (255, 20, 147)  # pink
    o = (255,140,0) # orange

    clock = pygame.time.Clock()
    clockEndOfGame = 0; 

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
                reader = SerialBoardAPI.GetLoaValue(serialObj)
            SerialBoardAPI.ResetTimer(serialObj)
            setupConnection = False
            
    if biosemi == True and setupBioConnection == True:
        bioSerialObj = SerialBoardAPI.SetupSerialCommuniation(bioComport)
        SerialBoardAPI.OpenCommunication(bioSerialObj)
        setupBioConnection == False

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start TrackIt', True, w)
    guidelineText = font.render("Hit the squares as fast and accurate as possible", True, w)

    textRect = introText.get_rect()
    guideTextRect = guidelineText.get_rect() 

    middleTextPos = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    textRect.center = middleTextPos
    guideTextRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) - 50)
    
    if forceDirection == "Upwards":
        for event in events:
            rectPos = 0
            if event.eventType == "R":
                rectPos = GetSystemMetrics(1) - event.targetPosition
                if rectPos < 0:
                    rectPos = 10
            elif event.eventType == "B" or event.eventType == "P":
                rectPos = (GetSystemMetrics(1)-  event.targetHeight  ) - event.targetPosition
            print("RECT POS : " + str(rectPos))
            event.targetPosition = rectPos
        
        guideTextRect.center = (GetSystemMetrics(0) // 2, 50)
        
    #Feeedback Variables 
    feedbackLength = dpg.get_value("feedbackLength")
    feedbackTimer = 0
    feedbackAcc = font.render('accuracy', True, w)
    feedbackAccRect = feedbackAcc.get_rect()
    feedbackAccRect.center = ((GetSystemMetrics(0) // 2) - 200, GetSystemMetrics(1) // 2)
    feedbackTime = font.render('timeOnTarget', True, w)
    feedbackTimeRect = feedbackAcc.get_rect()
    feedbackTimeRect.center = ((GetSystemMetrics(0) // 2) - 400, GetSystemMetrics(1) // 2 + 50)
    meanAccuracy = 0
    meanTimeOnTarget = 0 

    #CountDown 
    text_1 = font.render('1', True, w)
    text_2 = font.render('2', True, w)
    text_3 = font.render('3', True, w)
    text_1_Rect = text_1.get_rect()
    text_2_Rect = text_2.get_rect()
    text_3_Rect = text_3.get_rect()
    text_1_Rect.center = middleTextPos
    text_2_Rect.center = middleTextPos
    text_3_Rect.center = middleTextPos

    # level and Score text
    leveltext = font.render('Level : ', True, w )
    level_rect = leveltext.get_rect()
    level_rect.center = (100, 100)

    scoretext = font.render('Score : ', True, w )
    score_rect = scoretext.get_rect()
    score_rect.center = (GetSystemMetrics(0) - 200, 100)

    #Coin and SoundReward
    if coinEnabled:
        coinImg = pygame.image.load("Assets\images\smallcoin.png").convert_alpha()
        coinRect = coinImg.get_rect()
        coinRect.center = (GetSystemMetrics(0)// 2, events[0].targetPosition)
        coinImg.set_alpha(imgAlpha) 
        imgWidth = coinImg.get_width()
    
    if SoundEnabled:
        plingSound1 = pygame.mixer.Sound("Assets\sounds\pling_1.wav")
        plingSound2 = pygame.mixer.Sound("Assets\sounds\pling_2.wav")
        plingSound3 = pygame.mixer.Sound("Assets\sounds\pling_3.wav")
        plingSound4 = pygame.mixer.Sound("Assets\sounds\pling_4.wav")
        plingSound5 = pygame.mixer.Sound("Assets\sounds\pling_5.wav")


    def drawPlayer(ypos, color):
        pygame.draw.circle(gameDisplay, color, (GetSystemMetrics(0)/2, ypos), 6)

    def CollisionDetection(event, ypos, collisionDetected):
        if (ypos < event.targetHeight + event.targetPosition) and ypos > event.targetPosition and collisionDetected == False:
            collisionDetected = True
            event.targetEntryTime = gameTimeCounter
            return collisionDetected, event
        return collisionDetected, event
            
    def OverlapDetection(event, ypos, collisionDetected, dpg, score):
        if collisionDetected == True:
            event.timeOnTarget += clock.get_time()
            if dpg.get_value("visScore") == True:
                score += 1
            drawPlayer(ypos, g)
        return event, score

    def ExitDetection(event, ypos, collisionDetected):
        if (ypos > event.targetHeight + event.targetPosition or ypos < event.targetPosition) and collisionDetected == True:
            collisionDetected = False
            event.targetExitTime = gameTimeCounter
            return collisionDetected, event
        return collisionDetected, event

    def CalculateReactionTime(event, OldPosY, newPosY, reacted):
        if reacted == False and (abs(OldPosY-newPosY) < 100 and abs(OldPosY-newPosY) > 3):
            event.reactionTime = eventVisibleTime
            reacted = True
            return reacted
        return reacted

    def AdjustLevel(events, dpg):
        visibleEvents = 0 
        accumulatedAccuracy = 0
        averageAccuracy = 0
        if dpg.get_value("adaptiveDif") == True:
            for event in events:
                if event.eventType != "P":
                    visibleEvents += 1
                    accumulatedAccuracy += event.percentTimeOnTarget
            averageAccuracy = accumulatedAccuracy / visibleEvents

            if averageAccuracy >= dpg.get_value("addaptiveDifThreshold"):
                dpg.configure_item("playerLevel", default_value = dpg.get_value("playerLevel") + 1)
            else:
                dpg.configure_item("playerLevel", default_value = dpg.get_value("playerLevel") - 1)          

    def EndOfEvent(dpg, inputs, events, gameTimeCounter, eventIndex, collisionDetected, eventVisibleTime, gameOver, reacted, eventTriggerSend):
        events[eventIndex].timeOffTarget = events[eventIndex].targetTotalTime - events[eventIndex].timeOnTarget
        events[eventIndex].percentTimeOnTarget = events[eventIndex].timeOnTarget / (events[eventIndex].targetTotalTime / 100)
        if collisionDetected == True:
            
            events[eventIndex].targetExitTime = gameTimeCounter
            collisionDetected = False

        eventIndex += 1
        eventVisibleTime = 0

        if (inputMode == "USB/ADAM" or inputMode == "NIDAQ") and eventIndex < len(events)-1:
            TriggerSender.send_trigger(events[eventIndex].targetTrigger)
        if biosemi == True and eventIndex < len(events)-1:
            SerialBoardAPI.SendTrigger(bioSerialObj, events[eventIndex].targetTrigger)

        if eventIndex == len(events):
            AdjustLevel(events, dpg)
            events = statistics.CalculateInaccuracyAndStd(events)
            events = statistics.CalculateOverAndUndershoot(events, forceDirection)
            meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets  = statistics.CalculateDescriptiveStastics(events)
            SaveFiles.SaveDataToFile(events, inputs.inputdatas, meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets, gameTimeCounter, dpg)# Some data extraction senanegans 
            if(dpg.get_value("visScore") == True):
                name = str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) + 'No_Targets_' + str(len(events))
                highRep.UpdateHighScore(name, score)
            gameOver = True
        else:
            events[eventIndex].targetVisibleFromTime = gameTimeCounter
            reacted = False
            eventTriggerSend = False
            meanAccuracy = 0
            meanTimeOnTarget = 0 
        
        return eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex, meanAccuracy, meanTimeOnTarget


    while not gameOver:


        if(gameStarted == True):
            #resets image
            gameTimeCounter += clock.get_time()
            gameDisplay.fill(bl)

            if(dpg.get_value("visScore") == True):
                scoretext = font.render('Score : ' + str(score), True, w )
                gameDisplay.blit(scoretext, score_rect)

            if(dpg.get_value("levels") == True):
                leveltext = font.render('Level : ' + str(level), True, w )
                gameDisplay.blit(leveltext, level_rect)

            if(dpg.get_value("guidelines") == True):
                gameDisplay.blit(guidelineText, guideTextRect)

            if eventIndex == 0 and firstEvent == True:
                firstEvent = False

                if inputMode == "USB/ADAM" or inputMode == "NIDAQ":
                    TriggerSender.send_trigger(events[eventIndex].targetTrigger)
                if biosemi == True:
                    SerialBoardAPI.SendTrigger(bioSerialObj, events[eventIndex].targetTrigger)

                events[eventIndex].targetVisibleFromTime = gameTimeCounter

            if events[eventIndex].eventType == "R" or events[eventIndex].eventType == "B": #create rect based on current Event
                    pygame.draw.rect(gameDisplay, eval(events[eventIndex].eventColor),[0, events[eventIndex].targetPosition, GetSystemMetrics(0), events[eventIndex].targetHeight],rectBorderWidth)

            if eventTriggerSend == False:
                #send event trigger 
                events[eventIndex].targetTrigger
                eventTriggerSend = True

            voltage,ypos = inRep.InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader, smoothingFilter, pushPull)

            drawPlayer(ypos,r)

            tempInput = InputData.InputData(voltage,ypos,gameTimeCounter)
            inputs.AddInputData(tempInput)

            events[eventIndex].inputDuringEvent.AddInputData(tempInput)
            
            collisionDetected, events[eventIndex] = CollisionDetection(events[eventIndex], tempInput.screenPosY, collisionDetected)
            events[eventIndex], score = OverlapDetection(events[eventIndex], tempInput.screenPosY, collisionDetected, dpg, score)
            collisionDetected, events[eventIndex] = ExitDetection(events[eventIndex], tempInput.screenPosY, collisionDetected)
            
            reacted = CalculateReactionTime(events[eventIndex], tempPos, tempInput.screenPosY, reacted)
            tempPos = tempInput.screenPosY

            if useSustain == False:
                eventVisibleTime += clock.get_time()
                if eventVisibleTime >= events[eventIndex].targetTotalTime:
                    imgAlpha = 255 
                    playsound = True
                    eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex, meanAccuracy, meanTimeOnTarget = EndOfEvent(dpg, inputs, events, gameTimeCounter, eventIndex, collisionDetected, eventVisibleTime, gameOver, reacted, eventTriggerSend)
                    coinpos = events[eventIndex-1].targetPosition

            elif useSustain == True:
                eventVisibleTime += clock.get_time()
                
                if events[eventIndex].eventType == "P":
                    events[eventIndex].timeOnTarget += clock.get_time()

                if events[eventIndex].timeOnTarget >= minSustainTime:
                    imgAlpha = 255 
                    playsound = True
                    events[eventIndex].targetTotalTime = eventVisibleTime    
                     
                    eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex, meanAccuracy, meanTimeOnTarget = EndOfEvent(dpg, inputs, events, gameTimeCounter, eventIndex, collisionDetected, eventVisibleTime, gameOver, reacted, eventTriggerSend) 

            if events[eventIndex-1].percentTimeOnTarget > 60 and coinEnabled :
                coinpos -= 3 
                imgAlpha -= 4
                if imgWidth > 1 and towardsMinus:
                    imgWidth -= 2
                elif imgWidth <= 1 and towardsMinus:
                    towardsMinus = False 
                elif imgWidth < 50 and towardsMinus == False:
                    imgWidth += 2
                elif imgWidth >= 50 and towardsMinus == False:
                    towardsMinus = True
                
                coinImg.set_alpha(imgAlpha)

                rotatingCoin = pygame.transform.scale(coinImg,(imgWidth,coinImg.get_height()))

                coinRect.center = (GetSystemMetrics(0)// 2, coinpos)
                gameDisplay.blit(rotatingCoin, coinRect)

                if SoundEnabled and playsound:
                    playsound = False
                    randSound = random.randint(0,4)
                    if randSound == 0:
                        pygame.mixer.Sound.play(plingSound1)
                    elif randSound == 1:
                        pygame.mixer.Sound.play(plingSound2)
                    elif randSound == 2:
                        pygame.mixer.Sound.play(plingSound3)
                    elif randSound == 3:
                        pygame.mixer.Sound.play(plingSound4)
                    elif randSound == 4:
                        pygame.mixer.Sound.play(plingSound5)

        elif countdownStarted == True:
            countDownCounter += clock.get_time() 
            gameDisplay.fill(bl)
            if(countDownCounter < 1000):
                gameDisplay.blit(text_3, text_3_Rect)
            elif(countDownCounter < 2000):
                gameDisplay.blit(text_2, text_2_Rect)
            elif(countDownCounter < 3000):
                gameDisplay.blit(text_1, text_1_Rect)
            elif countDownCounter < 4000:
                countdownStarted = False
                gameStarted = True
        else:
            gameDisplay.blit(introText, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                smoothingFilter.ResetFilter()
                SerialBoardAPI.CloseCommunication(serialObj)
                SerialBoardAPI.CloseCommunication(bioSerialObj)
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    smoothingFilter.ResetFilter()
                    SerialBoardAPI.CloseCommunication(serialObj)
                    SerialBoardAPI.CloseCommunication(bioSerialObj)
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    countdownStarted = True

        pygame.display.update()
        clock.tick(120)
    
    while not endOfFeedback:
        gameDisplay.fill(bl)
        meanAccuracy = round(meanAccuracy)
        meanTimeOnTarget = round(meanTimeOnTarget)
        feedbackAcc = font.render('Average accuracy : ' + str(meanAccuracy) + '%', True, w)
        feedbackTime = font.render('Average Time on Target : ' + str(meanTimeOnTarget) + ' ms out of ' + str(dpg.get_value("stimDisplayTime")) + ' ms' , True, w)
        feedbackTimer += clock.get_time() - clockEndOfGame
        if feedbackTimer < feedbackLength:
            gameDisplay.blit(feedbackAcc, feedbackAccRect)
            gameDisplay.blit(feedbackTime, feedbackTimeRect)
        else:
            endOfFeedback = True
        pygame.display.update()
        clock.tick(120)

    smoothingFilter.ResetFilter()
    SerialBoardAPI.CloseCommunication(serialObj)
    SerialBoardAPI.CloseCommunication(bioSerialObj)
    pygame.quit()
