from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pandas as pd


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot(str)
    def file_name_changed(self, name):
        # update model
        data, valid = self.validate_ternary_file(name, "ternary")

        if valid:
            self._model.file_name = name


    def validate_ternary_file(self, name, file_type):
        columns = {"channels", "x", "y"}
        try:
            data = pd.read_csv(name)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate file format. Heading not found: {}".format(
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                return data, True
        except Exception:
            message = "Error: Invalidate {} file format.".format(file_type)
            self.task_bar_message.emit("red", message)
            return [], False


