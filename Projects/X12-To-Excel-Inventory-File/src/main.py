"""Main application module for EDI to Excel conversion."""
import argparse
import sys
import logging
from pathlib import Path
from src.parser import EDIParser
from src.transformer import DataTransformer
from src.writer import ExcelWriter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_edi_to_excel(input_file: str, output_file: str = None) -> bool:
    """
    Convert EDI 846 inventory file to Excel format.
    
    Orchestrates the parsing, transformation, and writing process.
    
    Args:
        input_file: Path to the input EDI file
        output_file: Path to the output Excel file (optional, auto-generated if not provided)
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        logger.info("=" * 60)
        logger.info(f"Starting EDI to Excel conversion")
        logger.info(f"Input file: {input_file}")
        logger.info("=" * 60)
        
        # Step 1: Parse EDI file
        logger.info("Step 1: Parsing EDI file...")
        parser = EDIParser()
        records = parser.parse_file(input_file)
        
        if not records:
            logger.error("No records found in EDI file")
            _print_summary(parser, 0, False)
            return False
        
        logger.info(f"✓ Parsed {len(records)} inventory records")
        
        # Step 2: Transform to DataFrame
        logger.info("Step 2: Transforming data...")
        transformer = DataTransformer()
        dataframe = transformer.transform(records)
        
        logger.info(f"✓ Transformed to {len(dataframe)} rows")
        
        # Step 3: Generate output filename if not provided
        if output_file is None:
            input_path = Path(input_file)
            base_name = input_path.stem
            output_file = ExcelWriter.generate_output_filename(
                base_name=base_name,
                output_dir="output"
            )
        
        # Step 4: Write to Excel
        logger.info("Step 3: Writing Excel file...")
        writer = ExcelWriter()
        writer.write(dataframe, output_file)
        
        logger.info(f"✓ Excel file created: {output_file}")
        
        # Print summary
        _print_summary(parser, len(dataframe), True)
        
        return True
        
    except FileNotFoundError as e:
        logger.error(f"✗ File not found: {e}")
        logger.error("Please check that the input file path is correct")
        return False
    except PermissionError as e:
        logger.error(f"✗ Permission denied: {e}")
        logger.error("Please check file permissions")
        return False
    except Exception as e:
        logger.error(f"✗ Conversion failed: {e}")
        logger.error("An unexpected error occurred during conversion")
        return False


def _print_summary(parser: EDIParser, rows_written: int, success: bool) -> None:
    """
    Print summary statistics of the conversion process.
    
    Args:
        parser: EDIParser instance with parsing statistics
        rows_written: Number of rows written to Excel
        success: Whether conversion was successful
    """
    logger.info("=" * 60)
    logger.info("CONVERSION SUMMARY")
    logger.info("=" * 60)
    
    summary = parser.get_summary()
    
    logger.info(f"Records processed: {summary['processed']}")
    logger.info(f"Errors encountered: {summary['errors']}")
    logger.info(f"Warnings: {summary['warnings']}")
    
    if success:
        logger.info(f"Excel rows written: {rows_written}")
        logger.info("Status: ✓ SUCCESS")
    else:
        logger.info("Status: ✗ FAILED")
    
    logger.info("=" * 60)


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Convert EDI 846 inventory files to Excel format'
    )
    parser.add_argument(
        'input_file',
        help='Path to the input EDI file'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='Path to the output Excel file (optional, auto-generated if not provided)'
    )
    
    args = parser.parse_args()
    
    # Perform conversion
    success = convert_edi_to_excel(args.input_file, args.output_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
