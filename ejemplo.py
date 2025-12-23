"""
Ejemplo de uso del módulo de localidades.

Este script demuestra cómo usar la funcionalidad de búsqueda de localidades
con fallback por partido.
"""

from localidades import crear_localidad, LocalidadMatcher


def main():
    """Función principal con ejemplos de uso."""
    
    print("=" * 80)
    print("EJEMPLO DE USO: Sistema de Búsqueda de Localidades con Fallback")
    print("=" * 80)
    print()
    
    # Crear lista principal de localidades (las que están disponibles en el sistema)
    print("1. Creando lista PRINCIPAL de localidades disponibles:")
    print("-" * 80)
    lista_principal = [
        crear_localidad("Acassuso", "San Isidro", "Buenos Aires"),
        crear_localidad("Beccar", "San Isidro", "Buenos Aires"),
        crear_localidad("Vicente López", "Vicente López", "Buenos Aires"),
        crear_localidad("Florida", "Vicente López", "Buenos Aires"),
        crear_localidad("Olivos", "Vicente López", "Buenos Aires"),
        crear_localidad("La Plata", "La Plata", "Buenos Aires"),
        crear_localidad("City Bell", "La Plata", "Buenos Aires"),
        crear_localidad("Rosario", "Rosario", "Santa Fe"),
        crear_localidad("Fisherton", "Rosario", "Santa Fe"),
    ]
    
    for loc in lista_principal:
        print(f"  - {loc.nombre} (Partido: {loc.partido}, Provincia: {loc.provincia})")
    print()
    
    # Crear lista de fallback (localidades que pueden no estar en la principal)
    print("2. Creando lista FALLBACK de localidades alternativas:")
    print("-" * 80)
    lista_fallback = [
        crear_localidad("San Isidro", "San Isidro", "Buenos Aires"),
        crear_localidad("Martínez", "San Isidro", "Buenos Aires"),
        crear_localidad("La Lucila", "Vicente López", "Buenos Aires"),
        crear_localidad("Villa Elisa", "La Plata", "Buenos Aires"),
        crear_localidad("Gonnet", "La Plata", "Buenos Aires"),
        crear_localidad("Funes", "Rosario", "Santa Fe"),
        crear_localidad("Roldán", "Rosario", "Santa Fe"),
    ]
    
    for loc in lista_fallback:
        print(f"  - {loc.nombre} (Partido: {loc.partido}, Provincia: {loc.provincia})")
    print()
    
    # Crear el matcher
    matcher = LocalidadMatcher(lista_principal, lista_fallback)
    
    # Ejemplos de búsqueda
    print("3. EJEMPLOS DE BÚSQUEDA:")
    print("=" * 80)
    print()
    
    # Caso 1: Buscar localidad que está en la lista principal
    print("Caso 1: Buscar 'Acassuso' (está en lista principal)")
    print("-" * 80)
    resultado = matcher.buscar_localidad("Acassuso")
    if resultado:
        print(f"✓ ENCONTRADO: {resultado}")
    else:
        print("✗ No encontrado")
    print()
    
    # Caso 2: Buscar localidad que NO está en principal pero SÍ en fallback
    print("Caso 2: Buscar 'San Isidro' (NO está en principal, SÍ en fallback)")
    print("-" * 80)
    print("Comportamiento esperado: Debe encontrar una localidad del partido 'San Isidro'")
    print("de la lista principal (Acassuso o Beccar)")
    resultado = matcher.buscar_localidad("San Isidro")
    if resultado:
        print(f"✓ ENCONTRADO (fallback a partido): {resultado}")
    else:
        print("✗ No encontrado")
    print()
    
    # Caso 3: Buscar otra localidad del fallback
    print("Caso 3: Buscar 'Martínez' (NO está en principal, SÍ en fallback)")
    print("-" * 80)
    print("Comportamiento esperado: Debe encontrar una localidad del partido 'San Isidro'")
    resultado = matcher.buscar_localidad("Martínez")
    if resultado:
        print(f"✓ ENCONTRADO (fallback a partido): {resultado}")
    else:
        print("✗ No encontrado")
    print()
    
    # Caso 4: Buscar localidad con diferente partido
    print("Caso 4: Buscar 'La Lucila' (partido Vicente López)")
    print("-" * 80)
    resultado = matcher.buscar_localidad("La Lucila")
    if resultado:
        print(f"✓ ENCONTRADO (fallback a partido): {resultado}")
    else:
        print("✗ No encontrado")
    print()
    
    # Caso 5: Buscar localidad que no existe en ninguna lista
    print("Caso 5: Buscar 'Localidad Inexistente' (no está en ninguna lista)")
    print("-" * 80)
    resultado = matcher.buscar_localidad("Localidad Inexistente")
    if resultado:
        print(f"✓ ENCONTRADO: {resultado}")
    else:
        print("✗ No encontrado (como se esperaba)")
    print()
    
    # Caso 6: Listar todas las localidades de un partido
    print("Caso 6: Listar TODAS las localidades del partido 'Vicente López'")
    print("-" * 80)
    localidades = matcher.buscar_todas_del_partido("Vicente López")
    print(f"Encontradas {len(localidades)} localidades:")
    for loc in localidades:
        print(f"  - {loc.nombre}")
    print()
    
    # Caso 7: Búsqueda case-insensitive
    print("Caso 7: Búsqueda case-insensitive 'ACASSUSO'")
    print("-" * 80)
    resultado = matcher.buscar_localidad("ACASSUSO")
    if resultado:
        print(f"✓ ENCONTRADO: {resultado}")
    else:
        print("✗ No encontrado")
    print()
    
    print("=" * 80)
    print("FIN DEL EJEMPLO")
    print("=" * 80)


if __name__ == "__main__":
    main()
