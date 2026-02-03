import unittest
from ConsultasBD import *

class TesteoLogica(unittest.TestCase):
    def test_agregar_producto(self):
        agregar_producto("Flan", 3.50, "Desayuno")
        agregar_producto("Cookie", 3.50, "Desayuno")
        agregar_producto("Medialuna", 3.50, "Desayuno")
        productos = ver_productos_por_categoria("Desayuno")
        self.assertTrue(any(p[1] == "Flan" for p in productos))
        self.assertTrue(any(p[1] == "Cookie" for p in productos))
        self.assertTrue(any(p[1] == "Medialuna" for p in productos))
    
    def test_consumo(self):
        agregar_mesa(6, "activo") # idmesa, estado
        agregar_consumo(1, 6, 2) #idproducto, idmesa, cantidad
        existe = ver_cantidad_de_un_producto(6, 1) #idmesa, idproducto
        self.assertEqual(existe, 2)
    
    def test_cerrar_mesa(self):
        agregar_consumo(1, 5, 2) #idproducto, idmesa, cantidad
        total = cerrar_mesa(5, "efectivo") #idmesa, metodoPago
        self.assertGreater(total, 0)

if __name__ == "__main__":
    unittest.main()