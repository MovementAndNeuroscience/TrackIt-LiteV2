class SviptTrial():
    completionTime = 0
    noEvents = 0
    events = []
    error = 0
    trialno = 0
    timeBetweenTrials = 0
    meanAccuracy = 0
    stdAccuracy = 0
    meanTimeOnTarget = 0 
    stdTimeOnTarget = 0
    totalTimeOnTargets = 0

    def __init__(self, noEvents):
        self.noEvents = noEvents

    def AddEvent(self, eventData):
        self.events.append(eventData)