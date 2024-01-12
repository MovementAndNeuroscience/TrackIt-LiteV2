import json

def SetupValueRepository(dpg):
    with dpg.value_registry():
        dpg.add_int_value(default_value= 1, tag="blockNo")
        dpg.add_string_value(default_value="John Doe", tag="investName")
        dpg.add_int_value(default_value= 0, tag="subjectId")
        dpg.add_string_value(default_value= "Mouse", tag="device")
        dpg.add_bool_value(default_value = False, tag = "Mouse")
        dpg.add_bool_value(default_value = False, tag = "USBADAM")
        dpg.add_bool_value(default_value = False, tag = "NIDAQ")
        dpg.add_string_value(default_value= "Downwards", tag="forceDirection")
        dpg.add_bool_value(default_value = False, tag = "Downwards")
        dpg.add_bool_value(default_value = False, tag = "Upwards")
        dpg.add_string_value(default_value= "R300r P400 R200b P200", tag="writtenEvents")
        dpg.add_int_value(default_value= 1000, tag="stimDisplayTime")
        dpg.add_int_value(default_value= 2000, tag="baseDisplayTime")
        dpg.add_int_value(default_value= 2000, tag="pauseTime")
        dpg.add_int_value(default_value= 50, tag="stimHeight")
        dpg.add_int_value(default_value= 2000, tag="feedbackLength")
        dpg.add_int_value(default_value= 50, tag="percentOfMaxCal")
        dpg.add_bool_value(default_value = False, tag = "baseline")
        dpg.add_bool_value(default_value = False, tag = "randomTargets")
        dpg.add_bool_value(default_value = False, tag = "adaptiveDif")
        dpg.add_bool_value(default_value = False, tag = "guidelines")
        dpg.add_bool_value(default_value = False, tag = "randomTargetHeight")
        dpg.add_bool_value(default_value = False, tag = "ownSequence")
        dpg.add_bool_value(default_value = False, tag = "trainingMode")
        dpg.add_bool_value(default_value = False, tag = "TargetSustain")
        dpg.add_bool_value(default_value = False, tag = "moreTargets")
        dpg.add_bool_value(default_value = False, tag = "extrinsicMotivation")
        dpg.add_int_value(default_value= 80, tag="minCloseness")
        dpg.add_int_value(default_value= 800, tag="maxCloseness")
        dpg.add_int_value(default_value= 75, tag="addaptiveDifThreshold")
        dpg.add_int_value(default_value= 75, tag="trainingThreshold")
        dpg.add_int_value(default_value= 300, tag="sustainOnTarget")
        dpg.add_int_value(default_value= 2, tag="targetsOnScreen")
        dpg.add_bool_value(default_value = False, tag = "levels")
        dpg.add_bool_value(default_value = False, tag = "visScore")
        dpg.add_bool_value(default_value = False, tag = "highscore")
        dpg.add_bool_value(default_value = False, tag = "soundRew")
        dpg.add_bool_value(default_value = False, tag = "coinRew")
        dpg.add_int_value(default_value = 5, tag = "SetNumOfRandomEvents")
        dpg.add_int_value(default_value = 1, tag = "playerLevel")
        dpg.add_int_value(default_value = 20, tag = "minRandomHeight")
        dpg.add_int_value(default_value = 50, tag = "maxRandomHeight")
        dpg.add_int_value(default_value = 0, tag = "calibrationInput")
        dpg.add_double_value(default_value = 1.0, tag = "maxVoltage") 
        dpg.add_double_value(default_value = 500000.0, tag = "minVoltage")
        dpg.add_double_value(default_value = 5.0, tag = "absMaxVoltage")
        dpg.add_string_value(default_value= "Relative", tag="absOrRelVoltage")
        dpg.add_bool_value(default_value = False, tag = "Relative")
        dpg.add_bool_value(default_value = False, tag = "Absolute")
        dpg.add_string_value(default_value= "Pull", tag="pushPull")
        dpg.add_bool_value(default_value = False, tag = "push")
        dpg.add_bool_value(default_value = False, tag = "pull")
        dpg.add_string_value(default_value= "ai1", tag="nidaqCh")  
        dpg.add_bool_value(default_value = False, tag = "svipt")
        dpg.add_int_value(default_value = 0, tag = "noSviptTrials")
        dpg.add_int_value(default_value = 0, tag = "noSviptEvents")
        dpg.add_string_value(default_value = "COM6", tag = "comport")
        dpg.add_string_value(default_value = "COM3", tag = "biosemiComport")
        dpg.add_bool_value(default_value = False, tag = "Biosemi")
        dpg.add_string_value(default_value = "A0", tag = "analogIn")
        dpg.add_string_value(default_value = "Dynamic", tag = "experimentMode")
        dpg.add_bool_value(default_value = False, tag = "Dynamic")
        dpg.add_bool_value(default_value = False, tag = "Isometric")
        dpg.add_bool_value(default_value = True, tag = "sVIPTColors")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight1")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight2")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight3")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight4")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight5")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight6")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight7")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight8")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight9")
        dpg.add_int_value(default_value = dpg.get_value("stimHeight"), tag = "gateHeight10")
        dpg.add_int_value(default_value = 100, tag = "minIsometricCaliVal")




