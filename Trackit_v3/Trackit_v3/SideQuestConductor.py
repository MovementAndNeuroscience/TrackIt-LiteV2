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
import random
import HighscoreRepository as highRep

def RunGame(dpg, sideQBlock, smoothingFilter):
    
#SETUP THE GAME
    pygame.init()
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Track-it V3 Side Quest')

    inputMode = dpg.get_value("device")
    forceDirection = dpg.get_value("forceDirection")
    maxVoltage = dpg.get_value("maxVoltage")
    minVoltage = dpg.get_value("minVoltage")
    neutralVal = dpg.get_value("neutralNIDAQval")
    percentageOfMaxVoltage = dpg.get_value("percentOfMaxCal")
    absOrRelvoltage = dpg.get_value("absOrRelVoltage")
    absoluteMaxVoltage = dpg.get_value("absMaxVoltage")
    feedbackLength = dpg.get_value("feedbackLength")
    comport = dpg.get_value("comport")
    bioComport = dpg.get_value("biosemiComport")
    biosemi = dpg.get_value("Biosemi")
    experimentalMode = dpg.get_value("experimentMode")
    level = dpg.get_value("playerLevel")
    coinEnabled = dpg.get_value("coinRew")
    SoundEnabled = dpg.get_value("soundRew")
    pushPull = dpg.get_value("pushPull")
    trialTime = dpg.get_value("sideQuestTrialTime")
    trialTime = trialTime*1000
    stabilizationTime = dpg.get_value("sideQuestStabiTime")
    linearLog = dpg.get_value("linearLog")


    serialObj = serial.Serial()
    bioSerialObj = serial.Serial() 
    inputs = InputDatas.InputDatas()
    trials = sideQBlock.trials

    nidaqCh = dpg.get_value("nidaqCh")
    reader = 0
    rectBorderWidth = 4

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
    gameOver = False
    feedbackStarted = False
    gameStarted = False
    countdownStarted = False
    eventTriggerSend = False
    collisionDetected = False
    trialStartTime = 0
    firstEvent = True
    firstGateEnabled = False
    gameTimeCounter = 0
    feedbackCounter = 0
    trialIndex = 0
    eventManager = 0
    eventVisibleTime = 0 
    tempPos = 0
    reacted = False 
    beginning = True
    setupConnection = True
    setupBioConnection = True
    score = 0
    coinAndSoundEnabled = False
    startOfTrialTrigger = True
    endOfTrialTrigger = False
    timeTrialintervalReacher = 0 
    visitedEvents = []
    visitedEvents.append(eventManager)

    breakBetweenGatesTimeMs = dpg.get_value("sideQBreak")
    millisecondSegments = GetSystemMetrics(0) / trialTime
    stabilisatorLength = millisecondSegments * (stabilizationTime*1000)
    breakBetweenGatesLength = millisecondSegments * breakBetweenGatesTimeMs; 
    gatesLength = (GetSystemMetrics(0)-(stabilisatorLength + (breakBetweenGatesLength * dpg.get_value("noSideEvents"))))/dpg.get_value("noSideEvents")

    coinImg = None
    coinRect = None
    imgAlpha = 255
    coinpos = GetSystemMetrics(1) // 2
    imgWidth = 0
    towardsMinus = True
    plingSound1 = None
    plingSound2 = None
    plingSound3 = None
    plingSound4 = None
    plingSound5 = None
    playsound = True


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
            
    if biosemi == True and  setupBioConnection == True:
        bioSerialObj = SerialBoardAPI.SetupSerialCommuniation(bioComport)
        SerialBoardAPI.OpenCommunication(bioSerialObj)
        setupBioConnection == False
        

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start TrackIt', True, w)
    stopFeedbackText = font.render('Stop', True, w)
    compTimeFeedbackText = font.render('74.0 Mean Accuracy in %', True, w)
    contienueText = font.render('Press Return to continue', True, w)
    guidelineText = font.render("Hit the squares as accurate as possible", True, w)
    rectNoTExt = font.render("1", True, r)

    textRect = introText.get_rect()
    stopFeedRect = stopFeedbackText.get_rect()
    compTimeFeedbackTextRect = compTimeFeedbackText.get_rect()
    continueTextRect =contienueText.get_rect()
    guideTextRect = guidelineText.get_rect()
    rectNoTextRect =  rectNoTExt.get_rect()
    middleTextPos = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    textRect.center = middleTextPos
    sfRX, sfRY = stopFeedRect.size
    stopFeedRect.x = GetSystemMetrics(0) // 2 - (sfRX/2)
    stopFeedRect.y = GetSystemMetrics(1) // 2 - 75
    cftRX, cftRY = compTimeFeedbackTextRect.size
    compTimeFeedbackTextRect.x = GetSystemMetrics(0) // 2 - (cftRX/2)
    compTimeFeedbackTextRect.y = GetSystemMetrics(1) // 2 
    ctRX, ctRY = continueTextRect.size; 
    continueTextRect.x = GetSystemMetrics(0) // 2 - (ctRX/2)
    continueTextRect.y = GetSystemMetrics(1) // 2 + 75
    
    
    if forceDirection == "Upwards":
        for trial in trials:
            for event in trial.events:
                rectPos = 0
                if event.eventType == 'R':
                    rectPos = GetSystemMetrics(1) - event.targetPosition
                    if rectPos < 0:
                        rectPos = 10
                elif event.eventType == 'B' or event.eventType == 'P':
                    rectPos = (GetSystemMetrics(1)-  event.targetHeight  ) - event.targetPosition
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
        coinRect.center = (GetSystemMetrics(0)// 2, 500)
        coinImg.set_alpha(imgAlpha) 
        imgWidth = coinImg.get_width()
    
    if SoundEnabled:
        plingSound1 = pygame.mixer.Sound("Assets\sounds\pling_1.wav")
        plingSound2 = pygame.mixer.Sound("Assets\sounds\pling_2.wav")
        plingSound3 = pygame.mixer.Sound("Assets\sounds\pling_3.wav")
        plingSound4 = pygame.mixer.Sound("Assets\sounds\pling_4.wav")
        plingSound5 = pygame.mixer.Sound("Assets\sounds\pling_5.wav")

    clock = pygame.time.Clock()

    def drawPlayer(xpos, ypos, color):
        pygame.draw.circle(gameDisplay, color, (xpos, ypos), 8) 

    def CollisionDetection(event, ypos, xpos, collisionDetected):
        if ypos < event.targetHeight + event.targetPosition and ypos > event.targetPosition:
            if xpos < event.targetXPosition + event.targetLength-1 and xpos > event.targetXPosition:
                if collisionDetected == False:
                    collisionDetected = True
                    event.targetEntryTime = gameTimeCounter
                    return collisionDetected, event
        return collisionDetected, event
            
    def OverlapDetection(event, ypos, collisionDetected, score):
        if collisionDetected == True:
            score += 1
            event.timeOnTarget += clock.get_time()
        return event, score

    def ExitDetection(event, ypos, xpos, collisionDetected):
        if (xpos > event.targetXPosition and ypos > event.targetHeight + event.targetPosition):
            if collisionDetected == True and event.targetEntryTime != 0.0:
                collisionDetected = False
                event.targetExitTime = gameTimeCounter 
                return collisionDetected, event
        elif ( xpos > event.targetXPosition and ypos < event.targetPosition):
            if collisionDetected == True and event.targetEntryTime != 0.0:
                collisionDetected = False
                event.targetExitTime = gameTimeCounter
                return collisionDetected, event
        elif xpos > event.targetXPosition + event.targetLength-1:
            if collisionDetected == True and event.targetEntryTime != 0.0:
                collisionDetected = False
                event.targetExitTime = gameTimeCounter
                return collisionDetected, event
        return collisionDetected, event

    def CalculateReactionTime(event, OldPosY, newPosY, reacted):
        if reacted == False and (abs(OldPosY-newPosY) < 100 and abs(OldPosY-newPosY) > 3):
            event.reactionTime = gameTimeCounter
            reacted = True
            return reacted
        return reacted
    
    def CheckAndSetExitTime(event, collisionDetected):
        if(event.targetExitTime == 0.0 and event.targetEntryTime != 0.0):
            event.targetExitTime = gameTimeCounter
            collisionDetected = False
        elif(collisionDetected == True and event.targetEntryTime != 0.0):
            collisionDetected = False
            event.targetExitTime = gameTimeCounter
        
        return event, collisionDetected
    
    def EndOfATrial(trial, score, coinAndSoundEnabled):
        trials[trialIndex].completionTime = (gameTimeCounter - trialStartTime)/1000
        trial.events = statistics.CalculateInaccuracyAndStd(trial.events)
        trial.events = statistics.CalculateOverAndUndershoot(trial.events, forceDirection)
        
        for event in trial.events:
            event.timeOffTarget = (event.targetLength/millisecondSegments)- event.timeOnTarget
            if (event.timeOffTarget < 0.0):
                event.timeOffTarget = 0.0
            event.percentTimeOnTarget = event.timeOnTarget / ((event.targetLength/millisecondSegments) / 100)
            if event.percentTimeOnTarget > 100 :
                event.percentTimeOnTarget = 100

            if event.overshoot == True or event.undershoot == True:
                trial.error += 1 
            elif event.overshoot == False and event.undershoot == False:
                score += 100
                coinAndSoundEnabled = True
        
        trial.meanAccuracy, trial.stdAccuracy, trial.meanTimeOnTarget, trial.stdTimeOnTarget, trial.totalTimeOnTargets  = statistics.CalculateDescriptiveStasticsSideQuest(trial.events)

        return trial, score, coinAndSoundEnabled

    def EndOfABlock(dpg, trials, inputs):
        SaveFiles.SaveSideQuestDataToFiles(dpg, trials, inputs)
        if(dpg.get_value("visScore") == True):
                name = str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) + '_SideQuest_' + str(len(trials))
                highRep.UpdateHighScore(name, score)

    def PlayPlingSound(plingSound1, plingSound2, plingSound3, plingSound4, plingSound5):
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

        return playsound
    
    def PlayPlingSound(plingSound):
        playsound = False
        pygame.mixer.Sound.play(plingSound)
        return playsound
    
    def DetectTheCurrentTarget(event):
        event.eventColor = "g"
        return event


