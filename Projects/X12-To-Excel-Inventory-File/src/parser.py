"""EDI 846 Parser module for extracting inventory data."""
import logging
from typing import List, Optional
from src.models import InventoryRecord, WarehouseInventory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_sku(lin_segment: str) -> Optional[str]:
    """Extract SKU from LIN segment.
    
    Format: LIN*{line_num}*SK*{sku}*...~
    
    Args:
        lin_segment: LIN segment string
        
    Returns:
        SKU string or None if not found
    """
    try:
        parts = lin_segment.strip().rstrip('~').split('*')
        if len(parts) >= 4 and parts[2] == 'SK':
            return parts[3]
    except Exception as e:
        logger.warning(f"Failed to extract SKU from LIN segment: {e}")
    return None


def extract_description(pid_segment: str) -> Optional[str]:
    """Extract product description from PID segment.
    
    Format: PID*F*08***{description}~
    
    Args:
        pid_segment: PID segment string
        
    Returns:
        Description string or None if not found
    """
    try:
        parts = pid_segment.strip().rstrip('~').split('*')
        if len(parts) >= 6:
            return parts[5]
    except Exception as e:
        logger.warning(f"Failed to extract description from PID segment: {e}")
    return None


def extract_quantity(qty_segment: str) -> Optional[int]:
    """Extract quantity from QTY segment.
    
    Format: QTY*33*{quantity}*EA~
    
    Args:
        qty_segment: QTY segment string
        
    Returns:
        Quantity as integer or None if not found
    """
    try:
        parts = qty_segment.strip().rstrip('~').split('*')
        if len(parts) >= 3:
            return int(parts[2])
    except Exception as e:
        logger.warning(f"Failed to extract quantity from QTY segment: {e}")
    return None


def extract_warehouse_code(ref_segment: str) -> Optional[str]:
    """Extract warehouse code from REF segment.
    
    Format: REF*WS*{warehouse_code}*{quantity}~
    
    Args:
        ref_segment: REF segment string
        
    Returns:
        Warehouse code or None if not found
    """
    try:
        parts = ref_segment.strip().rstrip('~').split('*')
        if len(parts) >= 3 and parts[1] == 'WS':
            return parts[2]
    except Exception as e:
        logger.warning(f"Failed to extract warehouse code from REF segment: {e}")
    return None


def extract_warehouse_quantity(ref_segment: str) -> Optional[int]:
    """Extract quantity from REF segment.
    
    Format: REF*WS*{warehouse_code}*{quantity}~
    
    Args:
        ref_segment: REF segment string
        
    Returns:
        Quantity as integer or None if not found
    """
    try:
        parts = ref_segment.strip().rstrip('~').split('*')
        if len(parts) >= 4 and parts[1] == 'WS':
            return int(parts[3])
    except Exception as e:
        logger.warning(f"Failed to extract quantity from REF segment: {e}")
    return None


def extract_date(dtm_segment: str) -> Optional[str]:
    """Extract date from DTM segment.
    
    Format: DTM*018*{date}***UN*{quantity}~
    
    Args:
        dtm_segment: DTM segment string
        
    Returns:
        Date string in YYYYMMDD format or None if not found
    """
    try:
        parts = dtm_segment.strip().rstrip('~').split('*')
        if len(parts) >= 3 and parts[1] == '018':
            return parts[2]
    except Exception as e:
        logger.warning(f"Failed to extract date from DTM segment: {e}")
    return None


def extract_dtm_quantity(dtm_segment: str) -> Optional[int]:
    """Extract quantity from DTM segment.
    
    Format: DTM*018*{date}***UN*{quantity}~
    
    Args:
        dtm_segment: DTM segment string
        
    Returns:
        Quantity as integer or None if not found
    """
    try:
        parts = dtm_segment.strip().rstrip('~').split('*')
        if len(parts) >= 6 and parts[1] == '018':
            return int(parts[5])
    except Exception as e:
        logger.warning(f"Failed to extract quantity from DTM segment: {e}")
    return None


