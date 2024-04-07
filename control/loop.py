from time import time
from random import randint
import nixnet
from nixnet import system
from nixnet import constants
from canbus import Frame


def control_loop(enqueue_ui_event, control_queue):
    """
    This is the control loop for the monolith project.
    """
    last_time = time()
    # Get CAN interface
    can_interfaces = system.System().intf_refs_can
    can_list = [can_interface for can_interface in can_interfaces]

    if not can_list:
        raise Exception("No CAN interfaces found")
    
    can_interface = can_list[0]
    print(can_interface)

    can_database = 'Current_Database'
    can_cluster = ':memory:'
    with nixnet.FrameInStreamSession(str(can_interface), str(can_database), str(can_cluster)) as input_session:
        input_session.intf.can_term = constants.CanTerm.OFF
        input_session.intf.baud_rate = 250000
        input_session.intf.can_fd_baud_rate = 250000

        input_session.start()

    while True:
        frames = input_session.frames.read(10000, constants.TIMEOUT_NONE)
        for frame in frames:
            print(Frame.get_timestamp(frame))
            print(Frame.sort_by_id(frame))

        ############################################
        # EXAMPLE

        # Check for control messages (these come from the UI)
        if not control_queue.empty():
            msg = control_queue.get()

            # handle messgae (e.g. open or close valve)

            # send update back to UI
            enqueue_ui_event(msg)

        # Sending dummy data to UI for pres and temp sensors
        if time() - last_time > 0.1:
            last_time = time()
            # generate random number from 0 to 100
            enqueue_ui_event(
                [
                    ("pres-FE", randint(1, 100), last_time),
                    ("temp-FE", randint(1, 25), last_time),
                    ("pres-OE", randint(1, 100), last_time),
                    ("temp-OE", randint(1, 25), last_time),
                ]
            )

        ############################################

# Following exclusively for Cece debugging 
if __name__ == "__main__":
    can_interfaces = system.System().intf_refs_can

    # 56789101112131415161718192021222324251234




    can_list = [can_interface for can_interface in can_interfaces]

    if not can_list:
        raise Exception("No CAN interfaces found")

    can_interface = can_list[0]
    print(can_interface)

    can_database = 'Current_Database'
    can_cluster = ':memory:'
    with nixnet.FrameInStreamSession(str(can_interface), str(can_database), str(can_cluster)) as input_session:
        input_session.intf.can_term = constants.CanTerm.OFF
        input_session.intf.baud_rate = 250000
        input_session.intf.can_fd_baud_rate = 250000

        input_session.start()

        for i in range(0, 10):
            frames = input_session.frames.read(10000, constants.TIMEOUT_NONE)
            for frame in frames:
                print(Frame.get_timestamp(frame))
                print(Frame.sort_by_id(frame))
            time.sleep(0.5)