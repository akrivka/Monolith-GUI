# from control.canbus_adam_stub import CanBus, CAN_ID_MAPPING
from control.canbus_adam import CanBus, CAN_ID_MAPPING
from time import time
import control.messages
import heapq

def control_loop(ui_queue, control_queue):
    """
    This is the control loop for the Monolith project.
    """

    def display(msg):
        try:
            ui_queue.put(msg)
        except:
            print("UI queue is full, control process probably dead")


    # Initialize CanBus interface
    canbus = CanBus()
    canbus.start()

    # Initialize outgoing can message buffer (priority queue)
    out_buffer = []

    # Main loop
    while True:
        # Read CAN message 
        #   - these come from the test stand
        #   - the CanBus class handles parsing and logging
        can_msgs = canbus.read()
        for can_msg in can_msgs:
            # TODO: (maybe) check for pressure/temperature thresholds, respond

            # Otherwise just let the UI handle the CAN message (make UI update)
            display(can_msg)

        # TODO: Check for device failures. 
        #       Check whether we've stopped receiving some message 
        #       and if so send a failure message to the UI
        #       (using `display(ObjectFailure(designator))`)

        # Process events from control queue (messages from UI)
        if not control_queue.empty():
            event = control_queue.get()

            if isinstance(event, control.messages.StartSequence):
                start_time = time()
                for can_msg in event.instantiate(start_time):
                    heapq.heappush(out_buffer, (can_msg.target_timestamp, can_msg))                
        
        # Send scheduled CAN messages
        while out_buffer and out_buffer[0][0] < time():
            _, can_msg = heapq.heappop(out_buffer)
            canbus.send(can_msg)