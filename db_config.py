"""
Database configuration and connection management for SQL Server.
"""
import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConfig:
    """Configuration for SQL Server database connection."""
    
    def __init__(self):
        self.server = os.getenv('DB_SERVER', 'localhost')
        self.database = os.getenv('DB_NAME', 'LocalidadesFyoCanjeadores')
        self.username = os.getenv('DB_USER', 'sa')
        self.password = os.getenv('DB_PASSWORD', '')
        self.driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    def get_connection_string(self):
        """Build SQL Server connection string."""
        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
        )


class DatabaseConnection:
    """Manage database connections."""
    
    def __init__(self, config=None):
        self.config = config or DatabaseConfig()
        self.connection = None
    
    def connect(self):
        """Establish connection to SQL Server."""
        try:
            connection_string = self.config.get_connection_string()
            self.connection = pyodbc.connect(connection_string)
            print(f"Connected to database: {self.config.database}")
            return self.connection
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        if not self.connection:
            raise Exception("Not connected to database. Call connect() first.")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Check if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
