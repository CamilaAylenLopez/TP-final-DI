import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from BaseDatos import *

class TicketWindow(QWidget):
    def __init__(self, idmesa):
        super().__init__()
        self.setWindowTitle("Ticket")
        self.setGeometry(100,100,600,400)

        self.layout_principal = QVBoxLayout()

        self.texto = QLabel("Ticket")
        self.layout_principal.addWidget(self.texto)

        self.setLayout(self.layout_principal)

        self.id = idmesa
        self.mostrarTicket()

    def mostrarTicket(self):
        consumo = ver_consumo_por_mesa(self.id)
        print(ver_consumo_por_mesa(5))
        for nombre, cantidad, precio in consumo:
            subtotal = cantidad * precio

            linea = QLabel(f"{nombre} x{cantidad} ${subtotal}")
            self.layout_principal.addWidget(linea)

        total = QLabel("Total: " + str(calcular_total_provisorio(self.id)))
        self.layout_principal.addWidget(total)