import dearpygui.dearpygui as dpg
import datetime
import os
import shutil

def SaveDataToFile(events, inputs, meanAccuracy, stdAccuracy, meanTimeOnTarget, stdTimeOnTarget, totalTimeOnTargets, gameTimeCounter, dpg):
    errors = 0
    file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_Events"
    with open('{}.txt'.format(file_name), 'w') as r:
        r.write("Rect_no\tEventType\tTrigger\tHeight\tPosition\ttotal_time_visible\t Visible_From" +
                "\tEntry_time_ms\t Calculated_Entry_time\tTime_on_target_ms\tSD_outside_Target_px\tMean_Inaccuracy_px_outside_target\tExit_time_ms"+
                "\tPercent_Time_On_Target\tReaction_Time_ms\ttime_Off_Target_ms\t overshoot?"+
                "\t overshoot_time\t undershoot?\t undershoot_time\n")
        for i , evt in enumerate(events):
            r.write("{i}\t{evt}\t{tr}\t{h}\t{pos}\t{ttv}\t{vf}\t{et}\t{cet}\t{tot}\t{sd}\t{inac}\t{ext}\t{ptot}\t{rt}\t{tofft}\t{os}\t{ost}\t{us}\t{ust}\n".format
                (i=events[i].targetId, evt=events[i].eventType, tr=events[i].targetTrigger,
                    h = events[i].targetHeight, pos = events[i].targetPosition, ttv = events[i].targetTotalTime, 
                    vf = events[i].targetVisibleFromTime ,et=events[i].targetEntryTime, cet = events[i].targetEntryTime - events[i].targetVisibleFromTime,
                    tot=events[i].timeOnTarget,sd= events[i].stdOfInput
                    ,inac= events[i].meanDistanceAwayFromTarget, 
                    ext=events[i].targetExitTime, ptot = events[i].percentTimeOnTarget, rt = events[i].reactionTime, 
                    tofft= events[i].timeOffTarget, os = events[i].overshoot, ost = events[i].overshootTime,
                    us = events[i].undershoot, ust = events[i].undershootTime))
            if events[i].undershoot == True or events[i].overshoot == True:
                errors += 1
                
    file_name_inputdata = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_InputData"
    with open('{}.txt'.format(file_name_inputdata), 'w') as r:
        r.write("Digital_Input\tScreen_Position_Y_axis(px)\ttime(ms)\n")
        for i , evt in enumerate(inputs):
            r.write("{di}\t{sp}\t{t}\n".format
                (di=inputs[i].digitalInput, sp=inputs[i].screenPosY ,t=inputs[i].time))

    file_name_statistic = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_Statistics"
    with open('{}.txt'.format(file_name_statistic), 'w') as r:
        r.write("Mean_Accuracy\t Std_Accuracy\tMean_Time_On_Target\t Std_Time_On_Target\t Total_Time_On_Target\t CompletionTime\t errors\n")
        r.write("{macc}\t{sacc}\t{mtot}\t{stot}\t{ttot}\t{ct}\t{err}\n".format
            (macc=meanAccuracy, sacc=stdAccuracy, mtot = meanTimeOnTarget, stot = stdTimeOnTarget,ttot = totalTimeOnTargets, ct = gameTimeCounter, err = errors))             
                    
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

def SaveSviptDataToFiles(dpg, trials, inputs):
    file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_SVIPTEvents"
    with open('{}.txt'.format(file_name), 'w') as r:
        r.write("Rect_no\tEventType\tTrigger\tHeight\tPosition\ttotal_time_visible\t Visible_From" +
                "\tEntry_time_ms\tCalculated_Entry_time\tTime_on_target_ms\tSD_outside_Target(px)\tMean_Inaccuracy(px_outside_target)\tExit_time(ms)"+
                "\tPercent_Time_On_Target(%)\tReaction_Time(ms)\ttime_Off_Target(ms)\t overshoot?"+
                "\t overshoot_time\t undershoot?\t undershoot_time\n")
            
        for trialindex , evt in enumerate(trials):
            for i, evt in enumerate(trials[trialindex].events):
                r.write("{i}\t{evt}\t{tr}\t{h}\t{pos}\t{ttv}\t{vf}\t{et}\t{cet}\t{tot}\t{sd}\t{inac}\t{ext}\t{ptot}\t{rt}\t{tofft}\t{os}\t{ost}\t{us}\t{ust}\n".format
                    (i=trials[trialindex].events[i].targetId, evt=trials[trialindex].events[i].eventType, tr=trials[trialindex].events[i].targetTrigger,
                        h = trials[trialindex].events[i].targetHeight, pos = trials[trialindex].events[i].targetPosition, ttv = trials[trialindex].events[i].targetTotalTime, 
                        vf = trials[trialindex].events[i].targetVisibleFromTime ,et=trials[trialindex].events[i].targetEntryTime, cet = trials[trialindex].events[i].targetEntryTime - trials[trialindex].events[i].targetVisibleFromTime,
                        tot=trials[trialindex].events[i].timeOnTarget,sd= trials[trialindex].events[i].stdOfInput
                        ,inac= trials[trialindex].events[i].meanDistanceAwayFromTarget, 
                        ext=trials[trialindex].events[i].targetExitTime, ptot = trials[trialindex].events[i].percentTimeOnTarget, rt = trials[trialindex].events[i].reactionTime, 
                        tofft= trials[trialindex].events[i].timeOffTarget, os = trials[trialindex].events[i].overshoot, ost = trials[trialindex].events[i].overshootTime,
                        us = trials[trialindex].events[i].undershoot, ust = trials[trialindex].events[i].undershootTime))
    
    file_name_svipt = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_SVIPTTrials"
    with open('{}.txt'.format(file_name_svipt), 'w') as r:
        r.write("Trial_no\tCompletionTime\tError\n")
        for i , evt in enumerate(trials):
            r.write("{i}\t{comp}\t{err}\n".format
                (i=trials[i].trialno, comp=trials[i].completionTime, err=trials[i].error))
                    
    file_name_inputdata = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_InputData"
    with open('{}.txt'.format(file_name_inputdata), 'w') as r:
        r.write("Digital_Input\tScreen_Position_Y_axis(px)\ttime(ms)\n")
        for i , evt in enumerate(inputs):
            r.write("{di}\t{sp}\t{t}\n".format
                (di=inputs[i].digitalInput, sp=inputs[i].screenPosY ,t=inputs[i].time))
                        
    try:
        dir_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId"))+'_'+ str(dpg.get_value("blockNo"))
        new_dir = os.path.join(os.getcwd(), dir_name)
        os.mkdir(new_dir)
        conf_name = str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) +'_'+'conf.cfg'
        shutil.copyfile(conf_name, os.path.join(new_dir, conf_name))
        shutil.move(file_name + '.txt', os.path.join(new_dir, file_name + '.txt'))
        shutil.move(file_name_svipt + '.txt', os.path.join(new_dir, file_name_svipt + '.txt'))
        shutil.move(file_name_inputdata + '.txt', os.path.join(new_dir, file_name_inputdata + '.txt'))
        print ('Results saved in the following folder: {}'.format(dir_name))
    except Exception as e:
        print(e)
        raise

