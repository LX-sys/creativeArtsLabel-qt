# -*- coding:utf-8 -*-
# @time:2023/4/414:42
# @author:LX
# @file:creativeArtsLabelUI.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QMainWindow,
    QHBoxLayout
)
from core.Palette import Palette

class CreativeArtsLabelUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creative Arts Label")
        self.resize(800,600)
        self.core = QWidget()
        self.setCentralWidget(self.core)

        self.setUI()

    def setUI(self):
        self.left_w = QWidget()
        self.palette = Palette()

        self.left_w.setMinimumWidth(60)
        self.left_w.setMaximumWidth(60)
        self.left_w.setStyleSheet('''
        border:1px solid red;
        ''')

        self.hboy = QHBoxLayout(self.core)
        self.hboy.setContentsMargins(0,0,0,0)
        self.hboy.setSpacing(0)

        self.hboy.addWidget(self.left_w)
        self.hboy.addWidget(self.palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = CreativeArtsLabelUI()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())