from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import uic
import requests
import os


MAP_WIDTH, MAP_HEIGHT = 600, 450


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.spn = '0.005'
        self.ll = ['40.951714', '57.777134']
        self.get_map()

    def get_map(self):
        map_params = {
            "ll": ",".join([self.ll[0], self.ll[1]]),
            "spn": ",".join([self.spn, self.spn]),
            "l": "map",
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        self.map_file = 'map.png'
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.paint_map()

    def paint_map(self):
        self.pixmap = QPixmap('map.png')
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec())
