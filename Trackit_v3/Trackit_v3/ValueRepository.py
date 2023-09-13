import json

def SetupValueRepository(dpg):
    with dpg.value_registry():
        dpg.add_int_value(default_value= 1, tag="blockNo")
        dpg.add_string_value(default_value="John Doe", tag="investName")
        dpg.add_int_value(default_value= 0, tag="subjectId")
        dpg.add_string_value(default_value= "Mouse", tag="device")
        dpg.add_string_value(default_value= "Downwards", tag="forceDirection")
        dpg.add_string_value(default_value= "R300r P400 R200b P200", tag="writtenEvents")
        dpg.add_int_value(default_value= 1000, tag="stimDisplayTime")
        dpg.add_int_value(default_value= 2000, tag="baseDisplayTime")
        dpg.add_int_value(default_value= 2000, tag="pauseTime")
        dpg.add_int_value(default_value= 50, tag="stimHeight")
        dpg.add_double_value(default_value= 2.2, tag="feedbackLength")
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
        dpg.add_int_value(default_value= 100, tag="minCloseness")
        dpg.add_int_value(default_value= 400, tag="maxCloseness")
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
        dpg.add_int_value(default_value = 50, tag = "minRandomHeight")
        dpg.add_int_value(default_value = 100, tag = "maxRandomHeight")
        dpg.add_int_value(default_value = 0, tag = "calibrationInput")
        dpg.add_double_value(default_value = 1.0, tag = "maxVoltage") 
        dpg.add_double_value(default_value = 0.0, tag = "minVoltage")
        dpg.add_double_value(default_value = 5.0, tag = "absMaxVoltage")
        dpg.add_string_value(default_value= "Relative", tag="absOrRelVoltage")
        dpg.add_string_value(default_value= "ai1", tag="nidaqCh")  


def SaveConfig(dpg):
    config = {
        "blockNo": str(dpg.get_value("blockNo")),
        "investName": str(dpg.get_value("investName")),
        "subjectId": str(dpg.get_value("subjectId")),
        "device": str(dpg.get_value("device")),
        "forceDirection": str(dpg.get_value("forceDirection")),
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
        "nidaqCh": str(dpg.get_value("nidaqCh"))
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
    dpg.configure_item("forceDirection", default_value = data['forceDirection'])
    dpg.configure_item("writtenEvents", default_value = data['writtenEvents'])
    dpg.configure_item("stimDisplayTime", default_value = int(data['stimDisplayTime']))
    dpg.configure_item("baseDisplayTime", default_value = int(data['baseDisplayTime']))
    dpg.configure_item("pauseTime", default_value = int(data['pauseTime']))
    dpg.configure_item("stimHeight", default_value = int(data['stimHeight']))
    dpg.configure_item("feedbackLength", default_value = float(data['feedbackLength']))
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
    dpg.configure_item("nidaqCh", default_value = data["nidaqCh"])


def TrueOrFalse(data):
    if data == 'False':
        return False
    if data == 'True':
        return True