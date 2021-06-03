import parametros as p
import os


def actualizar_armar_mapa(lista):
    with open(p.PATH_MAPA, "w", encoding="utf/8") as mapa:
        for cosa in lista:
            mapa.write(str(cosa[1]) + ",")
            mapa.write(str(cosa[2]) + ",")
            mapa.write(str(cosa[3]) + "\n")


def armar_lista(lista_mapa):
    with open(p.PATH_MAPA, "r", encoding="utf-8") as mapa:
        archivo = mapa.readlines()
        for i in archivo:
            linea = i.strip().split(",")
            objeto = ["agregar", linea[0], linea[1], linea[2]]
            lista_mapa.append(objeto)


def actualizar_reiniciar_datos(din, rep, ron, lista):
    with open(p.PATH_DATOS, "w", encoding="utf/8") as datos:
        datos.write(str(din) + ",")
        datos.write(str(rep) + ",")
        datos.write(str(ron) + "\n")
        if len(lista) == 0:
            datos.write("0")
        largo = len(lista)
        elemento = 1
        for cosa in lista:
            if len(lista) == elemento:
                datos.write(str(cosa))
            else:
                datos.write(str(cosa) + ",")
            elemento += 1


def recordar_datos(din, rep, ron, lista):
    with open(p.PATH_DATOS, "r", encoding="utf/8") as datos:
        archivo = datos.readlines()
        linea = archivo[0].strip().split(",")
        din = linea[0]
        rep = linea[1]
        ron = linea[2]
        linea_2 = archivo[1].strip().split(",")
        lista = linea_2
        if lista[0] != '':
            for cosa in lista:
                cosa = int(cosa)
        lista_final = [int(din), int(rep), int(ron), lista]
        return lista_final

