# Caja registradora

---

## 1. Descripción del proyecto
Es una aplicación de escritorio intuitiva ideada como una caja registradora digital pensada para bares o cafeterías.

Funciones principales:
- Ver productos por categoría
- Seleccionar productos
- Ver ticket
- Hacer cobros
- ver el historial de ventas
- Editar los precios de los productos
- Persistencia en base de datos (SQLite)

## 2. Logica del proyecto
Base de datos:
La base de datos cuenta con cuatro tablas:
- Mesa: guarda su número de cada mesa para identificarlas y su estado: 'activo' si es que hay personas consumiendo y 'vacio' en caso contrario.
- Producto: tiene un identificador, el nombre del producto, precio y a que categoría pertenece cada producto (por ejemplo, una cocacola pertenece a la categoría de 'Refrescos').
- Consumo: registra los productos que se estan consumiendo en cada mesa, la cantidad y un identificador único. Por ejemplo: en la mesa dos se está consumiendo 2 cocacolas, 1 cafe con leche y 3 croissants.
- Venta: se utiliza una vez que se realice el pago de lo consumido por la mesa, guardando el total pagado, el método de pago, la mesa y la fecha.

¿Qué puede hacer el usuario?
- Navegar por categorías y productos: en la pantalla principal contara con un apartado con las categorias de los productos (desayuno, merienda, almuerzo, refrescos) y debajo sus correspondientes productos. Al cambiar de categoria, los productos mostrados se actualizan automáticamente.
- Agregar productos al ticket: al seleccioanr un producto se agrega al ticket y a la base de datos. A su vez se pueden seleccionar cuantos productos se requieran y apareceran en pantalla, además se hara automaticamente la suma del precio. En caso de seleccionar varias veces un mismo producto, en vez de crear registros duplicados en la base de datos y que visualmente aparezca el mismo producto muchas veces en el ticket, se le sumara en el apartado de cantidad.
- Editar productos y gestionar la pantalla: el usuario puede editar el precio de los productos, salir de la pantalla, ver el historial de ventas, ver el ticket y realizar el cobro (ya sea en efectivo o en tarjeta).

Funcionamiento del cobro:
- Al cobrar, se guarda la información en la tabla de venta, se vacía la mesa correspondiente y se eliminan los registros de esa mesa de la tabla de consumos.

## 3. Tecnologías
La aplicación fue desarrollada con:
- Python 3
- Pyside6
- SQLite3

## 4. Estructura del proyecto


## 5. Mejoras para el futuro
- Poder elegir mesas desde la interfaz,
- Transferir el consumo de una mesa a otra.
- Dividir el consumo para pagar separados.
- Eliminar ítems especifico del ticket.
- Sistema de login con roles (admin/empleado).
