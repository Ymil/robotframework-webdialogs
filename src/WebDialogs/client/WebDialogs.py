from pathlib import Path
from robot.api.deco import keyword
from robot.api import logger
from ..server.server import start_flask_server
import requests
import time


def float_range(start, stop, step):
    while start < stop:
        yield start
        start += step


WEBDIALOGS_PATH = Path(__file__).parent
WEBDIALOGS_SYMLINK_TEMPLATES = WEBDIALOGS_PATH.joinpath(
    "..", "server", "templates", "dialogs", "custom"
)
WEBDIALOGS_SYMLINK_STATIC = WEBDIALOGS_PATH.joinpath(
    "..", "server", "static", "custom"
)


class WebDialogs:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, timeout=3600, poll_interval=0.5,
                 custom_templates="templates", custom_static="static"):
        self.server_url = "http://localhost:5000"
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.custom_templates = custom_templates
        self.custom_static = custom_static

        self.__prepare_enviroment__()

        requests.post(f"{self.server_url}/api/test/start")

    def __prepare_enviroment__(self):
        start_flask_server()

        for retry in range(0, 10):
            try:
                requests.get(f"{self.server_url}/api/ping")
            except:
                if retry == 9:
                    raise Exception("Timeout WebDialogs")
                logger.console("Waiting for WebDialogs to start...")
                time.sleep(1)
                

        custom_templates_path = Path(self.custom_templates)
        if custom_templates_path.exists():
            if WEBDIALOGS_SYMLINK_TEMPLATES.exists():
                WEBDIALOGS_SYMLINK_TEMPLATES.unlink()
            WEBDIALOGS_SYMLINK_TEMPLATES.symlink_to(
                custom_templates_path.absolute())

        custom_static_path = Path(self.custom_static)
        if custom_static_path.exists():
            if WEBDIALOGS_SYMLINK_STATIC.exists():
                WEBDIALOGS_SYMLINK_STATIC.unlink()
            WEBDIALOGS_SYMLINK_STATIC.symlink_to(custom_static_path.absolute())

        logger.console(f"WebDialogs initialized in {self.server_url}")

    def close(self):
        requests.post(f"{self.server_url}/api/test/stop")
        time.sleep(1)

    @keyword("Get Value From User")
    def get_value_from_user(self, message):
        requests.post(
            f"{self.server_url}/api/create/get_value_from_user", json={"message": message})
        return self.__get_response()

    # Get Selection From User
    @keyword("Get Selection From User")
    def wait_for_user_selection(self, message, options):
        requests.post(f"{self.server_url}/api/create/get_selection_from_user",
                      json={"message": message, "options": options})
        return self.__get_response()

    # Get Selections From User
    @keyword("Get Selections From User")
    def wait_for_user_selections(self, message, options):
        requests.post(f"{self.server_url}/api/create/get_selections_from_user",
                      json={"message": message, "options": options})
        return self.__get_response()

    # Execute Manual Step
    @keyword("Execute Manual Step")
    def execute_manual_step(self, message, default_error=""):
        requests.post(
            f"{self.server_url}/api/create/execute_manual_step", json={"message": message})
        response = self.__get_response()
        if response == "FAIL":
            if default_error:
                msg = default_error
            else:
                msg = self.get_value_from_user("Indique el motivo del fallo")
            raise AssertionError(msg)
        return response

    # Pause Execution
    @keyword("Pause Execution")
    def pause_execution(self, message):
        requests.post(
            f"{self.server_url}/api/create/pause_execution", json={"message": message})
        return self.__get_response()

    @keyword("Execute Custom Step")
    def execute_custom_step(self, step):
        requests.post(
            f"{self.server_url}/api/create/execute_custom_step", json={"message": "Custom Step", "step": step})
        return self.__get_response()

    def __get_response(self):
        # 2. Polling
        for _ in float_range(0, self.timeout, self.poll_interval):
            r = requests.get(f"{self.server_url}/api/get_response")
            if r.json()["response"] is not None:
                return r.json()["response"]
            time.sleep(self.poll_interval)

        raise Exception("Timeout esperando respuesta del usuario")
