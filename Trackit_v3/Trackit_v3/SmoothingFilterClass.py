#SmoothingFilterClass
class SmoothingFilterClass():
    def __init__(self):
        self.window = 5
        self.smoothingInput = []
        self.averageInput = 0

    def InsertInput(self, input):
        if len(self.smoothingInput) == self.window:
            self.smoothingInput.pop()
            self.smoothingInput.insert(0, input)
        else:
            self.smoothingInput.insert(0, input)

    def SetWindowSize(self, windowsize):
        self.window = windowsize

    def AverageInput(self):
        total = 0 
        for input in self.smoothingInput:
            total = total + input
        return total/self.window

    def ResetFilter(self):
        self.smoothingInput.clear()