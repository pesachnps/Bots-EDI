"""Data transformer module for converting EDI records to Excel format."""
import pandas as pd
from typing import List, Dict
from datetime import datetime
from src.models import InventoryRecord, WarehouseInventory


class DataTransformer:
    """Transforms parsed EDI inventory records into Excel-ready DataFrame format."""
    
    def transform(self, records: List[InventoryRecord]) -> pd.DataFrame:
        """
        Convert a list of InventoryRecord objects to a pandas DataFrame.
        
        Creates one row per warehouse location, flattening the nested warehouse data.
        Combines duplicate SKUs by summing their quantities.
        
        Args:
            records: List of InventoryRecord objects from the EDI parser
            
        Returns:
            DataFrame with columns: SKU, Description, Warehouse, Quantity, Date
        """
        all_rows = []
        
        for record in records:
            flattened_rows = self._flatten_warehouse_data(record)
            all_rows.extend(flattened_rows)
        
        # Create DataFrame with proper column names matching DSCO template
        df = pd.DataFrame(all_rows, columns=['SKU', 'Description', 'Warehouse', 'Quantity', 'Date'])
        
        # Combine duplicate SKUs by summing quantities across all warehouses
        # Group by SKU and Description only, summing all quantities
        if not df.empty:
            # First, sum quantities for each SKU
            grouped = df.groupby(['SKU', 'Description'], as_index=False).agg({
                'Quantity': 'sum',
                'Warehouse': 'first',  # Keep first warehouse for reference
                'Date': 'first'  # Keep first date for reference
            })
            # Reorder columns to match original order
            df = grouped[['SKU', 'Description', 'Warehouse', 'Quantity', 'Date']]
        
        return df
    
    def _flatten_warehouse_data(self, record: InventoryRecord) -> List[Dict]:
        """
        Flatten a single InventoryRecord into multiple rows, one per warehouse location.
        
        Args:
            record: InventoryRecord with potentially multiple warehouse locations
            
        Returns:
            List of dictionaries, each representing one row in the output
        """
        rows = []
        
        for warehouse in record.warehouses:
            row = {
                'SKU': str(record.sku),
                'Description': str(record.description),
                'Warehouse': str(warehouse.warehouse_code),
                'Quantity': int(warehouse.quantity),
                'Date': self._format_date(warehouse.date)
            }
            rows.append(row)
        
        return rows
    
    def _format_date(self, date_str: str) -> datetime:
        """
        Convert date string from YYYYMMDD format to datetime object.
        
        Args:
            date_str: Date string in YYYYMMDD format
            
        Returns:
            datetime object
        """
        try:
            return datetime.strptime(date_str, '%Y%m%d')
        except (ValueError, TypeError):
            # Return None for invalid dates, pandas will handle it
            return None
