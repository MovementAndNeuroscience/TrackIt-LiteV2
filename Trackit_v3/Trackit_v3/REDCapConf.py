class REDCapConf():
    def __init__(self):
        self.tokenString = ""
        self.subjectId = 0
        self.ReportNo = 0
        self.varName = ""
        self.armName = ""

    def __init__(self, tokenstring, subjectId, reportNo, varName, armName):
        self.tokenString = tokenstring
        self.subjectId = subjectId
        self.ReportNo = reportNo
        self.varName = varName
        self.armName = armName