import sys
import time
import csv


# helper functions
def byte_array_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder="little")


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


class ValveClose(CanMessage):
    def __init__(self, valve_id):
        self.valve_id = valve_id


class PressureReadingFailure(InternalMessage):
    def __init__(self, object_id):
        super().__init__()
        self.object_id = object_id

class PressureReading(CanMessage):
    TIMEOUT = 100 # ms
    last_timestamp = 0.0
    fail_msg = PressureReadingFailure

    def __init__(self, object_id, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp)
        self.object_id = object_id

        # TODO @Cece: needs to be implement proper voltage convertsion
        self.pressure = byte_array_to_int(payload)

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
        self.temperature = byte_array_to_int(payload)

        last_timestamp = self.timestamp

    def format(self, timestamp_offset=0.0):
        return f"temp,{self.object_id},{self.temperature},{self.timestamp + timestamp_offset}"

class ValvePosition(CanMessage):
    TIMEOUT = 1000 # ms

    def __init__(self, object_id, payload, can_id, can_timestamp):
        super().__init__(can_id, can_timestamp)
        self.object_id = object_id

        # TODO @Cece: needs to be implement proper voltage convertsion
        self.angle = byte_array_to_int(payload)

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