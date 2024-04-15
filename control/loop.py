from random import randint
from control.canbus_stub import Frame, CanBus
from time import time


def control_loop(enqueue_ui_event, control_queue):
    """
    This is the control loop for the monolith project.
    """
    last_time = time()
    # Get CAN interface
    canbus = CanBus()
    canbus.start()
    while True:
        msg = canbus.read()
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
    canbus = CanBus()
    canbus.start()
    while True:
        canbus.read()