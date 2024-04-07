from flask import Flask, Response, request, render_template, send_from_directory
from ui.sse import MessageAnnouncer
import threading


##############################
# HELPER FUNCTIONS
##############################


def process_event(updated_objects):
    return (
        "data: "
        + ",".join(
            obj + "=" + str(state) for (obj, state, timestamp) in updated_objects
        )
        + "\n\n"
    )


def create_server(enqueue_controL_event, ui_announcer):
    app = Flask("Monolith", template_folder="ui/templates")

    @app.route("/stream", methods=["GET"])
    def stream():
        def handle_stream():
            messages = ui_announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield process_event(msg)

        return Response(handle_stream(), mimetype="text/event-stream")

    ##############################
    # ROUTES
    ##############################
    @app.route("/valve-close/<valve_id>", methods=["GET"])
    def close_valve(valve_id):
        # Enqueue message in control process, wait for confirmation

        # For now assume it succeeded
        # ui_announcer.announce([(valve_id, 0)])
        enqueue_controL_event([(valve_id, 0, -1)])
        return {}, 200

    @app.route("/valve-open/<valve_id>", methods=["GET"])
    def open_valve(valve_id):
        enqueue_controL_event([(valve_id, 1, -1)])
        return {}, 200

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/pid")
    def pid():
        return render_template("pid.html")

    @app.route("/monitor")
    def monitor():
        return render_template("monitor.html")

    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory("ui/assets", path)

    return app


def ui_loop(ui_queue, announcer):
    while True:
        msg = ui_queue.get()
        announcer.announce(msg)


# Start server
def start_server(enqueue_controL_event, ui_queue):
    announcer = MessageAnnouncer()
    app = create_server(enqueue_controL_event, announcer)
    app.debug = False

    loop_thread = threading.Thread(
        target=ui_loop, args=(ui_queue, announcer), daemon=True
    )
    loop_thread.start()

    app.run(host="0.0.0.0", port=2000, threaded=True)

    loop_thread.join()
