import time
from control.messages import ValveOpen, ValveClose

def seq_OPEN_VALVE(designator):
    """Open"""
    return lambda t: [
        ValveOpen(designator, t),
        ValveOpen(designator, t + 50),
        ValveOpen(designator, t + 100),
        ValveOpen(designator, t + 150),
        ValveOpen(designator, t + 200)
    ]

def seq_CLOSE_VALVE(designator):
    """Close"""
    return lambda t: [
        ValveClose(designator, t),
        ValveClose(designator, t + 50),
        ValveClose(designator, t + 100),
        ValveClose(designator, t + 150),
        ValveClose(designator, t + 200)
    ]


def seq_IGNITE():
    """
        Fingers crossed...
    """
    return lambda t: []
    

