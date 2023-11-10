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
        firstSlopeDiversion = False
        positiveForce = False
        negativeForce = False

        for j, input in enumerate(events[i].inputDuringEvent.inputdatas):
            if j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0:
                
                prevSlope = events[i].inputDuringEvent.inputdatas[j-1].screenPosY - events[i].inputDuringEvent.inputdatas[j].screenPosY
                currentSlope = events[i].inputDuringEvent.inputdatas[j].screenPosY - events[i].inputDuringEvent.inputdatas[j+1].screenPosY
                nextSlope = events[i].inputDuringEvent.inputdatas[j+1].screenPosY - events[i].inputDuringEvent.inputdatas[j+2].screenPosY
                nextControlSlope = nextSlope = events[i].inputDuringEvent.inputdatas[j+2].screenPosY - events[i].inputDuringEvent.inputdatas[j+3].screenPosY

                if prevSlope > 0.0 and currentSlope > 0.0 and nextSlope > 0.0 and nextControlSlope > 0.0:
                    positiveForce = True
                    negativeForce = False

                if prevSlope < 0.0 and currentSlope < 0.0 and nextSlope < 0.0 and nextControlSlope < 0.0:
                    positiveForce = False
                    negativeForce = True

                if events[i].inputDuringEvent.inputdatas[j].time > events[i].reactionTime and nextSlope != 0 and firstSlopeDiversion == False:

                    if positiveForce and nextSlope < 0.0 and nextControlSlope < 0.0:
                        events, firstSlopeDiversion = OverOrUndershoot(events, i, j+1, firstSlopeDiversion)
                    elif negativeForce and nextSlope > 0.0 and nextControlSlope > 0.0:
                        events, firstSlopeDiversion = OverOrUndershoot(events, i, j+1, firstSlopeDiversion)
    return events

def OverOrUndershoot(events, i, j, firstSlopeDiversion):
    firstSlopeDiversion = True
    if events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition:
        events[i].overshoot = True
        events[i].overshootTime = events[i].inputDuringEvent.inputdatas[j].time

    if events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition:
        events[i].undershoot = True
        events[i].undershootTime = events[i].inputDuringEvent.inputdatas[j].time
    
    return events, firstSlopeDiversion

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