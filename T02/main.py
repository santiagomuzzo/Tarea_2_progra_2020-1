from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from inicial_window import InicialWindow
from final_window import FinalWindow
from entidad_dcc import DCC
from el_que_perdio_es_malo import TheLoserGuy
import sys


app = QApplication([]) 
lista_mapa = []
window = MainWindow()
inicial_window = InicialWindow()
final_window = FinalWindow()
dcc = DCC(window.display_x, window.display_y, lista_mapa)
loser = TheLoserGuy()
inicial_window.senal_nuevo_juego.connect(dcc.nuevo_juego)
inicial_window.senal_comenzar_ronda.connect(window.comienzo_ronda)
dcc.senal_nuevo_juego_armar.connect(window.iniciar_ventana_nueva)
window.senal_extender_lista_dcc.connect(dcc.actualizar_lista_extendida)
window.senal_nueva_reputacion.connect(dcc.mas_reputacion)

inicial_window.senal_continuar_juego.connect(dcc.cargar_mapa_seguir_juego) #se continua juego con datos anterioresa
dcc.senal_mandar_mapa.connect(window.cargar_mapa) #se envía mapa de datos anteriores. acá me falta actualizar el mapa y datos

dcc.senal_el_chef_cocina.connect(window.chef_trabajando)
dcc.senal_plato_recogido.connect(window.chef_trabajando)

window.senal_comenzar_ronda.connect(dcc.comienzo_ronda_dcc)
window.senal_traer_clientes.connect(dcc.arma_lista_clientes)
dcc.senal_nuevos_clientes.connect(window.llegada_clientes)
dcc.senal_aparece_bocadillo.connect(window.cliente_come)
dcc.senal_nuevo_estado_cliente.connect(window.metodo_cliente)
dcc.senal_termino.connect(window.cliente_termino)
window.senal_fin_ronda.connect(dcc.ronda_terminada)

window.senal_mover_jugador.connect(dcc.gamer.mover)
dcc.gamer.senal_nueva_posicion.connect(window.nueva_posicion)

window.senal_nuevo_drop.connect(dcc.revisar_cruce)
dcc.senal_comprobacion.connect(window.compra)
window.senal_acutalizar_lista.connect(dcc.actualizar_lista)
window.senal_eliminar_objeto.connect(dcc.eliminar_objeto)

dcc.senal_abrir_post_ronda.connect(final_window.armemos_y_abramos)
dcc.senal_perdiste.connect(loser.goodbye_my_friend)
dcc.senal_perdiste.connect(window.salir_perdedor)
final_window.senal_enviar_datos_guardar.connect(dcc.guardar_datos)

inicial_window.show()
sys.exit(app.exec_())