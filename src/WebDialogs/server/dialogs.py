import threading


class Dialog:
    def __init__(self, message):
        self.message = message
        self.response = None

    def answer(self, response):
        self.response = response

    def get_response(self):
        return self.response


class CustomStepDialog(Dialog):
    def __init__(self, message="", step=""):
        super().__init__(message)
        self.step = step


class PauseExecutionDialog(Dialog):
    pass


class ExecuteManualStepDialog(Dialog):
    pass


class GetSelectionFromUserDialog(Dialog):
    def __init__(self, message, options):
        super().__init__(message)
        self.options = options


class GetSelectionsFromUserDialog(GetSelectionFromUserDialog):
    pass


class GetValueFromUserDialog(Dialog):
    def __init__(self, message):
        super().__init__(message)


class DialogBuilder:
    @staticmethod
    def build(type, message, **kwargs) -> Dialog:
        if type == "execute_manual_step":
            return ExecuteManualStepDialog(message)
        elif type == "get_selection_from_user":
            return GetSelectionFromUserDialog(message, **kwargs)
        elif type == "get_selections_from_user":
            return GetSelectionsFromUserDialog(message, **kwargs)
        elif type == "get_value_from_user":
            return GetValueFromUserDialog(message)
        elif type == "pause_execution":
            return PauseExecutionDialog(message)
        elif type == "execute_custom_step":
            return CustomStepDialog(message, **kwargs)
        raise Exception(f"Unknown dialog type: {type}")


class DialogManager:
    def __init__(self):
        self.dialog: Dialog = None
        self.lock = threading.Lock()

    def reset(self):
        with self.lock:
            self.dialog = None

    def create(self, type, message, **kwargs):
        with self.lock:
            self.dialog = DialogBuilder.build(type, message, **kwargs)

    def get(self):
        return self.dialog

    def answer(self, response):
        with self.lock:
            self.dialog.answer(response)

    def get_response(self):
        if self.dialog is None:
            return None
        response = self.dialog.get_response()
        if response is not None:
            self.reset()
        return response

    def is_message_pending(self):
        return self.dialog is not None and self.dialog.response is None
