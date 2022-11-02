from PyQt5.QtCore import QThread, pyqtSignal
from serial import Serial


class WorkerThread(QThread):
    messageReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.serialDevice = Serial("/dev/serial/port")
        self.exiting = False
        self.start()

    def run(self):
        while True:
            pass

    def __del__(self):
        self.exiting = True
        self.wait()
