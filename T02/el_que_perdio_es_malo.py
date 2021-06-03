import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
from PyQt5 import uic
import sys
import parametros as p

window_name, base_class = uic.loadUiType(p.PATH_VENTANA_PERDEDOR)

class TheLoserGuy(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def goodbye_my_friend(self):
        self.show()

    def salir(self):
        sys.exit()