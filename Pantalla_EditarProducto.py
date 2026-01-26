from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from BaseDatos import modificar_producto, obtener_id_producto

class FormularioEmergente(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar producto")
        self.setGeometry(100,100,600,400)

        self.formulario()
    
    def formulario(self):
        layout = QVBoxLayout()

        self.texto_nombre = QLabel("Producto")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del producto")
        layout.addWidget(self.texto_nombre)
        layout.addWidget(self.input_nombre)

        self.texto_precio = QLabel("Precio")
        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Nombre del producto")
        layout.addWidget(self.texto_precio)
        layout.addWidget(self.input_precio)

        self.texto_categoria = QLabel("Categoria:")
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["Desayuno", "Almuerzo", "Merienda", "Refrescos"])
        layout.addWidget(self.texto_categoria)
        layout.addWidget(self.combo_categoria)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_datos)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.close)
        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_cancelar)

        self.setLayout(layout)

    def guardar_datos(self):
        nombre = self.input_nombre.text()
        precio = self.input_precio.text()
        categoria = self.combo_categoria.currentText()
        if not nombre or not precio:
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return
        
        try:
            precio = float(precio)
        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un numero")
            return

        id = obtener_id_producto(nombre, categoria)

        if id is None:
            QMessageBox.warning(self, "Producto no encontrado", f"No existe un producto con el nombre {nombre} y categoria {categoria}")
            return
        
        modificar_producto(id, nombre, precio, categoria)

        QMessageBox.information(self, "Exito", "Producto modificado correctamente")
        self.close()