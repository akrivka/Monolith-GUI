# """
# 	Canbus interface implementation/wrapper
# """

import sys
import time
import csv
import nixnet
from nixnet import system
from nixnet import constants


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
        self.input_session.intf.can_term = constants.CanTerm.OFF
        self.input_session.intf.baud_rate = 250000
        self.input_session.intf.can_fd_baud_rate = 250000

        # Load can_id to Python class mappings
        self.can_id_mapping = {}
        with open("control/can_id_mapping.csv", mode="r") as can_id_mapping_csv:
            reader = csv.reader(can_id_mapping_csv)
            next(reader, None)
            for can_id, target_class, object_id in reader:
                self.can_id_mapping[int(can_id)] = [
                    getattr(sys.modules[__name__], target_class),
                    object_id,
                ]

    def start(self):
        # Start CanBus session
        self.input_session.start()

    def read(self):
        # Read frames received since the last time we called this 
        # (it's an array because there could've been multiple)
        frames = self.input_session.frames.read(10000, constants.TIMEOUT_NONE)

        # TODO: IMPORTANT!!! SAVE RAW CAN MESSAGES HERE.

        # Return each one one by one to the control loop, instantied as 
        # a Python class defined by us
        for frame in frames:
            target_class, object_id = self.can_id_mapping[int(frame.identifier)]
            yield target_class(
                object_id, list(frame.payload), int(frame.identifier), frame.timestamp
            )

    def send(self, msg):
        # Look up can_id based on msg.__classname__ and msg.object_id
        # TODO

        # Construct payload using get_payload()
        # TODO

        # Init nixnet message
        can_msg = nixnet.Message(identifier=id, data=[])

        # Send it...
        nixnet.send(can_msg)