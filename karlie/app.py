import sys
import os
from model.model import Medusa
from view.main_view import MainView
from PyQt5.QtWidgets import QApplication
from controllers.main_ctrl import MainController



class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # covnert from ui to py for view
        os.system("pyuic5 view/app.ui -o view/main_view_ui.py")
        self.model = Medusa()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())