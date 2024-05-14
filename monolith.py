#!/usr/bin/env python

"""
	This is the main file for the monolith project.
"""

from ui.server import start_server
from control.loop import control_loop
from multiprocessing import Process, Queue

control_queue = Queue()
ui_queue = Queue()

def send_command(msg):
    try:
        print(msg)
        control_queue.put(msg)
    except Queue.full:
        print("Control queue is full, UI process probably dead")
        

def display(msg):
    try:
        ui_queue.put(msg)
    except:
        print("UI queue is full, control process probably dead")

def main():
    # start UI process
    ui_process = Process(target=start_server, args=(send_command, ui_queue))
    ui_process.start()

    # start control loop
    control_loop(display, control_queue)

    ui_process.join()


if __name__ == "__main__":
    main()
