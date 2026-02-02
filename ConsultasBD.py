import sqlite3
import datetime

def conectar():
    return sqlite3.connect("baseDatos.db") #si no existe lo crea

# CREAR TABLAS
def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        categoria TEXT
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mesa (
        id INTEGER PRIMARY KEY,
        estado TEXT
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consumo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idProducto INTEGER REFERENCES producto(id),
        idMesa INTEGER REFERENCES mesa(id),
        cantidad INT
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        metodoPago TEXT,
        idMesa INTEGER REFERENCES mesa(id),
        fecha DATETIME
    );
    """)

    conexion.commit()
    conexion.close()


#FUNCIONES AGREGAR
def agregar_producto(nombre, precio, categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO producto (nombre, precio, categoria) VALUES (?, ?, ?)",
        (nombre, precio, categoria)
    )

    conexion.commit()
    conexion.close()

def agregar_mesa(id, estado):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO mesa (id, estado) VALUES (?, ?)",
        (id, estado)
    )

    conexion.commit()
    conexion.close()

def agregar_venta(total, metodoPago, idMesa):
    conexion = conectar()
    cursor = conexion.cursor()

    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
        "INSERT INTO venta (total, metodoPago, idMesa, fecha) VALUES (?, ?, ?, ?)",
        (total, metodoPago, idMesa, fecha_actual)
    )

    conexion.commit()
    conexion.close()

def agregar_consumo(idProducto, idMesa, cantidad):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO consumo (idProducto, idMesa, cantidad) VALUES (?, ?, ?)",
        (idProducto, idMesa, cantidad)
    )

    conexion.commit()
    conexion.close()


#FUNCIONES VER
# Esta función busca la cantidad de veces que se selecciono un profucto en una mesa. Por ejemplo, si pidio una, dos o más cocacolas.
# Que se complementa con la función de abajo (sumar_producto_al_consumo), ya que si ya se había seleccionado ese producto se suma a la cantidad que habái antes.
# Por ejemplo si ya había elegido una vez la cocacola, en vez de que se cree otra entrada en el campo de cantidad dentro de la tabla consumo se le suma uno, por ende en pantalla va a parecer como dos cocacolas
def ver_cantidad_de_un_producto(idmesa, idproducto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT cantidad FROM consumo WHERE idMesa =? AND idProducto = ?",
        (idmesa, idproducto,)
    )

    cantidad = cursor.fetchone()
    conexion.close()

    if cantidad:
        return cantidad[0]
    return None

def sumar_producto_al_consumo(idmesa, idproducto):
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("UPDATE consumo SET cantidad = cantidad + 1 WHERE idMesa = ? AND idProducto = ?", (idmesa, idproducto))

    conexion.commit()
    conexion.close()

# VER CONSUMO DE UNA MESA
def ver_consumo_por_mesa(idMesa):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""SELECT producto.nombre, consumo.cantidad, producto.precio, producto.categoria  
                   FROM consumo JOIN producto ON consumo.idProducto = producto.id
                   WHERE consumo.idMesa = ?""", (idMesa,))
    
    consumo = cursor.fetchall()
    conexion.close()
    return consumo

# VER TODOS LOS CONSUMOS
def ver_consumos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM consumo")
    consumos = cursor.fetchall()

    conexion.close()
    return consumos

