from BaseDatos import *

crear_tablas()
print("Base de datos creada")

# AGREGAR PRODUCTOS DESAYUNO
agregar_producto("Cafe con leche", 1.90, "Desayuno")
agregar_producto("Americano", 1.70, "Desayuno")
agregar_producto("Cortado", 1.70, "Desayuno")
agregar_producto("Cafe solo", 1.50, "Desayuno")
agregar_producto("Croissant", 1.80, "Desayuno")
agregar_producto("Napolitana chocolate", 1.50, "Desayuno")
agregar_producto("Napolitana J&Q", 2.50, "Desayuno")
agregar_producto("Combo 1", 3.00, "Desayuno")
agregar_producto("Combo 2", 3.30, "Desayuno")

# AGREGAR PRODUCTOS MERIENDA
agregar_producto("Cafe con leche", 1.90, "Merienda")
agregar_producto("Americano", 1.70, "Merienda")
agregar_producto("Cortado", 1.70, "Merienda")
agregar_producto("Cafe solo", 1.50, "Merienda")
agregar_producto("Gofre", 5.00, "Merienda")
agregar_producto("Crepe", 8.00, "Merienda")
agregar_producto("Batido", 8.00, "Merienda")
agregar_producto("Combo 1", 10.00, "Merienda")
agregar_producto("Combo 2", 20.00, "Merienda")

# AGREGAR PRODUCTOS ALMUERZO
agregar_producto("Bocadillo J&Q", 3.00, "Almuerzo")
agregar_producto("Bocadillo P&Q", 3.00, "Almuerzo")
agregar_producto("Bocadillo atún", 1.90, "Almuerzo")
agregar_producto("Empanada carne", 2.90, "Almuerzo")
agregar_producto("Empanada pollo", 2.90, "Almuerzo")
agregar_producto("Empanda J&Q", 2.90, "Almuerzo")
agregar_producto("Empanda atún", 1.90, "Almuerzo")
agregar_producto("Combo 1", 5.90, "Almuerzo")
agregar_producto("Combo 2", 7.00, "Almuerzo")

# AGREGAR PRODUCTOS REFRESCOS
agregar_producto("Coca Cola", 2.50, "Refrescos")
agregar_producto("Coca Cola Zero", 2.50, "Refrescos")
agregar_producto("Sprite", 2.50, "Refrescos")
agregar_producto("Fanta naranja", 2.50, "Refrescos")
agregar_producto("Fanta limon", 2.50, "Refrescos")
agregar_producto("Aquarius naranja", 2.50, "Refrescos")
agregar_producto("Aquarios limon", 2.50, "Refrescos")
agregar_producto("Zumo natural", 3.50, "Refrescos")
agregar_producto("Zumo melocoton", 2.50, "Refrescos")

print("Productos agregados")

# VER LOS PRODUCTOS
productos = ver_productos()
for producto in productos:
    print(producto)


# agregar MESAS
agregar_mesa(1, "vacio")
agregar_mesa(2, "vacio")
agregar_mesa(3, "vacio")
agregar_mesa(4, "vacio")
agregar_mesa(5, "vacio")

print("Mesas creadas")
mesas = ver_mesas()
for mesa in mesas:
    print(mesa)


modificar_estado_mesa("activo", 1)
agregar_consumo(2, 1, 3)
agregar_consumo(4, 1, 1)

print (cerrar_mesa(1, "tarjeta"))

# PRUEBA PARA VER SI SE AGREGAN LOS PRODUCTOS A LA TABLA DE CONSUMO
# modificar_estado_mesa("activo", 5)
# agregar_consumo(2, 5, 3)
# agregar_consumo(4, 5, 1)

print("Categoria desayuno productos... ", ver_productos_por_categoria("Desayunos"))