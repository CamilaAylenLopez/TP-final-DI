import sqlite3

def conectar():
    return sqlite3.connect("caja.db") #si no existe lo crea

# CREAR TABLAS
def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

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
        estado TEXT,
        idConsumo INTEGER
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
        precio REAL,
        metodoPago TEXT,
        idMesa INTEGER REFERENCES mesa(id)
    );
    """)
    # DESPUÉS PARA LO DE VENTA DEBERÍA HACER UN JOIN EN DONDE SE CONECTE CON LA TABLA CONSUMO Y HAGA IDMESA = IDMESA Y 
    # SELECCIONE TODOS LOS PRODUCTOS QUE CONSUMIO Y Q LO MANDE A UNA FUNCION EN DONDE HAGA LA SUMA
    conexion.commit()
    conexion.close()




#FUNCIONES CREAR

# AGREGAR LOS PRODUCTOS
def agregar_producto(nombre, precio, categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO producto (nombre, precio, categoria) VALUES (?, ?, ?)",
        (nombre, precio, categoria)
    )

    conexion.commit()
    conexion.close()

def agregar_mesa(id, estado, idconsumo):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO mesa (id, estado, idconsumo) VALUES (?, ?, ?)",
        (id, estado, idconsumo)
    )

    conexion.commit()
    conexion.close()

def agregar_venta(precio, metodoPago, idMesa):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO venta (precio, metodoPago, idMesa) VALUES (?, ?, ?)",
        (precio, metodoPago, idMesa)
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


# FUNCIONES VER

# VER CONSUMO DE UNA MESA
def ver_consumo(idMesa):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM consumo WHERE idmesa = (?)", (idMesa,))
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

    cursor.execute("SELECT * FROM venta WHERE id = (?)", (id,))
    venta = cursor.fetchall()

    conexion.close()
    return venta

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

# VER MESAS
def ver_mesas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM mesa")
    mesas = cursor.fetchall()

    conexion.close()
    return mesas



# FUNCIONES ELIMINAR
def eliminar_mesa(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM mesa WHERE id = (?)", (id,))
    conexion.commit()
    conexion.close()
    return 0

def eliminar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM producto WHERE id = (?)", (id,))
    conexion.commit()
    conexion.close()
    return 0

def eliminar_consumo(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM consumo WHERE id = (?)", (id,))
    conexion.commit()
    conexion.close()
    return 0



# FUNCIONES MODIFICAR
def modificar_producto(id, nombre, precio, categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("UPDATE producto SET nombre = (?), precio = (?), categoria = (?) WHERE id = ?", 
                   (nombre, precio, categoria, id))
    conexion.commit()

    conexion.close()
    return 0

def transladar_mesa(idmesaVieja, idmesaNueva):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("UPDATE mesa SET id = (?) WHERE id = (?)", 
                   (idmesaNueva, idmesaVieja))
    conexion.commit()

    conexion.close()
    return 0

def modificar_estado_mesa(estado, id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("UPDATE mesa SET estado = (?) WHERE id = (?)", 
                   (estado, id))
    conexion.commit()

    conexion.close()
    return 0

def cerrar_mesa(idmesa, metodoPago):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
                   SELECT producto.precio, consumo.cantidad
                   FROM consumo JOIN producto ON consumo.idProducto = producto.id
                   WHERE consumo.idMesa = ?
                   """, (idmesa,))
    
    productos = cursor.fetchall()

    total = 0
    for precio, cantidad in productos:
        total += precio * cantidad
    
    cursor.execute("INSErT INTO venta (precio, metodoPago, idMesa) VALUES (?,?,?)", (total, metodoPago, idmesa))
    cursor.execute("UPDATE mesa SET estado = ? WHERE id = ?", ("vacio", idmesa))
    cursor.execute("DELETE FROM consumo WHERE idMesa = ?", (idmesa,))
    conexion.commit()
    conexion.close()
    
    return total