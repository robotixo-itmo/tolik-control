import sys

from PyQt5.QtWidgets import QApplication

from windows.main_window import MainWindow


def excepthook(cls, traceback, exception):
    sys.excepthook(cls, traceback, exception)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.excepthook = excepthook
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
