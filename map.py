import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap
import requests
from PyQt5.QtCore import Qt


def get_map_image(lat_lon, l, z, pt):
    params = {
        'll': f'{lat_lon[0]},{lat_lon[1]}',
        'l': l,
        'z': z,
        'pt': '37.617635,55.755814' + pt
    }
    response = requests.get('http://static-maps.yandex.ru/1.x/', params=params)
    if not response:
        raise RuntimeError('Ошибка такой карты не находит!!!')
    result = QPixmap()
    if l.startswith('map') and not l.endswith('sat'):
        result.loadFromData(response.content, 'PNG')
    elif l.startswith('sat'):
        result.loadFromData(response.content, 'JPG')
    return result


def clamp(v, min_v, max_v):
    return max(min_v, min(v, max_v))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.map_center = [37.617635, 55.755814]
        self.map_scale = 5
        self.l = 'map'
        self.pt = ''
        self.addresses = ['Россия, Москва']
        self.init_ui()

    def update_map(self):
        self.map_label.setPixmap(get_map_image(self.map_center, self.l, self.map_scale, self.pt))

    def init_ui(self):
        self.setGeometry(300, 300, 600, 450)
        self.map_label = QLabel('', self)
        self.update_map()
        self.map_switch = QRadioButton('Карта', self)
        self.map_switch.move(5, 370)
        self.map_switch.toggled.connect(self.l_switch)
        self.map_switch.toggle()

        self.sat_switch = QRadioButton('Спутник', self)
        self.sat_switch.move(5, 390)
        self.sat_switch.toggled.connect(self.l_switch)

        self.hyb_switch = QRadioButton('Гибрид', self)
        self.hyb_switch.move(5, 410)
        self.hyb_switch.toggled.connect(self.l_switch)

        self.search_input = QLineEdit(self)
        self.search_input.resize(200, 23)

        self.search_button = QPushButton('Поиск', self)
        self.search_button.resize(50, 25)
        self.search_button.move(200, -1)
        self.search_button.clicked.connect(self.button_clicked)

        self.reset_search = QPushButton('Сбросить поиск', self)
        self.reset_search.resize(100, 25)
        self.reset_search.move(250, 410)
        self.reset_search.clicked.connect(self.button_clicked)

        self.address = QLabel(self.addresses[-1], self)
        self.address.resize(800, 20)
        self.address.move(5, 430)

        self.postal_index = QCheckBox('Индекс', self)
        self.postal_index.move(255, 3)
        self.postal_index.toggled.connect(self.index_checked)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.map_scale += 1
        elif event.key() == Qt.Key_PageDown:
            self.map_scale -= 1
        elif event.key() == Qt.Key_W:
            self.map_center[1] += 180 / (2 ** self.map_scale * 2)
        elif event.key() == Qt.Key_S:
            self.map_center[1] -= 180 / (2 ** self.map_scale * 2)
        elif event.key() == Qt.Key_D:
            self.map_center[0] += 360 / (2 ** self.map_scale * 2)
        elif event.key() == Qt.Key_A:
            self.map_center[0] -= 360 / (2 ** self.map_scale * 2)
        self.map_scale = clamp(self.map_scale, 1, 18)
        self.map_center = [clamp(self.map_center[0], -180, 180),
                           clamp(self.map_center[1], -90, 90)]
        try:
            self.update_map()
        except RuntimeError:
            print(f'Так не пойдет!!!')

    def button_clicked(self):
        if self.sender() == self.search_button:
            if self.search_input.text():
                try:
                    self.geocoder_req = \
                        f'https://geocode-maps.yandex.ru/1.x?geocode="{self.search_input.text()}"' \
                        '&apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json'
                    self.response = requests.get(self.geocoder_req)
                    if self.response:
                        self.json_response = self.response.json()
                    if self.json_response["response"]["GeoObjectCollection"]["featureMember"]:
                        self.toponym = self.json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                    self.map_center = [float(x) for x in self.toponym['Point']['pos'].split()]
                    self.point_points = [str(x) for x in self.map_center]
                    self.pt += f'~{",".join(self.point_points)}'
                    if len(self.pt.split('~')) > 100:
                        print('Слишком много точек!! Сброс!!!!!')
                        self.pt = '~37.617635,55.755814'
                        self.addresses = ['Россия, Москва']
                    self.addresses.append(self.json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                                              "GeoObject"]['metaDataProperty']['GeocoderMetaData']['text'])
                    self.address.setText(self.addresses[-1])
                    if self.postal_index.isChecked():
                        try:
                            self.address.setText(
                                self.address.text() +
                                f', {self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}')
                        except Exception:
                            print('У этого места нет индекса!! Или не находит!!!')
                    self.update_map()
                except Exception:
                    print('Не ищет! ужас')
        elif self.sender() == self.reset_search:
            self.pt = '~'.join(self.pt.split('~')[:-1])
            if len(self.addresses) > 1:
                self.addresses = self.addresses[:-1]
                self.address.setText(self.addresses[-1])
            if self.postal_index.isChecked():
                try:
                    self.geocoder_req = \
                        f'https://geocode-maps.yandex.ru/1.x?geocode="{self.search_input.text()}"' \
                        '&apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json'
                    self.response = requests.get(self.geocoder_req)
                    if self.response:
                        self.json_response = self.response.json()
                    if self.json_response["response"]["GeoObjectCollection"]["featureMember"]:
                        self.toponym = self.json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                    if len(self.addresses) != 1:
                        self.address.setText(
                            self.address.text() +
                            f', {self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}')
                except Exception:
                    print('У этого места нет индекса!! Или не находит!!!')
            self.update_map()

    def l_switch(self):
        if self.sender() == self.map_switch:
            self.l = 'map'
            self.update_map()
        elif self.sender() == self.sat_switch:
            self.l = 'sat'
            self.update_map()
        elif self.sender() == self.hyb_switch:
            self.l = 'sat,skl'
            self.update_map()

    def index_checked(self):
        if self.sender() == self.postal_index:
            try:
                if self.postal_index.isChecked():
                    if len(self.addresses) != 1:
                        self.address.setText(
                            self.address.text() +
                            f', {self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}')
            except Exception:
                print('У этого места нет индекса!! Или не находит!!!')
            try:
                if not self.postal_index.isChecked() and \
                        self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]:
                    if len(self.addresses) != 1:
                        self.address.setText(', '.join(self.address.text().split(', ')[:-1]))
            except Exception:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    exit(app.exec())
