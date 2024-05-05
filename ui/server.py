from control.messages import ValveClose, ValveOpen
from flask import Flask, Response, request, render_template, send_from_directory
from ui.sse import MessageAnnouncer
import time
import threading


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

    @app.route("/valve-open/<valve_id>", methods=["GET"])
    def open_valve(valve_id):
        """Request to open valve valve_id"""
        send_command(ValveClose(valve_id))
        return {}, 200

    @app.route("/valve-close/<valve_id>", methods=["GET"])
    def close_valve(valve_id):
        """Request to close valve valve_id"""
        send_command(ValveOpen(valve_id))
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
            start_time = time.time()

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


# Start server
def start_server(send_command, ui_queue):
    """TODOC"""
    announcer = MessageAnnouncer()
    app = create_server(send_command, announcer)
    app.debug = False

    loop_thread = threading.Thread(
        target=ui_loop, args=(ui_queue, announcer), daemon=True
    )
    loop_thread.start()

    app.run(host="0.0.0.0", port=2000, threaded=True)

    loop_thread.join()
