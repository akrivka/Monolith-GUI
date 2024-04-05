from ui.server import enqueue_event
from time import time
from random import randint


def control_loop():
    """
    This is the control loop for the monolith project.
    """
    last_time = time()
    while True:
        ############################################
        # TO BE REPLACD BY CECE

        # If 100ms has passed send new dummy pres/temp data
        if time() - last_time > 0.1:
            last_time = time()
            # generate random number from 0 to 100
            enqueue_event(
                [
                    ("pres-FE", randint(1, 100)),
                    ("temp-FE", randint(1, 25)),
                    ("pres-OE", randint(1, 100)),
                    ("temp-OE", randint(1, 25)),
                ]
            )

        ############################################
