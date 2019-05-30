from PyQt5.QtCore import QObject, pyqtSignal


class Medusa(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._file_name = ''
        self._file_data = None
        self._file_header = None
        self._resistances = None

    @property
    def file_name(self):
        return self._file_name

    @property
    def resistances(self):
        return self._resistances

    @property
    def file_header(self):
        return self._file_header

    @property
    def file_data(self):
        return self._file_data

    @file_name.setter
    def file_name(self, value):
        self._file_name = value
        self.file_name_changed.emit(value)

    @file_header.setter
    def file_header(self, value):
        self._file_header = value
        # self.file_name_changed.emit(value)

    @file_data.setter
    def file_data(self, value):
        self._file_data = value
        # self._file_data.emit(value)

    @resistances.setter
    def resistances(self, value):
        self._resistances = value
        # self._file_data.emit(value)