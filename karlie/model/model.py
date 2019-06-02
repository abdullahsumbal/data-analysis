from PyQt5.QtCore import QObject, pyqtSignal


class Medusa(QObject):
    file_name_changed = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
        self._medusa_file_name = ''
        self._mass_file_name = ''
        self._x_y_file_name = ""
        self._config_file_name = ""
        self._file_name = ""
        self._file_data = None
        self._file_header = None
        self._resistances = None


    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        name = value[0]
        file_type = value[1]

        if file_type == "medusa":
            self._medusa_file_name = name
        elif file_type == "mass":
            self._mass_file_name = name
        elif file_type == "x_y":
            self._x_y_file_name = name
        elif file_type == "config":
            self._config_file_name = name

        self.file_name_changed.emit(name, file_type)


    @property
    def resistances(self):
        return self._resistances

    @property
    def file_header(self):
        return self._file_header

    @property
    def file_data(self):
        return self._file_data



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