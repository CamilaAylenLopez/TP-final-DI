from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ConsultasBD import *

class TicketWindow(QWidget):
    def __init__(self, idmesa = -1):
        super().__init__()
        self.setWindowTitle("Ticket")
        self.setGeometry(500,100,345,600)

        self.id = idmesa
        if self.id == -1:
            QMessageBox.warning(self, "Error inesperado", "Ha ocurrido un error inesperado al no encontrar la mesa")
            return

        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(20, 20, 20, 20)

        self.titulo = QLabel("Ticket")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout_principal.addWidget(self.titulo)

        self.direccion = QLabel("Calle ficticia 123\n46004 Ruzafa\nEspaña\nTel: 12345678")
        self.direccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.direccion.setStyleSheet("font-size: 16px; color: #9b9b9b;")
        self.layout_principal.addWidget(self.direccion)

        self.setLayout(self.layout_principal)

        self.mostrarTicket()

    def mostrarTicket(self):
        consumo = ver_consumo_por_mesa(self.id)
        #print(ver_consumo_por_mesa(0))
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(len(consumo))
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setHorizontalHeaderLabels(["cantidad", "Producto", "SubTotal"])

        for fila, (nombre, cantidad, precio) in enumerate(consumo):
            subtotal = cantidad * precio

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(nombre)))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(subtotal)))
        
        self.layout_principal.addWidget(self.tabla)

        total_provisorio = round(calcular_total_provisorio(self.id), 2)

        total = QLabel("Total: " + str(total_provisorio))
        total.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout_principal.addWidget(total)