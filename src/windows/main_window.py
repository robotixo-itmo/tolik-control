from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/windows/ui/main.ui', self)
        self.initUI()
        self.show()

    def initUI(self):
        self.buttons_group_1 = [self.plus_b, self.minus_b, self.plus_5_b, self.minus_5_b, self.start_b]
        for i in self.buttons_group_1:
            i.show()

        self.count = 0
        self.done = 0

        self.cycle_num.display(self.count)
        self.remainder_lbl.hide()
        self.done_lbl.hide()
        self.cancel_b.hide()
        self.res_pas_b.hide()

        self._listen_buttons()
        self.center()

    def _listen_buttons(self):
        self.plus_b.clicked.connect(lambda s, x=1: self.display_value_change(x))
        self.minus_b.clicked.connect(lambda s, x=-1: self.display_value_change(x))
        self.plus_5_b.clicked.connect(lambda s, x=5: self.display_value_change(x))
        self.minus_5_b.clicked.connect(lambda s, x=-5: self.display_value_change(x))
        self.res_pas_b.clicked.connect(self.pause_resume)
        self.cancel_b.clicked.connect(self.cancel)
        self.start_b.clicked.connect(self.start)

    def display_value_change(self, arg):
        self.count += arg
        if 0 > self.count or 99 < self.count:
            self.count = 0 if self.count < 0 else 99
        self.cycle_num.setDigitCount(int(len(str(self.count))))
        self.cycle_num.display(self.count)

    def start(self):
        for i in self.buttons_group_1:
            i.hide()

        self.cancel_b.show()
        self.res_pas_b.show()
        self.remainder_lbl.show()
        self.done_lbl.show()
        self.done_lbl.setText(f'Выполнено циклов: {self.done}/{self.count}')

    def pause_resume(self):
        pass

    def cancel(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
