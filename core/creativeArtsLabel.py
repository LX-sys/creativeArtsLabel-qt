# -*- coding:utf-8 -*-
# @time:2023/4/414:59
# @author:LX
# @file:creativeArtsLabel.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

from UI.creativeArtsLabelUI import CreativeArtsLabelUI




class CreativeArtsLabel(CreativeArtsLabelUI):
    def __init__(self):
        super().__init__()

        # 创建测试按钮
        self.btn_freedomLine = QPushButton("自由线")
        self.btn_rect = QPushButton("矩形")
        self.btn_ellipse = QPushButton("圆形")
        self.btn_line = QPushButton("线")

        self.btn_freedomLine.setMinimumHeight(30)
        self.btn_rect.setMinimumHeight(30)
        self.btn_ellipse.setMinimumHeight(30)
        self.btn_line.setMinimumHeight(30)

        self.btn_freedomLine.clicked.connect(lambda :self.palette.setGraph("freedomLine"))
        self.btn_rect.clicked.connect(lambda :self.palette.setGraph("rect"))
        self.btn_ellipse.clicked.connect(lambda :self.palette.setGraph("ellipse"))
        self.btn_line.clicked.connect(lambda :self.palette.setGraph("line"))

        self.vboy = QVBoxLayout(self.left_w)
        self.vboy.addWidget(self.btn_freedomLine)
        self.vboy.addWidget(self.btn_rect)
        self.vboy.addWidget(self.btn_ellipse)
        self.vboy.addWidget(self.btn_line)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = CreativeArtsLabel()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())