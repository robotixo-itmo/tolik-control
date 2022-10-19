import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5 import uic


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.count = 0

        self.cycle_num.display(self.count)
        self._listen_buttons()

        self.center()
        self.show()

    def _listen_buttons(self):
        self.plus_b.clicked.connect(lambda s, x=1: self.display_value_change(x))
        self.minus_b.clicked.connect(lambda s, x=-1: self.display_value_change(x))
        self.plus_5_b.clicked.connect(lambda s, x=5: self.display_value_change(x))
        self.minus_5_b.clicked.connect(lambda s, x=-5: self.display_value_change(x))
        self.start_b.clicked.connect(self.start)

    def display_value_change(self, arg):
        self.count += arg
        if 0 > self.count or 99 < self.count:
            self.count = 0 if self.count < 0 else 99
        self.cycle_num.setDigitCount(int(len(str(self.count))))
        self.cycle_num.display(self.count)

    def start(self):
        pass

    def reset(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def excepthook(cls, traceback, exception):
    sys.excepthook(cls, traceback, exception)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mn = Main()
    sys.excepthook = excepthook
    sys.exit(app.exec_())
