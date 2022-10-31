from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class CancelDialog(QDialog):
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Подтверждение выхода")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.__accept)
        self.buttonBox.rejected.connect(self.reject)

        self.__create_layout()
        self.setLayout(self.layout)

    def __create_layout(self):
        self.layout = QVBoxLayout()
        message = QLabel("Вы уверены, что хотите отменить операцию?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)

    def __accept(self):
        self.accepted.emit()
