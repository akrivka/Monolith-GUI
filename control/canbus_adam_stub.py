# """
# 	Canbus interface implementation/wrapper
# """

import sys
import time
import csv
import random

# LOAD CAN_ID_MAPPING
CAN_ID_MAPPING = {}
with open("control/can_id_mapping.csv", mode="r") as can_id_mapping_csv:
    reader = csv.reader(can_id_mapping_csv)
    next(reader, None)
    for can_id, classname, object_id in reader:
        if classname == "":
            continue
        CAN_ID_MAPPING[int(can_id, 16)] = [
            getattr(sys.modules["control.messages"], classname),
            object_id,
        ]


class CanBus:
    """ """

    def __init__(self):
        # Initialize NIXNET can interface
        # can_interfaces = system.System().intf_refs_can
        # can_list = [can_interface for can_interface in can_interfaces]

        # if not can_list:
        #     raise Exception("No CAN interfaces found")

        # can_interface = can_list[0]

        # can_database = "Current_Database"
        # can_cluster = ":memory:"

        # self.input_session = nixnet.FrameInStreamSession(
        #     str(can_interface), str(can_database), str(can_cluster)
        # )

        # Load message stubs
        with open("control/message_stubs.csv", mode="r") as message_stubs_csv:
            reader = csv.reader(message_stubs_csv)
            next(reader, None)
            self.message_stubs = list(reader)

    def start(self):
        # self.input_session.intf.can_term = constants.CanTerm.OFF
        # self.input_session.intf.baud_rate = 250000
        # self.input_session.intf.can_fd_baud_rate = 250000

        # self.input_session.start()
        pass

    def get_random_messages(self):
        # Choose random number from 1 to 10
        num_messages = random.randint(1, 10)
        for i in range(num_messages):
            # Choose random message from self.message_stubs
            can_id, timestamp, payload_max, _ = random.choice(self.message_stubs)

            # choose a random number between 0 and payload_max
            payload_number = random.randint(0, int(payload_max))

            # format payload_number as a byte array
            payload = []
            for i in range(8):
                payload.append(payload_number & 0xFF)
                payload_number >>= 8

            nixnet_message = {
                "identifier": int(can_id, 16),
                "timestamp": timestamp,
                "payload": payload,
            }
            yield nixnet_message

    def read(self):
        # frames = self.input_session.frames.read(10000, constants.TIMEOUT_NONE)
        time.sleep(0.01)
        frames = self.get_random_messages()
        for frame in frames:
            if int(frame["identifier"]) in CAN_ID_MAPPING:
                message_class, object_id = CAN_ID_MAPPING[int(frame["identifier"])]
                yield message_class(object_id, list(frame["payload"]), int(frame["identifier"]), frame["timestamp"])

    def send(self, msg):
        # Look up can_id based on msg.__classname__ and msg.object_id
        # TODO

        # Construct payload using get_payload()
        # TODO

        # Init nixnet message
        # can_msg = nixnet.Message(identifier=id, data=[])

        # Send it...
        # nixnet.send(can_msg)
        pass
