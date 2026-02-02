import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ConsultasBD import *
from Pantalla_Ticket import *
from Pantalla_EditarProducto import FormularioEmergente
from Pantalla_EliminarProducto import EliminarProductoDialog
from Pantalla_Ventas import VentasWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caja registradora")
        self.setGeometry(300,100,1000,600)

        self.idmesa = 0 # de momento va a ser siempre la mesa 0

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        grid = QGridLayout()
        central_widget.setLayout(grid)

        # menú
        self.crear_menu()

        # separo todo en las 4 categorias principales
        self.widget_categorias = QWidget()
        self.widget_productos = QWidget()
        self.widget_ticket = QWidget()
        self.widget_acciones = QWidget()

        # color de fondo de cada aparado
        self.widget_categorias.setStyleSheet("background-color: #4C5C3A;")
        self.widget_productos.setStyleSheet("background-color: #2F5E11;")
        self.widget_ticket.setStyleSheet("background-color: #535E47;")
        self.widget_acciones.setStyleSheet("background-color: #4C5C3A;")

        # grid.addWidget(widget, fila, columna, filasQueOcupa, columnasQueOcupa)
        grid.addWidget(self.widget_categorias, 0, 0, 1, 2)
        grid.addWidget(self.widget_productos, 1, 0, 2, 2)
        grid.addWidget(self.widget_ticket, 0, 2, 2, 1)
        grid.addWidget(self.widget_acciones, 2, 2, 1, 1)

        # grid del apartado de las categorias
        self.categoria = "Desayuno" # la categoria inicial va a ser el desyuno
        self.layout_categorias = QGridLayout()
        self.widget_categorias.setLayout(self.layout_categorias)
        self.mostrar_categorias()

        # grid del apartado de lod productos
        self.layout_productos = QGridLayout()
        self.widget_productos.setLayout(self.layout_productos)
        self.mostrar_productos(self.categoria)

        # grid del apartado de las acciones
        self.layout_acciones = QGridLayout()
        self.widget_acciones.setLayout(self.layout_acciones)
        self.crear_acciones()

        #grid del apartado del "ticket"
        self.layout_ticket = QVBoxLayout()
        self.widget_ticket.setLayout(self.layout_ticket)

        self.btnMesa = QPushButton(f"Mesa nº {self.idmesa}")
        self.btnMesa.setStyleSheet("font-size: 14px;")
        self.layout_ticket.addWidget(self.btnMesa)

        #scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout_ticket.addWidget(self.scroll_area)

        self.ticket_productos = QLabel("")
        self.scroll_area.setWidget(self.ticket_productos)
        self.total = QLabel("Total: 0")
        self.layout_ticket.addStretch()
        self.layout_ticket.addWidget(self.total)
        
        self.cargar_productos()

    def crear_menu(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        opciones_menu = QMenu("Opciones")
        menu_bar.addMenu(opciones_menu)

        editar_accion = QAction("Editar precios", self)
        editar_accion.triggered.connect(self.accion_editar_producto)
        opciones_menu.addAction(editar_accion)

        salir_accion = QAction("Salir", self)
        salir_accion.triggered.connect(self.accion_salir_app)
        opciones_menu.addAction(salir_accion)

    def mostrar_categorias(self):
        categorias = {
            'Desayuno': (0,0), 'Almuerzo': (0,1),
            'Merienda': (1,0), 'Refrescos': (1,1)
        }
        
        for texto, posicion in categorias.items():
            categoria = QPushButton(texto)
            categoria.setCursor(Qt.PointingHandCursor)
            estilo = "font-size: 20px; border: 2px solid #465435; border-radius: 10px; padding: 20px;"

            if self.categoria == texto:
                categoria.setStyleSheet(estilo + "font-weight: bold; background-color: #3B472D")
            else:
                categoria.setStyleSheet(estilo + "color: white;")

            categoria.clicked.connect(lambda checked=False, t=texto: self.mostrar_productos(t))
            self.layout_categorias.addWidget(categoria, *posicion)

    def limpiar_productos(self):
        while self.layout_productos.count(): # el .count() devuelve cuantos elementos hay en el layuot
            item = self.layout_productos.takeAt(0) # el .takeAt(0) saca el primer elemento del layout
            widget = item.widget() # agarra el widget y abajo lo elimina
            if widget:
                widget.deleteLater()

    def limpiar_categorias(self):
        while self.layout_categorias.count():
            item = self.layout_categorias.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def mostrar_productos(self, categoria):
        self.categoria = categoria
        self.limpiar_categorias()
        self.mostrar_categorias()
        productos = ver_productos_por_categoria(categoria)
        #print(productos)

        self.limpiar_productos() # se borran los botones anteriores al cambiar de categoria para que no se sobreescriba

        fila = 0
        col= 0
        for id_producto, nombre, precio in productos:
            producto = QPushButton(nombre)
            producto.setCursor(Qt.PointingHandCursor)
            producto.setStyleSheet("font-size: 16px; padding: 30px; font-weight: bold;")
            producto.clicked.connect(lambda checked=False, idP = id_producto: self.agregar_al_ticket(idP))
            self.layout_productos.addWidget(producto, fila, col)
            
            col += 1
            if col == 3:
                col = 0
                fila += 1

    def cargar_productos(self):
        productos = ver_consumo_por_mesa(self.idmesa) # la función se encarga de traer los productos anteriores de la mesa
        
        self.ticket_productos.clear()
        for n, c, p, categoria in productos:
            self.ticket_productos.setText(self.ticket_productos.text() + f"\n{c}   --   {n}   ---   {p}")
            self.ticket_productos.setStyleSheet("font-size: 16px;")

        total = round(calcular_total_provisorio(self.idmesa), 2)

        precio = str(total)
        self.total.setText("Total: " + precio)
        self.total.setStyleSheet("font-size: 18px; padding: 5px, 10px; color: #D4725D; font-weight: bold;")
        
    def agregar_al_ticket(self, idProducto):
        # si ya se habia seleccionado ese producto se suma y sino se agrega
        existe = ver_cantidad_de_un_producto(self.idmesa, idProducto)
        if existe:
            sumar_producto_al_consumo(self.idmesa, idProducto)
        else:
            agregar_consumo(idProducto, self.idmesa, 1)

        self.cargar_productos()

    def crear_acciones(self):
        acciones = {
            'Ticket': self.accion_ticket,
            'Cobrar': self.accion_cobrar,
            'Borrar': self.accion_borrar,
            'Visa': self.accion_visa,
            'Historial ventas': self.accion_historial_ventas,
            'Eliminar producto': self.accion_eliminar_producto,
            'Salir': self.accion_salir_app,
            'Editar precios': self.accion_editar_producto
        }
        posiciones = {
            'Ticket': (0,0), 'Cobrar': (0,2),
            'Borrar': (1,0), 'Visa': (1,2),
            'Historial ventas': (2,0), 'Eliminar producto': (2,2),
            'Salir': (3,0), 'Editar precios': (3,2),
        }
        
        for texto, funcion in acciones.items():
            boton =QPushButton(texto)
            boton.setCursor(Qt.PointingHandCursor)
            boton.setStyleSheet("font-size: 14px; padding: 10px;")
            boton.clicked.connect(funcion)
            self.layout_acciones.addWidget(boton, *posiciones[texto])
    
    def accion_salir_app(self):
        mensaje = QMessageBox.warning(self, "Atención", "¿Seguro que quiere salir?", QMessageBox.Ok | QMessageBox.Cancel)
        if mensaje == QMessageBox.Ok: # si presiona el boton de ok sale del programa
            sys.exit("Cerrando aplicacion...")

    def accion_ticket(self):
        self.ventana_ticket = TicketWindow(self.idmesa)
        QMessageBox.information(self, "Ticket", "Se imprimio el ticket")
        self.ventana_ticket.show()
    
    def accion_borrar(self):
        eliminar_consumo(self.idmesa)
        #print("VERIFICRA QUE SE ELIMINO (SI APARECEN CORCHETES VACIOS ES XQ SI SE LIMINO): ")
        #consumo = ver_consumo_por_mesa(self.idmesa)
        #for c in consumo:
            #print(c)
        
        self.total.setText("Total: 0")
        self.ticket_productos.setText("")
    
    def accion_cobrar(self):
        if self.ticket_productos.text() == "":
            QMessageBox.information(self, "Información", "No hay nada para cobrar")
            return
        self.accion_ticket()
        total = str(cerrar_mesa(self.idmesa, "efectivo"))
        self.total.setText("Total: 0")
        self.ticket_productos.setText("")
        QMessageBox.information(self, "Atención", f"Pago de {total} aceptado")

    def accion_visa(self):
        if self.ticket_productos.text() == "":
            QMessageBox.information(self, "Información", "No hay nada para cobrar")
            return
        self.accion_ticket()
        total = str(round(cerrar_mesa(self.idmesa, "tarjeta"), 2))
        self.total.setText("Total: 0")
        self.ticket_productos.setText("")
        QMessageBox.information(self, "Atención", f"Pago de {total} aceptado")

    def accion_editar_producto(self):
        dialogo = FormularioEmergente()
        dialogo.exec()
        self.cargar_productos() #para que se cargue el ticket con los nuevos precios
    
    def accion_eliminar_producto(self):
        dialogo = EliminarProductoDialog(self.idmesa)
        dialogo.exec()
        self.cargar_productos()
    
    def accion_historial_ventas(self):
        ventana_ventas = VentasWindow()
        ventana_ventas.exec()
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()