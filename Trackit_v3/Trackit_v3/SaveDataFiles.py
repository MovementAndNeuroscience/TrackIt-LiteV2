import dearpygui.dearpygui as dpg
import datetime
import os
import shutil

def SaveDataToFile(events, inputs, meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets, dpg):
    file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_Events"
    with open('{}.txt'.format(file_name), 'w') as r:
        r.write("Rect_no\tEventType\tTrigger\tHeight\tPosition\ttotal_time_visible\t Visible_From" +
                "\tEntry_time(ms)\tTime_on_target(ms)\tSD_outside_Target(px)\tMean_Inaccuracy(px_outside_target)\tExit_time(ms)"+
                "\tPercent_Time_On_Target(%)\tReaction_Time(ms)\ttime_Off_Target(ms)\t overshoot?"+
                "\t overshoot_time\t undershoot?\t undershoot_time\n")
        for i , evt in enumerate(events):
            r.write("{i}\t{evt}\t{tr}\t{h}\t{pos}\t{ttv}\t{vf}\t{et}\t{tot}\t{sd}\t{inac}\t{ext}\t{ptot}\t{rt}\t{tofft}\t{os}\t{ost}\t{us}\t{ust}\n".format
                (i=events[i].targetId, evt=events[i].eventType, tr=events[i].targetTrigger,
                    h = events[i].targetHeight, pos = events[i].targetPosition, ttv = events[i].targetTotalTime, 
                    vf = events[i].targetVisibleFromTime ,et=events[i].targetEntryTime, 
                    tot=events[i].timeOnTarget,sd= events[i].stdOfInput
                    ,inac= events[i].meanDistanceAwayFromTarget, 
                    ext=events[i].targetExitTime, ptot = events[i].percentTimeOnTarget, rt = events[i].reactionTime, 
                    tofft= events[i].timeOffTarget, os = events[i].overshoot, ost = events[i].overshootTime,
                    us = events[i].undershoot, ust = events[i].undershootTime))
                
    file_name_inputdata = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_InputData"
    with open('{}.txt'.format(file_name_inputdata), 'w') as r:
        r.write("Digital_Input\tScreen_Position_Y_axis(px)\ttime(ms)\n")
        for i , evt in enumerate(inputs):
            r.write("{di}\t{sp}\t{t}\n".format
                (di=inputs[i].digitalInput, sp=inputs[i].screenPosY ,t=inputs[i].time))

    file_name_statistic = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_Statistics"
    with open('{}.txt'.format(file_name_statistic), 'w') as r:
        r.write("Mean_Accuracy\t Std_Accuracy\tMean_Time_On_Target\t Std_Time_On_Target\t Total_Time_On_Target\n")
        r.write("{macc}\t{sacc}\t{mtot}\t{stot}\t{ttot}\n".format
            (macc=meanAccuracy, sacc=stdAccuracy, mtot = meanTimeOnTarget, stot = stdTimeOnTarget,ttot = totalTimeOnTargets))             
                    
    try:
        dir_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId"))+'_'+ str(dpg.get_value("blockNo"))
        new_dir = os.path.join(os.getcwd(), dir_name)
        os.mkdir(new_dir)
        conf_name = str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) +'_'+'conf.cfg'
        shutil.copyfile(conf_name, os.path.join(new_dir, conf_name))
        shutil.move(file_name + '.txt', os.path.join(new_dir, file_name + '.txt'))
        shutil.move(file_name_inputdata + '.txt', os.path.join(new_dir, file_name_inputdata + '.txt'))
        shutil.move(file_name_statistic + '.txt', os.path.join(new_dir, file_name_statistic + '.txt'))
        print ('Results saved in the following folder: {}'.format(dir_name))
    except Exception as e:
        print(e)
        raise