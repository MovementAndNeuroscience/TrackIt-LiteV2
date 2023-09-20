class SviptBlock():
    noTrials = 0
    trials = []
    
    def __init__(self, noTrials):
        self.noTrials = noTrials
    
    def AddTrial(self, sviptTrial):
        self.trials.append(sviptTrial)
