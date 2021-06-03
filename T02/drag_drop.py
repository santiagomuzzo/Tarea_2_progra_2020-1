import os
import parametros as p
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import sys


class ChefMove(widgets.QLabel):
    def __init__(self, label, parent):
        super().__init__(label, parent)
        self.nombre = label
        ruta = os.path.join("sprites/chef/meson_01.png")
        pix = gui.QPixmap(ruta)
        self.setPixmap(pix)
        self.x = 0
        self.y = 0
        self.resize(p.CHEF_X, p.CHEF_Y)
        self.press = False
        self.quitar = False
        self.disponible_para_quitar = True

    def mouseMoveEvent(self, event):
        if event.buttons() == core.Qt.LeftButton:
            m_data = core.QMimeData()
            drag = gui.QDrag(self)
            drag.setMimeData(m_data)
            pixmap = gui.QPixmap(self.size())
            painter = gui.QPainter(pixmap)
            painter.drawPixmap(self.rect(),
                            self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            dropAction = drag.exec_(core.Qt.CopyAction | core.Qt.MoveAction)
        else:
            return

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.press = True
        if event.button() == core.Qt.RightButton:
            if self.nombre == "ch1":
                return
            else:
                if self.disponible_para_quitar is True:
                    self.quitar = True
                    self.hide()


class TableMove(widgets.QLabel):
    def __init__(self, label, parent):
        super().__init__(label, parent)
        ruta = os.path.join("sprites/mapa/accesorios/silla_mesa_amarilla.png")
        pix = gui.QPixmap(ruta)
        self.setPixmap(pix)
        self.nombre = label
        self.x = 0
        self.y = 0
        self.resize(p.MESA_X, p.MESA_Y)
        self.press = False
        self.quitar = False
        self.disponible_para_quitar = True

    def mouseMoveEvent(self, event):
        if event.buttons() == core.Qt.LeftButton:
            m_data = core.QMimeData()
            drag = gui.QDrag(self)
            drag.setMimeData(m_data)
            pixmap = gui.QPixmap(self.size())
            painter = gui.QPainter(pixmap)
            painter.drawPixmap(self.rect(),
                            self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            dropAction = drag.exec_(core.Qt.CopyAction | core.Qt.MoveAction)
        else:
            return

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.press = True
        if event.button() == core.Qt.RightButton:
            if self.nombre == "T1":
                return
            else:
                if self.disponible_para_quitar is True:
                    self.quitar = True
                    self.hide()
            
