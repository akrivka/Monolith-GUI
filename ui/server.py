from flask import Flask, Response, request, render_template, send_from_directory
from ui.sse import MessageAnnouncer

app = Flask("Monolith", template_folder="ui/templates")
announcer = MessageAnnouncer()
objects = {"valve-FM": 0, "valve-OM": 0}


##############################
# HELPER FUNCTIONS
##############################


def process_event(updated_objects):
    print(updated_objects)
    return "data: " + ",".join(obj + "=" + str(state) for (obj, state) in updated_objects) + "\n\n"


def enqueue_event(evt):
    announcer.announce(evt)


##############################
# ROUTES
##############################


@app.route("/stream", methods=["GET"])
def stream():
    def handle_stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield process_event(msg)

    return Response(handle_stream(), mimetype="text/event-stream")


@app.route("/valve-close/<valve_id>", methods=["GET"])
def close_valve(valve_id):
    # Enqueue message in control process, wait for confirmation

    # For now assume it succeeded
    enqueue_event([(valve_id, 0)])
    return {}, 200


@app.route("/valve-open/<valve_id>", methods=["GET"])
def open_valve(valve_id):
    enqueue_event([(valve_id, 1)])
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


# Start server
def start_server():
    app.debug = False
    app.run(host="0.0.0.0", port=2000, threaded=True)
    print("Web server started.")
