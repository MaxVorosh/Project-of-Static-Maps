from PyQt5.QtWidgets import QWidget, QApplication
import sys
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ll = ["0", "0"]
        self.spn = "0.005"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.ll = [str(float(self.ll[0]) + float(self.spn) * 0.1), self.ll[1]]
        if event.key() == Qt.Key_Down:
            self.ll = [str(float(self.ll[0]) - float(self.spn) * 0.1), self.ll[1]]
        if event.key() == Qt.Key_Right:
            self.ll = [self.ll[0], str(float(self.ll[1]) + float(self.spn) * 0.1)]
        if event.key() == Qt.Key_Left:
            self.ll = [self.ll[0], str(float(self.ll[1]) - float(self.spn) * 0.1)]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_)
