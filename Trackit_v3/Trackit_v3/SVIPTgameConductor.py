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

def RunGame(dpg, sviptBlock):
    
#SETUP THE GAME
    pygame.init()
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Track-it V3 SVIPT')

    inputMode = dpg.get_value("device")
    forceDirection = dpg.get_value("forceDirection")
    maxVoltage = dpg.get_value("maxVoltage")
    minVoltage = dpg.get_value("minVoltage")
    percentageOfMaxVoltage = dpg.get_value("percentOfMaxCal")
    absOrRelvoltage = dpg.get_value("absOrRelVoltage")
    absoluteMaxVoltage = dpg.get_value("absMaxVoltage")

    inputs = InputDatas.InputDatas()
    trials = sviptBlock.trials

    print ("Trials " + str(len(trials)))

    nidaqCh = dpg.get_value("nidaqCh")
    reader = 0
    if inputMode == "NIDAQ":
        reader = daqmxlib.Reader({nidaqCh:1})

    bl = (0,0,0)
    f = (0,0,0)
    w = (255,255,255)
    r = (255,0,0)
    g = (0,255,0)
    b = (0,0,255)
    y = (255, 255, 0)  # yellow
    v = (148, 0, 211)  # violet
    c = (0, 255, 255)  # cyan
    p = (255, 20, 147)  # pink
    o = (255,140,0) # orange
    gameOver = False
    stopstarted = False
    gameStarted = False
    countdownStarted = False
    eventTriggerSend = False
    collisionDetected = False
    firstEvent = True
    gameTimeCounter = 0
    trialIndex = 0
    eventManager = 1
    eventVisibleTime = 0 
    tempPos = 0
    reacted = False 
        

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start TrackIt', True, w)
    stopText = font.render('Stop press enter to continue next trial', True, w)
    guidelineText = font.render("Hit the squares as fast and accurate as possible", True, w)
    rectNoTExt = font.render("1", True, r)

    textRect = introText.get_rect()
    stopRect = stopText.get_rect()
    guideTextRect = guidelineText.get_rect()
    rectNoTextRect =  rectNoTExt.get_rect()
    middleTextPos = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    textRect.center = middleTextPos
    stopRect.center = middleTextPos
    

    #CountDown 
    text_1 = font.render('1', True, w)
    text_2 = font.render('2', True, w)
    text_3 = font.render('3', True, w)
    go_text = font.render('GO', True, w)
    text_1_Rect = text_1.get_rect()
    text_2_Rect = text_2.get_rect()
    text_3_Rect = text_3.get_rect()
    go_text_Rect = go_text.get_rect()
    text_1_Rect.center = middleTextPos
    text_2_Rect.center = middleTextPos
    text_3_Rect.center = middleTextPos
    go_text_Rect.center = middleTextPos
    countDownCounter = 0 

    clock = pygame.time.Clock()

    def drawPlayer(ypos, color):
        pygame.draw.circle(gameDisplay, color, (GetSystemMetrics(0)/2, ypos), 5)

    def CollisionDetection(event, ypos, collisionDetected):
        if (ypos < event.targetHeight + event.targetPosition) and ypos > event.targetPosition and collisionDetected == False:
            collisionDetected = True
            event.targetEntryTime = gameTimeCounter
            return collisionDetected, event
        return collisionDetected, event
            
    def OverlapDetection(event, ypos, collisionDetected):
        if collisionDetected == True:
            event.timeOnTarget += clock.get_time()
            drawPlayer(ypos, g)
        return event

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
    
    def EndOfATrial(trial):
        trials[trialIndex].completionTime = gameTimeCounter
        trial.events = statistics.CalculateOverAndUndershoot(trial.events)
        for event in trial.events:
            if event.overshoot == True or event.undershoot == True:
                trial.error += 1 
        return trial

    def EndOfABlock(dpg, trials, inputs):
        SaveFiles.SaveSviptDataToFiles(dpg, trials, inputs)

