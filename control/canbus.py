# """
# 	Canbus interface implementation/wrapper
# """

import sys
from lib.util import time_ms
import csv
import datetime
import nixnet
from nixnet import system, constants, types

# LOAD CAN_ID_MAPPING
CAN_ID_MAPPING = {}
CAN_ID_MAPPING_INVERSE = {}
with open("control/can_id_mapping.csv", mode="r") as can_id_mapping_csv:
    reader = csv.reader(can_id_mapping_csv)
    next(reader, None) # Skip header row
    for _can_id, classname, designator in reader:
        # Skip emtpy rows
        if classname == "":
            continue

        # Convert can_id 
        can_id = int(_can_id, 16)

        # Save in mappings...
        CAN_ID_MAPPING[can_id] = (
            getattr(sys.modules["control.messages"], classname),
            designator,
        )
        CAN_ID_MAPPING_INVERSE[(classname, designator)] = can_id


class CanBus:
    """ """

    def __init__(self):
        # Initialize NIXNET can interface
        can_interfaces = system.System().intf_refs_can
        can_list = [can_interface for can_interface in can_interfaces]

        if not can_list:
            raise Exception("No CAN interfaces found")

        can_interface = can_list[0]

        can_database = "Current_Database"
        can_cluster = ":memory:"

        self.input_session = nixnet.FrameInStreamSession(
            str(can_interface), str(can_database), str(can_cluster)
        )
        self.output_session = nixnet.FrameOutStreamSession(
            str(can_interface), str(can_database), str(can_cluster)
        )
        self.input_session.intf.can_term = constants.CanTerm.OFF
        self.input_session.intf.baud_rate = 250000
        self.input_session.intf.can_fd_baud_rate = 250000
        self.output_session.intf.can_term = constants.CanTerm.OFF
        self.output_session.intf.baud_rate =  250000
        self.output_session.intf.can_fd_baud_rate = 250000

        # Format the current time as a string
        formatted_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Open a file to write raw CAN messages to
        self.raw_can_file = open(f"raw_can_{formatted_time}.csv", "w")

        # Write the header row
        self.raw_can_file.write("timestamp,can_id,data\n")


    def start(self):
        # Start CanBus session
        self.input_session.start()

    def read(self):
        # Read frames received since the last time we called this 
        # (it's an array because there could've been multiple)
        frames = self.input_session.frames.read(10000, constants.TIMEOUT_NONE)

        for frame in frames:
            # Write the frame to the raw_can_file
            self.raw_can_file.write(f"{frame.timestamp},{frame.identifier},\"{frame.payload}\"\n")    

        # Return each one one by one to the control loop, instantied as 
        # a Python class defined by us
        for frame in frames:
            if int(frame.identifier) in CAN_ID_MAPPING:
                message_class, designator = CAN_ID_MAPPING[int(frame.identifier)]
                yield message_class(designator, list(frame.payload), int(frame.identifier), frame.timestamp)

    def send(self, msg):
        # Look up can_id based on msg.__classname__ and msg.designator
        can_id = CAN_ID_MAPPING_INVERSE[(type(msg).__name__, msg.designator)]

        # Create a CAN Frame
        frame = types.CanFrame(types.CanIdentifier(can_id), constants.FrameType.CAN_DATA, bytearray(msg.get_payload()))

        # Send the frame (through the nixnet output session)
        self.output_session.frames.write([frame])