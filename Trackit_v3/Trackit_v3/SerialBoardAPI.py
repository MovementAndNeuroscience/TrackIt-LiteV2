import serial 

def SetupSerialCommuniation(comPort):
    serialObj = serial.Serial() 
    serialObj.baudrate = 115200
    serialObj.port = comPort
    serialObj.timeout = 0.016
    
    return serialObj

def testCommunication(serialObj):
    try:
        serialObj.open()
    except:
        print("wrong port")
        portsObj = serial.tools.list_ports
        ports = portsObj.comports()
        print(len(ports))
        for port in ports:
            print (port.device)
            serialObj.port = port.device
            try: 
                serialObj.open()
            except:
                print("wrong port chosen")
            else:
                serialObj.close()
                return serialObj
    else:
        serialObj.close()
        return serialObj


def OpenCommunication(serialObj):
    serialObj.open()
    serialObj.write(b"enableTimer\r")

def ResetTimer(serialObj):
    serialObj.write(b"!resetTimer\r")

def EnableDynamicMeasurement(serialObj):
    serialObj.write(b"!enablePot\r")

def EnableIsomeetricMeasurement(serialObj):
    serialObj.write(b"!enableLoadCell\r")

def GetPotValue(serialObj):
    serialObj.write(b"!getPotValue\r")
    output = serialObj.readline()
    output = str(output)
    print("Pot : " + output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def GetLoaValue(serialObj):
    serialObj.write(b"!getLoadValue\r")
    output = serialObj.readline()
    output = str(output)
    print("Load : " + output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def GetValueFromA0(serialObj):

    serialObj.write(b"!adcReq\r")
    output = serialObj.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def CloseCommunication(serialObj):
    serialObj.write(b"disableTimer\r")
    serialObj.close()