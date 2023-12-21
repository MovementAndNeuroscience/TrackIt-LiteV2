import SviptBlock
import SviptTrial
import InputDatas
import EventData
from win32api import GetSystemMetrics
import random
import copy

def GenerateSVIPT(dpg):

    importedEvents = dpg.get_value("writtenEvents")
    event_height = dpg.get_value("stimHeight")
    random_events = dpg.get_value("randomTargets")
    random_heights_for_events = dpg.get_value("randomTargetHeight")
    own_Sequence = dpg.get_value("ownSequence")
    min_closeness_between_events = dpg.get_value("minCloseness")
    max_closeness_between_events = dpg.get_value("maxCloseness")
    minRandomHeight = dpg.get_value("minRandomHeight")
    maxRandomHeight = dpg.get_value("maxRandomHeight")

    sviptblock = SviptBlock.SviptBlock(dpg.get_value("noSviptTrials"))
    sviptTrial = SviptTrial.SviptTrial(dpg.get_value("noSviptEvents"))

    sviptblock.trials = [] 
    sviptTrial.events = []   
    availablePixels = []
    pixel = 0 
    recursiveCounter = 0; 
    while pixel <= GetSystemMetrics(1):
        availablePixels.append(pixel)
        pixel += 1


    if random_events:
        
        baselineEvent = EventData.EventData(len(sviptTrial.events),event_height,0,'B','w',60000, InputDatas.InputDatas())
        sviptTrial.AddEvent(baselineEvent)

        i = 0
        previousLocation = 0; 
        while i < sviptTrial.noEvents:
            newLocation, event_height = CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height, recursiveCounter, i+1) 
            if newLocation == 99999:
                sviptblock.noTrials = 99999
                return sviptblock
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
                

                newEvent = EventData.EventData(len(sviptTrial.events), event_height, newLocation, 'R', gateColor, 10000, InputDatas.InputDatas())
                previousLocation = newLocation 
                sviptTrial.AddEvent(newEvent)
                i = i + 1 

    if own_Sequence:
        rects_pauses_list = importedEvents.split()

        for event in rects_pauses_list:
            if event[0] == "R" and len(sviptTrial.events) <= sviptTrial.noEvents :
                newEvent = EventData.EventData(len(sviptTrial.events), dpg.get_value("gateHeight" + str(len(sviptTrial.events))), int(event[1:-1]), event[0], event[-1], 10000, InputDatas.InputDatas())
                sviptTrial.AddEvent(newEvent)
            if event[0] == "B" and len(sviptTrial.events) == 0:
                newEvent = EventData.EventData(len(sviptTrial.events), event_height, 0, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                sviptTrial.AddEvent(newEvent)

        if random_heights_for_events:

            for event in sviptTrial.events:
                event.targetHeight = random.randint(minRandomHeight, maxRandomHeight)

    trialno = 0 
    while len(sviptblock.trials) < sviptblock.noTrials:
        sviptblock.AddTrial(copy.deepcopy(sviptTrial))
        sviptblock.trials[trialno].trialno = trialno
        trialno +=1


    return sviptblock

def CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height, recursiveCounter, gateNo):

    if random_heights_for_events:
        if(previousLocation == 0):
            pos = random.randint(100, dpg.get_value("calibrationInput"))
            height = random.randint(minRandomHeight, maxRandomHeight)
            availablePixels = ExtractFirstRectFromPixels(availablePixels, pos, height)

            return pos, height
        else:
            height, newPos = FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight,random_heights_for_events, event_height, recursiveCounter)
            return newPos, height
    else: 
        if(previousLocation == 0):
            pos = random.randint(100, dpg.get_value("calibrationInput"))
            availablePixels = ExtractFirstRectFromPixels(availablePixels, pos, dpg.get_value("gateHeight" + str(gateNo)))
            return pos, dpg.get_value("gateHeight" + str(gateNo))
        else:
            height, newPos = FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight, random_heights_for_events, dpg.get_value("gateHeight" + str(gateNo)), recursiveCounter)
            return newPos, height

def ExtractFirstRectFromPixels(availablePixels, pos, height):
    rectPixels = []
    currentPix = pos
    while currentPix < pos + height:
        rectPixels.append(currentPix)    
        currentPix += 1 

    for curr in rectPixels:
        if curr < len(availablePixels):
            availablePixels.remove(curr)

    return availablePixels

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
    while currentPix < newPos + height:
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
                recursiveCounter = 0
                height = 99999
                newPos = 99999
                break
            
    for curr in rectPixels:
        pixelPresent = availablePixels.count(curr)
        if pixelPresent == 0:
            recursiveCounter = 0 
            height = 99999
            newPos = 99999
            break
        availablePixels.remove(curr)
    return height,newPos
