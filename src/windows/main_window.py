from serial.tools import list_ports
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox
from PyQt5 import uic, QtCore

from src.windows.cancel_dialog import CancelDialog
from src.utils.port_listener import PortListener
from src.utils.worker_thread import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/ui/main.ui', self)

        self.port = ""
        self.dialog = ''
        self.currentDisplay = "start"

        self.count = 0
        self.done = 0
        self.currentDisplay = "start"

        self.elementsGroup = [
            self.plusButton, self.minusButton, self.plusFiveButton, self.minusFiveButton, self.startButton,
            self.comboBox, self.portLabel,
            self.cancelButton, self.resumePauseButton, self.remainderLabel,
            self.doneLabel, self.progressBar
        ]

        self.__initUI()

    def __initUI(self):
        self.setStyleSheet("QToolTip{color: black; font-size: 20px}")
        self.cycleNum.display(self.count)
        for element in self.elementsGroup[self.elementsGroup.index(self.cancelButton):]:
            element.hide()

        self.progressBar.setValue(0)
        self.updatePortList()
        self.portListener = PortListener()
        self.portListener.update.connect(self.updatePortList)

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
        for button, action in action_buttons.items():
            button.clicked.connect(action)

    def updatePortList(self):
        self.comboBox.clear()
        self.comboBox.setEditable(True)
        for port in list_ports.comports():
            self.comboBox.addItem(port.name)
        self.comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox.lineEdit().setReadOnly(True)
        self.comboBox.setStyleSheet('font-size: 20px; background-color: #e2e2e2')

    def __displayValueChange(self, arg):
        self.count += arg
        if 0 > self.count or 99 < self.count:
            self.count = 0 if self.count < 0 else 99
        self.cycleNum.setDigitCount(int(len(str(self.count))))
        self.cycleNum.display(self.count - self.done)

    def __dialog(self, title, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        return dlg

    def __start(self):
        if self.cycleNum.intValue() == 0:
            self.dialog = self.__dialog('Ошибка', 'Количество циклов не задано')
            self.dialog.exec()
            return

        if self.comboBox.currentText() == '':
            self.dialog = self.__dialog('Ошибка подключения',
                                        'Устройство не найдено. Переподключите и повторите попытку.')
            self.dialog.exec()
            return

        self.worker = WorkerThread(self.comboBox.currentText())
        self.worker.messageReceived.connect(self.__processBoardOutput)

        self.portListener.exit()

        for element in self.elementsGroup:
            element.setVisible(not element.isVisible())
        self.progressBar.setValue(round(self.done / self.count * 100))
        self.doneLabel.setText(f'Выполнено циклов: {self.done}/{self.count}')
        self.currentDisplay = "work"

    def __processBoardOutput(self, text: str):
        if text == 'done' and self.currentDisplay == "work":
            self.__displayValueChange(0)
            self.doneLabel.setText(f'Выполнено циклов: {self.done}/{self.count}')
            self.progressBar.setValue(0 if self.done == 0 else round(self.done / self.count * 100))
            if self.count <= self.done:
                self.dialog = self.__dialog('Конец', 'Работа завершена')
                self.currentDisplay = "start"
                self.dialog.exec()
                self.__backToMainWindow()
            else:
                self.done += 1
        elif text == 'disconnect':
            self.dialog = self.__dialog('Ошибка', 'Плата была отключена')
            self.currentDisplay = "start"
            self.dialog.exec()
            self.__backToMainWindow()

    def __pauseResume(self):
        self.worker.serialDevice.write(bytes(self.resumePauseButton.text(), 'ascii'))
        if self.resumePauseButton.text() == "pause":
            self.resumePauseButton.setText("resume")  # TODO: add action (send message to board, ..., ...)
        else:
            self.resumePauseButton.setText("pause")

    def __cancel(self):
        self.dialog = CancelDialog()
        self.dialog.accepted.connect(self.__backToMainWindow)
        self.dialog.exec()

    def __backToMainWindow(self):
        self.done, self.count = 0, 0
        self.__displayValueChange(-self.count)
        self.dialog.accept() if self.dialog else 0
        self.worker.exit()
        self.portListener.exiting = False
        self.portListener.start()
        for element in self.elementsGroup:
            element.setVisible(not element.isVisible())

    def __center(self):  # FIXME: rename
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
