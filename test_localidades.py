"""
Tests para el módulo de localidades.
"""

import unittest
from localidades import Localidad, LocalidadMatcher, crear_localidad


class TestLocalidad(unittest.TestCase):
    """Tests para la clase Localidad."""
    
    def test_crear_localidad(self):
        """Test que verifica la creación de una localidad."""
        loc = crear_localidad("San Isidro", "San Isidro", "Buenos Aires")
        self.assertEqual(loc.nombre, "San Isidro")
        self.assertEqual(loc.partido, "San Isidro")
        self.assertEqual(loc.provincia, "Buenos Aires")


class TestLocalidadMatcher(unittest.TestCase):
    """Tests para la clase LocalidadMatcher."""
    
    def setUp(self):
        """Configura las listas de localidades para los tests."""
        # Lista principal - localidades disponibles en el sistema
        self.lista_principal = [
            crear_localidad("Acassuso", "San Isidro", "Buenos Aires"),
            crear_localidad("Beccar", "San Isidro", "Buenos Aires"),
            crear_localidad("Vicente López", "Vicente López", "Buenos Aires"),
            crear_localidad("Florida", "Vicente López", "Buenos Aires"),
            crear_localidad("Olivos", "Vicente López", "Buenos Aires"),
            crear_localidad("La Plata", "La Plata", "Buenos Aires"),
            crear_localidad("City Bell", "La Plata", "Buenos Aires"),
        ]
        
        # Lista de fallback - localidades que pueden no estar en la principal
        # pero que tienen partidos que sí están
        self.lista_fallback = [
            crear_localidad("San Isidro", "San Isidro", "Buenos Aires"),
            crear_localidad("Martínez", "San Isidro", "Buenos Aires"),
            crear_localidad("La Lucila", "Vicente López", "Buenos Aires"),
            crear_localidad("Villa Elisa", "La Plata", "Buenos Aires"),
            crear_localidad("Gonnet", "La Plata", "Buenos Aires"),
        ]
        
        self.matcher = LocalidadMatcher(self.lista_principal, self.lista_fallback)
    
    def test_buscar_localidad_en_principal(self):
        """Test que busca una localidad que existe en la lista principal."""
        resultado = self.matcher.buscar_localidad("Acassuso")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Acassuso")
        self.assertEqual(resultado.partido, "San Isidro")
    
    def test_buscar_localidad_case_insensitive(self):
        """Test que la búsqueda no distingue mayúsculas/minúsculas."""
        resultado = self.matcher.buscar_localidad("acassuso")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Acassuso")
        
        resultado2 = self.matcher.buscar_localidad("ACASSUSO")
        self.assertIsNotNone(resultado2)
        self.assertEqual(resultado2.nombre, "Acassuso")
    
    def test_buscar_localidad_con_espacios(self):
        """Test que la búsqueda elimina espacios extras."""
        resultado = self.matcher.buscar_localidad("  Acassuso  ")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Acassuso")
    
    def test_buscar_localidad_no_existe_en_ninguna_lista(self):
        """Test que retorna None cuando la localidad no existe en ninguna lista."""
        resultado = self.matcher.buscar_localidad("Localidad Inexistente")
        self.assertIsNone(resultado)
    
    def test_buscar_localidad_en_fallback_retorna_del_mismo_partido(self):
        """
        Test principal: busca localidad en fallback y retorna una del mismo partido
        de la lista principal.
        """
        # "San Isidro" está en fallback pero no en principal
        resultado = self.matcher.buscar_localidad("San Isidro")
        self.assertIsNotNone(resultado)
        # Debe retornar una localidad del partido "San Isidro" que esté en la lista principal
        self.assertEqual(resultado.partido, "San Isidro")
        # Debe ser una de las localidades principales (Acassuso o Beccar)
        self.assertIn(resultado.nombre, ["Acassuso", "Beccar"])
    
    def test_buscar_martinez_retorna_del_partido_san_isidro(self):
        """
        Test: busca Martínez (en fallback) y debe retornar una localidad del partido
        San Isidro de la lista principal.
        """
        resultado = self.matcher.buscar_localidad("Martínez")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.partido, "San Isidro")
        self.assertIn(resultado.nombre, ["Acassuso", "Beccar"])
    
    def test_buscar_la_lucila_retorna_del_partido_vicente_lopez(self):
        """
        Test: busca La Lucila (en fallback) y debe retornar una localidad del partido
        Vicente López de la lista principal.
        """
        resultado = self.matcher.buscar_localidad("La Lucila")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.partido, "Vicente López")
        self.assertIn(resultado.nombre, ["Vicente López", "Florida", "Olivos"])
    
    def test_buscar_gonnet_retorna_del_partido_la_plata(self):
        """
        Test: busca Gonnet (en fallback) y debe retornar una localidad del partido
        La Plata de la lista principal.
        """
        resultado = self.matcher.buscar_localidad("Gonnet")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.partido, "La Plata")
        self.assertIn(resultado.nombre, ["La Plata", "City Bell"])
    
    def test_buscar_todas_del_partido(self):
        """Test que busca todas las localidades de un partido."""
        localidades_san_isidro = self.matcher.buscar_todas_del_partido("San Isidro")
        self.assertEqual(len(localidades_san_isidro), 2)
        nombres = [loc.nombre for loc in localidades_san_isidro]
        self.assertIn("Acassuso", nombres)
        self.assertIn("Beccar", nombres)
    
    def test_buscar_todas_del_partido_case_insensitive(self):
        """Test que buscar por partido no distingue mayúsculas/minúsculas."""
        localidades = self.matcher.buscar_todas_del_partido("vicente lópez")
        self.assertEqual(len(localidades), 3)
    
    def test_buscar_todas_del_partido_inexistente(self):
        """Test que retorna lista vacía para partido inexistente."""
        localidades = self.matcher.buscar_todas_del_partido("Partido Inexistente")
        self.assertEqual(len(localidades), 0)
    
    def test_matcher_sin_lista_fallback(self):
        """Test que el matcher funciona sin lista de fallback."""
        matcher = LocalidadMatcher(self.lista_principal)
        resultado = matcher.buscar_localidad("Acassuso")
        self.assertIsNotNone(resultado)
        
        # Sin fallback, no encuentra localidades que no estén en principal
        resultado2 = matcher.buscar_localidad("San Isidro")
        self.assertIsNone(resultado2)


if __name__ == '__main__':
    unittest.main()
