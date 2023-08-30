class EventData():
    targetId = 0 #
    targetHeight = 0   
    targetPosition = 0 
    eventType = 'R' #
    eventColor = 'r'
    targetTotalTime = 0 
    targetVisibleFromTime = 0.0 
    percentTimeOnTarget = 0 #
    targetEntryTime = 0.0 #
    targetExitTime = 0.0 #
    reactionTime = 0.0 #
    timeOnTarget = 0.0 #
    timeOffTarget = 0.0 #
    inputDuringEvent = [] #--
    meanDistanceAwayFromTarget= 0.0 #
    stdOfInput = 0 #
    meanOfInput = 0 #--
    targetTrigger = 0 #
    overshoot = False
    overshootTime = 0.0
    undershoot = False
    undershootTime = 0.0 

    
    def __init__(self, targetId, targetHeight, targetPosition, eventType, eventColor, targetTotalTime, targetVisibleFromTime, percentTimeOnTarget, targetEntryTime, targetExitTime, reactionTime, timeOnTarget, timeOffTarget, inputDuringEvent,meanDistanceAwayFromTarget ,stdInput, meanInput, targetTrigger ):
        self.targetId = targetId
        self.targetHeight = targetHeight
        self.targetPosition = targetPosition
        self.eventType = eventType
        self.eventColor = eventColor
        self.targetTotalTime = targetTotalTime
        self.targetVisibleFromTime = targetVisibleFromTime
        self.percentTimeOnTarget = percentTimeOnTarget
        self.targetEntryTime = targetEntryTime
        self.targetExitTime = targetExitTime
        self.reactionTime = reactionTime
        self.timeOnTarget = timeOnTarget
        self.timeOffTarget = timeOffTarget
        self.inputDuringEvent = inputDuringEvent
        self.meanDistanceAwayFromTarget = meanDistanceAwayFromTarget
        self.stdOfInput = stdInput
        self.meanOfInput = meanInput
        self.targetTrigger = targetTrigger
        
    def __init__(self, targetId, targetHeight, targetPosition, eventType, eventColor, targetTotalTime, inputDuringEvent):
        self.targetId = targetId
        self.targetHeight = targetHeight
        self.targetPosition = targetPosition
        self.eventType = eventType
        self.eventColor = eventColor
        self.targetTotalTime = targetTotalTime
        self.inputDuringEvent = inputDuringEvent