#RUN THE GAME 
    while not gameOver:
        if(gameStarted == True):
            #resets image
            gameTimeCounter += clock.get_time()
            gameDisplay.fill(bl)

            if trialIndex == 0 and firstEvent == True:
                firstEvent = False

                if inputMode == "USB/ADAM" or inputMode == "NIDAQ":
                    TriggerSender.send_trigger(trials[trialIndex].events[1].targetTrigger)

                trials[trialIndex].events[1].targetVisibleFromTime = gameTimeCounter
                
            eventToBeGenerated = 0 
            for event in trials[trialIndex].events:
                if event.eventType == "R" or event.eventType == "B": #create rect based on current Event
                    if eventToBeGenerated == eventManager:
                        event.eventColor = "g"
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[0, event.targetPosition, GetSystemMetrics(0), event.targetHeight],1)
                        rectNoTExt = font.render(str(event.targetId), True, eval(event.eventColor))
                        rectNoTextRect.center = (GetSystemMetrics(0) - 500 ,event.targetPosition + 50)
                        gameDisplay.blit(rectNoTExt, rectNoTextRect)
                    else : 
                        event.eventColor = "r"
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[0, event.targetPosition, GetSystemMetrics(0), event.targetHeight],1)
                        rectNoTExt = font.render(str(event.targetId), True, eval(event.eventColor))
                        rectNoTextRect.center = (GetSystemMetrics(0) - 400 ,event.targetPosition + 50 )
                        gameDisplay.blit(rectNoTExt, rectNoTextRect)

                    eventToBeGenerated += 1
                    

            if eventTriggerSend == False:
                #send event trigger 
                #events[eventIndex].targetTrigger
                eventTriggerSend = True

            if inputMode == "Mouse":                    
                mx,my=pygame.mouse.get_pos()
                drawPlayer(my,r)
                tempInput = InputData.InputData(my,my,gameTimeCounter)
                inputs.AddInputData(tempInput)
                
            if inputMode == "USB/ADAM":
                voltage = 0
                ypos=0 #USB/ADAM input goes here 
                drawPlayer(ypos, r)
                tempInput = InputData.InputData(voltage,ypos,gameTimeCounter)
                inputs.AddInputData(tempInput)

            if inputMode == "NIDAQ":
                voltage = reader.read()[0]
                ypos = 0 
                if forceDirection == "Downwards":
                    if absOrRelvoltage == "Relative":
                        ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
                    if absOrRelvoltage == "Absolute":  
                        ypos=VoltageConverter.get_px_from_voltage(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)  
                if forceDirection == "Upwards":
                    if absOrRelvoltage == "Relative":
                        ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
                        ypos = GetSystemMetrics(1) - ypos
                    if absOrRelvoltage == "Absolute":  
                        ypos=VoltageConverter.get_px_from_voltage(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)
                        ypos = GetSystemMetrics(1) - ypos  

                drawPlayer(ypos,r)
                tempInput = InputData.InputData(voltage,ypos,gameTimeCounter)
                inputs.AddInputData(tempInput)

            trials[trialIndex].events[eventManager].inputDuringEvent.AddInputData(tempInput)
            
            collisionDetected, trials[trialIndex].events[eventManager] = CollisionDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, collisionDetected)
            trials[trialIndex].events[eventManager] = OverlapDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, collisionDetected)
            collisionDetected, trials[trialIndex].events[eventManager] = ExitDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, collisionDetected)
            
            reacted = CalculateReactionTime(trials[trialIndex].events[eventManager], tempPos, tempInput.screenPosY, reacted)
            tempPos = tempInput.screenPosY

            eventVisibleTime += clock.get_time()
            
            if trials[trialIndex].events[eventManager].timeOnTarget > 150:
                print("event manager : " + str(eventManager))
                if eventManager != 0:
                    eventManager = 0
                    trials[trialIndex].events[eventManager].timeOnTarget = 0
                else:
                    index = 1 
                    tempTimeOntarget = 100
                    while tempTimeOntarget > 0:
                        index += 1 
                        if index < len(trials[trialIndex].events):
                            tempTimeOntarget = trials[trialIndex].events[index].timeOnTarget
                            print("temptimeOnTarget : " + str(tempTimeOntarget))
                        else:
                            trials[trialIndex] = EndOfATrial(trials[trialIndex])
                            trialIndex += 1
                            stopstarted = True
                            gameStarted = False
                            if trialIndex >= len(trials):
                                EndOfABlock(dpg, trials, inputs.inputdatas)
                                inputs.inputdatas
                                gameOver = True 
                                tempTimeOntarget = 0
                            else :
                                print("next trial")
                                tempTimeOntarget = 0
                    eventManager = index




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
                gameDisplay.blit(go_text, go_text_Rect)
            elif countDownCounter < 5000:
                countdownStarted = False
                gameStarted = True
        
        elif stopstarted == True:
            gameDisplay.fill(bl)
            gameDisplay.blit(stopText, stopRect)  
        else:
            gameDisplay.blit(introText, textRect)    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    if stopstarted == True:
                        countdownStarted = True
                        countDownCounter = 0
                        stopstarted = False
                        eventTriggerSend = False
                        reacted = False 
                        eventManager = 1
                    else:
                        countdownStarted = True
                        


        pygame.display.update()
        clock.tick(120)

    pygame.quit()
    

#CONCLUDE THE GAME 