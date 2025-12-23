"""
Excel file reader for lists a and b.
"""
import openpyxl
from typing import List, Tuple


class ExcelReader:
    """Read lists from Excel file."""
    
    def __init__(self, file_path: str):
        """
        Initialize Excel reader with file path.
        
        Args:
            file_path: Path to the Excel file
        """
        self.file_path = file_path
        self.workbook = None
    
    def load_workbook(self):
        """Load the Excel workbook."""
        try:
            self.workbook = openpyxl.load_workbook(self.file_path)
            print(f"Excel file loaded: {self.file_path}")
        except FileNotFoundError:
            print(f"Error: File not found - {self.file_path}")
            raise
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            raise
    
    def read_lists(self, sheet_name: str = None) -> Tuple[List, List]:
        """
        Read lists a and b from Excel file.
        Expected format:
        - Column A contains list 'a'
        - Column B contains list 'b'
        - First row may contain headers (will be skipped if they are strings)
        
        Args:
            sheet_name: Name of the sheet to read (default: first sheet)
        
        Returns:
            Tuple containing two lists: (list_a, list_b)
        """
        if not self.workbook:
            self.load_workbook()
        
        # Get the sheet
        if sheet_name:
            sheet = self.workbook[sheet_name]
        else:
            sheet = self.workbook.active
        
        list_a = []
        list_b = []
        
        # Read data from columns A and B
        for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_col=2, values_only=True), start=1):
            col_a_value, col_b_value = row
            
            # Skip header row if it contains non-numeric values
            if row_idx == 1:
                # Check if first row is a header
                if isinstance(col_a_value, str) and isinstance(col_b_value, str):
                    continue
            
            # Add values to lists if they are not None
            if col_a_value is not None:
                list_a.append(col_a_value)
            if col_b_value is not None:
                list_b.append(col_b_value)
        
        print(f"Read {len(list_a)} items from list A")
        print(f"Read {len(list_b)} items from list B")
        
        return list_a, list_b
    
    def close(self):
        """Close the workbook."""
        if self.workbook:
            self.workbook.close()
            print("Excel workbook closed.")
    
    def __enter__(self):
        """Context manager entry."""
        self.load_workbook()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
