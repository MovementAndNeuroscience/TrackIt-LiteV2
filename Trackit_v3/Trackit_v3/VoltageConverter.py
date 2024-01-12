#VoltageConverter
import Calibrationdata
from win32api import GetSystemMetrics
import numpy as np 

def get_px_from_voltage(voltage, max_voltage, min_voltage, percentOfMax):

    min_voltage = min_voltage*(percentOfMax/100)
    result =  (GetSystemMetrics(1)) * (voltage/(min_voltage/100))/100 # middle point on screen added by middle point on screen * percentge diversion from Min_voltage 
    if result <= 0.00:

        return 0.00
    return result

def get_px_from_voltage_calibration(voltage, max_voltage, min_voltage):

    result =  (GetSystemMetrics(1)) * (voltage/(min_voltage/100))/100 # middle point on screen added by middle point on screen * percentge diversion from Min_voltage
    return result 

#ADAM POTENTIOMETER 
def get_px_from_Potentiometer_calibration(voltage, max_voltage, min_voltage):

    voltage = voltage - min_voltage
    max_voltage = max_voltage - min_voltage
    if max_voltage <= 1.0:
        max_voltage = 10 
    if voltage <= 1:
        voltage = 2
    result = (GetSystemMetrics(1)) * (voltage/(max_voltage/100))/100 # Top point of the screen * percentge diversion from Max_voltage
    return result

# ADAM ISOMETRIC PULLING
def get_px_from_Pulling_Iso_calibration(voltage, max_voltage, min_voltage):

    voltage = voltage - max_voltage
    min_voltage = min_voltage - max_voltage
    if max_voltage <= 1.0:
        max_voltage = 10 
    print("Voltage : " + str(voltage))
    print("min voltage : " + str(min_voltage))
    print("max voltage : " + str(max_voltage))
    if voltage > 0.0:
       voltage = 0.1
    result = abs((GetSystemMetrics(1)) * (voltage/(min_voltage/100))/100) # Top point of the screen * percentge diversion from Max_voltage
    return result 

def get_px_from_Pulling_Iso(voltage, max_voltage, min_voltage, percentOfMax):
    
    min_voltage = (min_voltage- max_voltage)*(percentOfMax/100)
    voltage = voltage - max_voltage
    if max_voltage <= 1.0:
        max_voltage = 10 
    if voltage > 0.0:
        voltage = 0.1
    #if voltage /(min_voltage/100) < 2.2/(percentOfMax/100):
    #    voltage = 5

    result = (GetSystemMetrics(1)) * (voltage/(min_voltage/100))/100 # Top point of the screen * percentge diversion from Max_voltage

    if result <= 0.00:
        return 0.00
    return result 


def get_px_from_Potentiometer(voltage, max_voltage, min_voltage, percentOfMax):
    max_voltage = (max_voltage- min_voltage)*(percentOfMax/100)
    voltage = voltage - min_voltage
    if max_voltage <= 1.0:
        max_voltage = 10 
    if voltage <= 1:
        voltage = 1
    if voltage /(max_voltage/100) < 2.2/(percentOfMax/100):
        voltage = 2

    result = (GetSystemMetrics(1)) * (voltage/(max_voltage/100))/100 # Top point of the screen * percentge diversion from Max_voltage

    if result <= 0.00:
        return 0.00
    return result

#GENERAL CALIBRATION
def Calibrate_minAndMaxVoltage(voltage, calibrationData):
    if voltage < calibrationData.GetMinVoltage():
        calibrationData.SetMinVoltage(voltage)

    if voltage > calibrationData.GetMaxVoltage():
        calibrationData.SetMaxVoltage(voltage)

    return calibrationData

#CALIBRATION FOR ADAAM 
def Calibrate_minAndMaxVoltage_ADAM(voltage, calibrationData):
    #if voltage > 1900: # replace with frontend value 
    if voltage < calibrationData.GetMinVoltage():
        calibrationData.SetMinVoltage(voltage)

    if voltage > calibrationData.GetMaxVoltage():
        calibrationData.SetMaxVoltage(voltage)

    return calibrationData
