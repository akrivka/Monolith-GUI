# Monolith-PNID
Monolith test stand interactive Piping and Instrumentation Diagram implemented using a WebUI

## Plan

* Monolithic (haha) Python program, running the control loop, data collection, and serving an interactive web UI
	* Potentially implement using Python multithreading, to avoid web UI slowing down control loop (which is the critical component)
	* Using a venv and keep a requirements.txt file
* Use some web diagramming (mermaid?) and plotting (seaborn/graphana?) library. Other than that use Flask web server and HTMX (very simple).
* Configure test stand sensors (mainly their CAN bus message formats) using a YAML file that acts as a source of truth (avoid clunky NI programs)
* Dump CAN messages to a file. Consider using an sqlite database?

## Order of Implementation

1. Goal: get a simple button in a web UI open a valve on the test stand
	a. `canbus` and `web`, no control...
	b. First verify reading messages from canbus works
	c. Web UI should be quick

## Python Libraries

* `python-can` - for CAN communication
* `pyyaml` - for parsing YAML config files
* `Flask` - web server
