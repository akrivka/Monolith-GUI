#!/usr/bin/env python

"""
	This is the main file for the monolith project.
"""

from ui.server import start_server
from control.loop import control_loop
from multiprocessing import Process


def main():
    control_process = Process(target=control_loop)
    ui_process = Process(target=start_server)

    ui_process.start()
    control_process.start()

    ui_process.join()
    control_process.join()

if __name__ == "__main__":
    main()

