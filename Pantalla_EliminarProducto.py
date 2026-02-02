from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ConsultasBD import *

class EliminarProductoDialog(QDialog):
    def __init__(self, idmesa):
        super().__init__()
        self.setWindowTitle("Eliminar producto")
        self.idmesa = idmesa
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.texto = QLabel("Seleccione el producto para eliminar:")
        layout.addWidget(self.texto)

        self.opciones = QComboBox()
        self.cargar_productos()
        layout.addWidget(self.opciones)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        layout.addWidget(self.btn_eliminar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.close)
        layout.addWidget(self.btn_cancelar)
    
    def cargar_productos(self):
        productos = ver_consumo_por_mesa(self.idmesa)

        for nombre, cantidad, precio, categoria in productos:
            datos = f"{nombre} ({categoria}) - Cantidad: {cantidad}"
            self.opciones.addItem(datos, (nombre, categoria))
    
    def eliminar_producto(self):
        if self.opciones.count() == 0:
            QMessageBox.warning(self, "Error", "No hay ningun producto para eliminar.")
            return
        
        (nombre, categoria) = self.opciones.currentData()

        idProducto = obtener_id_producto(nombre, categoria)
        eliminar_producto_de_mesa(self.idmesa, idProducto)

        QMessageBox.information(self, "Producto eliminado", f"Se eliminó 1 unidad de '{nombre}'")
        self.close()
