"""
Data persistence module for saving lists to SQL Server.
"""
from typing import List
from db_config import DatabaseConnection
from db_schema import DatabaseSchema


class DataPersistence:
    """Handle data persistence operations."""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize with a database connection.
        
        Args:
            db_connection: DatabaseConnection instance
        """
        self.db_connection = db_connection
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        print("Creating database tables...")
        try:
            create_sql = DatabaseSchema.create_tables_sql()
            # Execute the entire SQL block as pyodbc can handle multiple statements
            self.db_connection.execute_query(create_sql)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    
    def clear_tables(self):
        """Clear all data from tables."""
        print("Clearing existing data from tables...")
        try:
            clear_sql = DatabaseSchema.clear_tables_sql()
            self.db_connection.execute_query(clear_sql)
            print("Tables cleared successfully.")
        except Exception as e:
            print(f"Error clearing tables: {e}")
            raise
    
    def save_list_a(self, list_a: List):
        """
        Save list A to database.
        
        Args:
            list_a: List of values to save
        """
        print(f"Saving {len(list_a)} items to ListaA...")
        insert_sql = DatabaseSchema.insert_list_a_sql()
        
        saved_count = 0
        for value in list_a:
            try:
                self.db_connection.execute_query(insert_sql, (value,))
                saved_count += 1
            except Exception as e:
                print(f"Error saving value '{value}' to ListaA: {e}")
        
        print(f"Saved {saved_count} items to ListaA.")
        return saved_count
    
    def save_list_b(self, list_b: List):
        """
        Save list B to database.
        
        Args:
            list_b: List of values to save
        """
        print(f"Saving {len(list_b)} items to ListaB...")
        insert_sql = DatabaseSchema.insert_list_b_sql()
        
        saved_count = 0
        for value in list_b:
            try:
                self.db_connection.execute_query(insert_sql, (value,))
                saved_count += 1
            except Exception as e:
                print(f"Error saving value '{value}' to ListaB: {e}")
        
        print(f"Saved {saved_count} items to ListaB.")
        return saved_count
    
    def save_lists(self, list_a: List, list_b: List, clear_existing: bool = True):
        """
        Save both lists to database.
        
        Args:
            list_a: List A values
            list_b: List B values
            clear_existing: Whether to clear existing data before saving
        """
        if clear_existing:
            self.clear_tables()
        
        count_a = self.save_list_a(list_a)
        count_b = self.save_list_b(list_b)
        
        print(f"\nSummary:")
        print(f"  - ListaA: {count_a} items saved")
        print(f"  - ListaB: {count_b} items saved")
        
        return count_a, count_b
    
    def verify_data(self):
        """Verify saved data by counting records."""
        print("\nVerifying saved data...")
        
        count_a_sql = "SELECT COUNT(*) FROM ListaA"
        count_b_sql = "SELECT COUNT(*) FROM ListaB"
        
        result_a = self.db_connection.execute_query(count_a_sql)
        result_b = self.db_connection.execute_query(count_b_sql)
        
        count_a = result_a[0][0] if result_a else 0
        count_b = result_b[0][0] if result_b else 0
        
        print(f"  - ListaA contains {count_a} records")
        print(f"  - ListaB contains {count_b} records")
        
        return count_a, count_b
