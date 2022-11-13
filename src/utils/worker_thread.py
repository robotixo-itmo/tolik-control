from time import sleep
import platform

from PyQt5.QtCore import QThread, pyqtSignal
from serial import Serial, SerialException


class WorkerThread(QThread):
    messageReceived = pyqtSignal(str)

    def __init__(self, port: str, parent=None):
        self.port = port
        QThread.__init__(self, parent)
        if self.check_port():
            if platform.system() == 'Windows':
                self.serialDevice = Serial(f"{self.port}")
            elif platform.system() == 'Linux':
                self.serialDevice = Serial(f"/dev/{self.port}")
            self.exiting = False
            self.start()

    def check_port(self):
        try:
            if platform.system() == 'Windows':
                self.serialDevice = Serial(f"{self.port}")
            elif platform.system() == 'Linux':
                self.serialDevice = Serial(f"/dev/{self.port}")
        except SerialException:
            return False
        self.serialDevice.close()
        return True

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