def SaveSideQuestDataToFiles(dpg, trials, inputs):
    file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_SideQuestGates"
    with open('{}.txt'.format(file_name), 'w') as r:
        r.write("Rect_no\tEventType\tTrigger\tHeight\tPosition" +
                "\tEntry_time_ms\tTime_on_target_ms\tSD_outside_Target(px)\tMean_Inaccuracy(px_outside_target)\tExit_time(ms)"+
                "\tPercent_Time_On_Target(%)\tReaction_Time(ms)\ttime_Off_Target(ms)\t overshoot?"+
                "\t overshoot_time\t undershoot?\t undershoot_time\n")
            
        for trialindex , evt in enumerate(trials):
            for i, evt in enumerate(trials[trialindex].events):
                r.write("{i}\t{evt}\t{tr}\t{h}\t{pos}\t{et}\t{tot}\t{sd}\t{inac}\t{ext}\t{ptot}\t{rt}\t{tofft}\t{os}\t{ost}\t{us}\t{ust}\n".format
                    (i=trials[trialindex].events[i].targetId, evt=trials[trialindex].events[i].eventType, tr=trials[trialindex].events[i].targetTrigger,
                        h = trials[trialindex].events[i].targetHeight, pos = trials[trialindex].events[i].targetPosition, 
                        et=trials[trialindex].events[i].targetEntryTime,
                        tot=trials[trialindex].events[i].timeOnTarget,sd= trials[trialindex].events[i].stdOfInput
                        ,inac= trials[trialindex].events[i].meanDistanceAwayFromTarget, 
                        ext=trials[trialindex].events[i].targetExitTime, ptot = trials[trialindex].events[i].percentTimeOnTarget, rt = trials[trialindex].events[i].reactionTime, 
                        tofft= trials[trialindex].events[i].timeOffTarget, os = trials[trialindex].events[i].overshoot, ost = trials[trialindex].events[i].overshootTime,
                        us = trials[trialindex].events[i].undershoot, ust = trials[trialindex].events[i].undershootTime))

    file_name_statistic = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_SideQuestTrials"
    with open('{}.txt'.format(file_name_statistic), 'w') as r:
        r.write("Mean_Accuracy\t Std_Accuracy\tMean_Time_On_Target\t Std_Time_On_Target\t Total_Time_On_Target\t Time_between_Trial\t errors\n")
        for i , evt in enumerate(trials):
            r.write("{macc}\t{sacc}\t{mtot}\t{stot}\t{ttot}\t{tbt}\t{err}\n".format
            (macc=trials[i].meanAccuracy, sacc=trials[i].stdAccuracy, mtot = trials[i].meanTimeOnTarget, stot = trials[i].stdTimeOnTarget,ttot = trials[i].totalTimeOnTargets, tbt = trials[i].timeBetweenTrials, err = trials[i].error))     
                    
    file_name_inputdata = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) + "_InputData"
    with open('{}.txt'.format(file_name_inputdata), 'w') as r:
        r.write("Digital_Input\tScreen_Position_Y_axis(px)\ttime(ms)\n")
        for i , evt in enumerate(inputs):
            r.write("{di}\t{sp}\t{t}\n".format
                (di=inputs[i].digitalInput, sp=inputs[i].screenPosY ,t=inputs[i].time))
                        
    try:
        dir_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_' + str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId"))+'_'+ str(dpg.get_value("blockNo"))
        new_dir = os.path.join(os.getcwd(), dir_name)
        os.mkdir(new_dir)
        conf_name = str(dpg.get_value("investName")) + '_'+ str(dpg.get_value("subjectId")) +'_'+ str(dpg.get_value("blockNo")) +'_'+'conf.cfg'
        shutil.copyfile(conf_name, os.path.join(new_dir, conf_name))
        shutil.move(file_name + '.txt', os.path.join(new_dir, file_name + '.txt'))
        shutil.move(file_name_statistic + '.txt', os.path.join(new_dir, file_name_statistic + '.txt'))
        shutil.move(file_name_inputdata + '.txt', os.path.join(new_dir, file_name_inputdata + '.txt'))
        print ('Results saved in the following folder: {}'.format(dir_name))
    except Exception as e:
        print(e)
        raise

