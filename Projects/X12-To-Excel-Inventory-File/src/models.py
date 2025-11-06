"""Data models for EDI inventory records."""
from dataclasses import dataclass
from typing import List


@dataclass
class WarehouseInventory:
    """Represents inventory at a specific warehouse location."""
    warehouse_code: str
    quantity: int
    date: str


@dataclass
class InventoryRecord:
    """Represents a complete inventory record for a SKU."""
    sku: str
    description: str
    warehouses: List[WarehouseInventory]
