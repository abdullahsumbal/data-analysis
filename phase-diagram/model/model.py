from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._ternary_file_name = ''
        self._ternary_file_data = []

    @property
    def file_name(self):
        return self._file_name

    @property
    def ternary_file_data(self):
        return self._ternary_file_data

    @file_name.setter
    def file_name(self, value):
        name = value["name"]
        data = value["data"]
        self._ternary_file_name = name
        self._ternary_file_data = data
        # update in model is reflected in view by sending a signal to view
        self.file_name_changed.emit(name)
