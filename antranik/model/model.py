from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._data_file_name = ''
        self._data_data = None

    @property
    def file_name(self):
        return self._file_name

    @property
    def data_data(self):
        return self._data_data


    @file_name.setter
    def file_name(self, value):
        file_name = value[0]
        data = value[1]
        file_type = value[2]
        emit_message = value[3]
        if file_type == "data":
            self._data_file_name = file_name
            self._data_data = data
            print(data)

        if emit_message:
            # update in model is reflected in view by sending a signal to view
            self.file_name_changed.emit(file_name, file_type)
