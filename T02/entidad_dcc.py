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
from classes_entities import Jugador, Chef, Table, Cliente, Bocadillo


class DCC(core.QObject):
    
    senal_mandar_mapa = core.pyqtSignal(list)
    senal_comprobacion = core.pyqtSignal(list)
    senal_nuevos_clientes = core.pyqtSignal(list)
    senal_nuevo_juego_armar = core.pyqtSignal(list)
    senal_nuevo_estado_cliente = core.pyqtSignal(object)
    senal_termino = core.pyqtSignal(object)
    senal_el_chef_cocina = core.pyqtSignal(object)
    senal_abrir_post_ronda = core.pyqtSignal(list)
    senal_plato_recogido = core.pyqtSignal(object)
    senal_aparece_bocadillo = core.pyqtSignal(object)
    senal_perdiste = core.pyqtSignal()

    def __init__(self, x, y, mapa):
        super().__init__()
        self.obstaculos = []
        self.lista_clientes = []
        self.lista_platos_chef = [0, 0, 0, 0]
        self.mapa = mapa
        self.gamer = Jugador(x, y, self)
        self.bocadillo = Bocadillo(self)
        self.ronda = 1
        self.dinero = p.DINERO_INICIAL
        self.chefs_iniciales = p.CHEFS_INICIALES
        self.mesas_iniciales = p.MESAS_INICIALES
        self.clientes_inciales = p.CLIENTES_INICIALES
        self.cuenta_chefs = p.CHEFS_INICIALES
        self.cuenta_mesas = p.MESAS_INICIALES
        self.pedidos_totales = 0
        self.pedidos_exitosos = 0
        self.reputacion = p.REPUTACION_INICIAL
        self.disponibilidad = False
        self.contador_prueba = 0
        
    def actualizar_lista(self, event):
        if event[0] == "agregar":
            if event[1] == "chef":
                self.obstaculos.append(event)
            elif event[1] == "mesa":
                self.obstaculos.append(event)

    def actualizar_lista_extendida(self, event):
        self.obstaculos = event

    def guardar_datos(self):
        actualizar_armar_mapa(self.obstaculos)
        actualizar_reiniciar_datos(self.dinero, self.reputacion, self.ronda - 1, self.lista_platos_chef)

    def cargar_mapa_seguir_juego(self):  
        armar_lista(self.mapa)
        datos_actual = recordar_datos(self.dinero, self.reputacion, self.ronda, self.lista_platos_chef)
        self.dinero = datos_actual[0]
        self.reputacion = datos_actual[1]
        self.ronda = datos_actual[2] + 1
        self.lista_platos_chef = datos_actual[3]
        for i in self.mapa:
            if i[1] == "chef":
                cuadro = widgets.QLabel()
                cuadro = core.QRect(core.QPoint(int(i[2]), int(i[3])), 
                                    core.QSize(p.CHEF_X, p.CHEF_Y))
                i.append(cuadro)
                self.cuenta_chefs += 1       
            elif i[1] == "mesa":
                cuadro = widgets.QLabel()
                cuadro = core.QRect(core.QPoint(int(i[2]), int(i[3])), 
                                    core.QSize(p.MESA_X, p.MESA_Y))               
                i.append(cuadro)
                self.cuenta_mesas += 1
            elif i[1] == "mesero":
                cuadro = widgets.QLabel()
                cuadro = core.QRect(core.QPoint(int(i[2]), int(i[3])), 
                                    core.QSize(p.MESERO_X, p.MESERO_Y))
                self.gamer.x = int(i[2])
                self.gamer.y = int(i[3])
                i.append(cuadro)
            self.obstaculos.append(i)        
        self.senal_mandar_mapa.emit([self.obstaculos, [self.dinero, self.reputacion, self.ronda,\
            self.lista_platos_chef]])

    def revisar_cruce(self, event):
        if self.disponibilidad is False:
            cruce = 0
            if event[0] == "agregar":
                for cosa in self.obstaculos:
                    if cosa[4].intersects(event[4]):
                        cruce += 1
                if cruce == 0:
                    if event[1] == "mesa" and self.dinero >= 100:
                        self.dinero -= 100
                        self.senal_comprobacion.emit([event, True, self.dinero])
                    elif event[1] == "chef" and self.dinero >= 300:
                        self.dinero -= 300
                        self.senal_comprobacion.emit([event, True, self.dinero])
                else:
                    self.senal_comprobacion.emit([event, False])
    
    def eliminar_objeto(self, event):      
        if event[0] == "eliminar":  #señal que vendrá desde un mousePressEvent
            for cosa in self.obstaculos:
                if cosa[1] == event[1] and cosa[2] == event[2] and cosa[3] == event[3]:
                    self.obstaculos.remove(cosa)

    def clientes_ronda(self):
        cantidad_clientes = p.CANTIDAD_CLIENTES_M * (p.CANTIDAD_CLIENTES_S + self.ronda)
        return cantidad_clientes

    def arma_lista_clientes(self, event):
            contador = 0
            clientes = self.clientes_ronda()
            self.lista_clientes = []
            while contador < clientes:
                tipo_prob = random.random()
                if tipo_prob <= p.PROB_APURADO:
                    nuevo_cliente = Cliente()
                    nuevo_cliente.espera = p.TIEMPO_ESPERA_APURADO
                    nuevo_cliente.senal_nuevo_estado_cliente = self.senal_nuevo_estado_cliente
                    nuevo_cliente.senal_termino = self.senal_termino
                else:
                    nuevo_cliente = Cliente()
                    nuevo_cliente.espera = p.TIEMPO_ESPERA_RELAJADO
                    nuevo_cliente.senal_nuevo_estado_cliente = self.senal_nuevo_estado_cliente
                    nuevo_cliente.senal_termino = self.senal_termino
                self.lista_clientes.append(nuevo_cliente)
                contador += 1
            self.pedidos_totales = len(self.lista_clientes)
            if self.disponibilidad is True:
                self.senal_nuevos_clientes.emit([self.lista_clientes, self.ronda, self.reputacion,\
                    self.lista_platos_chef])

    def comienzo_ronda_dcc(self, event):
        if event is True:
            self.disponibilidad = True
        
    def calcular_reputacion(self):
        nueva_rep = max(p.REPUTACION_DESDE1, min(p.REPUTACION_DESDE2, (self.reputacion + \
            floor(p.REPUTACION_M * (self.pedidos_exitosos / self.pedidos_totales) - p.REPUR))))
        self.reputacion = nueva_rep
        return self.reputacion

    def nuevo_juego(self):
        self.obstaculos = []
        lista_envi = []
        numero = 0
        for m in range(self.chefs_iniciales):
            lista = []
            chef_x = random.randint(276, p.LARGO_MAPA - 30)
            chef_y = random.randint(231, p.ANCHO_MAPA + 100)
            cuadro = widgets.QLabel()
            cuadro = core.QRect(core.QPoint(chef_x, chef_y), 
                                core.QSize(p.CHEF_X, p.CHEF_Y))
            lista.append("agregar")
            lista.append("chef")
            lista.append(chef_x)
            lista.append(chef_y)
            lista.append(cuadro)
            lista_envi.append(lista)
            self.obstaculos.append(lista)
            self.cuenta_chefs += 1            
        for m in range(self.mesas_iniciales):
            lista = []
            mesa_x = random.randint(30, 275)
            mesa_y = random.randint(230, p.ANCHO_MAPA + 100)
            cuadro = widgets.QLabel()
            cuadro = core.QRect(core.QPoint(mesa_x, mesa_y), 
                                core.QSize(p.MESA_X, p.MESA_Y))
            lista.append("agregar")
            lista.append("mesa")
            lista.append(mesa_x)
            lista.append(mesa_y)
            lista.append(cuadro)
            lista_envi.append(lista)
            self.obstaculos.append(lista)
            self.cuenta_mesas += 1
        mesero_x = random.randint(30, p.LARGO_MAPA - 30)
        mesero_y = random.randint(230, p.ANCHO_MAPA + 100)
        cuadro = widgets.QLabel()
        cuadro = core.QRect(core.QPoint(mesero_x, mesero_y), 
                            core.QSize(p.MESERO_X, p.MESERO_Y))
        self.gamer.x = mesero_x
        self.gamer.y = mesero_y
        lista = ["agregar", "mesero", mesero_x, mesero_y, cuadro]
        lista_envi.append(lista)
        self.obstaculos.append(lista)
        actualizar_armar_mapa(self.obstaculos)  # funcion guarda mapa
        self.mapa = []
        armar_lista(self.mapa)
        self.disponibilidad = True
        self.dinero = p.DINERO_INICIAL
        self.reputacion = p.REPUTACION_INICIAL
        self.ronda = 1
        actualizar_reiniciar_datos(self.dinero, self.reputacion, self.ronda, [])   
        self.senal_nuevo_juego_armar.emit([lista_envi, [self.dinero, self.reputacion, self.ronda,\
            self.lista_platos_chef]])
        
    def ronda_terminada(self, lista):  # se encarga de abrir ventana post ronda
        self.pedidos_exitosos = lista[0]
        self.reputacion = self.calcular_reputacion()
        self.disponibilidad = False
        self.dinero = lista[2]
        datos_chef = []
        for cosa in self.obstaculos:
            if cosa[1] == "chef":
                datos_chef.append(cosa[6].mi_cantidad_de_platos)
        self.lista_platos_chef = datos_chef
        datos_ronda = [self.ronda, self.dinero, [self.pedidos_exitosos, lista[1]], self.reputacion]
        datos_mapa = self.obstaculos
        if self.reputacion == 0:
            self.senal_perdiste.emit()
        else:
            self.senal_abrir_post_ronda.emit([datos_ronda, datos_mapa, datos_chef])                                   
        self.ronda += 1

    def mas_reputacion(self, event):
        self.reputacion = event

    def mesero_choque_chef(self, chef):
        chef.start()
        chef.senal_estoy_cocinando.connect(self.chef_cocinando)
        
    def chef_cocinando(self, event): 
        self.senal_el_chef_cocina.emit(event)

    def plato_recogido(self, chef):
        chef.frame += 1
        self.senal_plato_recogido.emit(chef)

    def llego_bocadillo(self, mesa):
        self.senal_aparece_bocadillo.emit(mesa)
