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
    if max_voltage <= 1.0:
        max_voltage = 10 
    result = (GetSystemMetrics(1)) * (voltage/(max_voltage/100))/100 # Top point of the screen * percentge diversion from Max_voltage
    return result 

def Calibrate_minAndMaxVoltage(voltage, calibrationData):
    if voltage < calibrationData.GetMinVoltage():
        calibrationData.SetMinVoltage(voltage)

    if voltage > calibrationData.GetMaxVoltage():
        calibrationData.SetMaxVoltage(voltage)

    return calibrationData