import sys
import time
import csv


# helper functions
PT_CALIBRATION = {}
with open("control/PT_Master.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        obj_id = row["OBJECT_ID"]
        obj_info = {"P_Low": int(row["P_Low"]), "P_High": int(row["P_High"]), "V_High": int(row["V_High"]), "V_Low": int(row["V_Low"])}
        PT_CALIBRATION[obj_id] = obj_info

def byte_array_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder="little")

def byte_array_to_high_low(byte_array):
    return byte_array[0] * byte_array[1] * 0xFF

def voltage_to_pressure(object_id, voltage):
    ph = PT_CALIBRATION[object_id]["P_High"]
    pl = PT_CALIBRATION[object_id]["P_Low"]
    vh = PT_CALIBRATION[object_id]["V_High"]
    vl = PT_CALIBRATION[object_id]["V_Low"]
    m = (ph - pl)/(vh - vl)
    b = m * vl - pl
    return m * voltage + b

def voltage_to_angle(voltage):
    angle = voltage * (360/1024)
    # voltage should NOT exceed 256
    # angle should NOT exceed 90
    return angle

class Message:
    """Top-level message class"""
    def __init__(self):
        self.timestamp = time.time()


# CAN MESSAGES
class CanMessage(Message):
    """
    Second-level subclass saying this is a message that gets
    sent over the CanBus
    """
    def __init__(self, can_id, can_timestamp):
        super().__init__()
        self.can_id = can_id
        self.can_timestamp = can_timestamp


class InternalMessage(Message):
    """
    Second-level subclass saying that this is a message only 
    sent internally within the Python application
    """
    def __init__(self):
        super().__init__()

class ValveOpen(CanMessage):
    def __init__(self, valve_id):
        self.valve_id = valve_id
    
    def get_payload():
        return [0,0,0,0,0,0,0,0]


class ValveClose(CanMessage):
    def __init__(self, valve_id):
        self.valve_id = valve_id
    
    def get_payload():
        return [0,0,0,0,0,0,0,0]


class PressureReading(CanMessage):
    TIMEOUT = 100 # ms

    def __init__(self, object_id, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp)
        self.object_id = object_id

        # TODO @Cece: needs to be implement proper voltage convertsion
        # self.pressure = byte_array_to_int(payload)
        # assuming the things mentioned above, like can_id > object_id and pt_master is in the filepath used to run
        self.pressure = voltage_to_pressure(object_id, byte_array_to_high_low(payload))

        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return (
            f"pres,{self.object_id},{self.pressure},{self.timestamp + timestamp_offset}"
        )

class ThermoReading(CanMessage):
    TIMEOUT = 100 # ms

    def __init__(self, object_id, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp)
        self.object_id = object_id

        # TODO @Cece: needs to be implement proper voltage convertsion
        # self.temperature = byte_array_to_int(payload)

        # if payload is byte_array, byte_array is low-high byte
        self.temperature = byte_array_to_high_low(payload)
        
        # if payload[7] != 0:
        #     if payload[7] != 2:
                    #short to GND
        #     if payload[7] != 4:
                    # short to VC


        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return f"temp,{self.object_id},{self.temperature},{self.timestamp + timestamp_offset}"

class ValvePosition(CanMessage):
    TIMEOUT = 1000 # ms

    def __init__(self, object_id, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp)
        self.object_id = object_id

        # TODO @Cece: needs to be implement proper voltage convertsion
        # self.angle = byte_array_to_int(payload)
        self.angle = voltage_to_angle(byte_array_to_high_low(payload))
        
        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return (
            f"valve,{self.object_id},{self.angle},{self.timestamp + timestamp_offset}"
        )

class ObjectFailure(InternalMessage):
    def __init__(self, object_id):
        super.__init__()
        self.object_id = object_id
    
    def format(self):
        return f"object_failure,{self.object_id}"