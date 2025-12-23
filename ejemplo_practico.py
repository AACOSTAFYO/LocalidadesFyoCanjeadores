"""
Ejemplo práctico - Caso de uso real

Este ejemplo muestra cómo usar el sistema en un escenario real
donde tienes una lista limitada de localidades disponibles para canje,
pero necesitas mapear cualquier localidad ingresada por el usuario.
"""
from localidades import Localidad, encontrar_localidad, encontrar_localidad_detallado


def main():
    # Lista de localidades donde FYO tiene canjeadores disponibles (Lista A)
    localidades_con_canjeadores = [
        Localidad("CABA", "Capital", "Buenos Aires"),
        Localidad("La Plata", "La Plata", "Buenos Aires"),
        Localidad("Mar del Plata", "General Pueyrredón", "Buenos Aires"),
        Localidad("Rosario", "Rosario", "Santa Fe"),
        Localidad("Córdoba", "Capital", "Córdoba"),
        Localidad("Mendoza", "Capital", "Mendoza"),
    ]
    
    # Lista completa de localidades argentinas (Lista B - base de datos completa)
    localidades_argentina = [
        *localidades_con_canjeadores,
        # Localidades del Gran Buenos Aires
        Localidad("Vicente López", "Vicente López", "Buenos Aires"),
        Localidad("San Isidro", "San Isidro", "Buenos Aires"),
        Localidad("San Fernando", "San Fernando", "Buenos Aires"),
        Localidad("Tigre", "Tigre", "Buenos Aires"),
        Localidad("Olivos", "Vicente López", "Buenos Aires"),
        Localidad("Martínez", "San Isidro", "Buenos Aires"),
        Localidad("Beccar", "San Isidro", "Buenos Aires"),
        # Localidades del partido de La Plata
        Localidad("City Bell", "La Plata", "Buenos Aires"),
        Localidad("Villa Elisa", "La Plata", "Buenos Aires"),
        Localidad("Gonnet", "La Plata", "Buenos Aires"),
        Localidad("Tolosa", "La Plata", "Buenos Aires"),
        # Localidades de Córdoba
        Localidad("Villa Carlos Paz", "Punilla", "Córdoba"),
        Localidad("Río Cuarto", "Río Cuarto", "Córdoba"),
        Localidad("Villa María", "General San Martín", "Córdoba"),
        # Localidades de Santa Fe
        Localidad("Santa Fe", "La Capital", "Santa Fe"),
        Localidad("Rafaela", "Castellanos", "Santa Fe"),
        # Localidades de Mendoza
        Localidad("Luján de Cuyo", "Luján de Cuyo", "Mendoza"),
        Localidad("Maipú", "Maipú", "Mendoza"),
    ]
    
    print("=" * 80)
    print("SISTEMA DE ASIGNACIÓN DE CANJEADORES FYO")
    print("=" * 80)
    print("\nLocalidades con canjeadores disponibles:")
    for loc in localidades_con_canjeadores:
        print(f"  • {loc.nombre} ({loc.provincia})")
    
    print("\n" + "=" * 80)
    print("EJEMPLOS DE BÚSQUEDA")
    print("=" * 80)
    
    # Casos de prueba realistas
    casos = [
        ("La Plata", "Usuario de La Plata ciudad"),
        ("City Bell", "Usuario de City Bell (partido La Plata)"),
        ("Villa Elisa", "Usuario de Villa Elisa (partido La Plata)"),
        ("Martínez", "Usuario de Martínez (partido San Isidro, Gran BA)"),
        ("Olivos", "Usuario de Olivos (partido Vicente López, Gran BA)"),
        ("Villa Carlos Paz", "Usuario de Villa Carlos Paz (Córdoba interior)"),
        ("Luján de Cuyo", "Usuario de Luján de Cuyo (Mendoza interior)"),
    ]
    
    for localidad_usuario, descripcion in casos:
        print(f"\n📍 {descripcion}")
        print(f"   Ingresó: '{localidad_usuario}'")
        
        resultado = encontrar_localidad_detallado(
            localidad_usuario,
            localidades_con_canjeadores,
            localidades_argentina
        )
        
        if resultado['encontrada']:
            print(f"   ✅ Canjeador asignado: {resultado['encontrada'].nombre}")
            print(f"      Método: {resultado['metodo']}")
            if resultado['metodo'] == 'partido':
                print(f"      Razón: Mismo partido ({resultado['referencia'].partido})")
            elif resultado['metodo'] == 'provincia':
                print(f"      Razón: Misma provincia ({resultado['referencia'].provincia})")
            elif resultado['metodo'] == 'exacta':
                print(f"      Razón: Coincidencia exacta")
        else:
            print(f"   ❌ No se pudo asignar canjeador")
    
    print("\n" + "=" * 80)
    print("RESUMEN DEL SISTEMA")
    print("=" * 80)
    print("""
El sistema funciona de la siguiente manera:

1. Si el usuario ingresa una localidad con canjeador disponible:
   → Se asigna directamente ese canjeador

2. Si el usuario ingresa una localidad sin canjeador pero del mismo partido:
   → Se asigna el canjeador del partido (ej: City Bell → La Plata)

3. Si no hay canjeador en el partido pero sí en la provincia:
   → Se asigna el canjeador más cercano de la provincia

4. Si no hay ninguna coincidencia razonable:
   → Se retorna None y se debe manejar manualmente

Esto permite cubrir mucho más territorio con menos canjeadores físicos,
asignando automáticamente basándose en proximidad geográfica.
    """)


if __name__ == "__main__":
    main()
