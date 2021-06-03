import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
from PyQt5 import uic
import sys
import parametros as p
from classes_entities import Chef, Table
from drag_drop import ChefMove, TableMove
import time

window_name, base_class = uic.loadUiType(p.PATH_VENTANA_PRINCIPAL)

class MainWindow(window_name, base_class):

    senal_comenzar_ronda = core.pyqtSignal(bool)
    senal_pausar_juego = core.pyqtSignal()
    senal_mover_jugador = core.pyqtSignal(str)
    senal_nuevo_drop = core.pyqtSignal(list)
    senal_acutalizar_lista = core.pyqtSignal(list)
    senal_eliminar_objeto = core.pyqtSignal(list)
    senal_traer_clientes = core.pyqtSignal(bool)
    senal_fin_ronda = core.pyqtSignal(list)
    senal_extender_lista_dcc = core.pyqtSignal(list)
    senal_nueva_reputacion = core.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._frame = 1
        self.display_y = p.ANCHO_MAPA
        self.display_x = p.LARGO_MAPA
        self.setupUi(self)
        self.personajes = dict()
        self.label_personaje.raise_()
        self.personajes["personaje"] = self.label_personaje
        self.initUI()
        self.cuenta_mesas = 1
        self.cuenta_chefs = 1
        self.mi_propia_lista = []
        self.lista_clientes = []
        self.lista_clientes_activos = []
        self.numero_cliente = 0
        self.reloj = core.QTimer(self)
        self.perdidos = 0
        self.atendidos = 0
        self.sopa_de_letras = ""

    def initUI(self):
        self.setAcceptDrops(True)
        self.chef_label = ChefMove("ch1", self)
        self.chef_label.move(670, 245)
        self.chef_label.raise_()
        self.mesa_label = TableMove("T1", self)
        self.mesa_label.move(690, 360)
        self.mesa_label.raise_()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event): 
        pos = event.pos()
        if self.chef_label.press is True:
            if  pos.x() < 275 or pos.x() > p.LARGO_MAPA - 30 or pos.y() < 230 or pos.y() > \
                p.ANCHO_MAPA + 100 :
                print("posicion mala")
            else:
                self.cuenta_chefs += 1
                nuevo = ChefMove(f"ch{self.cuenta_chefs}", self)
                nuevo.move(pos)
                mas_nuevo = Chef()
                mas_nuevo.x = pos.x()
                mas_nuevo.y = pos.y()
                nuevo.x = pos.x()
                nuevo.y = pos.y()
                cuadro = widgets.QLabel(self)
                cuadro = core.QRect(core.QPoint(pos.x(), pos.y()), 
                                    core.QSize(p.CHEF_X, p.CHEF_Y))
                self.senal_nuevo_drop.emit(["agregar", "chef", pos.x(), pos.y(), cuadro, nuevo, mas_nuevo])
                self.chef_label.press = False
        if self.mesa_label.press is True:
            if pos.x() < 30 or pos.x() >= 275 or pos.y() < 230 or pos.y() > \
                p.ANCHO_MAPA + 100:
                print("posicion mala")
            else:
                self.cuenta_mesas +=1
                nuevo = TableMove(f"T{self.cuenta_mesas}", self)
                nuevo.move(pos)
                mas_nuevo = Table()
                mas_nuevo.x = pos.x()
                mas_nuevo.y = pos.y()
                nuevo.x = pos.x()
                nuevo.y = pos.y()
                cuadro = widgets.QLabel(self)
                cuadro = core.QRect(core.QPoint(pos.x(), pos.y()), 
                                    core.QSize(p.MESA_X, p.MESA_Y))
                self.senal_nuevo_drop.emit(["agregar", "mesa", pos.x(), pos.y(), cuadro, nuevo, mas_nuevo])
                self.mesa_label.press = False
        event.setDropAction(core.Qt.MoveAction)
        event.accept()

    def compra(self, event):
        if event[1] is True:
            event[0][5].show()
            self.plata_lcd.display(event[2])
            self.dinero = int(event[2])
            self.mi_propia_lista.append(event[0])
            self.senal_acutalizar_lista.emit(event[0])

    def mousePressEvent(self, event): 
        cuenta_chef = 0
        cuenta_mesa = 0
        for cosa in self.mi_propia_lista:
            if cosa[1] == "chef":
                cuenta_chef += 1
            elif cosa[1] == "mesa":
                cuenta_mesa += 1
        if cuenta_chef > 1: 
            for cosa in self.mi_propia_lista:
                if cosa[1] == "chef":
                    if cosa[5].quitar is True:
                        cosa[0] = "eliminar"
                        self.mi_propia_lista.remove(cosa)
                        self.senal_eliminar_objeto.emit(cosa)
                else:
                    cosa[5].show()
        if cuenta_mesa > 1:
            for cosa in self.mi_propia_lista:
                if cosa[1] == "mesa":
                    if cosa[5].quitar is True:
                        cosa[0] = "eliminar"
                        self.mi_propia_lista.remove(cosa)
                        self.senal_eliminar_objeto.emit(cosa)
                else:
                    cosa[5].show()
        else:
            print("no puedes eliminar más objetos")
            for cosa in self.mi_propia_lista:
                cosa[5].show()
                cosa[5].quitar = False
       
    def iniciar_ventana_nueva(self, event): 
        for cosa in event[0]:
            if cosa[1] == "chef":
                self.cuenta_chefs += 1
                nuevo = ChefMove(f"ch{self.cuenta_chefs}", self)
                nuevo1 = Chef()
                nuevo.x = int(cosa[2])
                nuevo.y =int(cosa[3])
                nuevo1.x = int(cosa[2])
                nuevo1.y = int(cosa[3])
                nuevo.move(int(cosa[2]), int(cosa[3]))
                nuevo.show()
                cosa.append(nuevo)
                cosa.append(nuevo1)
                self.mi_propia_lista.append(cosa)
            elif cosa[1] == "mesa":
                self.cuenta_mesas += 1
                nuevo = TableMove(f"T{self.cuenta_mesas}", self)
                nuevo1 = Table()
                nuevo.x = int(cosa[2])
                nuevo.y =int(cosa[3])
                nuevo1.x = int(cosa[2])
                nuevo1.y = int(cosa[3])     
                nuevo.move(int(cosa[2]), int(cosa[3]))
                nuevo.show()
                cosa.append(nuevo)
                cosa.append(nuevo1)
                self.mi_propia_lista.append(cosa)
            elif cosa[1] == "mesero":
                self.label_personaje.move(int(cosa[2]), int(cosa[3]))
        self.dinero = int(event[1][0])
        self.plata_lcd.display(event[1][0])
        self.reputacion_w = event[1][2]
        self.label_ronda.setText(f"RONDA N°{event[1][2]}")
        self.label_bar_progress.setValue(event[1][1])
        cuenta_platos = 0
        for chef in self.mi_propia_lista:
            if chef[1] == "chef":
                if len(event[1][3]) > 0:
                    chef[6].mi_cantidad_de_platos = int(event[1][3][cuenta_platos])
                    cuenta_platos += 1
        self.senal_extender_lista_dcc.emit(self.mi_propia_lista)
        self.show()

    def comienzo_ronda(self):
        for cosa in self.mi_propia_lista:
            cosa[5].disponible_para_quitar = False
        self.senal_comenzar_ronda.emit(True) 
        self.senal_traer_clientes.emit(True)

    def keyPressEvent(self, event): 
        if event.key() in [core.Qt.Key_A]:
            self.senal_mover_jugador.emit("L")
        elif event.key() in [core.Qt.Key_D]:
            self.senal_mover_jugador.emit("R")
        elif event.key() in [core.Qt.Key_S]:
            self.senal_mover_jugador.emit("D")
        elif event.key() in [core.Qt.Key_W]:
            self.senal_mover_jugador.emit("U")
        if event.key() in [core.Qt.Key_M]:
            self.sopa_de_letras += "M"
        if event.key() in [core.Qt.Key_O]:
            self.sopa_de_letras += "O"
        if event.key() in [core.Qt.Key_N]:
            self.sopa_de_letras += "N"
        if event.key() in [core.Qt.Key_F]:
            self.sopa_de_letras += "F"
        if event.key() in [core.Qt.Key_I]:
            self.sopa_de_letras += "I"
        if event.key() in [core.Qt.Key_R]:
            self.sopa_de_letras += "R"
        if event.key() in [core.Qt.Key_T]:
            self.sopa_de_letras += "T"
        if event.key() in [core.Qt.Key_G]:
            self.sopa_de_letras += "G"
        if self.sopa_de_letras[-3:] == "MON":
            self.dinero += p.DINERO_TRAMPA
            self.plata_lcd.display(self.dinero)
            self.sopa_de_letras = ""
        if self.sopa_de_letras[-3:] == "RTG":
            self.reputacion_w += p.REPUTACION_TRAMPA
            if self.reputacion_w > 5:
                self.reputacion_w = 5
            self.label_bar_progress.setValue(self.reputacion_w)
            self.senal_nueva_reputacion.emit(self.reputacion_w)
            self.sopa_de_letras = ""

    def nueva_posicion(self, event):   
        char = self.personajes[event["char"]]
        if event["pedido"] is False:
            if event.get("sprite"):
                pixmap = gui.QPixmap(f"sprites/mesero/{event['sprite']}_0{event['frame']}.png")
                pixmap = pixmap.scaled(32, 32)
                char.setPixmap(pixmap)
            char.move(event['x'], event['y'])
        else:
            pixmap = gui.QPixmap(f"sprites/mesero/{event['sprite']}_snack_0{event['frame']}.png")
            pixmap = pixmap.scaled(32, 32)
            char.setPixmap(pixmap)
            char.move(event['x'], event['y'])

    def cargar_mapa(self, event):
        for cosa in event[0]:
            if cosa[1] == "chef":
                self.cuenta_chefs += 1
                nuevo = ChefMove(f"ch{self.cuenta_chefs}", self)
                nuevo1 = Chef()
                nuevo.x = int(cosa[2])
                nuevo.y =int(cosa[3])
                nuevo1.x = int(cosa[2])
                nuevo1.y = int(cosa[3])
                nuevo.move(int(cosa[2]), int(cosa[3]))
                nuevo.show()
                cosa.append(nuevo)
                cosa.append(nuevo1)
                self.mi_propia_lista.append(cosa)
            elif cosa[1] == "mesa":
                self.cuenta_mesas += 1
                nuevo = TableMove(f"T{self.cuenta_mesas}", self)
                nuevo1 = Table()
                nuevo.x = int(cosa[2])
                nuevo.y =int(cosa[3])
                nuevo1.x = int(cosa[2])
                nuevo1.y = int(cosa[3])     
                nuevo.move(int(cosa[2]), int(cosa[3]))
                nuevo.show()
                cosa.append(nuevo)
                cosa.append(nuevo1)
                self.mi_propia_lista.append(cosa)
            elif cosa[1] == "mesero":
                self.label_personaje.move(int(cosa[2]), int(cosa[3]))
        self.plata_lcd.display(event[1][0])
        self.dinero = int(event[1][0])
        self.label_ronda.setText(f"RONDA N°{event[1][2]}")
        self.reputacion_w = event[1][1]
        self.label_bar_progress.setValue(event[1][1])
        self.show()
        cuenta_platos = 0
        for chef in self.mi_propia_lista:
            if chef[1] == "chef":
                if len(event[1][3]) > 0:
                    chef[6].mi_cantidad_de_platos = int(event[1][3][cuenta_platos])
                    cuenta_platos += 1
        self.senal_extender_lista_dcc.emit(self.mi_propia_lista)
                
    def llegada_clientes(self, event):
        cuenta_platos = 0
        for chef in self.mi_propia_lista:
            if chef[1] == "chef":
                chef[6].mi_cantidad_de_platos = int(event[3][cuenta_platos])
                cuenta_platos += 1
        self.label_bar_progress.setValue(event[2])
        self.label_ronda.setText(f"RONDA N°{event[1]}")
        self.numero_cliente = 0
        self.perdidos = 0
        self.atendidos = 0
        self.cantidad_atendidos.setText(str(self.atendidos))
        self.cantidad_perdidos.setText(str(self.perdidos))
        self.cantidad = len(event[0])
        self.proximos_atender.setText(str(self.cantidad))
        self.lista_clientes = event[0]
        for cliente in self.lista_clientes:
            cliente.label = widgets.QLabel(self)
            cliente.label.setPixmap(gui.QPixmap(f"sprites/clientes/perro/perro_01.png"))
            cliente.label.setGeometry(0, 0, p.CLIENTE_X, p.CLIENTE_Y)
            cliente.label.setScaledContents(True)     
        self.reloj.timeout.connect(self.sentar_clientes)
        self.reloj.start(p.LLEGADA_CLIENTES)
  
    def sentar_clientes(self): 
        if len(self.lista_clientes) > self.numero_cliente:
            cliente_actual = self.lista_clientes[self.numero_cliente]           
            for mesa in self.mi_propia_lista:
                if mesa[1] == "mesa":
                    if mesa[6].ocupada is False:                      
                        cliente_actual.label.setGeometry(mesa[6].x, mesa[6].y - 10, p.CLIENTE_X, p.CLIENTE_Y)
                        cliente_actual.x = mesa[6].x
                        cliente_actual.y = mesa[6].y - 10
                        cliente_actual.label.show()
                        cliente_actual.start()
                        mesa[6].cliente = cliente_actual
                        mesa[6].ocupada = True
                        self.lista_clientes_activos.append(cliente_actual)
                        self.numero_cliente += 1
                        if len(self.lista_clientes) == self.numero_cliente:
                            cliente_actual.ultimo = True
                        self.cantidad -= 1
                        self.proximos_atender.setText(str(self.cantidad))
                        break
        else:
            self.reloj.stop()
            self.numero_cliente = 0
           
    def metodo_cliente(self, event):
        if event.frame == 14:
            for cliente in self.lista_clientes:
                if cliente.x == event.x and cliente.y == event.y:
                    cliente.label.setPixmap(gui.QPixmap(f"sprites/clientes/perro/perro_{event.frame}.png"))
                    cliente.label.setGeometry(cliente.x - 12, cliente.y - 13, p.CLIENTE_X_ENOJADO, p.CLIENTE_Y_ENOJADO)
                    cliente.label.setScaledContents(True)
                    
    def cliente_termino(self, event):
        for cliente in self.lista_clientes:
            if cliente == event:
                event.label.hide()
                if cliente.atendido:
                    self.atendidos += 1
                    self.cantidad_atendidos.setText(str(self.atendidos))
                    self.dinero += p.PRECIO_BOCADILLO 
                    self.plata_lcd.display(self.dinero)
                else:
                    self.perdidos += 1
                    print(self.perdidos, "perdido")
                    self.cantidad_perdidos.setText(str(self.perdidos))
                for objeto in self.mi_propia_lista:
                    if objeto[6].x == cliente.x and objeto[6].y == cliente.y + 10:
                        objeto[6].ocupada = False
                        objeto[6].llego_pedido = False
                        if objeto[6].label_bocadillo != "":
                            objeto[6].label_bocadillo.hide()
                if cliente.ultimo is True:
                    print("cliente ultimo") 
                    for cosa in self.mi_propia_lista:
                        if cosa[1] == "chef":
                            cosa[5].show()
                            cosa[6].label.hide()
                            cosa[6].cocinando = False
                            cosa[6].plato_listo = False
                    time.sleep(10)
                    self.senal_fin_ronda.emit([self.atendidos, self.perdidos, self.dinero])
                break

    def chef_trabajando(self, event): 
        for cosa in self.mi_propia_lista:
            if cosa[1] == "chef":
                if event.x == cosa[6].x and event.y == cosa[6].y:
                    if event.frame < 10:
                        frame = f"0{event.frame}"
                    else:
                        frame = event.frame
                    if event.frame != 1:
                        event.label.hide()
                    event.label = widgets.QLabel(self)
                    event.label.setPixmap(gui.QPixmap(f"sprites/chef/meson_{frame}.png"))
                    event.label.setGeometry(event.x, event.y, p.CHEF_X, p.CHEF_Y)
                    event.label.show()
                    cosa[5].hide()  
                    break
    
    def cliente_come(self, mesa):
        mesa.label_bocadillo = widgets.QLabel(self)
        mesa.label_bocadillo.setPixmap(gui.QPixmap(p.PATH_BOCADILLO))
        mesa.label_bocadillo.setGeometry(mesa.x + 4, mesa.y, p.MESA_X, p.MESA_Y)
        mesa.label_bocadillo.show()

    def salir(self):
        sys.exit()

    def salir_perdedor(self):
        self.hide()
