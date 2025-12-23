"""
Main script to read lists from Excel and persist them to SQL Server.
"""
import sys
import os
from excel_reader import ExcelReader
from db_config import DatabaseConnection
from db_schema import DatabaseSchema
from data_persistence import DataPersistence


def print_usage():
    """Print usage instructions."""
    print("\nUsage:")
    print("  python main.py <excel_file_path> [options]")
    print("\nOptions:")
    print("  --sheet <name>       Specify sheet name (default: first sheet)")
    print("  --keep-existing      Keep existing data in database (default: clear)")
    print("  --create-tables      Force create tables before importing")
    print("\nExample:")
    print("  python main.py datos.xlsx")
    print("  python main.py datos.xlsx --sheet Hoja1 --keep-existing")
    print()


def main():
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Error: Excel file path is required.")
        print_usage()
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"Error: File not found - {excel_file}")
        sys.exit(1)
    
    # Parse options
    sheet_name = None
    clear_existing = True
    create_tables = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--sheet' and i + 1 < len(sys.argv):
            sheet_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--keep-existing':
            clear_existing = False
            i += 1
        elif sys.argv[i] == '--create-tables':
            create_tables = True
            i += 1
        else:
            print(f"Warning: Unknown option '{sys.argv[i]}'")
            i += 1
    
    print("=" * 60)
    print("Excel to SQL Server - LocalidadesFyoCanjeadores")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Read lists from Excel
        print("Step 1: Reading data from Excel...")
        print(f"File: {excel_file}")
        if sheet_name:
            print(f"Sheet: {sheet_name}")
        print()
        
        with ExcelReader(excel_file) as reader:
            list_a, list_b = reader.read_lists(sheet_name)
        
        if not list_a and not list_b:
            print("Warning: No data found in Excel file.")
            sys.exit(0)
        
        print()
        
        # Step 2: Connect to database
        print("Step 2: Connecting to SQL Server...")
        print()
        
        with DatabaseConnection() as db_conn:
            persistence = DataPersistence(db_conn)
            
            # Step 3: Create tables if needed
            if create_tables:
                print("Step 3: Creating database tables...")
                persistence.create_tables()
                print()
            
            # Step 4: Save data
            print(f"Step {4 if create_tables else 3}: Saving data to database...")
            print(f"Clear existing data: {'Yes' if clear_existing else 'No'}")
            print()
            
            persistence.save_lists(list_a, list_b, clear_existing)
            
            print()
            
            # Step 5: Verify
            print(f"Step {5 if create_tables else 4}: Verification...")
            persistence.verify_data()
        
        print()
        print("=" * 60)
        print("Process completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
