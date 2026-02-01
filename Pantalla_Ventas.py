from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ConsultasBD import *

class VentasWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial ventas")
        self.setGeometry(500,100,300,300)

        self.historial()
    
    def historial(self):
        layout = QVBoxLayout()

        self.titulo = QLabel("Historial de ventas...")
        self.titulo.setAlignment(Qt.AlignTop)
        self.titulo.setStyleSheet("font-size: 18px; font-weight: bold; padding: 2px;")
        layout.addWidget(self.titulo)

        self.ventas = QLabel("")
        self.ventas.setAlignment(Qt.AlignTop)
        self.ventas.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.ventas)

        self.setLayout(layout)

        self.cargar_historial()
        
    def cargar_historial(self):
        try:
            with open("historial_ventas.txt", 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.ventas.setText(contenido)
        except FileNotFoundError:
            self.ventas.setText("No hay ventas registradas.")