# LocalidadesFyoCanjeadores

Sistema de búsqueda de localidades con fallback por partido.

## Descripción

Este módulo permite gestionar localidades (con sus partidos y provincias) y buscar coincidencias con lógica de fallback. Cuando se busca una localidad que no está en la lista principal, el sistema busca en una lista de fallback y retorna la mejor opción del mismo partido de la lista principal.

## Características

- ✅ Búsqueda de localidades en lista principal
- ✅ Fallback automático por partido cuando la localidad no está en lista principal
- ✅ Búsqueda case-insensitive (no distingue mayúsculas/minúsculas)
- ✅ Normalización de espacios en búsquedas
- ✅ Índices optimizados para búsqueda rápida
- ✅ Búsqueda de todas las localidades de un partido

## Instalación

No requiere dependencias externas. Solo Python 3.7+

```bash
# Clonar el repositorio
git clone https://github.com/AACOSTAFYO/LocalidadesFyoCanjeadores.git
cd LocalidadesFyoCanjeadores
```

## Uso Básico

```python
from localidades import crear_localidad, LocalidadMatcher

# Crear lista principal de localidades
lista_principal = [
    crear_localidad("Acassuso", "San Isidro", "Buenos Aires"),
    crear_localidad("Beccar", "San Isidro", "Buenos Aires"),
    crear_localidad("Vicente López", "Vicente López", "Buenos Aires"),
]

# Crear lista de fallback
lista_fallback = [
    crear_localidad("San Isidro", "San Isidro", "Buenos Aires"),
    crear_localidad("Martínez", "San Isidro", "Buenos Aires"),
]

# Crear el matcher
matcher = LocalidadMatcher(lista_principal, lista_fallback)

# Buscar una localidad que está en la lista principal
resultado = matcher.buscar_localidad("Acassuso")
print(resultado)  # Localidad(nombre='Acassuso', ...)

# Buscar una localidad que NO está en principal pero SÍ en fallback
# Retorna una localidad del mismo partido de la lista principal
resultado = matcher.buscar_localidad("San Isidro")
print(resultado)  # Localidad(nombre='Acassuso', partido='San Isidro', ...)
```

## Caso de Uso

**Problema**: Tengo una lista de localidades disponibles en mi sistema (lista A), pero los usuarios pueden ingresar localidades que no están en esa lista. Sin embargo, esas localidades pertenecen a partidos que sí tengo en mi lista.

**Solución**: Este sistema busca primero en la lista principal. Si no encuentra la localidad, busca en una lista de fallback (lista B). Si la encuentra en el fallback, retorna la mejor opción del mismo partido de la lista principal.

**Ejemplo Real**:
- Lista principal: ["Acassuso", "Beccar"] (ambas del partido San Isidro)
- Usuario ingresa: "Martínez" (no está en lista principal)
- El sistema busca "Martínez" en lista fallback y encuentra que es del partido "San Isidro"
- Retorna "Acassuso" (primera localidad del partido San Isidro en lista principal)

## API

### Clase `Localidad`

Representa una localidad con su partido y provincia.

```python
@dataclass
class Localidad:
    nombre: str
    partido: str
    provincia: str
```

### Función `crear_localidad`

Helper para crear una localidad.

```python
def crear_localidad(nombre: str, partido: str, provincia: str) -> Localidad
```

### Clase `LocalidadMatcher`

Clase principal para búsqueda de localidades con fallback.

#### Constructor

```python
def __init__(self, lista_principal: List[Localidad], lista_fallback: List[Localidad] = None)
```

#### Métodos

- `buscar_localidad(nombre_localidad: str) -> Optional[Localidad]`
  - Busca una localidad por nombre
  - Retorna la localidad si está en lista principal
  - Si no está en principal pero sí en fallback, retorna una localidad del mismo partido de la lista principal
  - Retorna None si no se encuentra en ninguna lista

- `buscar_todas_del_partido(partido: str) -> List[Localidad]`
  - Retorna todas las localidades de un partido en la lista principal

## Ejemplos

Ejecuta el script de ejemplo:

```bash
python ejemplo.py
```

## Tests

Ejecuta los tests unitarios:

```bash
python -m unittest test_localidades -v
```

## Estructura del Proyecto

```
LocalidadesFyoCanjeadores/
├── README.md              # Este archivo
├── localidades.py         # Módulo principal con la funcionalidad
├── test_localidades.py    # Tests unitarios
└── ejemplo.py             # Ejemplos de uso
```

## Licencia

MIT

## Autor

AACOSTAFYO