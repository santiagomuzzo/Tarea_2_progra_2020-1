import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
from PyQt5 import uic
import sys
import parametros as p
from funciones import actualizar_armar_mapa, actualizar_reiniciar_datos
import time

window_name, base_class = uic.loadUiType(p.PATH_VENTANA_FINAL)


class FinalWindow(window_name, base_class):
    
    senal_enviar_datos_guardar = core.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.mi_ultima_lista = []
        self.setupUi(self)

    def armemos_y_abramos(self, event):
        self.dinero = event[0][1]
        self.reputacion_final = event[0][3]
        self.ronda = event[0][0]
        self.lista_chef = event[2]
        self.mi_ultima_lista = event[1]
        self.titulo_ronda.setText(f"RESUMEN RONDA N°{event[0][0]}")
        self.dinero_acumulado_lcd.display(event[0][1])
        self.reputacion.setText(f"{event[0][3]}/5")
        if len(event[0][2]) > 1:
            self.atendidos_lcd.display(event[0][2][0])
            self.perdidos_lcd.display(event[0][2][1])
        self.show()
        
    def salir(self):
        sys.exit()

    def guardar(self): 
        self.senal_enviar_datos_guardar.emit()

    def continuar(self): 
        self.hide()