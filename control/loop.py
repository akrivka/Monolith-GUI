from random import randint
from control.canbus_adam_stub import CanBus, CAN_ID_MAPPING
from time import time

def control_loop(display, ui_command_queue):
    """
    This is the control loop for the Monolith project.
    """

    # Initialize CanBus interface
    canbus = CanBus()
    canbus.start()

    # Main loop
    while True:
        # Read CAN message 
        #   - these come from the test stand
        #   - the CanBus class handles logging and parsing
        can_msgs = canbus.read()
        for can_msg in can_msgs:
            # Handle CAN message
            # TODO: Implement CAN message handling 
            #       To send an update to the UI, you can just do 
            #       display(can_msg). The UI will handle the rest.
            #       Example:
            #           if isinstance(can_msg, PressureReading):
            #               display(can_msg)
            #           elif ...
            display(can_msg)

        # Read UI command
        # (these come from someone clicking a button in the UI)
        if not ui_command_queue.empty():
            ui_command = ui_command_queue.get()

            # Handle UI command
            # TODO: Implement UI command handling
            #       To send a CAN message, you can just do
            #       canbus.send(valve, value). The CanBus class will #
            #       handle the rest.
            #       Example:
            #           if isinstance(ui_msg, ValveOpen):
            #               canbus.send(ui_msg)
            #           elif ...
            pass

        # TODO: Sequence execution (check whether a new event should happen)
        #       (Infrastructure not set up for this yet.)

        # TODO: Check for device failures. 
        #       Check whether we've stopped receiving some message 
        #       and if so send a failure message to the UI
        #       (using `display(ObjectFailure(object_id))`)
            

# Following exclusively for Cece debugging 
if __name__ == "__main__":
    canbus = CanBus()
    canbus.start()
    while True:
        canbus.read()