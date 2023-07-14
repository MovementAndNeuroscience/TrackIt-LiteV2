#Trackit_v3_mainmenu
import dearpygui.dearpygui as dpg
import webbrowser
import ValueRepository as valRep

subjectId = dpg.mvInputInt

def save_callback():
    print("Save Clicked" + str(dpg.get_value("subjectId")) + " \ndevice : " + dpg.get_value("device"))
    
def start_game():
    print("starting game")

def load_configuration():
    print("load configuration")

def Start_Calibration():
    print("calibraiton started")

def import_events():
    print("importing events")

def quit_trackit():
    dpg.destroy_context()

def _configuration_menu():
    with dpg.window(label="Base Configuration", pos=[0,50]):

        with dpg.group(horizontal=True):
            dpg.add_input_int(label="Subject ID",width=125, source="subjectId")
            dpg.add_input_text(label="Investigator Name", width=250,indent= 250, source= "investName")
            dpg.add_input_int(label="Block No", width= 100,indent= 675, source= "blockNo")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_text("Input Device")
            dpg.add_radio_button(("Mouse", "USB/ADAM", "NIDAQ"), callback= save_callback, horizontal=True, source="device")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_input_text(label="TrackIt Events", width=500, source= "writtenEvents")
            dpg.add_button(label= "import event file", callback= import_events)

        dpg.add_text("R=Rectancle, P=Pause, b=blue, g=green,\ny=yellow, v=violet, r=red, p=pink, c=cyan, f=black ")
        dpg.add_input_int(label="stimuli display time (ms)", width=200, source= "stimDisplayTime")
        dpg.add_input_int(label="stimuli height (px)", width=200, source= "stimHeight")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_input_text(label="Rectangle to have triggers. \nwrite their order number \nseperate with spaces", width=200, source="rectsWithTriggers")
            dpg.add_input_text(label="Trigger values. \none per event, \nseperate by space", width=200, source="triggerValues")

        dpg.add_input_double(label= "Feedback screen, time in seconds (0 = non)", width=200, source="feedbackLength")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_text("Max input Calibration")
            dpg.add_button(label="Start Calibration", width=200, callback=Start_Calibration)
            dpg.add_input_int(label="% of maximum input", width=100, source= "percentOfMaxCal")

def _game_configuration_menu():
    with dpg.window(label="Game Configuration", pos=[0,50]):
        dpg.add_text("Choose Game Properties")
        dpg.add_checkbox(label="Return To Baseline", source = "baseline")

        with dpg.group(horizontal=True,horizontal_spacing= 148): 
            dpg.add_checkbox(label="Random Target Position", source = "randomTargets")
            dpg.add_button(label= "Configure",callback=_rand_target_conf)

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_checkbox(label="Adaptive Difficulty - \nadaptive target closeness and height", source="adaptiveDif")
            dpg.add_button(label= "Configure", callback=_adaptive_conf)
        
        dpg.add_checkbox(label="In game guidelines", source="guidelines")
        dpg.add_checkbox(label="Radnom target height", source="randomTargetHeight")
        dpg.add_checkbox(label="Write Your Own Sequence", source= "ownSequence")
        
        with dpg.group(horizontal=True,horizontal_spacing= 213): 
            dpg.add_checkbox(label="Training mode", source="trainingMode")
            dpg.add_button(label= "Configure", callback=_training_conf)
        
        dpg.add_checkbox(label="SVIPT - show all targets")

        with dpg.group(horizontal=True,horizontal_spacing= 135): 
            dpg.add_checkbox(label="Target sustain on screen", source="TargetSustain")
            dpg.add_button(label= "Configure", callback=_targ_sustein_conf)

        with dpg.group(horizontal=True,horizontal_spacing= 142): 
            dpg.add_checkbox(label="Show certain amount of \ntargets at a time", source= "moreTargets")
            dpg.add_button(label= "Configure", callback=_visible_targs_conf)

        with dpg.group(horizontal=True,horizontal_spacing= 162): 
            dpg.add_checkbox(label="Extrinsic motivation", source= "extrinsicMotivation")
            dpg.add_button(label= "Configure", callback=_extrinsic_mot_conf)   

def _rand_target_conf():
     with dpg.window(label="Random Target Configuration", pos=[450,50]):
        dpg.add_input_int(label="Min cloeseness in px", width= 100, source= "minCloseness")
        dpg.add_input_int(label="Maz cloeseness in px", width= 100, source= "maxCloseness")

def _adaptive_conf():
     with dpg.window(label="Adaptive Difficulty Configuration", pos=[450,50]):
        dpg.add_input_int(label="% accuracy threshold \nto increase level", width= 100, source="addaptiveDifThreshold")

def _training_conf():
     with dpg.window(label="Training Mode Configuration", pos=[450,50]):
        dpg.add_input_int(label="% accuracy threshold \nto beat training mode", width= 100, source="trainingThreshold")

def _targ_sustein_conf():
     with dpg.window(label="Target Sustain Configuration", pos=[450,50]):
        dpg.add_input_int(label="time on target in ms", width= 100, source="sustainOnTarget")

def _visible_targs_conf():
     with dpg.window(label="Visible Targets Configuration", pos=[450,50]):
        dpg.add_input_int(label="amount of targets \non screen", width= 100, source="targetsOnScreen")

def _extrinsic_mot_conf():
     with dpg.window(label="Extrinsic Motivation Configuration", pos=[450,50]):
        dpg.add_checkbox(label="Levels", source="levels")
        dpg.add_checkbox(label="Visible Score", source="visScore")
        dpg.add_checkbox(label="Highscore", source="highscore")
        dpg.add_checkbox(label="Sound reward", source="soundRew")
        dpg.add_checkbox(label="Coin reward", source="coinRew")

dpg.create_context()

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 20,20, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(85,82,93,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,(85,82,93,255), category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

valRep.SetupValueRepository(dpg)

#dpg.show_style_editor()

dpg.create_viewport(title= "Trackit_v3", width= 1025, height= 800)
dpg.setup_dearpygui()

with dpg.window(label="Trackit V3",min_size=[1000,50]):
    with dpg.menu_bar():

        with dpg.menu(label="Home menu"):

            dpg.add_menu_item(label="Start Trackit", callback= start_game)
            dpg.add_menu_item(label="Save Configuration", callback= save_callback)
            dpg.add_menu_item(label="Load Configuration", callback= load_configuration)
            dpg.add_menu_item(label="Quit Trackit_v3", callback= quit_trackit)

        with dpg.menu(label="Configuration"):

            dpg.add_menu_item(label="Show Base Configuration", callback= _configuration_menu)
            dpg.add_menu_item(label="Show Game Configuration", callback= _game_configuration_menu)
    

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()