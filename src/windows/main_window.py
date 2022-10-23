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

        self.initUI()
        self.show()

    def initUI(self):
        for button in self.firstButtonsGroup:
            button.show()

        self.cycleNum.display(self.count)
        self.remainderLabel.hide()
        self.doneLabel.hide()
        self.cancelButton.hide()
        self.resumePauseButton.hide()

        self._listenButtons()
        self.center()

    def _listenButtons(self):
        self.plusButton.clicked.connect(lambda s, x=1: self.displayValueChange(x))
        self.minusButton.clicked.connect(lambda s, x=-1: self.displayValueChange(x))
        self.plusFiveButton.clicked.connect(lambda s, x=5: self.displayValueChange(x))
        self.minusFiveButton.clicked.connect(lambda s, x=-5: self.displayValueChange(x))
        self.resumePauseButton.clicked.connect(self.pauseResume)
        self.cancelButton.clicked.connect(self.cancel)
        self.startButton.clicked.connect(self.start)

    def displayValueChange(self, arg):
        self.count += arg
        if 0 > self.count or 99 < self.count:
            self.count = 0 if self.count < 0 else 99
        self.cycleNum.setDigitCount(int(len(str(self.count))))
        self.cycleNum.display(self.count)

    def start(self):
        for button in self.firstButtonsGroup:
            button.hide()

        self.cancelButton.show()  # TODO: cycle
        self.resumePauseButton.show()
        self.remainderLabel.show()
        self.doneLabel.show()
        self.doneLabel.setText(f'Выполнено циклов: {self.done}/{self.count}')

    def pauseResume(self):
        pass

    def cancel(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