class EDIParser:
    """Parser for EDI 846 inventory files."""
    
    def __init__(self):
        """Initialize the EDI parser."""
        self.records: List[InventoryRecord] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.processed_count = 0
        self.error_count = 0
        
    def parse_file(self, filepath: str) -> List[InventoryRecord]:
        """Parse an EDI 846 file and extract inventory records.
        
        Args:
            filepath: Path to the EDI file
            
        Returns:
            List of InventoryRecord objects
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        self.records = []
        self.errors = []
        self.warnings = []
        self.processed_count = 0
        self.error_count = 0
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            error_msg = f"Input file not found: {filepath}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            raise FileNotFoundError(error_msg)
        except Exception as e:
            error_msg = f"Error reading file {filepath}: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            raise
        
        current_item = None
        in_warehouse_loop = False
        warehouse_segments = []
        line_num = 0
        
        for line in lines:
            line_num += 1
            line = line.strip()
            
            if not line:
                continue
            
            try:
                # Start of new line item
                if line.startswith('LIN*'):
                    # Save previous item if exists
                    if current_item:
                        # Validate before saving
                        if self._validate_record(current_item, line_num):
                            self.records.append(current_item)
                            self.processed_count += 1
                        else:
                            self.error_count += 1
                    
                    # Start new item
                    sku = extract_sku(line)
                    if sku:
                        current_item = {
                            'sku': sku,
                            'description': '',
                            'warehouses': [],
                            'line_num': line_num
                        }
                    else:
                        warning_msg = f"Line {line_num}: Could not extract SKU from LIN segment"
                        logger.warning(warning_msg)
                        self.warnings.append(warning_msg)
                        current_item = None
                
                # Product description
                elif line.startswith('PID*') and current_item:
                    description = extract_description(line)
                    if description:
                        current_item['description'] = description
                
                # Start of warehouse reference loop
                elif line.startswith('LS*REF'):
                    in_warehouse_loop = True
                    warehouse_segments = []
                
                # End of warehouse reference loop
                elif line.startswith('LE*REF'):
                    in_warehouse_loop = False
                    # Process warehouse segments
                    if current_item:
                        warehouses = self._parse_warehouse_segments(warehouse_segments)
                        current_item['warehouses'].extend(warehouses)
                    warehouse_segments = []
                
                # Warehouse reference
                elif line.startswith('REF*WS*') and in_warehouse_loop:
                    warehouse_segments.append(('REF', line))
                
                # Date/time reference
                elif line.startswith('DTM*018*') and in_warehouse_loop:
                    warehouse_segments.append(('DTM', line))
                    
            except Exception as e:
                error_msg = f"Line {line_num}: Error processing segment: {e}"
                logger.warning(error_msg)
                self.warnings.append(error_msg)
                continue
        
        # Don't forget the last item
        if current_item:
            if self._validate_record(current_item, line_num):
                self.records.append(current_item)
                self.processed_count += 1
            else:
                self.error_count += 1
        
        # Convert to InventoryRecord objects
        inventory_records = []
        for item in self.records:
            try:
                record = InventoryRecord(
                    sku=item['sku'],
                    description=item['description'],
                    warehouses=item['warehouses']
                )
                inventory_records.append(record)
            except Exception as e:
                error_msg = f"Failed to create InventoryRecord for SKU {item.get('sku', 'unknown')}: {e}"
                logger.warning(error_msg)
                self.warnings.append(error_msg)
        
        # Log summary
        logger.info(f"Parsed {len(inventory_records)} inventory records from {filepath}")
        logger.info(f"Successfully processed: {self.processed_count} records")
        if self.error_count > 0:
            logger.warning(f"Errors encountered: {self.error_count} records")
        if self.warnings:
            logger.warning(f"Total warnings: {len(self.warnings)}")
        
        return inventory_records
    
    def _validate_record(self, record: dict, line_num: int) -> bool:
        """Validate that a record has all required fields.
        
        Args:
            record: Dictionary containing record data
            line_num: Line number for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        if not record.get('sku'):
            error_msg = f"Line {line_num}: Missing required SKU"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False
        
        if not record.get('description'):
            warning_msg = f"Line {line_num}: Missing description for SKU {record['sku']}"
            logger.warning(warning_msg)
            self.warnings.append(warning_msg)
        
        if not record.get('warehouses'):
            warning_msg = f"Line {line_num}: No warehouse data for SKU {record['sku']}"
            logger.warning(warning_msg)
            self.warnings.append(warning_msg)
        
        return True
    
    def get_summary(self) -> dict:
        """Get a summary of the parsing results.
        
        Returns:
            Dictionary with parsing statistics
        """
        return {
            'processed': self.processed_count,
            'errors': self.error_count,
            'warnings': len(self.warnings),
            'total_records': len(self.records)
        }
    
    def _parse_warehouse_segments(self, segments: List[tuple]) -> List[WarehouseInventory]:
        """Parse warehouse reference segments into WarehouseInventory objects.
        
        The segments come in pairs: REF (warehouse code) followed by DTM (date).
        
        Args:
            segments: List of (type, segment) tuples
            
        Returns:
            List of WarehouseInventory objects
        """
        warehouses = []
        
        i = 0
        while i < len(segments):
            seg_type, segment = segments[i]
            
            if seg_type == 'REF':
                warehouse_code = extract_warehouse_code(segment)
                quantity = extract_warehouse_quantity(segment)
                
                # Look for corresponding DTM segment
                date = None
                if i + 1 < len(segments) and segments[i + 1][0] == 'DTM':
                    date = extract_date(segments[i + 1][1])
                    i += 1  # Skip the DTM segment
                
                if warehouse_code and quantity is not None:
                    warehouse = WarehouseInventory(
                        warehouse_code=warehouse_code,
                        quantity=quantity,
                        date=date or ''
                    )
                    warehouses.append(warehouse)
            
            i += 1
        
        return warehouses