def SaveConfig(dpg):
    config = {
        "blockNo": str(dpg.get_value("blockNo")),
        "investName": str(dpg.get_value("investName")),
        "subjectId": str(dpg.get_value("subjectId")),
        "device": str(dpg.get_value("device")),
        "Mouse": str(dpg.get_value("Mouse")),
        "USBADAM": str(dpg.get_value("USBADAM")),
        "NIDAQ": str(dpg.get_value("NIDAQ")),
        "forceDirection": str(dpg.get_value("forceDirection")),
        "Downwards": str(dpg.get_value("Downwards")),
        "Upwards": str(dpg.get_value("Upwards")),      
        "writtenEvents": str(dpg.get_value("writtenEvents")),
        "stimDisplayTime": str(dpg.get_value("stimDisplayTime")),
        "baseDisplayTime": str(dpg.get_value("baseDisplayTime")),
        "pauseTime": str(dpg.get_value("pauseTime")),
        "stimHeight": str(dpg.get_value("stimHeight")),
        "feedbackLength": str(dpg.get_value("feedbackLength")),
        "percentOfMaxCal": str(dpg.get_value("percentOfMaxCal")),
        "baseline": str(dpg.get_value("baseline")),
        "randomTargets": str(dpg.get_value("randomTargets")),
        "adaptiveDif": str(dpg.get_value("adaptiveDif")),
        "guidelines": str(dpg.get_value("guidelines")),
        "randomTargetHeight": str(dpg.get_value("randomTargetHeight")),
        "ownSequence": str(dpg.get_value("ownSequence")),
        "trainingMode": str(dpg.get_value("trainingMode")),
        "TargetSustain": str(dpg.get_value("TargetSustain")),
        "moreTargets": str(dpg.get_value("moreTargets")),
        "extrinsicMotivation": str(dpg.get_value("extrinsicMotivation")),
        "minCloseness": str(dpg.get_value("minCloseness")),
        "maxCloseness": str(dpg.get_value("maxCloseness")),
        "SetNumOfRandomEvents": str(dpg.get_value("SetNumOfRandomEvents")),
        "addaptiveDifThreshold": str(dpg.get_value("addaptiveDifThreshold")),
        "trainingThreshold": str(dpg.get_value("trainingThreshold")),
        "sustainOnTarget": str(dpg.get_value("sustainOnTarget")),
        "targetsOnScreen": str(dpg.get_value("targetsOnScreen")),
        "levels": str(dpg.get_value("levels")),
        "visScore": str(dpg.get_value("visScore")),
        "highscore": str(dpg.get_value("highscore")),
        "soundRew": str(dpg.get_value("soundRew")),
        "coinRew": str(dpg.get_value("coinRew")),
        "playerLevel": str(dpg.get_value("playerLevel")),
        "minRandomHeight": str(dpg.get_value("minRandomHeight")),
        "maxRandomHeight": str(dpg.get_value("maxRandomHeight")),
        "calibrationInput": str(dpg.get_value("calibrationInput")),
        "maxVoltage": str(dpg.get_value("maxVoltage") ),
        "minVoltage": str(dpg.get_value("minVoltage") ),
        "absMaxVoltage": str(dpg.get_value("absMaxVoltage")),
        "absOrRelVoltage": str(dpg.get_value("absOrRelVoltage")),
        "Relative": str(dpg.get_value("Relative")),
        "Absolute": str(dpg.get_value("Absolute")),
        "pushPull": str(dpg.get_value("pushPull")),
        "pull": str(dpg.get_value("pull")),
        "push": str(dpg.get_value("push")),
        "nidaqCh": str(dpg.get_value("nidaqCh")),
        "svipt": str(dpg.get_value("svipt")),
        "noSviptTrials": str(dpg.get_value("noSviptTrials")), 
        "noSviptEvents": str(dpg.get_value("noSviptEvents")),  
        "comport": str(dpg.get_value("comport")),
        "biosemiComport": str(dpg.get_value("biosemiComport")),
        "Biosemi": str(dpg.get_value("Biosemi")),
        "analogIn": str(dpg.get_value("analogIn")),
        "experimentMode": str(dpg.get_value("experimentMode")),
        "Dynamic": str(dpg.get_value("Dynamic")),
        "Isometric": str(dpg.get_value("Isometric")),
        "sVIPTColors":str(dpg.get_value("sVIPTColors")),
        "gateHeight1":str(dpg.get_value("gateHeight1")),
        "gateHeight2":str(dpg.get_value("gateHeight2")),
        "gateHeight3":str(dpg.get_value("gateHeight3")),
        "gateHeight4":str(dpg.get_value("gateHeight4")),
        "gateHeight5":str(dpg.get_value("gateHeight5")),
        "gateHeight6":str(dpg.get_value("gateHeight6")),
        "gateHeight7":str(dpg.get_value( "gateHeight7")),
        "gateHeight8":str(dpg.get_value("gateHeight8")),
        "gateHeight9":str(dpg.get_value("gateHeight9")),
        "gateHeight10":str(dpg.get_value("gateHeight10")),
        "minIsometricCaliVal":str(dpg.get_value("minIsometricCaliVal"))

    }
    nameOfFile =  str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) +'_'+'conf.cfg'
    with open(nameOfFile, 'w') as c:
        c.write(json.dumps(config, indent=4))

