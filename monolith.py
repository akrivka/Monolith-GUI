#!/usr/bin/env python

"""
	This is the main file for the monolith project.
"""

from canbus.canbus import Canbus
from canbus.canbus_ni import read



def main():
    # Create the Canbus interface
    canbus = Canbus("canbus/interfaces.toml")

    # Loop to receive messages
    while True:
        # Receive a message
        message = canbus.recv()

        # Print the message
        print(message)

        # Send the message back
        canbus.send(message)


if __name__ == "__main__":
    main()
