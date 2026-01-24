from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from BaseDatos import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caja registradora")
        #self.showFullScreen() # para que ocupe toda la pantalla
        self.setGeometry(100,100,600,400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        grid = QGridLayout()
        central_widget.setLayout(grid)

        # separo todo en las 4 categorias principales
        self.widget_categorias = QWidget()
        self.widget_productos = QWidget()
        self.widget_ticket = QWidget()
        self.widget_acciones = QWidget()

        # estilos de momento
        self.widget_categorias.setStyleSheet("background-color: red;")
        self.widget_productos.setStyleSheet("background-color: green;")
        self.widget_ticket.setStyleSheet("background-color: blue;")
        self.widget_acciones.setStyleSheet("background-color: pink;")

        # grid.addWidget(widget, fila, columna, filasQueOcupa, columnasQueOcupa)
        grid.addWidget(self.widget_categorias, 0, 0, 1, 2)
        grid.addWidget(self.widget_productos, 1, 0, 2, 2)
        grid.addWidget(self.widget_ticket, 0, 2, 2, 1)
        grid.addWidget(self.widget_acciones, 2, 2, 1, 1)

        # grid del apartado de las categorias
        self.categoria = "Desayunos" # la categoria inicial va a ser el desyuno
        self.layout_categorias = QGridLayout()
        self.widget_categorias.setLayout(self.layout_categorias)
        self.crear_categorias()

        # grid del apartado de lod productos
        self.layout_productos = QGridLayout()
        self.widget_productos.setLayout(self.layout_productos)
        self.crear_productos(self.categoria)

        # grid del apartado de las acciones
        self.layout_acciones = QGridLayout()
        self.widget_acciones.setLayout(self.layout_acciones)
        self.crear_acciones()

    def crear_categorias(self):
        categorias = {
            'Desayuno': (0,0), 'Almuerzo': (0,1),
            'Boyeria': (1,0), 'Refrescos': (1,1)
        }
        
        for texto, posicion in categorias.items():
            categoria = QPushButton(texto)
            categoria.setStyleSheet("font-size: 18px;")
            #categoria.clicked.connet()
            self.layout_categorias.addWidget(categoria, *posicion)
    
    def crear_productos(self, categoria):
        productos = ver_productos_por_categoria(categoria)
        print(productos)

        self.limpiar_productos() # se borran los botones anteriores al cambiar de categoria

        fila = 0
        col= 0
        for id_producto, nombre, precio in productos:
            producto = QPushButton(nombre)
            producto.setStyleSheet("font-size: 14px;")
            #producto.clicked.conect() --> agregar al ticket 
            self.layout_productos.addWidget(producto, fila, col)
            
            col += 1
            if col == 3:
                col = 0
                fila += 1

    # si cambia de categoria se borran los botones de los productos anteriores
    def limpiar_productos(self):
        while self.layout_productos.count(): # el .count() devuelve cuantos elementos hay en el layuot
            item = self.layout_productos.takeAt(0) # el .takeAt(0) saca el primer elemento del layout
            widget = item.widget() # agarra el widget y abajo lo elimina
            if widget:
                widget.deleteLater()

    def crear_acciones(self):
        acciones = {
            'Guardar': (0,0), 'Abrir': (0,1), 'Cobrar': (0,2),
            'Borrar': (1,0), 'Ticket': (1,1), 'Visa': (1,2),
            'Salir': (2,0), 'Traspasar': (2,1), 'Editar Producto': (2,2),
        }
        
        for texto, posicion in acciones.items():
            accion = QPushButton(texto)
            accion.setStyleSheet("font-size: 13px;")
            #accion.clicked.connet()
            self.layout_acciones.addWidget(accion, *posicion)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()