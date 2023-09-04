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
 
def RunGame(dpg, eventsData):

    pygame.init()
    #Setup calibration space and such 
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Track-it V3')
    
    inputs = InputDatas.InputDatas()
    events = eventsData.eventDatas
    nidaqCh = dpg.get_value("nidaqCh")
    reader = daqmxlib.Reader({nidaqCh:1})

    useSustain = dpg.get_value("TargetSustain")
    minSustainTime = dpg.get_value("sustainOnTarget")
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

    clock = pygame.time.Clock()
    inputMode = dpg.get_value("device")
    gameStarted = False
    gameOver = False
    gameTimeCounter = 0
    eventIndex = 0
    eventVisibleTime = 0 
    collisionDetected = False
    firstEvent = True
    reacted = False 
    eventTriggerSend = False
    tempPos = 0
    maxVoltage = dpg.get_value("maxVoltage")
    minVoltage = dpg.get_value("minVoltage")
    percentageOfMaxVoltage = dpg.get_value("percentOfMaxCal")
    absOrRelvoltage = dpg.get_value("absOrRelVoltage")
    absoluteMaxVoltage = dpg.get_value("absMaxVoltage")

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start TrackIt', True, w)
    guidelineText = font.render("Hit the squares as fast and accurate as possible", True, w)

    textRect = introText.get_rect()
    guideTextRect = guidelineText.get_rect() 

    textRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    guideTextRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) - 50)

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
            print("target Exit at : " + str(event.targetExitTime))
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
            print("Target exit at the very last update : " + str(events[eventIndex].targetExitTime))
            collisionDetected = False

        print(str(events[eventIndex].timeOffTarget) + " " + str(events[eventIndex].timeOnTarget) + " " + str(events[eventIndex].percentTimeOnTarget) + " " + str(events[eventIndex].reactionTime))
        print("lengths of time array : " + str(len(events[eventIndex].inputDuringEvent.inputdatas)))


        eventIndex += 1
        eventVisibleTime = 0
        if inputMode == "USB/ADAM" or inputMode == "NIDAQ" and eventIndex != len(events):
            TriggerSender.send_trigger(events[eventIndex].targetTrigger)

        if eventIndex == len(events):
            AdjustLevel(events, dpg)
            events = statistics.CalculateInaccuracyAndStd(events)
            events = statistics.CalculateOverAndUndershoot(events)
            meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets  = statistics.CalculateDescriptiveStastics(events)
            SaveFiles.SaveDataToFile(events, inputs.inputdatas, meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets, dpg)# Some data extraction senanegans 
            gameOver = True
        else:
            events[eventIndex].targetVisibleFromTime = gameTimeCounter
            reacted = False
            eventTriggerSend = False
        
        return eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex


    while not gameOver:

        if(gameStarted == True):
            #resets image
            gameTimeCounter += clock.get_time()
            gameDisplay.fill(bl)

            if(dpg.get_value("guidelines") == True):
                gameDisplay.blit(guidelineText, guideTextRect)

            if eventIndex == 0 and firstEvent == True:
                firstEvent = False

                if inputMode == "USB/ADAM" or inputMode == "NIDAQ":
                    TriggerSender.send_trigger(events[eventIndex].targetTrigger)

                events[eventIndex].targetVisibleFromTime = gameTimeCounter

            if events[eventIndex].eventType == "R" or events[eventIndex].eventType == "B": #create rect based on current Event
                pygame.draw.rect(gameDisplay, eval(events[eventIndex].eventColor),[0, events[eventIndex].targetPosition, GetSystemMetrics(0), events[eventIndex].targetHeight],1)

            if eventTriggerSend == False:
                #send event trigger 
                events[eventIndex].targetTrigger
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
                if absOrRelvoltage == "Relative":
                    ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
                if absOrRelvoltage == "Absolute":  
                    ypos=VoltageConverter.get_px_from_voltage(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)  
                drawPlayer(ypos,r)
                tempInput = InputData.InputData(voltage,ypos,gameTimeCounter)
                inputs.AddInputData(tempInput)

            events[eventIndex].inputDuringEvent.AddInputData(tempInput)
            
            collisionDetected, events[eventIndex] = CollisionDetection(events[eventIndex], tempInput.screenPosY, collisionDetected)
            events[eventIndex] = OverlapDetection(events[eventIndex], tempInput.screenPosY, collisionDetected)
            collisionDetected, events[eventIndex] = ExitDetection(events[eventIndex], tempInput.screenPosY, collisionDetected)
            
            reacted = CalculateReactionTime(events[eventIndex], tempPos, tempInput.screenPosY, reacted)
            tempPos = tempInput.screenPosY

            if useSustain == False:
                eventVisibleTime += clock.get_time()
                if eventVisibleTime >= events[eventIndex].targetTotalTime:

                    eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex = EndOfEvent(dpg, inputs, events, gameTimeCounter, eventIndex, collisionDetected, eventVisibleTime, gameOver, reacted, eventTriggerSend)

            elif useSustain == True:
                eventVisibleTime += clock.get_time()
                
                if events[eventIndex].eventType == "P":
                    events[eventIndex].timeOnTarget += clock.get_time()

                if events[eventIndex].timeOnTarget >= minSustainTime:

                    events[eventIndex].targetTotalTime = eventVisibleTime    
                     
                    eventVisibleTime, gameOver, reacted, eventTriggerSend, collisionDetected, events, eventIndex = EndOfEvent(dpg, inputs, events, gameTimeCounter, eventIndex, collisionDetected, eventVisibleTime, gameOver, reacted, eventTriggerSend) 

        else:
            gameDisplay.blit(introText, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    gameStarted = True

        pygame.display.update()
        clock.tick(120)
    pygame.quit()



