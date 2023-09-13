#EventDataGenerator
#this Scripts takes care of generating the needed events for Trackit to he able to function
import Eventsdata
import EventData 
import InputDatas
from win32api import GetSystemMetrics
import random

def GenerateEvents(dpg):
    importedEvents = dpg.get_value("writtenEvents")
    event_display_time = dpg.get_value("stimDisplayTime")
    baseline_display_time = dpg.get_value("baseDisplayTime")
    pause_time = dpg.get_value("pauseTime")
    event_height = dpg.get_value("stimHeight")
    event_baseline = dpg.get_value("baseline")
    random_events = dpg.get_value("randomTargets")
    num_of_random_events = dpg.get_value("SetNumOfRandomEvents")
    random_heights_for_events = dpg.get_value("randomTargetHeight")
    own_Sequence = dpg.get_value("ownSequence")
    sustain_events = dpg.get_value("TargetSustain")
    visible_events = dpg.get_value("moreTargets")
    min_closeness_between_events = dpg.get_value("minCloseness")
    max_closeness_between_events = dpg.get_value("maxCloseness")
    amount_of_visible_events = dpg.get_value("targetsOnScreen")
    minRandomHeight = dpg.get_value("minRandomHeight")
    maxRandomHeight = dpg.get_value("maxRandomHeight")


    tempEventList = Eventsdata.EventsData()
    tempEventListWithBaseline = Eventsdata.EventsData()
    tempEventListWithBaselineAndPause = Eventsdata.EventsData()

    if(own_Sequence):
        rects_pauses_list = importedEvents.split()

        for event in rects_pauses_list:
            if event[0] == "R":
                newEvent = EventData.EventData(len(tempEventList.eventDatas), event_height, int(event[1:-1]), event[0], event[-1], event_display_time, InputDatas.InputDatas())
                tempEventList.AddEventData(newEvent)
            if event[0] == "B":
                newEvent = EventData.EventData(len(tempEventList.eventDatas), event_height, 0, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                tempEventList.AddEventData(newEvent)
            if event[0] == "P":
                newEvent = EventData.EventData(len(tempEventList.eventDatas), event_height, 10000, event[0], event[-1], int(event[1:-1]), InputDatas.InputDatas())
                tempEventList.AddEventData(newEvent)

    if(random_events):
        i = 0
        previousLocation = 0; 
        while i < num_of_random_events:
            newLocation = CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg) 
            newEvent = EventData.EventData(len(tempEventList.eventDatas), event_height, newLocation, 'R', 'b', event_display_time, InputDatas.InputDatas())
            previousLocation = newLocation 
            tempEventList.AddEventData(newEvent)
            newPause = EventData.EventData(len(tempEventList.eventDatas), event_height, 10000, 'P', 'y', pause_time, InputDatas.InputDatas())
            tempEventList.AddEventData(newPause)
            i = i + 1 

    if(random_heights_for_events):
        for i,  event in enumerate(tempEventList.eventDatas):
            tempEventList.eventDatas[i].targetHeight = random.randint(minRandomHeight, maxRandomHeight)

    if(sustain_events):
        for i,  event in enumerate(tempEventList.eventDatas):
            tempEventList.eventDatas[i].targetTotalTime = 60000

    if(event_baseline):

        for event in tempEventList.eventDatas:
            tempEvent = event
            tempEvent.targetId = len(tempEventListWithBaseline.eventDatas)
            tempEventListWithBaseline.AddEventData(event)

            if len(tempEventListWithBaseline.eventDatas)%3 == 2 and sustain_events: 
                baselineEvent = EventData.EventData(len(tempEventListWithBaseline.eventDatas),event_height,0,'B','g',60000, InputDatas.InputDatas())
                tempEventListWithBaseline.AddEventData(baselineEvent)

            
            elif len(tempEventListWithBaseline.eventDatas)%3 == 2:
                baselineEvent = EventData.EventData(len(tempEventListWithBaseline.eventDatas),event_height,0,'B','g',baseline_display_time, InputDatas.InputDatas())
                tempEventListWithBaseline.AddEventData(baselineEvent)

        for event in tempEventListWithBaseline.eventDatas:
            tempEvent = event
            tempEvent.targetId = len(tempEventListWithBaselineAndPause.eventDatas)
            tempEventListWithBaselineAndPause.AddEventData(event)
            
            if len(tempEventListWithBaselineAndPause.eventDatas)%4 == 3:
                pauseEvent = EventData.EventData(len(tempEventListWithBaselineAndPause.eventDatas),event_height,1100,'P','',pause_time, InputDatas.InputDatas())
                tempEventListWithBaselineAndPause.AddEventData(pauseEvent)

        eventsdata = tempEventListWithBaselineAndPause
        print('lengths of eventsdata ' + str(len(eventsdata.eventDatas)))
        return eventsdata
    else:
        eventsdata = tempEventList
        print('lengths of eventsdata ' + str(len(eventsdata.eventDatas)))
        return eventsdata




def CalculateNewLocation(previousLocation,min_closeness_between_events,max_closeness_between_events, dpg):
    if(previousLocation == 0):
        return random.randint(100, dpg.get_value("calibrationInput"))
    else:
        newPos = random.randint(100, dpg.get_value("calibrationInput"))
        distFromOldToNewPos = abs(previousLocation-newPos)
        while distFromOldToNewPos <  min_closeness_between_events or distFromOldToNewPos >  max_closeness_between_events:
            newPos = random.randint(100, dpg.get_value("calibrationInput"))
            distFromOldToNewPos = abs(previousLocation-newPos)
        return newPos

        #puase_list = filter(lambda x: x.startswith("P"), rects_pauses_list)
