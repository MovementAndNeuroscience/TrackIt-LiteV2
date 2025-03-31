class Calibrationdata():
    def __init__(self, maxinput, maxVoltage, minVoltage, neurtalNIDAQVal):
        self.maxinput = maxinput
        self.maxVoltage = maxVoltage
        self.minVoltage = minVoltage
        self.neurtalNIDAQVal = neurtalNIDAQVal

    def __init__(self):
        self.maxinput = 0
        self.maxVoltage = -5000.0
        self.minVoltage = 500000.0
        self.neurtalNIDAQVal = 500000.0

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
    
    def GetNeutralVal(self):
        return self.neurtalNIDAQVal
    
    def SetNeutralVal(self, neutralVal):
        self.neurtalNIDAQVal = neutralVal