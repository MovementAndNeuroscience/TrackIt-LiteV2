#SideQuestGenerator
import SviptBlock
import SviptTrial
import InputDatas
import EventData
from win32api import GetSystemMetrics
import random
import copy

def GenerateSideQuest(dpg):

    importedEvents = dpg.get_value("writtenEvents")
    event_height = dpg.get_value("gateHeight" + str(1))
    baseline_height = dpg.get_value("stabGateHeight")
    random_events = dpg.get_value("noSideEvents")
    random_heights_for_events = dpg.get_value("randomTargetHeight")
    own_Sequence = dpg.get_value("ownSequence")
    min_closeness_between_events = dpg.get_value("minCloseness")
    max_closeness_between_events = dpg.get_value("maxCloseness")
    minRandomHeight = dpg.get_value("minRandomHeight")
    maxRandomHeight = dpg.get_value("maxRandomHeight")

    sideQBlock = SviptBlock.SviptBlock(dpg.get_value("noSideQuestTrials"))
    sideQTrial = SviptTrial.SviptTrial(dpg.get_value("noSideEvents"))

    sideQBlock.trials = [] 
    sideQTrial.events = []   
    availablePixels = []
    pixel = 0 
    recursiveCounter = 0; 

    # How to divide screen into sections of one seconds or finer. 
    # we know screen lengths GetSystemMetrics(0):
    # we know how long time the whole trial ahould last sideQuestTrialTime
    # we know how much time the stabilization trials should last. 
    # we can define time between gates to be 500ms

    breakBetweenGatesTimeMs = dpg.get_value("sideQBreak")
    millisecondSegments = GetSystemMetrics(0) / (dpg.get_value("sideQuestTrialTime")*1000)
    stabilisatorLength = millisecondSegments * (dpg.get_value("sideQuestStabiTime")*1000)
    breakBetweenGatesLength = millisecondSegments * breakBetweenGatesTimeMs; 
    gatesLength = (GetSystemMetrics(0)-(stabilisatorLength + (breakBetweenGatesLength * dpg.get_value("noSideEvents"))))/dpg.get_value("noSideEvents")

    while pixel <= GetSystemMetrics(1):
        availablePixels.append(pixel)
        pixel += 1


    if random_events:
        baselineEvent = EventData.EventData(len(sideQTrial.events), baseline_height, GetSystemMetrics(1)/2,"B",'w', 60000, InputDatas.InputDatas())
        baselineEvent.targetLength = stabilisatorLength
        baselineEvent.targetXPosition = 0


        sideQTrial.AddEvent(baselineEvent)

        i = 0
        previousLocation = 0; 
        while i < sideQTrial.noEvents:
            newLocation, event_height = CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height, recursiveCounter, i+1) 
            if newLocation == 99999:
                sideQBlock.noTrials = 99999
                return sideQBlock
            else:
                gateColor = 'r'
                match i:
                    case 0:
                        gateColor = 'r'
                    case 1:
                        gateColor = 'd'
                    case 2:
                        gateColor = 'h'
                    case 3:
                        gateColor = 'b'
                    case 4:
                        gateColor = 'g'
                    case 5:
                        gateColor = 'c'
                    case 6:
                        gateColor = 'y'
                    case 7:
                        gateColor = 'v'
                    case 8:
                        gateColor = 'p'
                    case 9:
                        gateColor = 'o'
                    case _:
                        gateColor = 'w'
                
                newEvent = EventData.EventData(len(sideQTrial.events), dpg.get_value("gateHeight" + str(i+1)), newLocation, "R", gateColor, 10000, InputDatas.InputDatas())
                newEvent.targetLength = gatesLength
                previousLocation = newLocation 
                sideQTrial.AddEvent(newEvent)
                i = i + 1 

    if own_Sequence:
        rects_pauses_list = importedEvents.split()

        for event in rects_pauses_list:
            if event[0] == "R" and len(sideQTrial.events) <= sideQTrial.noEvents :
                newEvent = EventData.EventData(len(sideQTrial.events), dpg.get_value("gateHeight" + str(len(sideQTrial.events))), int(event[1:-1]), event[0], event[-1], 10000, InputDatas.InputDatas())
                sideQTrial.AddEvent(newEvent)
            if event[0] == "B" and len(sideQTrial.events) == 0:
                newEvent = EventData.EventData(len(sideQTrial.events), event_height, 0, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                sideQTrial.AddEvent(newEvent)

        if random_heights_for_events:

            for event in sideQTrial.events:
                event.targetHeight = random.randint(minRandomHeight, maxRandomHeight)

    trialno = 1
    sideQBlock.AddTrial(sideQTrial)

    while len(sideQBlock.trials) < sideQBlock.noTrials:
        
        availablePixels = []
        pixel = 0
        while pixel <= GetSystemMetrics(1):
            availablePixels.append(pixel)
            pixel += 1
        sideQTrial.__delattr__
        sideQTrial = SviptTrial.SviptTrial(dpg.get_value("noSideEvents"))
        sideQTrial.events = []       
        recursiveCounter = 0
        event_height = sideQBlock.trials[0].events[0].targetHeight


        tempSideQBlock, tempSideQTrial = CreateNewTrial(dpg, random_events, sideQTrial, stabilisatorLength, max_closeness_between_events,min_closeness_between_events, random_heights_for_events, availablePixels, minRandomHeight,
                   maxRandomHeight, recursiveCounter, sideQBlock, gatesLength, own_Sequence, importedEvents, event_height, baseline_height)
        if sideQBlock.noTrials == 99999:
            return sideQBlock
        sideQBlock.AddTrial(tempSideQTrial)
        sideQBlock.trials[trialno].trialno = trialno
        trialno +=1
                    
    return sideQBlock

def CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height, recursiveCounter, gateNo):

    if(previousLocation == 0):
        pos = random.randint(100, dpg.get_value("calibrationInput"))
        if random_heights_for_events:
            height = random.randint(minRandomHeight, maxRandomHeight)
        else:
            height = event_height

        return pos, height
    else:
        height, newPos = FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight,random_heights_for_events, dpg.get_value("gateHeight" + str(gateNo)), recursiveCounter)
        return newPos, height

def FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight, random_heights_for_events, event_height, recursiveCounter):
    height = event_height
    newPos = random.randint(100, dpg.get_value("calibrationInput"))
    rectPixels = []
    currentPix = 0

    distFromOldToNewPos = abs(previousLocation-newPos)

    while distFromOldToNewPos <  min_closeness_between_events or distFromOldToNewPos >  max_closeness_between_events:
        newPos = random.randint(100, dpg.get_value("calibrationInput"))
        distFromOldToNewPos = abs(previousLocation-newPos)

    if random_heights_for_events:        
        height = random.randint(minRandomHeight, maxRandomHeight)

    currentPix = newPos
    while currentPix < newPos + 1:
        rectPixels.append(currentPix)    
        currentPix += 1 

    for curr in rectPixels:
        pixelPresent = availablePixels.count(curr)
        if pixelPresent == 0:  
            if recursiveCounter < 899:
                recursiveCounter += 1
                height, newPos = FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight, random_heights_for_events, height, recursiveCounter)
                if (height == 99999):
                    return height, newPos
            else :
                print("we tried")
                recursiveCounter = 0
                height = 99999
                newPos = 99999
                break
            
    return height,newPos

def CreateNewTrial(dpg, random_events, sideQTrial, stabilisatorLength, max_closeness_between_events,min_closeness_between_events, random_heights_for_events, availablePixels, minRandomHeight,
                   maxRandomHeight, recursiveCounter, sideQBlock, gatesLength, own_Sequence, importedEvents, event_height, baseline_height):
    if random_events:
        
        baselineEvent = EventData.EventData(len(sideQTrial.events),baseline_height,GetSystemMetrics(1)/2,"B",'w',60000, InputDatas.InputDatas())
        baselineEvent.targetLength = stabilisatorLength
        sideQTrial.AddEvent(baselineEvent)

        i = 0
        previousLocation = 0; 
        while i < sideQTrial.noEvents:
            newLocation, event_height = CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height, recursiveCounter, i+1) 
            
            if newLocation == 99999:
                sideQBlock.noTrials = 99999
                return sideQBlock, sideQTrial
            else:
                gateColor = 'r'
                match i:
                    case 0:
                        gateColor = 'r'
                    case 1:
                        gateColor = 'd'
                    case 2:
                        gateColor = 'h'
                    case 3:
                        gateColor = 'b'
                    case 4:
                        gateColor = 'g'
                    case 5:
                        gateColor = 'c'
                    case 6:
                        gateColor = 'y'
                    case 7:
                        gateColor = 'v'
                    case 8:
                        gateColor = 'p'
                    case 9:
                        gateColor = 'o'
                    case _:
                        gateColor = 'w'
                

                newEvent = EventData.EventData(len(sideQTrial.events), dpg.get_value("gateHeight" + str(i+1)), newLocation,"R", gateColor, 10000, InputDatas.InputDatas())
                newEvent.targetLength = gatesLength

                previousLocation = newLocation 
                sideQTrial.AddEvent(newEvent)
                
                i = i + 1 


    if own_Sequence:
        rects_pauses_list = importedEvents.split()

        for event in rects_pauses_list:
            if event[0] == "R" and len(sideQTrial.events) <= sideQTrial.noEvents :
                newEvent = EventData.EventData(len(sideQTrial.events), dpg.get_value("gateHeight" + str(len(sideQTrial.events))), int(event[1:-1]), event[0], event[-1], 10000, InputDatas.InputDatas())
                sideQTrial.AddEvent(newEvent)
            if event[0] == "B" and len(sideQTrial.events) == 0:
                newEvent = EventData.EventData(len(sideQTrial.events), event_height, 0, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                sideQTrial.AddEvent(newEvent)

        if random_heights_for_events:

            for event in sideQTrial.events:
                event.targetHeight = random.randint(minRandomHeight, maxRandomHeight)

    return sideQBlock, sideQTrial 

