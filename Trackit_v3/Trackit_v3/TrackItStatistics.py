import numpy as np

def CalculateInaccuracyAndStd(events):
    
    for i, event in enumerate(events):
        inputOutsideRect = []

        for j, input in enumerate(events[i].inputDuringEvent.inputdatas):
            if events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition:
                inputOutsideRect.append(events[i].inputDuringEvent.inputdatas[j].screenPosY - (events[i].targetHeight + events[i].targetPosition))

            elif events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition:    
                inputOutsideRect.append(events[i].targetPosition - events[i].inputDuringEvent.inputdatas[j].screenPosY)

        events[i].meanDistanceAwayFromTarget = np.mean(inputOutsideRect)
        events[i].stdOfInput = np.std(inputOutsideRect)

    return events

def CalculateOverAndUndershoot(events):
        
    for i, event in enumerate(events):
        slope = []
        firstSlopeDiversion = False
        print("event nr : " + str(i))

        for j, input in enumerate(events[i].inputDuringEvent.inputdatas):
            if j+1 < len(events[i].inputDuringEvent.inputdatas):
                currentSlope = events[i].inputDuringEvent.inputdatas[j].screenPosY - events[i].inputDuringEvent.inputdatas[j+1].screenPosY
                if events[i].inputDuringEvent.inputdatas[j].time > events[i].reactionTime and currentSlope != 0:
                    slope.append(np.abs(currentSlope))
                    meanSlope = np.mean(slope)
                    stdSlope = np.std(slope)
                    #print ("Slope : "  + str(np.abs(currentSlope)) + " avr : " + str(meanSlope) + " std : " + str(stdSlope) + " Found slope diversion : " + str(firstSlopeDiversion) + " At time : " + str(events[i].inputDuringEvent.inputdatas[j].time))

                    if np.abs(currentSlope) < meanSlope - stdSlope and firstSlopeDiversion == False: 
                        firstSlopeDiversion = True
                        if events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition:
                            events[i].overshoot = True
                            events[i].overshootTime = events[i].inputDuringEvent.inputdatas[j].time
                            print("overshoot time : "  + str(events[i].inputDuringEvent.inputdatas[j].time) + "  " +str(j))

                        if events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition:
                            events[i].undershoot = True
                            events[i].undershootTime = events[i].inputDuringEvent.inputdatas[j].time
                            print("undershoot time : "  + str(events[i].inputDuringEvent.inputdatas[j].time)+ "  " +str(j))
    return events

def CalculateDescriptiveStastics(events):
    acc = []
    timeOnTarget = []
    for event in events:
        if event.eventType == "R" or event.eventType == "B":
            acc.append(event.percentTimeOnTarget)
            timeOnTarget.append(event.timeOnTarget)

    meanAccuracy = np.mean(acc)
    stdAccuracy = np.std(acc)
    meanTimeOnTarget = np.mean(timeOnTarget)
    stdTimeOnTarget = np.std(timeOnTarget)
    totalTimeOnTargets = np.sum(timeOnTarget)
        

    return meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets 