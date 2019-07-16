from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._ternary_file_data = None
        self._config_data = None

    @property
    def config_data(self):
        return self._config_data

    @property
    def ternary_file_data(self):
        return self._ternary_file_data

    @ternary_file_data.setter
    def ternary_file_data(self, value):
        self._ternary_file_data = value
        self.file_name_changed.emit("master")

    def add_data(self, data, file_type):

        if file_type == "ternary":
            self._ternary_file_data = data
        if file_type == "master":
            self._ternary_file_data = data
        elif file_type == "config":
            self._config_data = data

        self.file_name_changed.emit(file_type)