#RUN THE GAME 
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

            if trialIndex == 0 and firstEvent == True:
                trialStartTime = gameTimeCounter
                firstEvent = False

                trials[trialIndex].events[0].targetVisibleFromTime = gameTimeCounter

            if startOfTrialTrigger == True:
                if biosemi == True:
                    SerialBoardAPI.SendTrigger(bioSerialObj, 1)
                    
                if inputMode == "USB/ADAM" or inputMode == "NIDAQ":
                    TriggerSender.send_trigger(1)
                    
                startOfTrialTrigger = False



            trials[trialIndex].events[eventManager] = DetectTheCurrentTarget(trials[trialIndex].events[eventManager])

            gateCounter = 0 
            gateHeight = 50
            for event in trials[trialIndex].events:
                if event.eventType == "R" or event.eventType == "B": #create rect based on current Event
                    if (gateCounter == 0):
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[0, event.targetPosition, event.targetLength, event.targetHeight],rectBorderWidth)
                    elif (gateCounter == 1):
                        event.targetXPosition = stabilisatorLength + breakBetweenGatesLength 
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[event.targetXPosition, event.targetPosition, event.targetLength, event.targetHeight],rectBorderWidth)
                    elif (gateCounter < 11):
                        event.targetXPosition = stabilisatorLength + (breakBetweenGatesLength*gateCounter) + (gatesLength * (gateCounter-1))
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[event.targetXPosition, event.targetPosition, event.targetLength, event.targetHeight],rectBorderWidth)
                        gateHeight = event.targetHeight
                    else : 
                        event.targetHeight = gateHeight
                        event.targetXPosition = stabilisatorLength + (breakBetweenGatesLength*gateCounter) + (gatesLength * (gateCounter-1))
                        pygame.draw.rect(gameDisplay, eval(event.eventColor),[event.targetXPosition, event.targetPosition, event.targetLength, event.targetHeight],rectBorderWidth)
                    gateCounter = gateCounter + 1

            if eventTriggerSend == False:
                #send event trigger 
                #events[eventIndex].targetTrigger
                eventTriggerSend = True

            voltage, ypos = inRep.InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader, smoothingFilter, pushPull, linearLog, neutralVal)

            if ((gameTimeCounter - trialStartTime) < (trialTime)):
                xpos =  GetSystemMetrics(0) * (( gameTimeCounter - trialStartTime)/(trialTime))
                drawPlayer(xpos,ypos,r)

            if(xpos < stabilisatorLength):
                eventManager = 0
            elif((xpos > stabilisatorLength) and (xpos < stabilisatorLength + breakBetweenGatesLength + gatesLength) and firstGateEnabled == False):
                trials[trialIndex].events[eventManager], collisionDetected = CheckAndSetExitTime(trials[trialIndex].events[eventManager], collisionDetected)
                eventManager = 1
                reacted = False
                firstGateEnabled = True
            elif((xpos > stabilisatorLength + breakBetweenGatesLength*eventManager + gatesLength*eventManager) and (xpos < stabilisatorLength + breakBetweenGatesLength*(eventManager+1) + gatesLength*(eventManager+1))):
                trials[trialIndex].events[eventManager], collisionDetected = CheckAndSetExitTime(trials[trialIndex].events[eventManager], collisionDetected)
                eventManager = eventManager +1
                reacted = False

                


            tempInput = InputData.InputData(voltage,ypos,gameTimeCounter)
            inputs.AddInputData(tempInput)

            trials[trialIndex].events[eventManager].inputDuringEvent.AddInputData(tempInput)
            trials[trialIndex].events[eventManager].inputXDuringEvent.append(xpos)
            collisionDetected, trials[trialIndex].events[eventManager] = CollisionDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, xpos , collisionDetected)
            trials[trialIndex].events[eventManager], score = OverlapDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, collisionDetected, score)
            collisionDetected, trials[trialIndex].events[eventManager] = ExitDetection(trials[trialIndex].events[eventManager], tempInput.screenPosY, xpos,collisionDetected)
            
            reacted = CalculateReactionTime(trials[trialIndex].events[eventManager], tempPos, tempInput.screenPosY, reacted)
            tempPos = tempInput.screenPosY
            
            if ((gameTimeCounter - trialStartTime) > trialTime):
                    trials[trialIndex].events[eventManager], collisionDetected = CheckAndSetExitTime(trials[trialIndex].events[eventManager], collisionDetected)
                    ## we need to change some things here. Here we need to wrap up the trial. 
                    index = 1 
                    tempTimeOntarget = 100

                    while tempTimeOntarget > 0:
                        index += 1 
                        if index < len(trials[trialIndex].events):
                            tempTimeOntarget = trials[trialIndex].events[index].timeOnTarget
                            if tempTimeOntarget == 0:
                                tempTimeOntarget = 1
                        else:
                            trials[trialIndex], score, coinAndSoundEnabled = EndOfATrial(trials[trialIndex], score, coinAndSoundEnabled)
                            trialIndex += 1
                            feedbackStarted = True
                            gameStarted = False
                            #End Of Trial Trigger
                            if biosemi == True:
                                SerialBoardAPI.SendTrigger(bioSerialObj, 2)
                            if inputMode == "USB/ADAM" or inputMode == "NIDAQ":
                                TriggerSender.send_trigger(2)
                            startOfTrialTrigger = True

                            if trialIndex >= len(trials):
                                inputs.inputdatas
                                feedbackStarted = True
                                gameStarted = False
                                tempTimeOntarget = 0
                            else :
                                tempTimeOntarget = 0
                    visitedEvents.append(index)
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
            gameDisplay.fill(bl)
            
            if coinAndSoundEnabled and coinEnabled:
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
                    playsound = PlayPlingSound(plingSound1, plingSound2, plingSound3, plingSound4, plingSound5)    

            feedbackCounter += clock.get_time() 
            prevTrial = trialIndex - 1
            stopFeedbackText = font.render("Stop", True, w)
            compTimeFeedbackText =  font.render(str(np.round(trials[prevTrial].meanAccuracy)) + " Mean Accuracy in %", True, w)
            contienueText = font.render("Press Return to continue" , True, w )

            gameDisplay.blit(stopFeedbackText, stopFeedRect)
            gameDisplay.blit(compTimeFeedbackText, compTimeFeedbackTextRect)
            gameDisplay.blit(contienueText, continueTextRect)

        else:
            gameDisplay.blit(introText, textRect)    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                smoothingFilter.ResetFilter()
                if inputMode == "USB/ADAM":
                    SerialBoardAPI.CloseCommunication(serialObj)
                if biosemi == True:
                    SerialBoardAPI.CloseCommunication(bioSerialObj)
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    smoothingFilter.ResetFilter()
                    if inputMode == "USB/ADAM":
                        SerialBoardAPI.CloseCommunication(serialObj)
                    if biosemi == True:
                        SerialBoardAPI.CloseCommunication(bioSerialObj)
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    if beginning == True:
                        countdownStarted = True
                        beginning = False
                    if feedbackStarted:
                        if trialIndex >= len(trials):
                            trials[prevTrial].timeBetweenTrials = feedbackCounter
                            EndOfABlock(dpg, trials, inputs.inputdatas)
                            feedbackCounter = 0 
                            eventManager = 1
                            feedbackStarted = False
                            gameOver = True 
                            
                        else :
                            coinpos = GetSystemMetrics(1) // 2
                            eventManager = 1
                            trials[prevTrial].timeBetweenTrials = feedbackCounter
                            feedbackStarted = False
                            coinAndSoundEnabled = False
                            imgAlpha = 255 
                            playsound = True
                            gameTimeCounter = 0
                            countdownStarted = True                
                            countDownCounter = 0
                            feedbackCounter = 0 
                            eventTriggerSend = False
                            reacted = False 


                        


        pygame.display.update()
        clock.tick(120)

    smoothingFilter.ResetFilter()
    if inputMode == "USB/ADAM":
        SerialBoardAPI.CloseCommunication(serialObj)
    if biosemi == True:
        SerialBoardAPI.CloseCommunication(bioSerialObj)
    pygame.quit()
        