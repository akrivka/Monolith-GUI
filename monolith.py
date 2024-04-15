#!/usr/bin/env python

"""
	This is the main file for the monolith project.
"""

from ui.server import start_server
from control.loop import control_loop
from multiprocessing import Process, Queue, set_start_method

control_queue = Queue()
ui_queue = Queue()

def enqueue_control_event(msg):
    control_queue.put(msg)

def enqueue_ui_event(msg):
    ui_queue.put(msg)

def main():
    # start UI process
    ui_process = Process(target=start_server, args=(enqueue_control_event, ui_queue))
    ui_process.start()

    # start control loop
    control_loop(enqueue_ui_event, control_queue)

    ui_process.join()


if __name__ == "__main__":
    main()
