from control.messages import ValveOpen, ValveClose

def seq_OPEN_VALVE(designator):
    """Open"""
    return lambda t: [
        ValveOpen(t, designator),
        ValveOpen(t + 50, designator),
        ValveOpen(t + 100, designator),
        ValveOpen(t + 150, designator),
        ValveOpen(t + 200, designator)
    ]

def seq_CLOSE_VALVE(designator):
    """Close"""
    return lambda t: [
        ValveClose(t, designator),
        ValveClose(t + 50, designator),
        ValveClose(t + 100, designator),
        ValveClose(t + 150, designator),
        ValveClose(t + 200, designator)
    ]

# def seq_TEST():
#     """"""
#     def f(start_time):
#         VALVES = ["OVBV","OVBV","OMBV","OMBV","OPBV","OPBV","OFBV","OFBV","FVBV","FVBV","FMBV","FMBV","FPBV","FPBV","FFBV","FFBV"]
#         t = 0
#         sequence = []
#         for valve in VALVES:

            


def seq_IGNITE():
    """
        Fingers crossed...
    """
    return lambda t: []
    
