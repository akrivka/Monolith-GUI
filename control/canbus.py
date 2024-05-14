# """
# 	Canbus interface implementation/wrapper
# """

import nixnet
from nixnet import system
from nixnet import constants
from time import sleep
import csv
# import tomli
# import nixnet
# from nixnet import system
# from nixnet import constants

import datetime
import time

FUEL_SWITCH_LOOKUP = {0: "FFSO", 1: "FFSC", 2: "FMSO", 3: "FMSC", 4: "FVSO", 5: "FVSC", 6: "FPSO", 7: "FPSC"}
LOX_SWITCH_LOOKUP = {0: "OFSO", 1: "OFSC", 2: "OMSO", 3: "OMSC", 4: "OVSO", 5: "OVSC", 6: "OPSO", 7: "OPSC"}

FUEL_SWITCH_STATUS = {'FFSO' : 0x0, 'FFSC': 0x0, 'FMSO': 0x0, 'FMSC': 0x0, 'FVSO': 0x0, 'FVSC': 0x0, 'FPSO': 0x0, 'FPSC': 0x0}
LOX_SWITCH_STATUS = {'OFSO' : 0x0, 'OFSC': 0x0, 'OMSO': 0x0, 'OMSC': 0x0, 'OVSO': 0x0, 'OVSC': 0x0, 'OPSO': 0x0, 'OPSC': 0x0}

# # Get CAN interface
# can_interfaces = system.System().intf_refs_can

# can_list = [can_interface for can_interface in can_interfaces]

# if not can_list:
#     raise Exception("No CAN interfaces found")

# can_interface = can_list[0]
# print(can_interface)

# can_database = 'Current_Database'
# can_cluster = ':memory:'
# with nixnet.FrameInStreamSession(str(can_interface), str(can_database), str(can_cluster)) as input_session:
#     input_session.intf.can_term = constants.CanTerm.OFF
#     input_session.intf.baud_rate = 250000
#     input_session.intf.can_fd_baud_rate = 250000

#     input_session.start()

#     for i in range(0, 100):
#         frames = input_session.frames.read(10000, constants.TIMEOUT_NONE)
#         for frame in frames:
#             print(frame)
#             print(frame.payload)
#         time.sleep(0.1)



class CanBus:
    """
    """
    def __init__(self):
        can_interfaces = system.System().intf_refs_can
        can_list = [can_interface for can_interface in can_interfaces]

        if not can_list:
            raise Exception("No CAN interfaces found")
            
        can_interface = can_list[0]
        # print(can_interface)

        can_database = 'Current_Database'
        can_cluster = ':memory:'


        self.input_session = nixnet.FrameInStreamSession(str(can_interface), str(can_database), str(can_cluster))

  
    def start(self):
        self.input_session.intf.can_term = constants.CanTerm.OFF
        self.input_session.intf.baud_rate = 250000
        self.input_session.intf.can_fd_baud_rate = 250000

        self.input_session.start()
    
    def read(self):
        frames = self.input_session.frames.read(10000, constants.TIMEOUT_NONE)
        for frame in frames:
            frame = Frame(frame.timestamp, frame.identifier, frame.payload)
            print(frame.get_timestamp())
            print(frame.sort_by_id())
    
    def send(self, valve, value):
        nixnet.send(self.construct_message(valve, value))

    def construct_message(self, valve, value):
        id = nixnet.CanIdentifer(0x0)
        payload = bytearray([0, 0, 0, 0, 0, 0, 0, 0])

        if list(FUEL_SWITCH_LOOKUP.values()).contains(valve):
            id = nixnet.CanIdentifier(0x1)
            self.FUEL_SWITCH_STATUS[valve] = value
            payload = bytearray(self.FUEL_SWITCH_STATUS)

        if list(LOX_SWITCH_LOOKUP.values()).contains(valve):
            id = nixnet.CanIdentifier(0x2)
            self.LOX_SWITCH_STATUS[valve] = value
            payload = bytearray(self.LOX_SWITCH_STATUS)
        
        message = nixnet.Message(identifier = id, data = payload)
        return message


