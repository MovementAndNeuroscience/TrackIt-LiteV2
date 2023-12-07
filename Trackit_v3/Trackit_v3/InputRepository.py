import pygame 
from win32api import GetSystemMetrics
import SerialBoardAPI
import VoltageConverter
import daqmxlib
import serial
import numpy as np

#Calibraition Input calculations 


def DetermineADAMOutputCalibration(calibrationDataClass, experimentalMode, voltage, ypos):
        if experimentalMode == "Dynamic":
            if voltage <= 0.0:
                voltage = 0.01
            ypos=VoltageConverter.get_px_from_Potentiometer_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        if experimentalMode == "Isometric":
            if voltage <= 0.0:
                voltage = 0.01
            ypos=VoltageConverter.get_px_from_voltage_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        return ypos


def CalibrationInputCalculations(inputMode, serialObj, calibrationDataClass, experimentalMode, forcedirection, reader):
                
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
        if experimentalMode == "Isometric":
            voltage = SerialBoardAPI.GetLoaValue(serialObj)
            voltage = int(voltage)
        ypos=0 #USB/ADAM input goes here 
        calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage(voltage, calibrationDataClass)
        feedbackVoltage = voltage
        if forcedirection == "Downwards":
            ypos = DetermineADAMOutputCalibration(calibrationDataClass, experimentalMode, voltage, ypos)
        elif forcedirection == "Upwards":
            ypos = DetermineADAMOutputCalibration(calibrationDataClass, experimentalMode, voltage, ypos)
            ypos = GetSystemMetrics(1) - ypos
                
        if(ypos > calibrationDataClass.GetMaxInput()):
            calibrationDataClass.SetMaxInput(ypos)
            
        return(ypos, calibrationDataClass, feedbackVoltage)

    if inputMode == "NIDAQ":
        voltage = reader.read()[0]
        print("Voltage : " + str(voltage))
        ypos=0
        calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage(voltage, calibrationDataClass)
        feedbackVoltage = voltage
        if forcedirection == "Downwards":
            ypos=VoltageConverter.get_px_from_voltage_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
        elif forcedirection == "Upwards":
            ypos=VoltageConverter.get_px_from_voltage_calibration(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
            ypos = GetSystemMetrics(1) - ypos

        if(ypos > calibrationDataClass.GetMaxInput()):
             calibrationDataClass.SetMaxInput(ypos)

        return(ypos, calibrationDataClass, feedbackVoltage)

#Game Input Calculations 

def DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos):
    if experimentalMode == "Dynamic":
        if voltage <= 0.0:
            voltage = 0.01
        if absOrRelvoltage == "Relative":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
        elif absOrRelvoltage == "Absolute":
            ypos=VoltageConverter.get_px_from_Potentiometer(voltage,absoluteMaxVoltage, minVoltage, percentageOfMaxVoltage)
        return ypos 
    if experimentalMode == "Isometric":
        if voltage <= 0.0:
            voltage = 0.01
        if absOrRelvoltage == "Relative":
            ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
        elif absOrRelvoltage == "Absolute":
            ypos=VoltageConverter.get_px_from_voltage(voltage,absoluteMaxVoltage, minVoltage, percentageOfMaxVoltage)
        return ypos    


def InputCalculations(inputMode, serialObj, forceDirection, absOrRelvoltage, experimentalMode, absoluteMaxVoltage, percentageOfMaxVoltage, minVoltage, maxVoltage, reader):
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
        ypos=0 #USB/ADAM input goes here 
        if forceDirection == "Downwards":
            ypos = DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos)
        elif forceDirection == "Upwards":
            ypos = DetermineADAMOutput(maxVoltage, minVoltage, percentageOfMaxVoltage, experimentalMode, voltage, absoluteMaxVoltage, absOrRelvoltage, ypos)
            ypos = GetSystemMetrics(1) - ypos
        
        return(voltage,ypos)   

    if inputMode == "NIDAQ":
        voltage = reader.read()[0]
        ypos = 0 
        if forceDirection == "Downwards":
            if absOrRelvoltage == "Relative":
                ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
            if absOrRelvoltage == "Absolute":  
                ypos=VoltageConverter.get_px_from_voltage(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)  
        if forceDirection == "Upwards":
            if absOrRelvoltage == "Relative":
                ypos=VoltageConverter.get_px_from_voltage(voltage,maxVoltage, minVoltage, percentageOfMaxVoltage)
                ypos = GetSystemMetrics(1) - ypos
            if absOrRelvoltage == "Absolute":  
                ypos=VoltageConverter.get_px_from_voltage(voltage,0, -absoluteMaxVoltage, percentageOfMaxVoltage)
                ypos = GetSystemMetrics(1) - ypos  

        return(voltage,ypos)
