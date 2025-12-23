"""
Ejemplo de uso del módulo de localidades.

Este ejemplo demuestra cómo usar la funcionalidad de búsqueda de localidades
con fallback a partido y provincia.
"""
from localidades import Localidad, encontrar_localidad, encontrar_localidad_detallado


# Lista principal de localidades disponibles (Lista A)
localidades_disponibles = [
    Localidad("Vicente López", "Vicente López", "Buenos Aires"),
    Localidad("San Isidro", "San Isidro", "Buenos Aires"),
    Localidad("La Plata", "La Plata", "Buenos Aires"),
    Localidad("Berisso", "Berisso", "Buenos Aires"),
    Localidad("Ensenada", "Ensenada", "Buenos Aires"),
    Localidad("Córdoba Capital", "Capital", "Córdoba"),
    Localidad("Villa Carlos Paz", "Punilla", "Córdoba"),
    Localidad("Rosario", "Rosario", "Santa Fe"),
    Localidad("Santa Fe Capital", "La Capital", "Santa Fe"),
]

# Lista de referencia completa (Lista B) - incluye más localidades
localidades_referencia = [
    # Incluir todas las de la lista A
    *localidades_disponibles,
    # Agregar localidades adicionales que no están en la lista principal
    Localidad("Martínez", "San Isidro", "Buenos Aires"),
    Localidad("Acassuso", "San Isidro", "Buenos Aires"),
    Localidad("Beccar", "San Isidro", "Buenos Aires"),
    Localidad("Florida", "Vicente López", "Buenos Aires"),
    Localidad("Olivos", "Vicente López", "Buenos Aires"),
    Localidad("Villa Allende", "Colón", "Córdoba"),
    Localidad("Salsipuedes", "Colón", "Córdoba"),
    Localidad("City Bell", "La Plata", "Buenos Aires"),
    Localidad("Gonnet", "La Plata", "Buenos Aires"),
]


def ejemplo_basico():
    """Ejemplo básico de búsqueda de localidades."""
    print("=" * 70)
    print("EJEMPLO BÁSICO - Búsqueda de Localidades")
    print("=" * 70)
    
    # Caso 1: Buscar localidad que existe en la lista principal
    print("\n1. Buscar 'La Plata' (existe en lista principal):")
    resultado = encontrar_localidad("La Plata", localidades_disponibles, localidades_referencia)
    print(f"   Resultado: {resultado}")
    
    # Caso 2: Buscar localidad que NO existe en lista principal pero SÍ en referencia
    print("\n2. Buscar 'Martínez' (no está en lista principal, pero está en referencia):")
    print("   Martínez pertenece al partido 'San Isidro'")
    resultado = encontrar_localidad("Martínez", localidades_disponibles, localidades_referencia)
    print(f"   Resultado: {resultado}")
    print("   -> Retorna 'San Isidro' porque es del mismo partido")
    
    # Caso 3: Buscar otra localidad del partido Vicente López
    print("\n3. Buscar 'Olivos' (partido Vicente López):")
    resultado = encontrar_localidad("Olivos", localidades_disponibles, localidades_referencia)
    print(f"   Resultado: {resultado}")
    print("   -> Retorna 'Vicente López' porque es del mismo partido")
    
    # Caso 4: Buscar localidad de partido no disponible pero provincia sí
    print("\n4. Buscar 'Villa Allende' (partido Colón, no disponible en lista principal):")
    resultado = encontrar_localidad("Villa Allende", localidades_disponibles, localidades_referencia)
    print(f"   Resultado: {resultado}")
    print("   -> Retorna localidad de la misma provincia (Córdoba)")


def ejemplo_detallado():
    """Ejemplo con información detallada del proceso de búsqueda."""
    print("\n" + "=" * 70)
    print("EJEMPLO DETALLADO - Información del Proceso")
    print("=" * 70)
    
    casos_prueba = [
        "Florida",      # Partido Vicente López
        "Beccar",       # Partido San Isidro
        "City Bell",    # Partido La Plata
        "Salsipuedes",  # Partido Colón (no en lista principal, fallback a provincia)
    ]
    
    for localidad_buscar in casos_prueba:
        print(f"\nBuscando: '{localidad_buscar}'")
        resultado = encontrar_localidad_detallado(
            localidad_buscar, 
            localidades_disponibles, 
            localidades_referencia
        )
        
        print(f"  - Referencia encontrada: {resultado['referencia']}")
        print(f"  - Método de búsqueda: {resultado['metodo']}")
        print(f"  - Similitud: {resultado['similitud']:.2f}")
        print(f"  - Localidad retornada: {resultado['encontrada']}")


def ejemplo_sin_referencia():
    """Ejemplo usando solo la lista principal (sin lista de referencia)."""
    print("\n" + "=" * 70)
    print("EJEMPLO - Sin Lista de Referencia")
    print("=" * 70)
    print("\nCuando no se provee lista de referencia, se usa la misma lista principal")
    
    localidad_buscar = "La Plata"
    resultado = encontrar_localidad(localidad_buscar, localidades_disponibles)
    print(f"\nBuscando '{localidad_buscar}': {resultado}")


if __name__ == "__main__":
    ejemplo_basico()
    ejemplo_detallado()
    ejemplo_sin_referencia()
    
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print("""
La funcionalidad implementada:
1. Busca primero coincidencia exacta en la lista principal
2. Si no encuentra, busca en la lista de referencia
3. Usa la información de partido/provincia de la referencia
4. Retorna la mejor coincidencia de la lista principal:
   - Prioridad 1: Mismo partido
   - Prioridad 2: Misma provincia
   - Si no hay coincidencia: None
    """)
