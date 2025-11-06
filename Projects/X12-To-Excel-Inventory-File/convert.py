#!/usr/bin/env python
"""Conversion script for converting rawEDI (5).txt to Excel format."""
from src.main import convert_edi_to_excel

if __name__ == '__main__':
    # Input file from workspace
    input_file = "rawEDI (5).txt"
    
    # Output will be auto-generated with timestamp in output/ directory
    # Format: rawEDI (5)_YYYYMMDD_HHMMSS.xlsx
    
    print("Converting EDI file to Excel format...")
    print(f"Input: {input_file}")
    print()
    
    success = convert_edi_to_excel(input_file)
    
    if success:
        print("\n✓ Conversion completed successfully!")
    else:
        print("\n✗ Conversion failed. Check the logs above for details.")