def LoadConfig(dpg, app_data):
    file = open(app_data["file_path_name"], 'r')
    data = json.load(file)

    print(data['randomTargets'])
    print(bool(data['randomTargets']))
    
    dpg.configure_item("blockNo", default_value = int(data['blockNo']))
    dpg.configure_item("investName", default_value = data['investName'])
    dpg.configure_item("subjectId", default_value = int(data['subjectId']))
    dpg.configure_item("device", default_value = data['device'])
    dpg.configure_item("Mouse", default_value = (TrueOrFalse(data['Mouse'])))
    dpg.configure_item("USBADAM", default_value = (TrueOrFalse(data['USBADAM'])))
    dpg.configure_item("NIDAQ", default_value = (TrueOrFalse(data['NIDAQ'])))
    dpg.configure_item("forceDirection", default_value = data['forceDirection'])
    dpg.configure_item("Downwards", default_value = (TrueOrFalse(data['Downwards'])))
    dpg.configure_item("Upwards", default_value = (TrueOrFalse(data['Upwards'])))
    dpg.configure_item("writtenEvents", default_value = data['writtenEvents'])
    dpg.configure_item("stimDisplayTime", default_value = int(data['stimDisplayTime']))
    dpg.configure_item("baseDisplayTime", default_value = int(data['baseDisplayTime']))
    dpg.configure_item("pauseTime", default_value = int(data['pauseTime']))
    dpg.configure_item("stimHeight", default_value = int(data['stimHeight']))
    dpg.configure_item("feedbackLength", default_value = int(data['feedbackLength']))
    dpg.configure_item("percentOfMaxCal", default_value = int(data['percentOfMaxCal']))
    dpg.configure_item("baseline", default_value = (TrueOrFalse(data['baseline'])))
    dpg.configure_item("randomTargets", default_value = (TrueOrFalse(data['randomTargets'])))
    dpg.configure_item("adaptiveDif", default_value = (TrueOrFalse(data['adaptiveDif'])))
    dpg.configure_item("guidelines", default_value = (TrueOrFalse(data['guidelines'])))
    dpg.configure_item("randomTargetHeight", default_value = (TrueOrFalse(data['randomTargetHeight'])))
    dpg.configure_item("ownSequence", default_value = (TrueOrFalse(data['ownSequence'])))
    dpg.configure_item("trainingMode", default_value = (TrueOrFalse(data['trainingMode'])))
    dpg.configure_item("TargetSustain", default_value = (TrueOrFalse(data['TargetSustain'])))
    dpg.configure_item("moreTargets", default_value = (TrueOrFalse(data['moreTargets'])))
    dpg.configure_item("extrinsicMotivation", default_value = (TrueOrFalse(data['extrinsicMotivation'])))
    dpg.configure_item("minCloseness", default_value = int(data['minCloseness']))
    dpg.configure_item("maxCloseness", default_value = int(data['maxCloseness']))
    dpg.configure_item("SetNumOfRandomEvents", default_value = int(data['SetNumOfRandomEvents']))
    dpg.configure_item("addaptiveDifThreshold", default_value = int(data['addaptiveDifThreshold']))
    dpg.configure_item("trainingThreshold", default_value = int(data['trainingThreshold']))
    dpg.configure_item("sustainOnTarget", default_value = int(data['sustainOnTarget']))
    dpg.configure_item("targetsOnScreen", default_value = int(data['targetsOnScreen']))
    dpg.configure_item("levels", default_value = (TrueOrFalse(data['levels'])))
    dpg.configure_item("visScore", default_value = (TrueOrFalse(data['visScore'])))
    dpg.configure_item("highscore", default_value = (TrueOrFalse(data['highscore'])))
    dpg.configure_item("soundRew", default_value = (TrueOrFalse(data['soundRew'])))   
    dpg.configure_item("coinRew", default_value = (TrueOrFalse(data['coinRew'])))
    dpg.configure_item("playerLevel", default_value = int(data["playerLevel"])) 
    dpg.configure_item("minRandomHeight", default_value = int(data["minRandomHeight"]))
    dpg.configure_item("maxRandomHeight", default_value = int(data["maxRandomHeight"]))
    dpg.configure_item("calibrationInput", default_value = int(data["calibrationInput"]))
    dpg.configure_item("maxVoltage", default_value = float(data["maxVoltage"]))
    dpg.configure_item("minVoltage", default_value = float(data["minVoltage"]))
    dpg.configure_item("absMaxVoltage", default_value = float(data["absMaxVoltage"]))
    dpg.configure_item("absOrRelVoltage", default_value = data["absOrRelVoltage"])
    dpg.configure_item("Absolute", default_value = (TrueOrFalse(data['Absolute'])))
    dpg.configure_item("Relative", default_value = (TrueOrFalse(data['Relative'])))
    dpg.configure_item("pushPull", default_value = data["pushPull"])
    dpg.configure_item("push", default_value = (TrueOrFalse(data['push'])))
    dpg.configure_item("pull", default_value = (TrueOrFalse(data['pull'])))
    dpg.configure_item("nidaqCh", default_value = data["nidaqCh"])
    dpg.configure_item("svipt", default_value = (TrueOrFalse(data['svipt'])))
    dpg.configure_item("noSviptTrials", default_value = int(data["noSviptTrials"]))
    dpg.configure_item("noSviptEvents", default_value = int(data["noSviptEvents"]))
    dpg.configure_item("comport", default_value = data['comport'])
    dpg.configure_item("biosemiComport", default_value = data["biosemiComport"]),
    dpg.configure_item("Biosemi", default_value = (TrueOrFalse(data['Biosemi'])))
    dpg.configure_item("analogIn", default_value = data['analogIn'])
    dpg.configure_item("experimentMode", default_value = data['experimentMode'])
    dpg.configure_item("Dynamic", default_value = (TrueOrFalse(data["Dynamic"])))
    dpg.configure_item("Isometric", default_value = (TrueOrFalse(data["Isometric"])))
    dpg.configure_item("sVIPTColors", default_value = (TrueOrFalse(data['sVIPTColors'])))
    dpg.configure_item("gateHeight1", default_value = int(data["gateHeight1"]))
    dpg.configure_item("gateHeight2", default_value = int(data["gateHeight2"]))
    dpg.configure_item("gateHeight3", default_value = int(data["gateHeight3"]))
    dpg.configure_item("gateHeight4", default_value = int(data["gateHeight4"]))
    dpg.configure_item("gateHeight5", default_value = int(data["gateHeight5"]))
    dpg.configure_item("gateHeight6", default_value = int(data["gateHeight6"]))
    dpg.configure_item("gateHeight7", default_value = int(data["gateHeight8"]))
    dpg.configure_item("gateHeight8", default_value = int(data["gateHeight8"]))
    dpg.configure_item("gateHeight9", default_value = int(data["gateHeight9"]))
    dpg.configure_item("gateHeight10", default_value = int(data["gateHeight10"]))
    dpg.configure_item("minIsometricCaliVal", default_value = int(data["minIsometricCaliVal"]))

    TrasferForceDirectionToForceD(dpg)
    TransferDeviceToInputDevice(dpg)
    TransferAbsOrRelVoltageToAbsOrRelVol(dpg)
    TransfertrainingModeToexpTrainingMode(dpg)


