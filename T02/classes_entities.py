import sys
import random
import time
from math import floor
import PyQt5.QtCore as core
import parametros as p
import PyQt5.QtWidgets as widgets
import time
import PyQt5.QtGui as gui
import os
from funciones import actualizar_armar_mapa, actualizar_reiniciar_datos, armar_lista, \
    recordar_datos


class Jugador(core.QObject):

    senal_nueva_posicion = core.pyqtSignal(dict)
    senal_con_comida = core.pyqtSignal()

    def __init__(self, x, y, dcc):
        super().__init__()
        self.display_x = x
        self.display_y = y
        self.dcc = dcc
        self.__x = p.X_INICIAL
        self.__y = p.Y_INICIAL
        self.__frame = 2
        self.direccion = "up"
        self.lista_cosas = []
        self.llevo_comida = False

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self.__frame = 1
        else:
            self.__frame = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        predecir = core.QRect(core.QPoint(value, self.y), 
                              core.QSize(p.MESERO_X, p.MESERO_Y))
        choque = 0
        if 27 < value < self.display_x:
            for cosa in self.dcc.obstaculos:
                if cosa[1] != "mesero":
                    if cosa[4].intersects(predecir):
                        choque += 1
                        if type(cosa[6]) is Chef:
                            if cosa[6].cocinando is False and self.llevo_comida is False and \
                                cosa[6].plato_listo is False:
                                cosa[6].cocinando = True
                                self.dcc.mesero_choque_chef(cosa[6])
                            if cosa[6].plato_listo is True and self.llevo_comida is False:
                                cosa[6].plato_listo = False 
                                self.llevo_comida = True
                                self.dcc.plato_recogido(cosa[6])
                                cosa[6].cocinando = False
                        if type(cosa[6]) is Table:
                            if cosa[6].ocupada is True and self.llevo_comida is True and \
                                cosa[6].llego_pedido is False:
                                self.llevo_comida = False
                                cosa[6].cliente.atendido = True
                                cosa[6].llego_pedido = True
                                self.dcc.llego_bocadillo(cosa[6])
            if choque == 0:
                self.__x = value
                self.senal_nueva_posicion.emit(
                    {'char': 'personaje',
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": self.direccion, 
                    "pedido": self.llevo_comida})
            
    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        predecir = core.QRect(core.QPoint(self.x, value), 
                              core.QSize(p.MESERO_X, p.MESERO_Y))
        choque = 0
        if 220 < value < self.display_y + 130:
            for cosa in self.dcc.obstaculos:
                if cosa[1] != "mesero":
                    if cosa[4].intersects(predecir):
                        choque += 1
                        if type(cosa[6]) is Chef:
                            if cosa[6].cocinando is False and self.llevo_comida is False and \
                                cosa[6].plato_listo is False:
                                cosa[6].cocinando = True
                                self.dcc.mesero_choque_chef(cosa[6])
                            if cosa[6].plato_listo is True and self.llevo_comida is False:
                                cosa[6].plato_listo = False
                                self.llevo_comida = True
                                self.dcc.plato_recogido(cosa[6])
                                cosa[6].cocinando = False
                        if type(cosa[6]) is Table:
                            if cosa[6].ocupada is True and self.llevo_comida is True and \
                                cosa[6].llego_pedido is False:
                                self.llevo_comida = False
                                cosa[6].cliente.atendido = True
                                cosa[6].llego_pedido = True
                                self.dcc.llego_bocadillo(cosa[6])
            if choque == 0:
                self.__y = value
                self.senal_nueva_posicion.emit(
                    {'char': 'personaje',
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": self.direccion, 
                    "pedido": self.llevo_comida})

    def mover(self, event):
        if self.dcc.disponibilidad is True:
            self.frame += 1
            if event == 'R':
                self.direccion = "right"
                self.x += p.VEL_MOVIMIENTO
            if event == 'L':
                self.direccion = "left"
                self.x -= p.VEL_MOVIMIENTO
            if event == 'U':  
                self.direccion = "up"
                self.y -= p.VEL_MOVIMIENTO
            if event == 'D':
                self.direccion = "down"
                self.y += p.VEL_MOVIMIENTO

    
class Cliente(core.QThread):

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.label = ""
        self.espera = 0
        self.probabilidad = 0
        self.frame = 1
        self.en_mesa = False
        self.senal_nuevo_estado_cliente = None
        self.senal_termino = None
        self.termino = False
        self.enojado = False
        self.ultimo = False
        self.atendido = False

    def run(self):
        self.atendido = False
        self.en_mesa = True
        time.sleep(self.espera / 2)
        self.frame = 14
        if self.atendido is False:
            self.enojado = True
            self.senal_nuevo_estado_cliente.emit(self)
        time.sleep(self.espera / 2)
        self.en_mesa = False
        self.termino = True
        print("termino")
        self.senal_termino.emit(self)
        self.exit()


class Chef(core.QThread):

    senal_estoy_cocinando = core.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.label = widgets.QLabel()
        self.frame = 0
        self.cocinando = False
        self.plato_listo = False
        self.mi_cantidad_de_platos = 0
        self.nivel_experiencia()
        
    def run(self):
        cocinando = 16
        self.frame = 0
        while cocinando > 0:
            time.sleep(0.5)
            self.frame += 1
            cocinando -= 1
            self.senal_estoy_cocinando.emit(self)
        print("termino de cocinar")
        self.cocinando = False
        fallo = self.probabilidad_fallo()
        num_random = random.random()
        if num_random <= fallo:
            self.plato_listo = False
            print("se quemo la comida")
        else:
            self.plato_listo = True
            self.mi_cantidad_de_platos += 1
            self.nivel_experiencia()
        self.frame = 0
        self.exit()

    def nivel_experiencia(self):
        if self.mi_cantidad_de_platos <= p.PLATOS_INTERMEDIO:
            self.chef_nivel = p.EXP_PRINCIPIANTE
        if self.mi_cantidad_de_platos >= p.PLATOS_INTERMEDIO and \
            self.mi_cantidad_de_platos < p.PLATOS_EXPERTO:
            self.chef_nivel = p.EXP_INTERMEDIO
        if self.mi_cantidad_de_platos >= p.PLATOS_EXPERTO:
            self.chef_nivel = p.EXP_EXPERTO

    def probabilidad_fallo(self):
        self.prob_fallo = p.FALLAR_NUMERAODR / (self.chef_nivel + p.FALLAR_DENOMINADOR)
        return self.prob_fallo


class Table:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ocupada = False
        self.llego_pedido = False
        self.cliente = ""
        self.label_bocadillo = ""


class Bocadillo:
    def __init__(self, dcc):
        self.precio = p.PRECIO_BOCADILLO
        self.tiempo_prepa = 0
        self.calidad_pedido = 0
    
    def tiempo_preparacion(self):
        pass

