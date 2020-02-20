import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.spn = "0.005"

    def scale(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = str(float(self.spn) + 0.0005)
        elif event.key() == Qt.Key_PageDown:
            self.spn = str(float(self.spn) - 0.0005)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
