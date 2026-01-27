from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ConsultasBD import *

class TicketWindow(QWidget):
    def __init__(self, idmesa = -1):
        super().__init__()
        self.setWindowTitle("Ticket")
        self.setGeometry(500,100,300,600)

        self.id = idmesa
        if self.id == -1:
            QMessageBox.warning(self, "Error inesperado", "Ha ocurrido un error inesperado al no encontrar la mesa")
            return

        self.layout_principal = QVBoxLayout()

        self.texto = QLabel("Ticket")
        self.texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.texto.setStyleSheet("font-size: 24px;")
        self.layout_principal.addWidget(self.texto)

        self.setLayout(self.layout_principal)

        self.mostrarTicket()

    def mostrarTicket(self):
        consumo = ver_consumo_por_mesa(self.id)
        #print(ver_consumo_por_mesa(0))
        for nombre, cantidad, precio in consumo:
            subtotal = cantidad * precio

            linea = QLabel(f"{cantidad}  {nombre}   ---    ${subtotal}")
            self.layout_principal.addWidget(linea)

        total_provisorio = round(calcular_total_provisorio(self.id), 2)

        total = QLabel("Total: " + str(total_provisorio))
        total.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout_principal.addWidget(total)