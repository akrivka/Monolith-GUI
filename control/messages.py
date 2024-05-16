import sys
import time
import csv


# helper functions
PT_CALIBRATION = {}
with open("control/PT_Master.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        obj_id = row["designator"]
        obj_info = {"P_Low": int(row["P_Low"]), "P_High": int(row["P_High"]), "V_High": int(row["V_High"]), "V_Low": int(row["V_Low"])}
        PT_CALIBRATION[obj_id] = obj_info

def byte_array_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder="little")

def byte_array_to_high_low(byte_array):
    return byte_array[0] * byte_array[1] * 0xFF

def voltage_to_pressure(designator, voltage):
    ph = PT_CALIBRATION[designator]["P_High"]
    pl = PT_CALIBRATION[designator]["P_Low"]
    vh = PT_CALIBRATION[designator]["V_High"]
    vl = PT_CALIBRATION[designator]["V_Low"]
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
        self.created_timestamp = time.time()


# CAN MESSAGES
class CanMessageIn(Message):
    """
    TODOC
    """
    def __init__(self, can_id, can_timestamp, designator):
        super().__init__()
        self.can_id = can_id
        self.can_timestamp = can_timestamp
        self.designator = designator

class CanMessageOut(Message):
    """
    TODOC
    """
    def __init__(self, target_timestamp, designator):
        super().__init__()
        self.target_timestamp = target_timestamp
        self.designator = designator

class InternalMessage(Message):
    """
    TODOC
    """
    def __init__(self):
        super().__init__()

class ValveOpen(CanMessageOut):
    def __init__(self, target_timestamp, designator):
        super().__init__(0, target_timestamp, designator)
    
    def get_payload(self):
        return [0,0,0,0,0,0,0,0]


class ValveClose(CanMessageOut):
    def __init__(self, target_timestamp, designator):
        super().__init__(0, target_timestamp, designator)
    
    def get_payload(self):
        return [0,0,0,0,0,0,0,0]


class PressureReading(CanMessageIn):
    TIMEOUT = 100 # ms

    def __init__(self, designator, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp, designator)

        # TODO @Cece: needs to be implement proper voltage convertsion
        # self.pressure = byte_array_to_int(payload)
        # assuming the things mentioned above, like can_id > designator and pt_master is in the filepath used to run
        self.pressure = voltage_to_pressure(designator, byte_array_to_high_low(payload))

        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return (
            f"pres,{self.designator},{self.pressure},{self.timestamp + timestamp_offset}"
        )

class ThermoReading(CanMessageIn):
    TIMEOUT = 100 # ms

    def __init__(self, designator, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp, designator)

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
        return f"temp,{self.designator},{self.temperature},{self.timestamp + timestamp_offset}"

class ValvePosition(CanMessageIn):
    TIMEOUT = 1000 # ms

    def __init__(self, designator, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp, designator)

        # TODO @Cece: needs to be implement proper voltage convertsion
        # self.angle = byte_array_to_int(payload)
        self.angle = voltage_to_angle(byte_array_to_high_low(payload))
        
        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return (
            f"valve,{self.designator},{self.angle},{self.timestamp + timestamp_offset}"
        )

class ObjectFailure(InternalMessage):
    def __init__(self, designator):
        super.__init__()
        self.designator = designator
    
    def format(self):
        return f"object_failure,{self.designator}"
    
class StartSequence(InternalMessage):
    def __init__(self, sequence):
        super().__init__()
        self.sequence = sequence