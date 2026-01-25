import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from BaseDatos import *
from Pantalla_Ticket import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caja registradora")
        #self.showFullScreen() # para que ocupe toda la pantalla
        self.setGeometry(100,100,600,400)

        self.idmesa = 5 # de momento va a ser siempre la mesa 5

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
        self.categoria = "Desayuno" # la categoria inicial va a ser el desyuno
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

        #grod del apartado del "ticket"
        self.layout_ticket = QGridLayout()
        self.widget_ticket.setLayout(self.layout_ticket)
        self.btnMesa = QPushButton(f"Mesa nº {self.idmesa}") # PONERLE ESTILO PARA QUE APAREZCA CENTRADO ARRIBA
        self.layout_ticket.addWidget(self.btnMesa)
        self.ticket_productos = QLabel("")
        self.layout_ticket.addWidget(self.ticket_productos)
        #self.btnMesa.clicked.connect()

    def crear_categorias(self):
        categorias = {
            'Desayuno': (0,0), 'Almuerzo': (0,1),
            'Merienda': (1,0), 'Refrescos': (1,1)
        }
        
        for texto, posicion in categorias.items():
            categoria = QPushButton(texto)
            categoria.setStyleSheet("font-size: 18px;")
            categoria.clicked.connect(lambda checked=False, t=texto: self.crear_productos(t)) # !!!! si no pongo esto así toma el último valor de texto por ende solo aparecen los refrescos
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
            producto.clicked.connect(lambda checked=False, idP = id_producto, n=nombre: self.agregar_al_ticket(n, idP))
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

    def agregar_al_ticket(self, nombre, idProducto):
        # SI SE CIERRA Y SE VUELVE A ABRIR TIENE QUE APARECER LO QUE HABÑIA ANTEEEEEEEEEEEEEEEEEEEEEE !!!!!!!!!!!!!!!
        agregar_consumo(idProducto, self.idmesa, 1)
        productos = self.ticket_productos.text() # estos son los productos que ya se habían cargado antes
        precio = ver_precio_producto(idProducto)
        self.ticket_productos.setText(productos + f"\n{nombre}   ---   precio: {precio}")

    def crear_acciones(self):
        acciones = {
            'Ticket': self.accion_ticket,
            'Cobrar': self.accion_cobrar,
            'Borrar': self.accion_borrar,
            'Visa': self.accion_visa,
            'Salir': self.accion_salir_app,
            'Editar producto': self.accion_editar_producto
        }
        posiciones = {
            'Ticket': (0,0), 'Cobrar': (0,2),
            'Borrar': (1,0), 'Visa': (1,2),
            'Salir': (2,0), 'Editar producto': (2,2),
        }
        
        for texto, funcion in acciones.items():
            boton =QPushButton(texto)
            boton.setStyleSheet("font-size: 13px;")
            boton.clicked.connect(funcion)
            self.layout_acciones.addWidget(boton, *posiciones[texto])

    
    def accion_salir_app(self):
        mensaje = QMessageBox.warning(self, "Atención", "¿Seguro que quiere salir?", QMessageBox.Ok | QMessageBox.Cancel)
        if mensaje == QMessageBox.Ok: # si presiona el boton de ok sale
            sys.exit("Cerrando aplicacion...")

    def accion_ticket(self):
        self.ventana_ticket = TicketWindow(self.idmesa)
        self.ventana_ticket.show()
    
    def accion_cobrar(self):
        mensaje = QMessageBox.information(self, "Atención", "Proximamente")
    
    def accion_borrar(self):
        eliminar_consumo(self.idmesa)
        print("VERIFICRA QUE SE ELIMINO: ")
        consumo = ver_consumo_por_mesa(self.idmesa)
        for c in consumo:
            print(c)
    
    def accion_visa(self):
        mensaje = QMessageBox.information(self, "Atención", "Proximamente")

    def accion_editar_producto(self):
        mensaje = QMessageBox.information(self, "Atención", "Proximamente")
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()