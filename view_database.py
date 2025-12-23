"""
Script to view data stored in the SQL Server database.
"""
import sys
from db_config import DatabaseConnection
from db_schema import DatabaseSchema


def view_database_contents():
    """View contents of both tables."""
    print("=" * 70)
    print("Database Contents Viewer - LocalidadesFyoCanjeadores")
    print("=" * 70)
    print()
    
    try:
        with DatabaseConnection() as db_conn:
            # Get Lista A
            print("Lista A:")
            print("-" * 70)
            select_a_sql = DatabaseSchema.select_all_list_a_sql()
            results_a = db_conn.execute_query(select_a_sql)
            
            if results_a:
                for row in results_a:
                    id_val, valor, fecha_creacion, fecha_actualizacion = row
                    print(f"  [{id_val:3d}] {valor}")
                print(f"\nTotal: {len(results_a)} records")
            else:
                print("  (No data)")
            
            print()
            
            # Get Lista B
            print("Lista B:")
            print("-" * 70)
            select_b_sql = DatabaseSchema.select_all_list_b_sql()
            results_b = db_conn.execute_query(select_b_sql)
            
            if results_b:
                for row in results_b:
                    id_val, valor, fecha_creacion, fecha_actualizacion = row
                    print(f"  [{id_val:3d}] {valor}")
                print(f"\nTotal: {len(results_b)} records")
            else:
                print("  (No data)")
            
            print()
            print("=" * 70)
            print("View completed successfully!")
            print("=" * 70)
    
    except Exception as e:
        print(f"Error viewing database: {e}")
        print("\nMake sure:")
        print("  1. SQL Server is running")
        print("  2. Database connection is configured in .env file")
        print("  3. Tables have been created (run with --create-tables)")
        sys.exit(1)


if __name__ == "__main__":
    view_database_contents()
