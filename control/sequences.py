from control.messages import ValveOpen, ValveClose

N = 5
INTERVAL = 5
def seq_OPEN_VALVE(designator):
    """Open"""
    return lambda t: [ValveOpen(t + i * INTERVAL, designator) for i in range(N) ]

def seq_CLOSE_VALVE(designator):
    """Close"""
    return lambda t: [ValveClose(t + i * INTERVAL, designator) for i in range(N)]



def seq_TEST():
    """
    Open and close all valves

    Open valve A, wait 2 seconds, close valve B, wait 3 seconds, repeat

    """
    def f(st):
        VALVES = ["OVBV","OVBV","OMBV","OMBV","OPBV","OPBV","OFBV","OFBV","FVBV","FVBV","FMBV","FMBV","FPBV","FPBV","FFBV","FFBV"]
        t = 0
        sequence = []
        for designator in VALVES:
            sequence += seq_OPEN_VALVE(designator)(st + t) + seq_CLOSE_VALVE(designator)(st + t + 2000)
            t += 5000
        return sequence
    
    return f


def seq_IGNITE():
    """
        Fingers crossed...
    """
    return lambda t: []
    
