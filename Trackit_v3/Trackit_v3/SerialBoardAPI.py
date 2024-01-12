import serial 

def SetupSerialCommuniation(comPort):
    serialObj = serial.Serial() 
    serialObj.baudrate = 115200
    serialObj.port = comPort
    serialObj.timeout = 0.016
    
    return serialObj

def testCommunication(serialObj):
    isPortOpen = serialObj.isOpen()
    if isPortOpen == False :
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
    else :
        return serialObj


def OpenCommunication(serialObj):
    isPortOpen = serialObj.isOpen()
    if isPortOpen == False :
        serialObj.open()
        timer = serialObj.write(b"!enableTimer\r")
        isPortOpen = True

def ResetTimer(serialObj):
    serialObj.write(b"!resetTimer\r")

def EnableDynamicMeasurement(serialObj):
    serialObj.write(b"!enablePot\r")

def EnableIsomeetricMeasurement(serialObj):
    loadcell = serialObj.write(b"!enableLoadCell\r")
    print("loadcell : " +  str(loadcell))

def GetPotValue(serialObj):
    serialObj.write(b"!getPotValue\r")
    output = serialObj.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def GetLoaValue(serialObj):
    serialObj.write(b"!getLoadValue\r")
    output = serialObj.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]
    return output

def OffsetLoadCell(serialObj):
    tare = serialObj.write(b"!hxtare\r")

def GetValueFromA0(serialObj):

    serialObj.write(b"!adcReq\r")
    output = serialObj.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def SendTrigger (SerialObj, triggerNo):
    SerialObj.write(str.encode(chr(triggerNo)))
    
def CloseCommunication(serialObj):
    isPortOpen = serialObj.isOpen()
    if isPortOpen:
        serialObj.write(b"disableTimer\r")
        serialObj.close()
