import threading

from flask import Blueprint, Flask, redirect, render_template, request

from .dialogs import CustomStepDialog, DialogManager
from .testmanager import TestManager

app = Flask(__name__)
dialog_manager = DialogManager()
test_manager = TestManager()
api = Blueprint("api", __name__, url_prefix="/api")
dialog = Blueprint("dialog", __name__, url_prefix="/dialog")


@app.route("/")
def home():
    return render_template("home.html")


@dialog.route("/")
def show_dialog():
    dialog = dialog_manager.get()

    if dialog is None:
        return redirect("/")
    elif isinstance(dialog, CustomStepDialog):
        return render_template(f"dialogs/custom/{dialog.step}.html", **dialog.__dict__)

    return render_template(f"dialogs/{dialog.__class__.__name__}.html", **dialog.__dict__)


@dialog.post("/submit")
def submit_dialog():

    data = {}

    for key in request.form:
        values = request.form.getlist(key)
        data[key] = values if len(values) > 1 else values[0]

    dialog = dialog_manager.get()
    if isinstance(dialog, CustomStepDialog):
        value = data
    else:
        value = data["response"]

    dialog_manager.answer(value)
    return redirect("/")


@api.route("/create/<type>", methods=["POST"])
def api_create(type):
    data = request.get_json()
    print(data)
    dialog_manager.create(type, **data)
    return {}


@api.route("/get_response")
def api_get_response():
    value = dialog_manager.get_response()
    return {"response": value}


@api.route("/test/start", methods=["POST"])
def api_start_test():
    dialog_manager.reset()
    test_manager.start()
    return {"message": "Test started"}


@api.route("/response_awaiting")
def api_is_message_pending():
    return {"status": dialog_manager.is_message_pending()}


@api.route("/test/status")
def api_test_status():
    return {"status": test_manager.get_status()}


@api.route("/test/stop", methods=["POST"])
def api_stop_test():
    dialog_manager.reset()
    test_manager.stop()
    return {"message": "Test stopped"}


@api.route("/ping")
def api_ping():
    return {"message": "pong"}


app.register_blueprint(api)
app.register_blueprint(dialog)


def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)


def start_flask_server():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
