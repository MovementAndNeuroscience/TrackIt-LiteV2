import SviptBlock
import SviptTrial
import InputDatas
import EventData
from win32api import GetSystemMetrics
import random

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

    availablePixels = []
    pixel = 0 
    while pixel < GetSystemMetrics(1):
        availablePixels.append(pixel)
        pixel += 1


    if random_events:
        
        baselineEvent = EventData.EventData(len(sviptTrial.events),event_height,0,'B','g',60000, InputDatas.InputDatas())
        sviptTrial.AddEvent(baselineEvent)

        i = 0
        previousLocation = 0; 
        while i <= sviptTrial.noEvents:
            newLocation, event_height = CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height) 
            newEvent = EventData.EventData(len(sviptTrial.events), event_height, newLocation, 'R', 'b', 10000, InputDatas.InputDatas())
            previousLocation = newLocation 
            sviptTrial.AddEvent(newEvent)
            i = i + 1 

    if own_Sequence:
        rects_pauses_list = importedEvents.split()

        for event in rects_pauses_list:
            if event[0] == "R" and len(sviptTrial.events) <= sviptTrial.noEvents :
                newEvent = EventData.EventData(len(sviptTrial.events), event_height, int(event[1:-1]), event[0], event[-1], 10000, InputDatas.InputDatas())
                sviptTrial.AddEvent(newEvent)
            if event[0] == "B" and len(sviptTrial.events) == 0:
                newEvent = EventData.EventData(len(sviptTrial.events), event_height, 0, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                sviptTrial.AddEvent(newEvent)

        if random_heights_for_events:

            for event in sviptTrial.events:
                event.targetHeight = random.randint(minRandomHeight, maxRandomHeight)

    while len(sviptblock.trials) <= sviptblock.noTrials:
        sviptblock.AddTrial(sviptTrial)

    return sviptblock

def CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg, random_heights_for_events, availablePixels, minRandomHeight, maxRandomHeight, event_height):

    if random_heights_for_events:
        if(previousLocation == 0):
            pos = random.randint(100, dpg.get_value("calibrationInput"))
            height = random.randint(minRandomHeight, maxRandomHeight)
            availablePixels = ExtractFirstRectFromPixels(availablePixels, pos, height)

            return pos, height
        else:
            height, newPos = FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight,random_heights_for_events, event_height)
            return newPos, height
    else: 
        if(previousLocation == 0):
            pos = random.randint(100, dpg.get_value("calibrationInput"))
            availablePixels = ExtractFirstRectFromPixels(availablePixels, pos, event_height)
            return pos, event_height
        else:
            height, newPos =FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight, random_heights_for_events, event_height)
            return height, newPos

def ExtractFirstRectFromPixels(availablePixels, pos, height):
    rectPixels = []
    currentPix = pos
    while currentPix < pos + height:
        rectPixels.append(currentPix)    
        currentPix += 1 

    for curr in rectPixels:
        availablePixels.remove(curr)

    return availablePixels

def FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight, random_heights_for_events, event_height):
    newPos = random.randint(100, dpg.get_value("calibrationInput"))
    distFromOldToNewPos = abs(previousLocation-newPos)
    while distFromOldToNewPos <  min_closeness_between_events or distFromOldToNewPos >  max_closeness_between_events:
        newPos = random.randint(100, dpg.get_value("calibrationInput"))
        distFromOldToNewPos = abs(previousLocation-newPos)
    height = event_height
    if random_heights_for_events:        
        height = random.randint(minRandomHeight, maxRandomHeight)
    rectPixels = []
    currentPix = newPos
    while currentPix < newPos + height:
        rectPixels.append(currentPix)    
        currentPix += 1 

    for curr in rectPixels:
        pixelPresent = availablePixels.count(curr)
        if pixelPresent == 0:
            FindTheNextRect(previousLocation, min_closeness_between_events, max_closeness_between_events, dpg, availablePixels, minRandomHeight, maxRandomHeight)

    for curr in rectPixels:
        availablePixels.remove(curr)

    return height,newPos
