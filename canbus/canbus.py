# """
# 	Canbus interface implementation/wrapper
# """

import nixnet
from nixnet import system
from nixnet import constants
from time import sleep
# import tomli
# import nixnet
# from nixnet import system
# from nixnet import constants

import datetime
import time

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


class Frame:
    """Breaks down Canbus messages (frames) into readable data packets including
            1) CanIdentifier -- number in hex representing data type
            2) TimeStamp -- Epoch Hex data
            3) Payload -- an 8-byte value 
        Returns theses processed values for use in GUI/Dashboard.
    """

    def __init__(self, frame):
        self.frame = frame
    
    def get_can_id(self):
        """Takes the CanIdentifier object and returns the ID in hex
        """
        idn = str(self.frame.identifier)
        idn = idn[14: len(idn) - 1]
        hex_idn = int(idn, 16)
        return hex(hex_idn)
    
    def get_timestamp(self):
        """Takes the hex epoch returned by the Can frame (results in integer 
           value of timestamp), and returns it in datetime format
        """
        timestamp = self.frame.timestamp
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)
        # potential for incorrect timestamp reading/error
        return datetime_obj

    
    def get_payload(self):
        """Takes b'string provided by the Can Bus frame and returns a list of
           8 8-bit values in hex
        """
        payload = str(self.frame.payload)
        payload = payload[3: len(payload) - 1]
        byte_list = payload.split('\\')
        byte_list = ["0" + i for i in byte_list]
        byte_list = [hex(int(i, 16)) for i in byte_list]
        return byte_list
    
    # if 3 <= hex_idn <= 9:
    def get_hi_low_val(self, byte_list):
        """Given a list of 8 bytes, returns the value using
           Low byte and High byte where byte 0 is low, and byte
           1 is high
        """
        val = byte_list[0] * byte_list[1] * 0xFF
        return val

"""
	Canbus interface implementation/wrapper
"""




def read():
    with nixnet.FrameInStreamSession("CAN1") as input_session:
        input_session.intf.can_term = constants.CanTerm.OFF
        input_session.intf.baud_rate = 250000
        input_session.intf.can_fd_baud_rate = 250000
        frames = input_session.frames.read(8)
        for frame in frames:
            print("Received frame:")
            print(frame)
            print(frame.payload)
            frame = Frame(frame)
            bytes = frame.get_payload()
            print(bytes)
            for byte in bytes:
                if byte != '0x0':
                    print("byte " + str(bytes.index(byte)) + " high")
            

while True:
    read()