from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._master_data = None
        self._master_name = ""

    @property
    def master_name(self):
        return self._master_name

    @property
    def master_data(self):
        return self._master_data

    @master_name.setter
    def master_name(self, value):
        self._master_name = value[1]
        self._master_data = value[0]
        self.file_name_changed.emit(self._master_name)
