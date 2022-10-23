from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/windows/ui/main.ui', self)

        self.count = 0
        self.done = 0
        self.firstButtonsGroup = [
            self.plusButton, self.minusButton, self.plusFiveButton, self.minusFiveButton, self.startButton
        ]

        self.__initUI()
        self.show()

    def __initUI(self):
        for button in self.firstButtonsGroup:
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
        for button in self.firstButtonsGroup:
            button.hide()

        for element in self.cancelButton, self.resumePauseButton, self.remainderLabel, self.doneLabel:
            element.show()
        self.doneLabel.setText(f'Выполнено циклов: {self.done}/{self.count}')

    def __pauseResume(self):
        pass

    def __cancel(self):
        pass

    def __center(self):  # FIXME: rename
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
