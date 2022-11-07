from PyQt5.QtCore import QThread, pyqtSignal
from serial.tools import list_ports


class PortListener(QThread):
    update = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.exiting = False
        self.start()

    def run(self):
        ports_list = self.get_ports_list()
        self.update.emit()
        while not self.exiting:
            current_ports_list = self.get_ports_list()
            if ports_list != current_ports_list:
                ports_list = current_ports_list
                self.update.emit()

    def exit(self):
        self.exiting = True

    @staticmethod
    def get_ports_list():
        return [port.name for port in list_ports.comports()]
