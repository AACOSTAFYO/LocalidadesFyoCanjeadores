-- Script para crear la base de datos y tablas en SQL Server
-- LocalidadesFyoCanjeadores

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'LocalidadesFyoCanjeadores')
BEGIN
    CREATE DATABASE LocalidadesFyoCanjeadores;
    PRINT 'Base de datos LocalidadesFyoCanjeadores creada.';
END
ELSE
BEGIN
    PRINT 'Base de datos LocalidadesFyoCanjeadores ya existe.';
END
GO

-- Usar la base de datos
USE LocalidadesFyoCanjeadores;
GO

-- Crear tabla ListaA
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaA')
BEGIN
    CREATE TABLE ListaA (
        id INT IDENTITY(1,1) PRIMARY KEY,
        valor NVARCHAR(255) NOT NULL,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_actualizacion DATETIME DEFAULT GETDATE()
    );
    PRINT 'Tabla ListaA creada.';
END
ELSE
BEGIN
    PRINT 'Tabla ListaA ya existe.';
END
GO

-- Crear tabla ListaB
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaB')
BEGIN
    CREATE TABLE ListaB (
        id INT IDENTITY(1,1) PRIMARY KEY,
        valor NVARCHAR(255) NOT NULL,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_actualizacion DATETIME DEFAULT GETDATE()
    );
    PRINT 'Tabla ListaB creada.';
END
ELSE
BEGIN
    PRINT 'Tabla ListaB ya existe.';
END
GO

-- Verificar tablas creadas
SELECT 'ListaA' AS Tabla, COUNT(*) AS NumeroRegistros FROM ListaA
UNION ALL
SELECT 'ListaB' AS Tabla, COUNT(*) AS NumeroRegistros FROM ListaB;
GO

PRINT 'Script completado exitosamente.';
