# LocalidadesFyoCanjeadores

Sistema para gestionar localidades y encontrar coincidencias basadas en partido y provincia.

## Descripción

Este módulo proporciona funcionalidad para buscar localidades con un sistema de fallback inteligente. Cuando se busca una localidad que no está en la lista principal, el sistema:

1. Busca la localidad en una lista de referencia
2. Identifica el partido y provincia de esa localidad
3. Retorna la mejor coincidencia de la lista principal, priorizando:
   - **Primero**: Localidades del mismo partido
   - **Segundo**: Localidades de la misma provincia
   - **Tercero**: `None` si no hay coincidencias

## Estructura del Proyecto

```
LocalidadesFyoCanjeadores/
├── localidades.py          # Módulo principal con la lógica de búsqueda
├── ejemplo.py              # Ejemplos de uso
├── test_localidades.py     # Tests unitarios
└── README.md              # Esta documentación
```

## Instalación

No requiere dependencias externas. Solo necesitas Python 3.7+.

```bash
# Clonar el repositorio
git clone https://github.com/AACOSTAFYO/LocalidadesFyoCanjeadores.git
cd LocalidadesFyoCanjeadores
```

## Uso Básico

### Ejemplo Simple

```python
from localidades import Localidad, encontrar_localidad

# Definir lista principal de localidades disponibles
localidades_disponibles = [
    Localidad("Vicente López", "Vicente López", "Buenos Aires"),
    Localidad("San Isidro", "San Isidro", "Buenos Aires"),
    Localidad("La Plata", "La Plata", "Buenos Aires"),
]

# Definir lista de referencia (incluye más localidades)
localidades_referencia = [
    *localidades_disponibles,
    Localidad("Martínez", "San Isidro", "Buenos Aires"),
    Localidad("Florida", "Vicente López", "Buenos Aires"),
]

# Buscar una localidad que no está en la lista principal
resultado = encontrar_localidad("Martínez", localidades_disponibles, localidades_referencia)
print(resultado)
# Output: Localidad(nombre='San Isidro', partido='San Isidro', provincia='Buenos Aires')
```

### Búsqueda Detallada

Para obtener información sobre el proceso de búsqueda:

```python
from localidades import encontrar_localidad_detallado

resultado = encontrar_localidad_detallado("Martínez", localidades_disponibles, localidades_referencia)
print(f"Método: {resultado['metodo']}")  # 'partido'
print(f"Similitud: {resultado['similitud']}")  # 0.XX
print(f"Encontrada: {resultado['encontrada']}")
print(f"Referencia: {resultado['referencia']}")
```

## API

### Clase `Localidad`

```python
@dataclass
class Localidad:
    nombre: str      # Nombre de la localidad
    partido: str     # Partido al que pertenece
    provincia: str   # Provincia
```

### Función `encontrar_localidad`

```python
def encontrar_localidad(
    localidad_buscada: str,
    lista_principal: List[Localidad],
    lista_referencia: Optional[List[Localidad]] = None
) -> Optional[Localidad]:
```

**Parámetros:**
- `localidad_buscada`: Nombre de la localidad a buscar
- `lista_principal`: Lista de localidades disponibles (lista A)
- `lista_referencia`: Lista de referencia opcional (lista B). Si es `None`, usa `lista_principal`

**Retorna:**
- `Localidad` encontrada o `None` si no hay coincidencias

### Función `encontrar_localidad_detallado`

Similar a `encontrar_localidad` pero retorna un diccionario con información detallada:

```python
{
    'encontrada': Localidad o None,
    'metodo': 'exacta' | 'partido' | 'provincia' | 'no_encontrada',
    'similitud': float,  # 0.0 a 1.0
    'referencia': Localidad o None
}
```

## Ejemplos de Uso

Ejecuta el archivo de ejemplos:

```bash
python ejemplo.py
```

Esto mostrará varios casos de uso incluyendo:
- Búsqueda exacta
- Búsqueda por partido
- Búsqueda por provincia (fallback)
- Información detallada del proceso

## Tests

Ejecutar los tests unitarios:

```bash
python test_localidades.py
```

O con pytest (si está instalado):

```bash
pytest test_localidades.py -v
```

## Casos de Uso

### Caso 1: Localidad existe en lista principal
```python
resultado = encontrar_localidad("La Plata", localidades_disponibles, localidades_referencia)
# Retorna directamente "La Plata"
```

### Caso 2: Localidad no existe pero su partido sí
```python
# "Martínez" no está en lista principal, pero pertenece al partido "San Isidro"
resultado = encontrar_localidad("Martínez", localidades_disponibles, localidades_referencia)
# Retorna "San Isidro" (mismo partido)
```

### Caso 3: Localidad no existe, su partido tampoco, pero su provincia sí
```python
# "Villa Allende" es del partido "Colón" (no disponible)
# pero es de provincia "Córdoba"
resultado = encontrar_localidad("Villa Allende", localidades_disponibles, localidades_referencia)
# Retorna una localidad de Córdoba disponible en lista principal
```

### Caso 4: Sin coincidencias
```python
resultado = encontrar_localidad("LocalidadInexistente123", localidades_disponibles, localidades_referencia)
# Retorna None
```

## Algoritmo de Búsqueda

1. **Búsqueda exacta**: Verifica si la localidad existe en la lista principal (case-insensitive)
2. **Búsqueda en referencia**: Busca la localidad en la lista de referencia usando similitud de texto
3. **Filtrado por partido**: Busca en la lista principal localidades del mismo partido
4. **Fallback por provincia**: Si no hay coincidencias por partido, busca por provincia
5. **Mejor similitud**: De los candidatos filtrados, retorna el más similar al nombre buscado

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto es de código abierto.

## Contacto

Para preguntas o sugerencias, por favor abre un issue en GitHub.