# VER VENTA ESPECIFICA
def ver_venta(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM venta WHERE id = ?", (id,))
    venta = cursor.fetchall()

    conexion.close()
    return venta

# VER PRECIO DE UN PRODUCTO A TRAVÉS DEL ID
def ver_precio_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT precio FROM producto WHERE id = ?", (id,))
    precio = cursor.fetchone()

    conexion.close()
    if precio:
        return precio[0]
    return None

# VER VENTAS
def ver_ventas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM venta")
    ventas = cursor.fetchall()

    conexion.close()
    return ventas

# VER PRODUCTOS
def ver_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()

    conexion.close()
    return productos

# VER PRODUCTOS POR CATEGORIA
def ver_productos_por_categoria(categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, precio FROM producto WHERE categoria = ?", (categoria,))
    productos = cursor.fetchall()

    conexion.close()
    return productos

# VER MESAS
def ver_mesas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM mesa")
    mesas = cursor.fetchall()

    conexion.close()
    return mesas

# OBTENER EL ID DE UN PRODUCTO PRODUCTO
def obtener_id_producto(nombre, categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM producto WHERE nombre = ? AND categoria = ?", (nombre, categoria))

    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        return resultado[0]
    else:
        return None

# FUNCIONES ELIMINAR
def eliminar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM producto WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    return 0

def eliminar_consumo(idmesa):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM consumo WHERE idMesa = ?", (idmesa,))
    conexion.commit()
    conexion.close()
    return 0

# borra el consumo de una mesa, ejemplo se coloco una cocacola en la mesa 2, pero ocurre algo y ya no la quieren y se tiene que eliminar.
# la idea es que si hay una cocacola, por ejemplo, se borra completamente pero si hay dos cocacolas solo se borre (o sea que la cantidad disminuye -1)
def eliminar_producto_de_mesa(idmesa, idproducto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT cantidad FROM consumo WHERE idMesa = ? AND idProducto = ?", (idmesa, idproducto,))
    fila = cursor.fetchone()
    
    if not fila:
        conexion.close()
        return
    
    cantidad = fila[0]

    if cantidad > 1:
        cursor.execute("UPDATE consumo SET cantidad = cantidad - 1 WHERE idMesa = ? AND idProducto = ?", (idmesa, idproducto,))
    else:
        cursor.execute("DELETE FROM consumo WHERE idMesa = ? AND idProducto = ?", (idmesa,idproducto,))
        
    conexion.commit()
    conexion.close()
    return 0

# FUNCIONES MODIFICAR
def modificar_producto(id, nombre, precio, categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("UPDATE producto SET nombre = ?, precio = ?, categoria = ? WHERE id = ?", 
                   (nombre, precio, categoria, id))
    conexion.commit()

    conexion.close()
    return 0

def modificar_estado_mesa(estado, id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("UPDATE mesa SET estado = ? WHERE id = ?", 
                   (estado, id))
    conexion.commit()

    conexion.close()
    return 0

# para que pueda aparecer en el main y en el ticket antes de pagar y q se cierre la mesa
def calcular_total_provisorio(idmesa):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
                   SELECT consumo.cantidad, producto.precio
                   FROM consumo JOIN producto ON consumo.idProducto = producto.id
                   WHERE consumo.idMesa = ?
                   """, (idmesa,))
    
    productos = cursor.fetchall()

    total = 0
    for cantidad, precio in productos:
        total += precio * cantidad
    
    total = round(total, 2)

    conexion.close()
    
    return total

def cerrar_mesa(idmesa, metodoPago):
    total = calcular_total_provisorio(idmesa)
    
    conexion = conectar()
    cursor = conexion.cursor()

    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO venta (total, metodoPago, idmesa, fecha) VALUES (?,?,?,?)", (total, metodoPago, idmesa, fecha_actual))
    idVenta = cursor.lastrowid
    cursor.execute("UPDATE mesa SET estado = ? WHERE id = ?", ("vacio", idmesa))
    cursor.execute("DELETE FROM consumo WHERE idMesa = ?", (idmesa,))
    conexion.commit()
    conexion.close()

    guardar_historial_venta(idVenta, idmesa, total, metodoPago, fecha_actual)
    
    return total

# función para que el historial de ventas se guarde en un archivo de texto
def guardar_historial_venta(idventa, idmesa, total, metodoPago, fecha_actual):
    with open("historial_ventas.txt", "a", encoding="utf-8") as f:
        f.write(f"ID: {idventa} | Mesa: {idmesa} | Total: {total} | Metodo de pago: {metodoPago} | Hora: {fecha_actual}\n")