class Frame:
    """Breaks down Canbus messages (frames) into readable data packets including
            1) CanIdentifier -- number in hex representing data type
            2) TimeStamp -- Epoch Hex data
            3) Payload -- an 8-byte value 
        Returns theses processed values for use in GUI/Dashboard.
    """

    def __init__(self, timestamp, identifier, payload):
        """Breaks down Canbus messages (frames) into readable data packets including
            1) CanIdentifier -- number in hex representing data type
            2) TimeStamp -- Epoch Hex data
            3) Payload -- an 8-byte value 
        """
        self.timestamp = timestamp
        self.identifier = identifier
        self.payload = payload
    
    def get_can_id(self):
        """Takes the CanIdentifier object and returns the ID in hex

            Example output: a CanIdentifier(0x2) would return 0x2 
        """
        idn = str(self.identifier)
        idn = idn[14: len(idn) - 1]
        hex_idn = int(idn, 16)
        return hex(hex_idn)
    
    def get_timestamp(self):
        """Takes the hex epoch returned by the Can frame (results in integer 
           value of timestamp), and returns it in datetime format

           Actually, right now, until we determine what the can bus frame of 
           reference is for the timestamp (currently outputting 1974), just grabs
           timestamp of time of processing.
           
           Example output: 2024-04-07 14:20:57.329298
        """
        # timestamp = self.timestamp # tbd what time this is
        not_can_time = datetime.datetime.now()
        return not_can_time

    
    def get_payload(self):
        """Takes b'string provided by the Can Bus frame and returns a list of
           8 8-bit values in decimal

           Example output: [19, 0, 0, 0, 0, 0, 0, 0]
        """
        payload = list(self.payload)
        print(payload)
        return payload
    
    # if 3 <= hex_idn <= 9:
    def get_hi_low_val(self, byte_list):
        """Given a list of 8 bytes, returns the value using
           Low byte and High byte where byte 0 is low, and byte
           1 is high

           Example output: 0
        """
        val = byte_list[0] * byte_list[1] * 0xFF
        return val
        
    def sort_by_id(self):
        """Given a frame, returns either valve statuses or a pressure, or a temperature.

            Example output: 
            LOX Switches: {'OFSO': 0, 'OFSC': 0, 'OMSO': 0, 'OMSC': 0, 'OVSO': 0, 'OVSC': 0, 'OPSO': 0, 'OPSC': 0}
            0 --> a voltage or temperature
        """
        id = self.get_can_id()
        byte_list = self.get_payload()

        """Returns list of opened valves"""

        if id == "0x1":       # Returns open fuel valves
            message = "Fuel Switches: "
            switch_dictionary = {}
            for i in range(len(byte_list)):
                if byte_list[i] == 0:
                    switch_dictionary[FUEL_SWITCH_LOOKUP[i]] = 0
                else:
                    switch_dictionary[FUEL_SWITCH_LOOKUP[i]] = 1
            return message + str(switch_dictionary)
        
        if id == "0x2":   # Returns open oxygen valves
            message = "LOX Switches: "
            switch_dictionary = {}
            for i in range(len(byte_list)):
                if byte_list[i] == 0:
                    switch_dictionary[LOX_SWITCH_LOOKUP[i]] = 0
                else:
                    switch_dictionary[LOX_SWITCH_LOOKUP[i]] = 1
            return message + str(switch_dictionary)
        
        else: 
            voltage = self.get_hi_low_val(byte_list)
            with open("PT_Master.csv") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if id == row["CanID"]:
                        m = (int(row["P_High"]) - int(row["P_Low"]))/(int(row["V_High"]) - int(row["V_Low"]))
                        b = int(row["P_Low"]) - (m * int(row["P_High"]))
                        pressure = (voltage * m) + b
                        return pressure
                    else:
                        return voltage

        
        


        

    
    

"""
	Canbus interface implementation/wrapper
"""