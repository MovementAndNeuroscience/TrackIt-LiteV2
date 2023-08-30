import EventData as event
class EventsData(): 
    def __init__(self):
        self.eventDatas = []

    def AddEventData(self, event):
        self.eventDatas.append(event)