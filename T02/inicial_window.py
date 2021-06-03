import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
from PyQt5 import uic
import parametros as p
import sys


window_name, base_class = uic.loadUiType(p.PATH_VENTANA_INICIAL)


class InicialWindow(window_name, base_class):

    #aqui va una señal?
    senal_nuevo_juego = core.pyqtSignal()
    senal_continuar_juego = core.pyqtSignal()
    senal_comenzar_ronda = core.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def new_game(self):
        self.senal_nuevo_juego.emit()
        self.senal_comenzar_ronda.emit()
        self.hide()

    def continue_game(self):
        self.senal_continuar_juego.emit()
        self.hide()

    
if __name__ == '__main__':
    app = widgets.QApplication([])
    window = InicialWindow()
    sys.exit(app.exec())