#TriggerGenerator
import Eventsdata

def GenerateTriggers(events):

    for i, event in enumerate(events.eventDatas):
        
        # baseline Trigger = 10 
        # Pause Trigger = 15
        # Red Rectance Trigger = 20
        # green rectance Trigger = 21 
        # blue Ractance Trigger = 22 
        # yellow Rectance Trigger = 23
        # violet Rectance Trigger = 24
        # cyan Rectance Trigger = 25
        # pink Rectance Trigger = 26
        # SVIPT START Trial Trigger = 1 
        # SVIPT END Trial Trigger = 2

        if events.eventDatas[i].eventType == "B":
            events.eventDatas[i].targetTrigger = 10
        elif events.eventDatas[i].eventType == "P":
            events.eventDatas[i].targetTrigger = 15
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "r":
            events.eventDatas[i].targetTrigger = 20
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "g":
            events.eventDatas[i].targetTrigger = 21
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "b":
            events.eventDatas[i].targetTrigger = 22
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "y":
            events.eventDatas[i].targetTrigger = 23
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "v":
            events.eventDatas[i].targetTrigger = 24
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "c":
            events.eventDatas[i].targetTrigger = 25
        elif events.eventDatas[i].eventType == "R" and events.eventDatas[i].eventColor == "p":
            events.eventDatas[i].targetTrigger = 26

    return events