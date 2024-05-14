#!/usr/bin/env python

"""
	This is the main file for the monolith project.
"""

from ui.server import start_server
from control.loop import control_loop
from multiprocessing import Process, Queue
 
def main():
    control_queue = Queue()
    ui_queue = Queue()

    # start UI process
    ui_process = Process(target=start_server, args=(control_queue, ui_queue))
    ui_process.start()

    # start control loop
    control_loop(ui_queue, control_queue)

    ui_process.join()


if __name__ == "__main__":
    main()
