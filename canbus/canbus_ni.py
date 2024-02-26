"""
	Canbus interface implementation/wrapper
"""

import tomli
import nixnet
from nixnet import system
from nixnet import constants


def read():
    with nixnet.FrameInStreamSession("CAN1") as input_session:
        input_session.intf.can_term = constants.CanTerm.OFF
        input_session.intf.baud_rate = 250000
        input_session.intf.can_fd_baud_rate = 250000
        frames = input_session.frames.read(8)
        for frame in frames:
            print("Received frame:")
            print(frame)