def TrueOrFalse(data):
    if data == 'False':
        return False
    if data == 'True':
        return True
    
def TrasferForceDirectionToForceD(dpg):
    if dpg.get_value("Upwards") == True:
        dpg.set_value("forceDirection", "Upwards")
    if dpg.get_value("Downwards") == True:
        dpg.set_value("forceDirection", "Downwards")

def TransferDeviceToInputDevice(dpg):
    if dpg.get_value("Mouse") == True:
        dpg.set_value("device", "Mouse")
    if dpg.get_value("NIDAQ") == True:
        dpg.set_value("device", "NIDAQ")
    if dpg.get_value("USBADAM") == True:
        dpg.set_value("device", "USB/ADAM")

def TransferAbsOrRelVoltageToAbsOrRelVol(dpg):
    if dpg.get_value("Absolute") == True:
        dpg.set_value("absOrRelVoltage", "Absolute")
    if dpg.get_value("Relative") == True:
        dpg.set_value("absOrRelVoltage", "Relative")

def TransfertrainingModeToexpTrainingMode(dpg):
    if dpg.get_value("Dynamic") == True:
        dpg.set_value("ExperimentMode", "Dynamic")
    if dpg.get_value("Isometric") == True:
        dpg.set_value("ExperimentMode", "Isometric")
