#tSerialportTest 
import serial 
import serial.tools.list_ports

def RunOnValidComport(ser):
    ser.write(b"!adcReq\r")
    output = ser.readline()
    output = str(output)
    output = output.split(',')
    output = output[len(output)-1]
    output = output[:-3]

    print (output)

    ser.close() 


validport = 'COM2'
ser = serial.Serial() 
ser.baudrate = 115200
ser.port = 'COM2'
ser.timeout = 0.016
try:
    ser.open()
except:
    print("wrong port chosen")
    portsObj = serial.tools.list_ports
    ports = portsObj.comports()
    print(len(ports))
    for port in ports:
        print (port.device)
        ser.port = port.device
        try:
            ser.open()
        except:
            print("wrong port chosen")
        else:
            validport = port
            RunOnValidComport(ser)
            break
else:
    RunOnValidComport(ser)

