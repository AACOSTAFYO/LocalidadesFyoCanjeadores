"""
Validation script to verify all components work correctly.
This script tests the functionality without requiring a SQL Server connection.
"""
import sys
from excel_reader import ExcelReader
from db_schema import DatabaseSchema

def test_excel_reading():
    """Test Excel reading functionality."""
    print("\n" + "=" * 70)
    print("TEST 1: Excel Reading")
    print("=" * 70)
    
    try:
        excel_file = "sample_data.xlsx"
        with ExcelReader(excel_file) as reader:
            list_a, list_b = reader.read_lists()
        
        print(f"✓ Successfully read {len(list_a)} items from Lista A")
        print(f"✓ Successfully read {len(list_b)} items from Lista B")
        
        # Display sample data
        print("\nSample from Lista A:")
        for item in list_a[:3]:
            print(f"  - {item}")
        
        print("\nSample from Lista B:")
        for item in list_b[:3]:
            print(f"  - {item}")
        
        return True, list_a, list_b
    except Exception as e:
        print(f"✗ Error reading Excel: {e}")
        return False, [], []

def test_database_schema():
    """Test database schema SQL generation."""
    print("\n" + "=" * 70)
    print("TEST 2: Database Schema SQL Generation")
    print("=" * 70)
    
    try:
        # Test schema SQL generation
        create_sql = DatabaseSchema.create_tables_sql()
        print("✓ Create tables SQL generated successfully")
        print(f"  SQL length: {len(create_sql)} characters")
        
        clear_sql = DatabaseSchema.clear_tables_sql()
        print("✓ Clear tables SQL generated successfully")
        print(f"  SQL length: {len(clear_sql)} characters")
        
        insert_a_sql = DatabaseSchema.insert_list_a_sql()
        print("✓ Insert Lista A SQL: " + insert_a_sql)
        
        insert_b_sql = DatabaseSchema.insert_list_b_sql()
        print("✓ Insert Lista B SQL: " + insert_b_sql)
        
        select_a_sql = DatabaseSchema.select_all_list_a_sql()
        print("✓ Select Lista A SQL: " + select_a_sql)
        
        select_b_sql = DatabaseSchema.select_all_list_b_sql()
        print("✓ Select Lista B SQL: " + select_b_sql)
        
        return True
    except Exception as e:
        print(f"✗ Error with database schema: {e}")
        return False

def test_sql_statements(list_a, list_b):
    """Test that SQL statements can be formatted correctly."""
    print("\n" + "=" * 70)
    print("TEST 3: SQL Statement Formatting")
    print("=" * 70)
    
    try:
        insert_a_sql = DatabaseSchema.insert_list_a_sql()
        insert_b_sql = DatabaseSchema.insert_list_b_sql()
        
        # Test formatting with sample data
        if list_a:
            sample_a = list_a[0]
            print(f"✓ Sample INSERT for Lista A: {insert_a_sql} with value '{sample_a}'")
        
        if list_b:
            sample_b = list_b[0]
            print(f"✓ Sample INSERT for Lista B: {insert_b_sql} with value '{sample_b}'")
        
        print(f"\n✓ Would insert {len(list_a)} records into ListaA")
        print(f"✓ Would insert {len(list_b)} records into ListaB")
        
        return True
    except Exception as e:
        print(f"✗ Error formatting SQL: {e}")
        return False

def test_configuration_loading():
    """Test configuration loading."""
    print("\n" + "=" * 70)
    print("TEST 4: Configuration Loading")
    print("=" * 70)
    
    try:
        from db_config import DatabaseConfig
        
        config = DatabaseConfig()
        print(f"✓ Database configuration loaded")
        print(f"  Server: {config.server}")
        print(f"  Database: {config.database}")
        print(f"  Driver: {config.driver}")
        print(f"  User: {config.username}")
        print("  Password: ****" if config.password else "  Password: (not set)")
        
        conn_string = config.get_connection_string()
        print(f"\n✓ Connection string generated ({len(conn_string)} chars)")
        
        return True
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return False

def main():
    """Run all validation tests."""
    print("\n" + "=" * 70)
    print("VALIDATION SUITE - LocalidadesFyoCanjeadores")
    print("=" * 70)
    
    results = []
    
    # Test 1: Excel Reading
    success, list_a, list_b = test_excel_reading()
    results.append(("Excel Reading", success))
    
    # Test 2: Database Schema
    success = test_database_schema()
    results.append(("Database Schema", success))
    
    # Test 3: SQL Formatting
    success = test_sql_statements(list_a, list_b)
    results.append(("SQL Formatting", success))
    
    # Test 4: Configuration
    success = test_configuration_loading()
    results.append(("Configuration", success))
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED! ✓")
        print("\nThe system is ready to use. To connect to SQL Server:")
        print("1. Configure your database connection in .env file")
        print("2. Ensure SQL Server is running and accessible")
        print("3. Run: python main.py sample_data.xlsx --create-tables")
    else:
        print("SOME TESTS FAILED! ✗")
    print("=" * 70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
