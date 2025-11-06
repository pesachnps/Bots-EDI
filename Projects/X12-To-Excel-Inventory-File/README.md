# EDI to Excel Converter

Converts EDI 846 inventory files to Excel format with DSCO template formatting.

## Features

- Parses EDI 846 inventory files
- Extracts SKU, description, warehouse, quantity, and date information
- Transforms data into Excel format with proper formatting
- Generates timestamped output files
- Comprehensive error handling and logging

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Use the provided conversion script:

```bash
python convert.py
```

This will convert `rawEDI (5).txt` to Excel format in the `output/` directory.

### Command Line

Convert any EDI file:

```bash
python -m src.main input_file.txt
```

Specify output file:

```bash
python -m src.main input_file.txt -o output_file.xlsx
```

### Programmatic Usage

```python
from src.main import convert_edi_to_excel

# Auto-generate output filename
convert_edi_to_excel("input.txt")

# Specify output filename
convert_edi_to_excel("input.txt", "output.xlsx")
```

## Output Format

The Excel file contains the following columns:
- **SKU**: Product SKU
- **Description**: Product description
- **Warehouse**: Warehouse code
- **Quantity**: Inventory quantity
- **Date**: Inventory date (YYYY-MM-DD format)

## Project Structure

```
.
├── src/
│   ├── models.py       # Data models
│   ├── parser.py       # EDI parser
│   ├── transformer.py  # Data transformer
│   ├── writer.py       # Excel writer
│   └── main.py         # Main application
├── output/             # Generated Excel files
├── convert.py          # Conversion script
└── requirements.txt    # Dependencies
```
