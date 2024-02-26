"""
	Canbus interface implementation/wrapper
"""

import tomli
import can

class Canbus:
	"""
		Canbus interface implementation/wrapper
	"""

	def __init__(self, config_file):
		"""
			Initializes the Canbus interface

			:param config_file: The configuration file for the Canbus interface
		"""

		# Load the configuration file
		with open(config_file, "rb") as file:
			config = tomli.load(file)

		# Create the Canbus interface
		self.bus = can.Bus(interface="socketcan", channel="CAN1", bitrate=250000)

	def send(self, message):
		"""
			Sends a message over the Canbus interface

			:param message: The message to send
		"""

		# Create a Canbus message
		msg = can.Message(arbitration_id=message["id"], data=message["data"], is_extended_id=message["extended"])

		# Send the message
		self.bus.send(msg)

	def recv(self):
		"""
			Receives a message from the Canbus interface

			:return: The received message
		"""

		# Receive a message
		msg = self.bus.recv()

		# Create a message object
		message = {
			"id": msg.arbitration_id,
			"data": msg.data,
			"extended": msg.is_extended_id
		}

		return message