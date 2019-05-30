from PyQt5.QtCore import QObject, pyqtSignal


class Medusa(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._file_name = ''

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value
        self.file_name_changed.emit(value)
