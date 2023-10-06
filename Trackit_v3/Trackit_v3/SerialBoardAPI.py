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

def GetValueFromA0(serialObj):

    serialObj.write(b"!adcReq\r")
    output = serialObj.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    return output

def CloseCommunication(serialObj):
    serialObj.close()