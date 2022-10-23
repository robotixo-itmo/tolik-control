from PyQt5.QtWidgets import QWidget


class Error(QWidget):
    def __init__(self):
        super().__init__()
        #  uic.loadUi('main.ui', self)
        self.initUI()
        self.show()

    def initUI(self):
        pass
