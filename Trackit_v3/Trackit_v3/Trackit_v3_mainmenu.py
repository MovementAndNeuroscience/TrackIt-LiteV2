#Trackit_v3_mainmenu
import dearpygui.dearpygui as dpg
import ValueRepository as valRep
import Calibrationdata as caliDat
import CalibrationConductor as caliConductor
import AdaptiveDifficultyConductor as adaptDifConductor
import GameConductor
import Eventsdata
import EventData 
import EventDataGenerator
import TriggerGenerator

calibrationData = caliDat.Calibrationdata()
eventsData = Eventsdata.EventsData()


def save_configuration():

    valRep.SaveConfig(dpg)
    
def start_game():
    print("starting game")
    print(calibrationData.GetMaxInput())

    if dpg.get_value("adaptiveDif") == True:
        adaptDifConductor.changeDifficulty(dpg)
        
    eventsData = EventDataGenerator.GenerateEvents(dpg)
    eventsData = TriggerGenerator.GenerateTriggers(eventsData)
    
    print(str(len(eventsData.eventDatas)) + " amount of data ")
    GameConductor.RunGame(dpg,eventsData)

def load_configuration(sender, app_data):
    
    valRep.LoadConfig(dpg, app_data)     

def Start_Calibration():
    caliConductor.RunCalibration(dpg,calibrationData)
    dpg.set_value("calibrationInput", calibrationData.maxinput)
    dpg.set_value("maxVoltage", calibrationData.maxVoltage) 
    dpg.set_value("minVoltage", calibrationData.minVoltage) 

def quit_trackit():
    dpg.destroy_context()

def Import_event_callback(sender, app_data):
        data = open(app_data["file_path_name"], 'r')
        dpg.configure_item("writtenEvents", default_value = data.read())

def _configuration_menu():

    with dpg.file_dialog(directory_selector=False, show=False, callback=Import_event_callback, id="importEventWindow", width=700 ,height=400):
        dpg.add_file_extension(".txt")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[TrackItv3_Events]")   

    with dpg.window(label="Base Configuration", pos=[0,50]):

        with dpg.group(horizontal=True):
            dpg.add_input_int(label="Subject ID",width=125, source="subjectId")
            dpg.add_input_text(label="Investigator Name", width=250,indent= 250, source= "investName")
            dpg.add_input_int(label="Block No", width= 100,indent= 675, source= "blockNo")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_text("Input Device")
            dpg.add_radio_button(("Mouse", "USB/ADAM", "NIDAQ"), horizontal=True, source="device")
            dpg.add_input_text(label="NIDAQ input channel", width=50,indent= 450, source= "nidaqCh")
        
        with dpg.group(horizontal=True,horizontal_spacing= 50):   
            dpg.add_text("Direction of the force")
            dpg.add_radio_button(("Downwards","Upwards"), horizontal=True, source="forceDirection")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_input_text(label="TrackIt Events", width=500, source= "writtenEvents")
            dpg.add_button(label= "import event file", callback=lambda: dpg.show_item("importEventWindow"))

        dpg.add_text("R=Rectancle, P=Pause, b=blue, g=green,\ny=yellow, v=violet, r=red, p=pink, c=cyan, f=black, o=orange ")
        
        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_input_int(label="stimuli display time (ms)", width=125, source= "stimDisplayTime")
            dpg.add_input_int(label="Baseline display time (ms)", width=125, source= "baseDisplayTime")
            dpg.add_input_int(label="Pause time (ms)", width=125, source= "pauseTime")

        dpg.add_input_int(label="stimuli height (px)", width=125, source= "stimHeight")

        dpg.add_input_double(label= "Feedback screen, time in seconds (0 = non)", width=125, source="feedbackLength")
       
        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_text("Absolute or Relative (calibrated) Maximum Voltage")
            dpg.add_radio_button(("Absolute", "Relative"), horizontal=True, source="absOrRelVoltage")

        with dpg.group(horizontal=True,horizontal_spacing= 50):
            dpg.add_text("Max input Calibration")
            dpg.add_button(label="Start Calibration", width=200, callback=Start_Calibration)
            dpg.add_input_int(label="% of maximum input", width=100, source= "percentOfMaxCal")
            dpg.add_input_double(label="Absolute Max input voltage", width=100, source = "absMaxVoltage")



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
        
        dpg.add_checkbox(label="SVIPT - show all targets")#need its own variable 

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
        dpg.add_input_int(label="Max cloeseness in px", width= 100, source= "maxCloseness")
        dpg.add_input_int(label="Number of Events", width= 100, source= "SetNumOfRandomEvents")


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
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(57,62,73,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,(83,83,99,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvStyleVar_WindowRounding, 10, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,(9,13,32,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg,(5,7,18,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg,(8,11,25,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border,(61,72,122,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow,(24,34,84,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,(45,65,150,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,(74,95,196,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg,(0,0,0,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,(20,64,134,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,(15,15,70,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,(122,139,217,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(37,50,110,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(45,65,150,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header,(51,51,55,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(34,56,120,255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,(0,119,200,255), category=dpg.mvThemeCat_Core)


dpg.bind_theme(global_theme)

valRep.SetupValueRepository(dpg)



dpg.create_viewport(title= "Trackit_v3", width= 1050, height= 800)
dpg.setup_dearpygui()
#dpg.show_style_editor()
with dpg.file_dialog(directory_selector=False, show=False, callback=load_configuration, id="loadConfigWindow", width=700 ,height=400):
    dpg.add_file_extension(".cfg")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension(".cfg", color=(0, 255, 0, 255), custom_text="[TRackItv3_Config]")   

with dpg.window(label="Trackit V3",min_size=[1028,50]):
    with dpg.menu_bar():

        with dpg.menu(label="Home menu"):

            dpg.add_menu_item(label="Start Trackit", callback= start_game)
            dpg.add_menu_item(label="Save Configuration", callback= save_configuration)
            dpg.add_menu_item(label="Load Configuration", callback=lambda: dpg.show_item("loadConfigWindow"))
            dpg.add_menu_item(label="Quit Trackit_v3", callback= quit_trackit)

        with dpg.menu(label="Configuration"):

            dpg.add_menu_item(label="Show Base Configuration", callback= _configuration_menu)
            dpg.add_menu_item(label="Show Game Configuration", callback= _game_configuration_menu)
    

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()