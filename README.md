# LocalidadesFyoCanjeadores

Sistema para importar listas desde Excel y persistirlas en una base de datos SQL Server.

## Descripción

Este proyecto permite leer dos listas (Lista A y Lista B) desde un archivo Excel y guardarlas en una base de datos SQL Server. Es útil para la gestión de localidades y canjeadores FYO.

## Requisitos

- Python 3.7 o superior
- SQL Server (cualquier versión compatible con ODBC Driver 17)
- ODBC Driver 17 for SQL Server

## Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/AACOSTAFYO/LocalidadesFyoCanjeadores.git
cd LocalidadesFyoCanjeadores
```

2. **Instalar dependencias de Python:**
```bash
pip install -r requirements.txt
```

3. **Configurar la conexión a la base de datos:**

Copiar el archivo de ejemplo de configuración:
```bash
cp .env.example .env
```

Editar el archivo `.env` con las credenciales de tu base de datos SQL Server:
```
DB_SERVER=tu_servidor
DB_NAME=LocalidadesFyoCanjeadores
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_DRIVER=ODBC Driver 17 for SQL Server
```

4. **Crear la base de datos en SQL Server:**

Puedes crear la base de datos manualmente o el script la creará automáticamente si tienes permisos suficientes.

```sql
CREATE DATABASE LocalidadesFyoCanjeadores;
```

## Uso

### Crear un archivo Excel de ejemplo

Para crear un archivo Excel de ejemplo con datos de muestra:

```bash
python create_sample_excel.py
```

Esto generará un archivo `sample_data.xlsx` con datos de ejemplo.

### Importar datos desde Excel

**Uso básico:**
```bash
python main.py archivo.xlsx
```

**Con opciones:**
```bash
# Especificar una hoja específica
python main.py archivo.xlsx --sheet NombreHoja

# Mantener datos existentes (no limpiar tablas)
python main.py archivo.xlsx --keep-existing

# Forzar creación de tablas
python main.py archivo.xlsx --create-tables
```

**Ejemplos:**
```bash
# Importar desde el archivo de ejemplo
python main.py sample_data.xlsx

# Importar manteniendo datos existentes
python main.py nuevos_datos.xlsx --keep-existing

# Importar de una hoja específica y crear tablas
python main.py datos.xlsx --sheet Hoja1 --create-tables
```

## Formato del archivo Excel

El archivo Excel debe tener el siguiente formato:

| Lista A          | Lista B        |
|------------------|----------------|
| Buenos Aires     | Canjeador 001  |
| Córdoba          | Canjeador 002  |
| Rosario          | Canjeador 003  |
| ...              | ...            |

- **Columna A**: Contiene los valores de la Lista A (ej: localidades)
- **Columna B**: Contiene los valores de la Lista B (ej: canjeadores)
- La primera fila puede contener encabezados (se detectan automáticamente)
- Las celdas vacías se omiten

## Estructura de la Base de Datos

El sistema crea dos tablas:

### Tabla ListaA
```sql
CREATE TABLE ListaA (
    id INT IDENTITY(1,1) PRIMARY KEY,
    valor NVARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_actualizacion DATETIME DEFAULT GETDATE()
);
```

### Tabla ListaB
```sql
CREATE TABLE ListaB (
    id INT IDENTITY(1,1) PRIMARY KEY,
    valor NVARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_actualizacion DATETIME DEFAULT GETDATE()
);
```

## Estructura del Proyecto

```
LocalidadesFyoCanjeadores/
├── main.py                  # Script principal
├── excel_reader.py          # Módulo para leer archivos Excel
├── db_config.py             # Configuración y conexión a la base de datos
├── db_schema.py             # Esquema de la base de datos
├── data_persistence.py      # Lógica de persistencia de datos
├── create_sample_excel.py   # Script para crear archivo de ejemplo
├── requirements.txt         # Dependencias de Python
├── .env.example            # Ejemplo de configuración
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## Módulos

### excel_reader.py
Módulo para leer listas desde archivos Excel usando `openpyxl`.

### db_config.py
Gestión de la conexión a SQL Server usando `pyodbc`.

### db_schema.py
Define el esquema de la base de datos y consultas SQL.

### data_persistence.py
Lógica para persistir datos en la base de datos.

### main.py
Script principal que orquesta el proceso completo.

## Solución de Problemas

### Error de conexión a SQL Server

Si recibes un error de conexión:
1. Verifica que SQL Server esté ejecutándose
2. Verifica las credenciales en el archivo `.env`
3. Asegúrate de que el ODBC Driver 17 esté instalado
4. Verifica que el puerto de SQL Server esté abierto (por defecto 1433)

### Error al leer el archivo Excel

Si no puede leer el archivo Excel:
1. Verifica que el archivo exista
2. Asegúrate de que el archivo no esté abierto en Excel
3. Verifica que el formato sea .xlsx

### Tablas no existen

Si recibes un error de que las tablas no existen:
```bash
python main.py archivo.xlsx --create-tables
```

## Licencia

Este proyecto es de código abierto.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.