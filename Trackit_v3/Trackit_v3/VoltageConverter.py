#VoltageConverter
import Calibrationdata
from win32api import GetSystemMetrics

def get_px_from_voltage(voltage, max_voltage, min_voltage):

    #if voltage <= max_voltage and voltage >= 0.00:
     #  result = (GetSystemMetrics(1)/2) - ((GetSystemMetrics(1)/2) * (voltage/(max_voltage/100))/100) # middle point on screen subtracted by middle point on screen * percentge diversion from Max_voltage 
     #  return result
    
    #elif voltage >= min_voltage and voltage <= 0.00:
    result =  (GetSystemMetrics(1)) * (voltage/(min_voltage/100))/100 # middle point on screen added by middle point on screen * percentge diversion from Min_voltage 
    return result

    

def Calibrate_minAndMaxVoltage(voltage, calibrationData):
    if voltage < calibrationData.GetMinVoltage():
        calibrationData.SetMinVoltage(voltage)

    if voltage > calibrationData.GetMaxVoltage():
        calibrationData.SetMaxVoltage(voltage)

    return calibrationData