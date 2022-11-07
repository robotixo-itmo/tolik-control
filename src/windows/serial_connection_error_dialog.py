from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class SerialConnectionErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ошибка подключения')

        buttons = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)

        self.create_layout()
        self.setLayout(self.layout)

    def create_layout(self):
        self.layout = QVBoxLayout()
        message = QLabel("Устройство не найдено. Переподключите и повторите попытку.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
