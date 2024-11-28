class Calibrationdata():
    def __init__(self, maxinput, maxVoltage, minVoltage):
        self.maxinput = maxinput
        self.maxVoltage = maxVoltage
        self.minVoltage = minVoltage

    def __init__(self):
        self.maxinput = 0
        self.maxVoltage = -5
        self.minVoltage = 500000

    def SetMaxInput(self, maxinput):
        self.maxinput = maxinput

    def GetMaxInput(self):
        return self.maxinput
    
    def SetMaxVoltage(self, maxVoltage):
        self.maxVoltage = maxVoltage

    def GetMaxVoltage(self):
        return self.maxVoltage
    
    def SetMinVoltage(self, minVoltage):
        self.minVoltage = minVoltage

    def GetMinVoltage(self):
        return self.minVoltage