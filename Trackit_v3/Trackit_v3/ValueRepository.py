


def SetupValueRepository(dpg):
    with dpg.value_registry():
        dpg.add_int_value(default_value= 1, tag="blockNo")
        dpg.add_string_value(default_value="John Doe", tag="investName")
        dpg.add_int_value(default_value= 0, tag="subjectId")
        dpg.add_string_value(default_value= "Mouse", tag="device")
        dpg.add_string_value(default_value= "R300r, P400, R200b, P200", tag="writtenEvents")
        dpg.add_int_value(default_value= 200, tag="stimDisplayTime")
        dpg.add_int_value(default_value= 50, tag="stimHeight")
        dpg.add_string_value(default_value= "1 2 3 5", tag="rectsWithTriggers")
        dpg.add_string_value(default_value= "1 1 1 2", tag="triggerValues")
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
        dpg.add_int_value(default_value= 200, tag="minCloseness")
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