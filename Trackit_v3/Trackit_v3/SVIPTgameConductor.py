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
    feedbackLength = dpg.get_value("feedbackLength")
    comport = dpg.get_value("comport")
    experimentalMode = dpg.get_value("experimentMode")

    serialObj = serial.Serial() 
    inputs = InputDatas.InputDatas()
    trials = sviptBlock.trials

    print ("Trials " + str(len(trials)))

    nidaqCh = dpg.get_value("nidaqCh")
    reader = 0

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
    feedbackStarted = False
    gameStarted = False
    countdownStarted = False
    eventTriggerSend = False
    collisionDetected = False
    trialStartTime = 0
    firstEvent = True
    gameTimeCounter = 0
    feedbackCounter = 0
    trialIndex = 0
    eventManager = 1
    eventVisibleTime = 0 
    tempPos = 0
    reacted = False 
    beginning = True
    setupConnection = True


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
    introText = font.render('Press Return to Start TrackIt', True, w)
    stopFeedbackText = font.render('Stop', True, w)
    compTimeFeedbackText = font.render('Din samlede Tid', True, w)
    errorFeedbackText = font.render('Du skød', True, w)
    guidelineText = font.render("Hit the squares as fast and accurate as possible", True, w)
    rectNoTExt = font.render("1", True, r)

    textRect = introText.get_rect()
    stopFeedRect = stopFeedbackText.get_rect()
    compTimeFeedbackTextRect = compTimeFeedbackText.get_rect()
    errorFeedbackTextRect = errorFeedbackText.get_rect()
    guideTextRect = guidelineText.get_rect()
    rectNoTextRect =  rectNoTExt.get_rect()
    middleTextPos = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    textRect.center = middleTextPos
    stopFeedRect.x = GetSystemMetrics(0) // 2
    stopFeedRect.y = GetSystemMetrics(1) // 2
    compTimeFeedbackTextRect.x = GetSystemMetrics(0) // 2 - 200
    compTimeFeedbackTextRect.y = GetSystemMetrics(1) // 2 + 50
    errorFeedbackTextRect.x = GetSystemMetrics(0) // 2 - 200
    errorFeedbackTextRect.y = GetSystemMetrics(1) // 2 + 100
    
    if forceDirection == "Upwards":
        for trial in trials:
            for event in trial.events:
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
    
    def EndOfATrial(trial):
        trials[trialIndex].completionTime = gameTimeCounter - trialStartTime
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
                trialStartTime = gameTimeCounter
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
                        rectNoTextRect.center = (GetSystemMetrics(0)/2 + 100 ,event.targetPosition + event.targetHeight/2)
                        gameDisplay.blit(rectNoTExt, rectNoTextRect)
                    else : 
                        event.eventColor = "r"
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[0, event.targetPosition, GetSystemMetrics(0), event.targetHeight],1)
                        rectNoTExt = font.render(str(event.targetId), True, eval(event.eventColor))
                        rectNoTextRect.center = (GetSystemMetrics(0)/2 + 200,event.targetPosition + event.targetHeight/2)
                        gameDisplay.blit(rectNoTExt, rectNoTextRect)

                    eventToBeGenerated += 1
                    

            if eventTriggerSend == False:
                #send event trigger 
                #events[eventIndex].targetTrigger
                eventTriggerSend = True

            voltage, ypos = inRep.InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader)

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
                            feedbackStarted = True
                            gameStarted = False
                            if trialIndex >= len(trials):
                                EndOfABlock(dpg, trials, inputs.inputdatas)
                                inputs.inputdatas
                                feedbackStarted = True
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
                trialStartTime = gameTimeCounter
        
        elif feedbackStarted == True:
            if feedbackCounter < feedbackLength:
                feedbackCounter += clock.get_time() 
                prevTrial = trialIndex - 1
                comparedToTrial = prevTrial - 1
                if prevTrial == 0 :
                    stopFeedbackText = font.render("Stop", True, w)
                    compTimeFeedbackText =  font.render("Din totale tid var : " + str(trials[prevTrial].completionTime /1000) + " s", True, w)
                    errorFeedbackText = font.render("Du skød " + str(trials[prevTrial].error) + " gange forbi målet", True, w )
                    
                else:
                    compTimeFeedbackTextRect.x = GetSystemMetrics(0) // 2 - 500
                    difCompletionTime = (trials[prevTrial].completionTime - trials[comparedToTrial].completionTime)/1000
                    difErrors = trials[prevTrial].error - trials[comparedToTrial].error
                    if difCompletionTime < 0.00 :
                        if difErrors < 0 : 
                            stopFeedbackText = font.render("Stop", True, w)
                            compTimeFeedbackText =  font.render("Du klarede banen " + str(abs(difCompletionTime)) + " s langsommere end sidste omgang", True, w)
                            errorFeedbackText = font.render("Du skød " + str(abs(difErrors)) + " flere gange forbi", True, w )
                        else:
                            stopFeedbackText = font.render("Stop", True, w)
                            compTimeFeedbackText =  font.render("Du klarede banen " + str(abs(difCompletionTime)) + " s langsommere end sidste omgang", True, w)
                            errorFeedbackText = font.render("Du skød " + str(abs(difErrors)) + " færre gange forbi", True, w )
                    else:
                        if difErrors < 0 : 
                            stopFeedbackText = font.render("Stop", True, w)
                            compTimeFeedbackText =  font.render("Du klarede banen " + str(abs(difCompletionTime)) + " s hurtigere end sidste omgang", True, w)
                            errorFeedbackText = font.render("Du skød " + str(abs(difErrors)) + " flere gange forbi", True, w )
                        else:
                            stopFeedbackText = font.render("Stop", True, w)
                            compTimeFeedbackText =  font.render("Du klarede banen " + str(abs(difCompletionTime)) + " s hurtigere end sidste omgang", True, w)
                            errorFeedbackText = font.render("Du skød " + str(abs(difErrors)) + " færre gange forbi", True, w )

                gameDisplay.fill(bl)
                gameDisplay.blit(stopFeedbackText, stopFeedRect)
                gameDisplay.blit(compTimeFeedbackText, compTimeFeedbackTextRect)
                gameDisplay.blit(errorFeedbackText, errorFeedbackTextRect)
            else: 
                if trialIndex >= len(trials):
                    eventManager = 1
                    feedbackStarted = False
                    gameOver = True 
                else :
                    eventManager = 1
                    feedbackStarted = False
                    countdownStarted = True                
                    countDownCounter = 0
                    feedbackCounter = 0 
                    eventTriggerSend = False
                    reacted = False 
        
        else:
            gameDisplay.blit(introText, textRect)    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    if beginning == True:
                        countdownStarted = True
                        beginning = False
                        


        pygame.display.update()
        clock.tick(120)

    pygame.quit()