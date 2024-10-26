from PySide6.QtWidgets import QWidget, QApplication
from qtacrylic import WindowEffect  # import the module
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedWidth(400)  # set a fixed width for the window
        self.setFixedHeight(400)  # set a fixed height for the window

        self.setWindowFlags(Qt.FramelessWindowHint)  # make the window frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # make the window translucent

        self.ui_layout = QtWidgets.QGridLayout(self)  # create a ui layout
        self.ui_layout.setAlignment(Qt.AlignCenter)  # center the layout

        self.label = QtWidgets.QLabel("Hello World!", self)  # create a label to display a text
        self.label.setFont(QFont("Segoe UI", 14))  # configure the text size and font
        self.ui_layout.addWidget(self.label)  # add the label widget into the layout

        self.windowFX = WindowEffect()  # instatiate the WindowEffect class
        self.windowFX.setAcrylicEffect(self.winId())  # set the Acrylic effect by specifying the window id


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    app.exec_()