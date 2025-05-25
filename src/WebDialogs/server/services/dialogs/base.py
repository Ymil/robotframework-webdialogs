from abc import ABC


class Dialog(ABC):
    template = None

    def __init__(self, message):
        self.message = message
        self.response = None

    def answer(self, response):
        self.response = response

    def get_response(self):
        return self.response


class CustomStepDialog(Dialog):
    template = None

    def __init__(self, message="", step=""):
        super().__init__(message)
        self.step = step
        self.template = "custom/" + step


class PauseExecutionDialog(Dialog):
    template = "PauseExecutionDialog"


class ExecuteManualStepDialog(Dialog):
    template = "ExecuteManualStepDialog"


class GetSelectionFromUserDialog(Dialog):
    template = "GetSelectionFromUserDialog"

    def __init__(self, message, options):
        super().__init__(message)
        self.options = options


class GetSelectionsFromUserDialog(GetSelectionFromUserDialog):
    template = "GetSelectionsFromUserDialog"


class GetValueFromUserDialog(Dialog):
    template = "GetValueFromUserDialog"

    def __init__(self, message):
        super().__init__(message)
