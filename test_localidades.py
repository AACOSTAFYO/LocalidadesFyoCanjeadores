"""
Tests para el módulo de localidades.
"""
import unittest
from localidades import Localidad, encontrar_localidad, encontrar_localidad_detallado, similitud_texto


class TestSimilitudTexto(unittest.TestCase):
    """Tests para la función de similitud de texto."""
    
    def test_textos_identicos(self):
        """Textos idénticos deben tener similitud 1.0"""
        self.assertEqual(similitud_texto("Buenos Aires", "Buenos Aires"), 1.0)
    
    def test_textos_diferentes_case(self):
        """Textos con diferente case deben ser similares"""
        similitud = similitud_texto("Buenos Aires", "buenos aires")
        self.assertGreater(similitud, 0.9)
    
    def test_textos_totalmente_diferentes(self):
        """Textos diferentes deben tener baja similitud"""
        similitud = similitud_texto("Buenos Aires", "Córdoba")
        self.assertLess(similitud, 0.5)


class TestEncontrarLocalidad(unittest.TestCase):
    """Tests para la función de búsqueda de localidades."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.lista_principal = [
            Localidad("Vicente López", "Vicente López", "Buenos Aires"),
            Localidad("San Isidro", "San Isidro", "Buenos Aires"),
            Localidad("La Plata", "La Plata", "Buenos Aires"),
            Localidad("Córdoba Capital", "Capital", "Córdoba"),
        ]
        
        self.lista_referencia = [
            *self.lista_principal,
            Localidad("Martínez", "San Isidro", "Buenos Aires"),
            Localidad("Florida", "Vicente López", "Buenos Aires"),
            Localidad("Villa Allende", "Colón", "Córdoba"),
        ]
    
    def test_coincidencia_exacta(self):
        """Debe encontrar coincidencia exacta en lista principal."""
        resultado = encontrar_localidad("La Plata", self.lista_principal, self.lista_referencia)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Plata")
        self.assertEqual(resultado.partido, "La Plata")
    
    def test_coincidencia_exacta_case_insensitive(self):
        """Debe encontrar coincidencia exacta sin importar mayúsculas."""
        resultado = encontrar_localidad("la plata", self.lista_principal, self.lista_referencia)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Plata")
    
    def test_busqueda_por_partido(self):
        """Debe encontrar localidad del mismo partido cuando no está en lista principal."""
        # Martínez no está en lista principal, pero está en referencia con partido San Isidro
        resultado = encontrar_localidad("Martínez", self.lista_principal, self.lista_referencia)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.partido, "San Isidro")
        self.assertEqual(resultado.nombre, "San Isidro")
    
    def test_busqueda_por_provincia_fallback(self):
        """Debe buscar por provincia cuando no hay partido disponible."""
        # Villa Allende es partido Colón (no en lista principal), pero es provincia Córdoba
        resultado = encontrar_localidad("Villa Allende", self.lista_principal, self.lista_referencia)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.provincia, "Córdoba")
    
    def test_localidad_no_encontrada(self):
        """Debe retornar None cuando no se encuentra ninguna coincidencia."""
        # Usar un nombre totalmente diferente sin similitud
        resultado = encontrar_localidad("XYZ123ABC", self.lista_principal, self.lista_referencia)
        self.assertIsNone(resultado)
    
    def test_sin_lista_referencia(self):
        """Debe funcionar usando solo lista principal como referencia."""
        resultado = encontrar_localidad("La Plata", self.lista_principal)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "La Plata")
    
    def test_busqueda_similar_mismo_partido(self):
        """Debe encontrar localidad similar del mismo partido."""
        # Florida pertenece a Vicente López
        resultado = encontrar_localidad("Florida", self.lista_principal, self.lista_referencia)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.partido, "Vicente López")


class TestEncontrarLocalidadDetallado(unittest.TestCase):
    """Tests para la función detallada de búsqueda."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.lista_principal = [
            Localidad("Vicente López", "Vicente López", "Buenos Aires"),
            Localidad("San Isidro", "San Isidro", "Buenos Aires"),
        ]
        
        self.lista_referencia = [
            *self.lista_principal,
            Localidad("Martínez", "San Isidro", "Buenos Aires"),
        ]
    
    def test_metodo_exacta(self):
        """Debe indicar método 'exacta' para coincidencias exactas."""
        resultado = encontrar_localidad_detallado(
            "San Isidro", self.lista_principal, self.lista_referencia
        )
        self.assertEqual(resultado['metodo'], 'exacta')
        self.assertEqual(resultado['similitud'], 1.0)
        self.assertEqual(resultado['encontrada'].nombre, "San Isidro")
    
    def test_metodo_partido(self):
        """Debe indicar método 'partido' cuando busca por partido."""
        resultado = encontrar_localidad_detallado(
            "Martínez", self.lista_principal, self.lista_referencia
        )
        self.assertEqual(resultado['metodo'], 'partido')
        self.assertIsNotNone(resultado['referencia'])
        self.assertEqual(resultado['referencia'].nombre, "Martínez")
        self.assertEqual(resultado['encontrada'].partido, "San Isidro")
    
    def test_metodo_no_encontrada(self):
        """Debe indicar 'no_encontrada' cuando no hay coincidencia."""
        resultado = encontrar_localidad_detallado(
            "XYZ123", self.lista_principal, self.lista_referencia
        )
        self.assertEqual(resultado['metodo'], 'no_encontrada')
        self.assertIsNone(resultado['encontrada'])


class TestLocalidad(unittest.TestCase):
    """Tests para la clase Localidad."""
    
    def test_creacion_localidad(self):
        """Debe crear localidad correctamente."""
        loc = Localidad("Buenos Aires", "Partido BA", "Provincia BA")
        self.assertEqual(loc.nombre, "Buenos Aires")
        self.assertEqual(loc.partido, "Partido BA")
        self.assertEqual(loc.provincia, "Provincia BA")
    
    def test_repr_localidad(self):
        """Debe tener representación legible."""
        loc = Localidad("Test", "Partido", "Provincia")
        repr_str = repr(loc)
        self.assertIn("Test", repr_str)
        self.assertIn("Partido", repr_str)
        self.assertIn("Provincia", repr_str)


if __name__ == "__main__":
    unittest.main()
