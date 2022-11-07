from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal
from serial import Serial


class WorkerThread(QThread):
    messageReceived = pyqtSignal(str)

    def __init__(self, port: str, parent=None):
        QThread.__init__(self, parent)
        self.serialDevice = Serial(f"/dev/{port}")
        self.exiting = False
        self.start()

    def run(self):
        while not self.exiting:
            line = self.serialDevice.readline()
            self.messageReceived.emit(str(line))
            sleep(1)

    def exit(self):
        self.exiting = True

    def __del__(self):
        self.exiting = True
        self.wait()
