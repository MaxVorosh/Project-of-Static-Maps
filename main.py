from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import uic
import requests
from PyQt5.QtCore import Qt
import os


MAP_WIDTH, MAP_HEIGHT = 600, 450


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.spn = '0.005'
        self.ll = ['40.951714', '57.777134']
        self.map_params = {
                "ll": ",".join([self.ll[0], self.ll[1]]),
                "spn": ",".join([self.spn, self.spn]),
                "l": "map",
            }
        self.l = "map"
        self.code = ""
        self.get_map()
        self.initUi()

    def initUi(self):
        self.findButton.clicked.connect(self.findFunc)
        self.buttonGroup.buttonClicked.connect(self.change_view)
        self.pushButton.clicked.connect(self.del_pt)
        self.checkBox.stateChanged.connect(self.post_code_show)

    def post_code_show(self, state):
        if state == Qt.Checked:
            self.address.setText(self.address.text() + "\t" + self.code)
        else:
            self.address.setText(self.address.text().split("\t")[0])

    def del_pt(self):
        if "pt" in self.map_params.keys():
            del(self.map_params["pt"])
        self.findLine.setText('')
        self.address.setText('')
        self.get_map()

    def findFunc(self):
        address = self.findLine.text()
        geo_name = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"
        response = requests.get(geo_name)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
        self.address.setText(toponym["metaDataProperty"]["GeocoderMetaData"]["text"])
        try:
            self.code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except Exception:
            pass
        self.ll = toponym_coordinates.split()
        self.get_map(f"{','.join(self.ll)},pm2lbm1")

    def get_map(self, pt=None):
        if "pt" in self.map_params:
            self.map_params = {
                "ll": ",".join([self.ll[0], self.ll[1]]),
                "spn": ",".join([self.spn, self.spn]),
                "l": self.l,
                "pt": self.map_params["pt"],
            }
        if pt is not None:
            self.map_params = {
                "ll": ",".join([self.ll[0], self.ll[1]]),
                "spn": ",".join([self.spn, self.spn]),
                "l": self.l,
                "pt": pt,
            }
        elif "pt" in self.map_params:
            self.map_params = {
                "ll": ",".join([self.ll[0], self.ll[1]]),
                "spn": ",".join([self.spn, self.spn]),
                "l": self.l,
                "pt": self.map_params["pt"],
            }
        else:
            self.map_params = {
                "ll": ",".join([self.ll[0], self.ll[1]]),
                "spn": ",".join([self.spn, self.spn]),
                "l": self.l,
            }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=self.map_params)
        self.map_file = 'map'
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.paint_map()

    def paint_map(self):
        self.pixmap = QPixmap('map')
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.ll = [str(float(self.ll[0]) + float(self.spn) * 0.1), self.ll[1]]
        if event.key() == Qt.Key_Left:
            self.ll = [str(float(self.ll[0]) - float(self.spn) * 0.1), self.ll[1]]
        if event.key() == Qt.Key_Up:
            self.ll = [self.ll[0], str(float(self.ll[1]) + float(self.spn) * 0.1)]
        if event.key() == Qt.Key_Down:
            self.ll = [self.ll[0], str(float(self.ll[1]) - float(self.spn) * 0.1)]
        if event.key() == Qt.Key_PageUp:
            self.spn = str(float(self.spn) + 0.005)
        if event.key() == Qt.Key_PageDown:
            self.spn = str(float(self.spn) - 0.005)
        os.remove(self.map_file)
        self.get_map()

    def change_view(self, sender):
        if sender.text() == 'Схема':
            self.l = 'map'
        elif sender.text() == 'Гибрид':
            self.l = 'sat,skl'
        else:
            self.l = 'sat'
        self.get_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec_())