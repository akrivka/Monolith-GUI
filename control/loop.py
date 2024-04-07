from time import time
from random import randint


def control_loop(enqueue_ui_event, control_queue):
    """
    This is the control loop for the monolith project.
    """
    last_time = time()
    while True:
        ############################################
        # TO BE REPLACD BY CECE

        if not control_queue.empty():
            msg = control_queue.get_nowait()            
            enqueue_ui_event(msg)

        # If 100ms has passed send new dummy pres/temp data
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
