
import PyDAQmx
import numpy as np
from PyDAQmx import Task

def send_trigger(TriggerNo):
    # Actuate a single digital pulse (period between 1 and 2 ms) on a desired port, depending on trigger mode value.
    # trigger_mode: either "random" or "series"
     print ("Sending TMS trigger signal... No = %s" % TriggerNo)
     dev_port_line = "1"
     dev_port_line = "/Dev1/port1/line2"  ### THERE MAY BE OTHER DEV NUMBER!
     print (str(dev_port_line))
     task = Task()
     task.CreateDOChan(dev_port_line, "", PyDAQmx.DAQmx_Val_ChanForAllLines)
     task.StartTask()
     task.WriteDigitalLines(1, 1, 1.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([1], dtype=np.uint8), None, None)
     task.WriteDigitalLines(1, 1, 5.0, PyDAQmx.DAQmx_Val_GroupByChannel, np.array([0], dtype=np.uint8), None, None)
     task.StopTask()
