"""
Database schema management for LocalidadesFyoCanjeadores.
"""


class DatabaseSchema:
    """Manage database schema creation and updates."""
    
    @staticmethod
    def create_tables_sql():
        """
        Return SQL statements to create tables for lists a and b.
        """
        return """
        -- Create table for List A
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaA')
        BEGIN
            CREATE TABLE ListaA (
                id INT IDENTITY(1,1) PRIMARY KEY,
                valor NVARCHAR(255) NOT NULL,
                fecha_creacion DATETIME DEFAULT GETDATE(),
                fecha_actualizacion DATETIME DEFAULT GETDATE()
            );
        END
        
        -- Create table for List B
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaB')
        BEGIN
            CREATE TABLE ListaB (
                id INT IDENTITY(1,1) PRIMARY KEY,
                valor NVARCHAR(255) NOT NULL,
                fecha_creacion DATETIME DEFAULT GETDATE(),
                fecha_actualizacion DATETIME DEFAULT GETDATE()
            );
        END
        """
    
    @staticmethod
    def drop_tables_sql():
        """
        Return SQL statements to drop tables.
        """
        return """
        IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaA')
        BEGIN
            DROP TABLE ListaA;
        END
        
        IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaB')
        BEGIN
            DROP TABLE ListaB;
        END
        """
    
    @staticmethod
    def clear_tables_sql():
        """
        Return SQL statements to clear data from tables.
        """
        return """
        IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaA')
        BEGIN
            DELETE FROM ListaA;
        END
        
        IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ListaB')
        BEGIN
            DELETE FROM ListaB;
        END
        """
    
    @staticmethod
    def insert_list_a_sql():
        """Return SQL for inserting into ListaA."""
        return "INSERT INTO ListaA (valor) VALUES (?)"
    
    @staticmethod
    def insert_list_b_sql():
        """Return SQL for inserting into ListaB."""
        return "INSERT INTO ListaB (valor) VALUES (?)"
    
    @staticmethod
    def select_all_list_a_sql():
        """Return SQL for selecting all from ListaA."""
        return "SELECT id, valor, fecha_creacion, fecha_actualizacion FROM ListaA ORDER BY id"
    
    @staticmethod
    def select_all_list_b_sql():
        """Return SQL for selecting all from ListaB."""
        return "SELECT id, valor, fecha_creacion, fecha_actualizacion FROM ListaB ORDER BY id"
