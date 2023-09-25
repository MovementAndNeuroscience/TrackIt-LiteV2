class SviptTrial():
    completionTime = 0
    noEvents = 0
    events = []
    error = 0
    trialno = 0

    def __init__(self, noEvents):
        self.noEvents = noEvents

    def AddEvent(self, eventData):
        self.events.append(eventData)