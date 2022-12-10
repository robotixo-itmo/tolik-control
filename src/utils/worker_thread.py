from time import sleep
import platform

from PyQt5.QtCore import QThread, pyqtSignal
from serial import Serial, SerialException


class WorkerThread(QThread):
    messageReceived = pyqtSignal(str)

    def __init__(self, port: str, parent=None):
        self.port = port
        self.exiting = False
        QThread.__init__(self, parent)
        platforms = {
            'Windows': f"{self.port}",
            'Linux': f"/dev/{self.port}",
            'macOS': f"/dev/{self.port}"
        }
        try:
            self.serialDevice = Serial(platforms[platform.system()], 9600)
            sleep(6)
            self.start()
        except SerialException:
            pass

    def run(self):
        self.exiting = False
        while not self.exiting:
            try:
                line = self.serialDevice.readline()
                self.messageReceived.emit(line.decode())
                sleep(0.5)
            except SerialException:
                self.messageReceived.emit('disconnect')
                self.exit()

    def exit(self):
        self.exiting = True
        self.serialDevice.close()

    def __del__(self):
        self.exiting = True
        self.wait()
