from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic

from windows.cancel_dialog import CancelDialog
from utils.worker_thread import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/windows/ui/main.ui', self)

        self.count = 0
        self.done = 0
        self.buttonsGroup = [
            self.plusButton, self.minusButton, self.plusFiveButton, self.minusFiveButton, self.startButton
        ]
        self.elementsGroup = [
            self.cancelButton, self.resumePauseButton, self.remainderLabel, self.doneLabel
        ]

        self.__initUI()
        self.show()

    def __initUI(self):
        for button in self.buttonsGroup:
            button.show()

        self.cycleNum.display(self.count)
        for element in self.remainderLabel, self.doneLabel, self.cancelButton, self.resumePauseButton:
            element.hide()

        self.__listenButtons()
        self.__center()

    def __listenButtons(self):
        operation_buttons = {
            1: self.plusButton,
            5: self.plusFiveButton,
            -1: self.minusButton,
            -5: self.minusFiveButton
        }
        for i in operation_buttons.keys():
            operation_buttons[i].clicked.connect(lambda s, x=i: self.__displayValueChange(x))

        action_buttons = {
            self.resumePauseButton: self.__pauseResume,
            self.cancelButton: self.__cancel,
            self.startButton: self.__start
        }
        for button, action in zip(action_buttons.keys(), action_buttons.values()):
            button.clicked.connect(action)

    def __displayValueChange(self, arg):
        self.count += arg
        if 0 > self.count or 99 < self.count:
            self.count = 0 if self.count < 0 else 99
        self.cycleNum.setDigitCount(int(len(str(self.count))))
        self.cycleNum.display(self.count)

    def __start(self):
        self.worker = WorkerThread()
        self.worker.messageReceived.connect(self.__processBoardOutput)

        for button in self.buttonsGroup:
            button.hide()

        for element in self.elementsGroup:
            element.show()
        self.doneLabel.setText(f'Выполнено циклов: {self.done}/{self.count}')

    def __processBoardOutput(self, text: str):
        pass

    def __pauseResume(self):
        if self.resumePauseButton.text() == "pause":
            self.resumePauseButton.setText("resume")  # TODO: add action (send message to board, ..., ...)
        else:
            self.resumePauseButton.setText("pause")

    def __cancel(self):
        self.dialog = CancelDialog()
        self.dialog.accepted.connect(self.__backToMainWindow)
        self.dialog.exec()

    def __backToMainWindow(self):
        self.dialog.accept()
        for element in self.elementsGroup:
            element.hide()

        for button in self.buttonsGroup:
            button.show()

    def __center(self):  # FIXME: rename
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
