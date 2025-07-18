import numpy as np
from win32api import GetSystemMetrics

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

def CalculateOverAndUndershoot(events, forceDirection):
    baselinePos = 0
    baselinePos = DetermineBaselineHeight(events)

    for i, event in enumerate(events):
        firstSlopeDiversion = False
        positiveForce = False
        negativeForce = False
        enteredTarget = False
        exitTarget = False
        enteringTime = 0 
        exitingTime = 0

        if events[i].eventType == 'R':
            for j, input in enumerate(events[i].inputDuringEvent.inputdatas):
                if events[i].targetLength > 1:

                    if events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetHeight + events[i].targetPosition and events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition and events[i].inputXDuringEvent[j] < events[i].targetLength + events[i].targetXPosition and events[i].inputXDuringEvent[j] > events[i].targetXPosition and enteredTarget == False:
                        enteredTarget = True
                        print("entered target")
                        enteringTime = events[i].inputDuringEvent.inputdatas[j].time

                    if (events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition or events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetPosition or events[i].inputXDuringEvent[j] > events[i].targetLength + events[i].targetXPosition) and enteredTarget == True:
                        exitTarget = True
                        print("exited target")
                        exitingTime = events[i].inputDuringEvent.inputdatas[j].time

                    if exitingTime - enteringTime < 150 and firstSlopeDiversion == True and exitTarget == True and enteredTarget == True:
                        print("False Directionn Diversion Detected ")
                        print("Time on target : " + str(exitingTime - enteringTime ))
                        firstSlopeDiversion = False


                    if baselinePos > GetSystemMetrics(1)-300:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0 and events[i].inputDuringEvent.inputdatas[j].screenPosY < baselinePos):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)
                        
                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas)and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)
                            
                    elif baselinePos < 300:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0 and events[i].inputDuringEvent.inputdatas[j].screenPosY > baselinePos):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)

                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas)and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)
                    else:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)
                        
                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas) and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)

                else:

                    if events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetHeight + events[i].targetPosition and events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition and enteredTarget == False:
                        enteredTarget = True
                        enteringTime = events[i].inputDuringEvent.inputdatas[j].time

                    if (events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition or events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetPosition) and enteredTarget == True:
                        exitTarget = True
                        exitingTime = events[i].inputDuringEvent.inputdatas[j].time

                    if exitingTime - enteringTime < 150 and firstSlopeDiversion == True and exitTarget == True and enteredTarget == True:
                        print("False Directionn Diversion Detected ")
                        print("Time on target : " + str(exitingTime - enteringTime ))
                        firstSlopeDiversion = False

                    if baselinePos == 0:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)
                        
                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas) and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)

                    elif baselinePos > GetSystemMetrics(1)-300:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0 and events[i].inputDuringEvent.inputdatas[j].screenPosY < baselinePos):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)
                        
                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas)and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)
                            
                    elif baselinePos < 300:
                        if (j+1 < len(events[i].inputDuringEvent.inputdatas) and j+2 < len(events[i].inputDuringEvent.inputdatas) and
                        j+3 < len(events[i].inputDuringEvent.inputdatas) and j-1 > 0 and events[i].inputDuringEvent.inputdatas[j].screenPosY > baselinePos):
                            events, firstSlopeDiversion, positiveForce, negativeForce = DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection)

                        elif (firstSlopeDiversion == False and j+3 == len(events[i].inputDuringEvent.inputdatas)and events[i].timeOnTarget < 130):
                            events = NoMovementUndershoot(events, i, j)

                
                    
    return events

def NoMovementUndershoot(events, i, j):
    prevSlope = events[i].inputDuringEvent.inputdatas[j-2].screenPosY - events[i].inputDuringEvent.inputdatas[j-1].screenPosY
    currentSlope = events[i].inputDuringEvent.inputdatas[j-1].screenPosY - events[i].inputDuringEvent.inputdatas[j].screenPosY
    nextSlope = events[i].inputDuringEvent.inputdatas[j].screenPosY - events[i].inputDuringEvent.inputdatas[j+1].screenPosY
    nextControlSlope = events[i].inputDuringEvent.inputdatas[j+1].screenPosY - events[i].inputDuringEvent.inputdatas[j+2].screenPosY

    if(prevSlope == 0.0 and currentSlope == 0.0 and nextSlope == 0.0 and nextControlSlope == 0.0):
        events[i].undershoot = True
        events[i].undershootTime = events[i].inputDuringEvent.inputdatas[j+2].time
    return events

def DetermineBaselineHeight(events):
    baselinePos = 0
    for event in events: 
        if event.eventType == 'B':
            baselinePos = event.targetPosition
            if baselinePos < 200 : 
                baselinePos = baselinePos + event.targetHeight + 20
            elif baselinePos > GetSystemMetrics(1)-200 : 
                baselinePos = baselinePos - event.targetHeight - 20
    return baselinePos

def DirectionCalculation(events, i, firstSlopeDiversion, j, positiveForce, negativeForce, forceDirection):
    prevSlope = events[i].inputDuringEvent.inputdatas[j-1].screenPosY - events[i].inputDuringEvent.inputdatas[j].screenPosY
    currentSlope = events[i].inputDuringEvent.inputdatas[j].screenPosY - events[i].inputDuringEvent.inputdatas[j+1].screenPosY
    nextSlope = events[i].inputDuringEvent.inputdatas[j+1].screenPosY - events[i].inputDuringEvent.inputdatas[j+2].screenPosY
    nextControlSlope = events[i].inputDuringEvent.inputdatas[j+2].screenPosY - events[i].inputDuringEvent.inputdatas[j+3].screenPosY

    if prevSlope > 0.0 and currentSlope > 0.0 and nextSlope > 0.0 and nextControlSlope > 0.0:
        positiveForce = True
        negativeForce = False

    if prevSlope < 0.0 and currentSlope < 0.0 and nextSlope < 0.0 and nextControlSlope < 0.0:
        positiveForce = False
        negativeForce = True

    if events[i].inputDuringEvent.inputdatas[j].time > events[i].reactionTime and nextSlope != 0 and nextControlSlope !=0 and firstSlopeDiversion == False:
        if positiveForce and nextSlope < 0.0 and nextControlSlope < 0.0:
            events, firstSlopeDiversion = OverOrUndershoot(events, i, j+1, firstSlopeDiversion, forceDirection)
        elif negativeForce and nextSlope > 0.0 and nextControlSlope > 0.0:
            events, firstSlopeDiversion = OverOrUndershoot(events, i, j+1, firstSlopeDiversion, forceDirection)
    return events, firstSlopeDiversion, positiveForce, negativeForce

def OverOrUndershoot(events, i, j, firstSlopeDiversion, forceDirection):
    firstSlopeDiversion = True
    if events[i].inputDuringEvent.inputdatas[j].screenPosY > events[i].targetHeight + events[i].targetPosition:
        if forceDirection == "Upwards" : 
            events[i].undershoot = True
            events[i].undershootTime = events[i].inputDuringEvent.inputdatas[j].time
        else:
            events[i].overshoot = True
            events[i].overshootTime = events[i].inputDuringEvent.inputdatas[j].time

    if events[i].inputDuringEvent.inputdatas[j].screenPosY < events[i].targetPosition:
        if forceDirection == "Upwards" : 
            events[i].overshoot = True
            events[i].overshootTime = events[i].inputDuringEvent.inputdatas[j].time
        else:
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