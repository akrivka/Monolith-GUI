from control.messages import StartSequence, ValveClose, ValveOpen
from control.sequences import seq_OPEN_VALVE, seq_CLOSE_VALVE
from flask import Flask, Response, request, render_template, send_from_directory
from ui.sse import MessageAnnouncer
from lib.util import time_ms
import threading
from multiprocessing import Queue
from signal import signal, SIGINT


##############################
# FLASK SERVER
##############################


def format_sse_message(msg):
    """Format the event to be sent to the UI"""
    return "data: " + msg + "\n\n"


def create_server(send_command, ui_announcer):
    """TODOC"""
    app = Flask("Monolith", template_folder="ui/templates")

    ##############################
    # ROUTES
    ##############################
    @app.route("/")
    def index():
        """Main page"""
        return render_template("index.html")

    @app.route("/pid")
    def pid():
        """Interactive Piping and Instrumentation Diagram page"""
        return render_template("pid.html")

    @app.route("/valve-open/<designator>", methods=["GET"])
    def open_valve(designator):
        """Request to open valve designator"""
        send_command(StartSequence((seq_OPEN_VALVE, [designator])))
        return {}, 200

    @app.route("/valve-close/<designator>", methods=["GET"])
    def close_valve(designator):
        """Request to close valve designator"""
        send_command(StartSequence((seq_CLOSE_VALVE, [designator])))
        return {}, 200

    @app.route("/monitor")
    def monitor():
        """Page with graphs and data"""
        return render_template("monitor.html")

    @app.route("/assets/<path:path>")
    def send_assets(path):
        """Serve static assets (css, js, images, etc.)"""
        return send_from_directory("ui/assets", path)

    ##############################
    # STREAMS
    ##############################
    @app.route("/pid-stream", methods=["GET"])
    def pid_stream():
        """Stream of events from control loop to update the UI

        Receives messages from ui_loop below
        """
        def handle_stream():
            messages = ui_announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield format_sse_message(msg.format())

        return Response(handle_stream(), mimetype="text/event-stream")

    @app.route("/monitor-stream", methods=["GET"])
    def monitor_stream():
        """Stream of events from control loop to update the UI

        Receives messages from ui_loop below
        """

        def handle_stream():
            # Send the current time to the client
            start_time = time_ms()

            messages = ui_announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                if (
                    msg.__class__.__name__ == "PressureReading"
                    or msg.__class__.__name__ == "TemperatureReading"
                ):
                    yield format_sse_message(msg.format(-start_time))

        return Response(handle_stream(), mimetype="text/event-stream")

    return app


def ui_loop(ui_queue, announcer):
    """TODOC"""
    while True:
        msg = ui_queue.get()
        announcer.announce(msg)


def handler(signalnum, frame):
    raise TypeError

# Start server
def start_server(control_queue, ui_queue):
    """TODOC"""
    # Install SIGINT handler so that Ctrl+C propagates to the parent 
    signal(SIGINT, handler)

    def send_command(msg):
        try:
            control_queue.put(msg)
        except Queue.full:
            print("Control queue is full, UI process probably dead")

    announcer = MessageAnnouncer()
    app = create_server(send_command, announcer)
    app.debug = False

    loop_thread = threading.Thread(
        target=ui_loop, args=(ui_queue, announcer), daemon=True
    )
    loop_thread.start()

    app.run(host="0.0.0.0", port=2000, threaded=True)

    loop_thread.join()
