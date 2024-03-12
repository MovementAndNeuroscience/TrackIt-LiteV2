import pygame 
from win32api import GetSystemMetrics
import SerialBoardAPI
import VoltageConverter
import daqmxlib
import serial
import numpy as np

#Calibraition Input calculations 


def DetermineADAMOutputCalibration(calibrationDataClass, voltage, ypos, experimentalMode, pushPull):
        

        if experimentalMode == "Isometric" and pushPull == "Pull":
           ypos=VoltageConverter.get_px_from_Pulling_Iso_calibration(voltage, calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        
        if experimentalMode == "Isometric" and pushPull == "Push":
            if voltage <= 0.0:
               voltage = 0.01
            ypos=VoltageConverter.get_px_from_Potentiometer_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        
        if experimentalMode == "Dynamic":
            if voltage <= 0.0:
               voltage = 0.01
            ypos=VoltageConverter.get_px_from_Potentiometer_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        
        print ("YPOS = " + str(ypos))
        return ypos


def CalibrationInputCalculations(inputMode, serialObj, calibrationDataClass, experimentalMode, forcedirection, reader, smoothingFilter, minIsoCalibrationValue, pushPull):
                
    if inputMode == "Mouse":
        mx,my=pygame.mouse.get_pos()
        feedbackVoltage = my
        if(my > calibrationDataClass.GetMaxInput()):
            calibrationDataClass.SetMaxInput(my)
        
        return(my, calibrationDataClass, feedbackVoltage)
            
    if inputMode == "USB/ADAM":
        voltage = 0 
        if experimentalMode == "Dynamic":
            voltage = SerialBoardAPI.GetPotValue(serialObj)
            voltage = int(voltage)        
            calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage_ADAM(voltage, calibrationDataClass)
            smoothingFilter.InsertInput(voltage)
            voltage = smoothingFilter.AverageInput()
        if experimentalMode == "Isometric":
            voltage = SerialBoardAPI.GetLoaValue(serialObj)
            voltage = int(voltage)
            voltage = np.round(voltage/10)
            smoothingFilter.InsertInput(voltage)
            voltage = smoothingFilter.AverageInput()
            # include pushing / pulling in frontend
            # if pushing do the thing below 
            if pushPull == "Push":
                if voltage > minIsoCalibrationValue:
                   calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage_ADAM(voltage, calibrationDataClass)
            if pushPull == "Pull":
                if voltage < minIsoCalibrationValue:
                   calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage_ADAM(voltage, calibrationDataClass)
        ypos=0 #USB/ADAM input goes here 
        feedbackVoltage = voltage

        if forcedirection == "Downwards":
            ypos = DetermineADAMOutputCalibration(calibrationDataClass, voltage, ypos, experimentalMode, pushPull)
        elif forcedirection == "Upwards":
            ypos = DetermineADAMOutputCalibration(calibrationDataClass, voltage, ypos, experimentalMode, pushPull)
            ypos = GetSystemMetrics(1) - ypos
                
        if(ypos > calibrationDataClass.GetMaxInput()):
            calibrationDataClass.SetMaxInput(ypos)
            
        return(ypos, calibrationDataClass, feedbackVoltage)

    if inputMode == "NIDAQ":
        voltage = reader.read()[0]
        voltage = abs(voltage)
        ypos=0
        calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage(voltage, calibrationDataClass)
        feedbackVoltage = voltage
        if forcedirection == "Downwards":
            ypos=VoltageConverter.get_px_from_NIDAQ_Potentiometer_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage()) # Edited to work with external potentiometer through NIDAQ
        elif forcedirection == "Upwards":
            ypos=VoltageConverter.get_px_from_NIDAQ_Potentiometer_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage()) # Edited to work with external potentiometer through NIDAQ
            ypos = GetSystemMetrics(1) - ypos

        if(ypos > calibrationDataClass.GetMaxInput()):
             calibrationDataClass.SetMaxInput(ypos)

        return(ypos, calibrationDataClass, feedbackVoltage)

#Game Input Calculations 

def DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos, pushPull):
    if experimentalMode == "Dynamic":
        if voltage <= 0.0:
            voltage = 0.01
        if absOrRelvoltage == "Relative":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
        elif absOrRelvoltage == "Absolute":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,absoluteMaxVoltage, minVoltage, percentageOfMaxVoltage)
        return ypos 
    if experimentalMode == "Isometric" and pushPull == "Pull":
        if absOrRelvoltage == "Relative":
            ypos=VoltageConverter.get_px_from_Pulling_Iso(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage) 
        elif absOrRelvoltage == "Absolute":
            ypos=VoltageConverter.get_px_from_Pulling_Iso(voltage,absoluteMaxVoltage, minVoltage, percentageOfMaxVoltage)
    if experimentalMode == "Isometric" and pushPull == "Push":
        if voltage <= 0.0:
            voltage = 0.01
        if absOrRelvoltage == "Relative":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage) 
        elif absOrRelvoltage == "Absolute":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,absoluteMaxVoltage, minVoltage, percentageOfMaxVoltage)
    return ypos    


def InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader, smoothingFilter, pushPull):
    if inputMode == "Mouse":                    
        mx,my=pygame.mouse.get_pos()

        return(my,my)
                
    if inputMode == "USB/ADAM":
        voltage = 0 
        if experimentalMode == "Dynamic":
            voltage = SerialBoardAPI.GetPotValue(serialObj)
            voltage = int(voltage)
        if experimentalMode == "Isometric":
            voltage = SerialBoardAPI.GetLoaValue(serialObj)
            voltage = int(voltage)
            voltage = np.round(voltage/10)
        smoothingFilter.InsertInput(voltage)
        voltage = smoothingFilter.AverageInput()
        ypos=0 #USB/ADAM input goes here 
        if forceDirection == "Downwards":
            ypos = DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos, pushPull)
        elif forceDirection == "Upwards":
            ypos = DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos, pushPull)
            ypos = GetSystemMetrics(1) - ypos
        
        return(voltage,ypos)   

    if inputMode == "NIDAQ":
        voltage = reader.read()[0]
        voltage = abs(voltage)
        ypos = 0 
        if forceDirection == "Downwards":
            if absOrRelvoltage == "Relative":
                ypos=VoltageConverter.get_px_from_voltage_NIDAQ_Potentiometer(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
            if absOrRelvoltage == "Absolute":  
                ypos=VoltageConverter.get_px_from_voltage_NIDAQ_Potentiometer(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)  
        if forceDirection == "Upwards":
            if absOrRelvoltage == "Relative":
                ypos=VoltageConverter.get_px_from_voltage_NIDAQ_Potentiometer(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
                ypos = GetSystemMetrics(1) - ypos
            if absOrRelvoltage == "Absolute":  
                ypos=VoltageConverter.get_px_from_voltage_NIDAQ_Potentiometer(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)
                ypos = GetSystemMetrics(1) - ypos  

        return(voltage,ypos)
