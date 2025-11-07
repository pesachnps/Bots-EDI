# X12 Grammar Creation Guide for Bots EDI Framework

## Table of Contents
1. [Introduction to Bots X12 Grammar Structure](#1-introduction)
2. [Understanding X12 Transaction Set Anatomy](#2-x12-anatomy)
3. [Python Grammar File Structure](#3-python-structure)
4. [Segment Definition Format](#4-segment-definitions)
5. [Loop and Hierarchical Level Implementation](#5-loops-and-levels)
6. [Research Process: Where to Find X12 Specifications](#6-research-process)
7. [Step-by-Step Example: Building 855 from Scratch](#7-step-by-step-example)
8. [Common Patterns in Retail Transaction Sets](#8-common-patterns)
9. [Testing and Validation Approach](#9-testing-validation)
10. [Troubleshooting Common Grammar Errors](#10-troubleshooting)
11. [Appendix: Quick Reference for All 17 Retail Transaction Sets](#11-appendix)
12. [Glossary](#12-glossary)

---

## 1. Introduction to Bots X12 Grammar Structure {#1-introduction}

### Overview of Bots EDI Framework
Bots is an open-source EDI (Electronic Data Interchange) translator written in Python. It translates between various EDI formats including X12, EDIFACT, XML, JSON, and CSV. Grammar files define the structure and rules for parsing and generating EDI documents.

### Purpose of Grammar Files
Grammar files in Bots serve as:
- **Structure definitions** that describe the hierarchical organization of segments
- **Validation rules** that specify which segments are mandatory or optional
- **Parsing instructions** for the Bots engine to correctly interpret EDI files
- **Generation templates** for creating outbound EDI documents

### File Naming Conventions
X12 grammar files follow this pattern: `[transaction_set][version].py`

Examples:
- `850004010.py` - Purchase Order for version 004010
- `810004010.py` - Invoice for version 004010  
- `855004010.py` - Purchase Order Acknowledgment for version 004010

---

## 2. Understanding X12 Transaction Set Anatomy {#2-x12-anatomy}

### X12 Document Hierarchy

```
Interchange (ISA/IEA)                    ← Envelope level
│
├── Functional Group (GS/GE)             ← Group level
│   │
│   ├── Transaction Set (ST/SE)          ← Transaction level
│   │   │
│   │   ├── Beginning Segment            ← Transaction-specific segments
│   │   ├── Header Segments
│   │   ├── Detail Segments (loops)
│   │   ├── Summary Segments
│   │   └── SE (Transaction Set Trailer)
│   │
│   └── GE (Functional Group Trailer)
│
└── IEA (Interchange Control Trailer)
```

### Segment Descriptions

**ISA (Interchange Control Header)** - Envelope level
- Contains sender/receiver IDs, control numbers
- Not defined in transaction-specific grammars (handled by envelope.py)

**GS (Functional Group Header)** - Group level
- Groups multiple transaction sets of the same type
- Functional group code identifies transaction family (e.g., 'PO' for purchase orders)

**ST (Transaction Set Header)** - Transaction level
- Marks the beginning of a transaction set
- Contains transaction set identifier (850, 810, etc.) and control number

**Transaction-Specific Segments**
- BEG, BAK, BIG, BSN, etc. - Beginning segments that identify the transaction purpose
- Detail segments - REF, DTM, N1, PO1, IT1, etc.
- Summary segments - CTT (transaction totals), TDS (total monetary value)

**SE (Transaction Set Trailer)** - Transaction level
- Marks the end of a transaction set
- Contains segment count and control number

---

## 3. Python Grammar File Structure {#3-python-structure}

### Basic Template

```python
from bots.botsconfig import *
from .records004010 import recorddefs

syntax = {
    'version': '00401',  # ISA version
    'functionalgroup': 'XX',  # Functional group code
}

structure = [
{ID: 'ST', MIN: 1, MAX: 1, LEVEL: [
    # Segment definitions here
    {ID: 'SE', MIN: 1, MAX: 1},
]},
]
```

### Import Statements

**`from bots.botsconfig import *`**
- Imports Bots framework constants (ID, MIN, MAX, LEVEL, etc.)
- Required in all grammar files

**`from .records004010 import recorddefs`**
- Imports segment definitions (field structures) for version 004010
- The `.` indicates relative import from same directory
- Different versions have different recorddefs files (records004010.py, records005010.py, etc.)

### Syntax Dictionary

The `syntax` dictionary contains metadata about the transaction set:

```python
syntax = {
    'version': '00401',  # ISA version to send (004010 format)
    'functionalgroup': 'PO',  # Functional group code
}
```

Common functional group codes for retail:
- `PO` - Purchase Order (850)
- `PR` - Purchase Order Acknowledgment (855)
- `PC` - Purchase Order Change (860)
- `PA` - Purchase Order Change Acknowledgment (865)
- `SH` - Ship Notice/Manifest (856)
- `IN` - Invoice (810)
- `RA` - Remittance Advice (820)
- `IB` - Inventory/Product Activity (846, 852)
- `SM` - Shipping/Transportation (753, 754)
- `WA` - Warehouse (940, 943, 944, 945, 947)
- `FA` - Functional Acknowledgment (997)

### Structure Array

The `structure` array defines the hierarchical organization of segments:

```python
structure = [
{ID: 'ST', MIN: 1, MAX: 1, LEVEL: [
    {ID: 'BEG', MIN: 1, MAX: 1},
    {ID: 'REF', MIN: 0, MAX: 99999},
    {ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
        {ID: 'N2', MIN: 0, MAX: 2},
        {ID: 'N3', MIN: 0, MAX: 2},
    ]},
    {ID: 'SE', MIN: 1, MAX: 1},
]},
]
```

---

## 4. Segment Definition Format {#4-segment-definitions}

### Field Descriptions

**ID** - Segment Identifier
- 2-3 character code identifying the segment type
- Examples: `'ST'`, `'BEG'`, `'N1'`, `'PO1'`

**MIN** - Minimum Occurrences
- `0` = Optional segment
- `1` or higher = Mandatory segment (must appear at least MIN times)

**MAX** - Maximum Occurrences
- `1` = Segment can appear only once
- `99999` = Effectively unlimited occurrences
- Specific number = Exact maximum allowed

**LEVEL** - Hierarchical Nesting
- Contains child segments that belong to this parent segment
- Creates loops and hierarchical relationships
- Empty list `[]` or omitted if segment has no children

### Examples

**Mandatory segment (appears exactly once)**
```python
{ID: 'BEG', MIN: 1, MAX: 1}
```

**Optional segment (may or may not appear)**
```python
{ID: 'CUR', MIN: 0, MAX: 1}
```

**Repeating segment (can appear multiple times)**
```python
{ID: 'REF', MIN: 0, MAX: 99999}
```

**Segment with child segments (loop)**
```python
{ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
    {ID: 'N2', MIN: 0, MAX: 2},   # Additional name information
    {ID: 'N3', MIN: 0, MAX: 2},   # Address information
    {ID: 'N4', MIN: 0, MAX: 1},   # Geographic location
    {ID: 'REF', MIN: 0, MAX: 12}, # Reference numbers
]},
```

---

## 5. Loop and Hierarchical Level Implementation {#5-loops-and-levels}

### What is a Loop?

In X12, a loop is a group of segments that repeat together as a unit. The parent segment identifies the loop, and child segments provide additional details.

### Simple Loop Example: N1 (Name/Address)

The N1 loop represents a trading partner (buyer, seller, ship-to, etc.):

```python
{ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
    {ID: 'N2', MIN: 0, MAX: 2},  # Additional name info
    {ID: 'N3', MIN: 0, MAX: 2},  # Street address
    {ID: 'N4', MIN: 0, MAX: 1},  # City/State/ZIP
    {ID: 'REF', MIN: 0, MAX: 12}, # Reference IDs
    {ID: 'PER', MIN: 0, MAX: 3},  # Contact person
]},
```

This loop can repeat up to 200 times, allowing multiple trading partners to be identified.

### Complex Hierarchy Example: 856 (Ship Notice)

The 856 uses HL (Hierarchical Level) segments to create nested relationships:

```python
{ID: 'HL', MIN: 1, MAX: 200000, LEVEL: [
    # Item details
    {ID: 'LIN', MIN: 0, MAX: 1},  # Item identification
    {ID: 'SN1', MIN: 0, MAX: 1},  # Item detail
    {ID: 'PID', MIN: 0, MAX: 200}, # Product description
    
    # Party identification
    {ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
        {ID: 'N2', MIN: 0, MAX: 2},
        {ID: 'N3', MIN: 0, MAX: 2},
        {ID: 'N4', MIN: 0, MAX: 1},
    ]},
]},
```

The HL segment creates a hierarchy:
- Shipment level (top)
  - Order level
    - Pack level
      - Item level (bottom)

### Nested Loop Example: Item with Pricing

```python
{ID: 'PO1', MIN: 1, MAX: 100000, LEVEL: [
    {ID: 'PID', MIN: 0, MAX: 1000, LEVEL: [
        {ID: 'MEA', MIN: 0, MAX: 10},  # Measurements within product description
    ]},
    {ID: 'CTP', MIN: 0, MAX: 25},  # Pricing information
    {ID: 'SAC', MIN: 0, MAX: 25, LEVEL: [
        {ID: 'CUR', MIN: 0, MAX: 1},  # Currency within charge
    ]},
]},
```

---

## 6. Research Process: Where to Find X12 Specifications {#6-research-process}

### Official X12 Resources

**X12.org** (https://x12.org)
- Official standards organization
- Requires paid membership for full documentation
- Most authoritative source

**Washington Publishing Company (WPC)** (https://www.wpc-edi.com)
- Sells X12 implementation guides
- Detailed segment-by-segment documentation
- Includes examples and business context

### Free Resources

**X12Parser.com** (https://www.x12parser.com)
- Free reference for segment structures
- Basic transaction set outlines
- No membership required

**EDI Academy** (https://ediacademy.com)
- Tutorials and guides
- Basic X12 concepts
- Free introductory materials

**VICS (Voluntary Interindustry Commerce Standards)**
- Retail-specific X12 guidelines
- Available through GS1 US
- Focuses on retail supply chain

### Using Existing Grammar Files

The best resource is often existing grammar files in the Bots installation:
- `env/default/usersys/grammars/x12/` directory
- Examine similar transaction sets
- Copy structure patterns
- Adapt to your specific needs

### Implementation Guides vs. Standards

**Transaction Set Standards**
- Define all possible segments
- Very comprehensive and complex
- May include segments rarely used

**Implementation Guides**
- Subset of full standard
- Industry-specific or company-specific
- Practical and focused
- Often better for creating grammars

---

## 7. Step-by-Step Example: Building 855 from Scratch {#7-step-by-step-example}

### Step 1: Research

Locate the 855 specification:
- 855 = Purchase Order Acknowledgment
- Used to confirm receipt and acceptance of a purchase order
- Functional group code: `PR`

### Step 2: Identify Key Segments

From the specification:
- **ST** - Transaction Set Header (mandatory)
- **BAK** - Beginning Segment for Purchase Order Acknowledgment (mandatory)
- **REF** - Reference Identification (optional, repeating)
- **DTM** - Date/Time Reference (optional)
- **N1** - Name/Address loop (optional, repeating)
- **ACK** - Line Item Acknowledgment loop (optional, repeating)
- **CTT** - Transaction Totals (optional)
- **SE** - Transaction Set Trailer (mandatory)

### Step 3: Create Basic Structure

```python
from bots.botsconfig import *
from .records004010 import recorddefs

syntax = {
    'version': '00401',
    'functionalgroup': 'PR',
}

structure = [
{ID: 'ST', MIN: 1, MAX: 1, LEVEL: [
    {ID: 'BAK', MIN: 1, MAX: 1},
    # More segments to add
    {ID: 'SE', MIN: 1, MAX: 1},
]},
]
```

### Step 4: Add Header Segments

```python
structure = [
{ID: 'ST', MIN: 1, MAX: 1, LEVEL: [
    {ID: 'BAK', MIN: 1, MAX: 1},
    {ID: 'CUR', MIN: 0, MAX: 1},
    {ID: 'REF', MIN: 0, MAX: 99999},
    {ID: 'PER', MIN: 0, MAX: 3},
    {ID: 'DTM', MIN: 0, MAX: 10},
    # More to add
    {ID: 'SE', MIN: 1, MAX: 1},
]},
]
```

### Step 5: Add N1 Loop

```python
{ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
    {ID: 'N2', MIN: 0, MAX: 2},
    {ID: 'N3', MIN: 0, MAX: 2},
    {ID: 'N4', MIN: 0, MAX: 1},
    {ID: 'REF', MIN: 0, MAX: 12},
    {ID: 'PER', MIN: 0, MAX: 3},
]},
```

### Step 6: Add ACK Loop (Item Acknowledgment)

```python
{ID: 'ACK', MIN: 0, MAX: 100000, LEVEL: [
    {ID: 'DTM', MIN: 0, MAX: 10},
    {ID: 'PID', MIN: 0, MAX: 1000},
    {ID: 'MEA', MIN: 0, MAX: 40},
    {ID: 'REF', MIN: 0, MAX: 99999},
    # Nested N1 loop for line-level parties
    {ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
        {ID: 'N2', MIN: 0, MAX: 2},
        {ID: 'N3', MIN: 0, MAX: 2},
        {ID: 'N4', MIN: 0, MAX: 1},
    ]},
]},
```

### Step 7: Add Comments

```python
{ID: 'ACK', MIN: 0, MAX: 100000, LEVEL: [
    # Date/Time Reference - up to 10
    {ID: 'DTM', MIN: 0, MAX: 10},
    # Product/Item Description - up to 1000
    {ID: 'PID', MIN: 0, MAX: 1000},
    # Measurements - up to 40
    {ID: 'MEA', MIN: 0, MAX: 40},
]},
```

### Step 8: Final Review

Check:
- ✅ All mandatory segments present (ST, BAK, SE)
- ✅ MIN/MAX values match specification
- ✅ LEVEL nesting is correct
- ✅ Functional group code is correct
- ✅ Comments document segment purposes

---

## 8. Common Patterns in Retail Transaction Sets {#8-common-patterns}

### Purchase Order Family (850, 855, 860, 865)

**Common header segments:**
- Currency (CUR)
- Reference (REF)
- Contact (PER)
- Terms (ITD)
- Pricing (CTP)

**Common loops:**
- N1 - Trading partners (buyer, seller, ship-to, bill-to)
- PO1/ACK/POC - Line items

**Pattern:**
```python
Header segments
├── N1 loop (trading partners)
└── Item loop (PO1, ACK, or POC)
    └── Line-level details
```

### Shipping Family (753, 754, 856, 940, 945)

**Common segments:**
- Shipment identification (BSN, W05, W06)
- Dates (DTM, G62)
- Carrier details (TD1, TD3, TD4, TD5)
- Marks and numbers (MAN)

**856 uses hierarchical levels (HL):**
```python
HL (Shipment)
└── HL (Order)
    └── HL (Pack)
        └── HL (Item)
```

### Warehouse Family (940, 943, 944, 945, 947)

**Common segments:**
- Warehouse identification (W05, W06, W13, W17)
- Item details (W01)
- Quantities (W76, W20)
- Line item (LX)

**Pattern:**
```python
Warehouse header (W05, W06, etc.)
├── Reference loops (N9)
├── Party identification (N1)
└── Item detail loop (W01, LX)
```

### Inventory Family (846, 852)

**Common segments:**
- Beginning segment (BIA, XPO)
- Line item identification (LIN)
- Quantities (QTY)
- Dates (DTM)

**Pattern:**
```python
Header
├── N1 loop (locations)
└── LIN loop (items)
    ├── QTY (quantities)
    └── PID (descriptions)
```

### Financial Family (810, 820)

**810 (Invoice) pattern:**
```python
BIG (beginning)
├── N1 loop (parties)
└── IT1 loop (items)
    ├── PID, SAC, TXI
    └── TDS (totals)
```

**820 (Payment) pattern:**
```python
BPR (payment)
├── TRN (trace)
├── REF (references)
└── RMR loop (remittance detail)
```

### Common Segment Groups

**Name/Address (N1 loop)**
```python
{ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
    {ID: 'N2', MIN: 0, MAX: 2},   # Additional name
    {ID: 'N3', MIN: 0, MAX: 2},   # Address
    {ID: 'N4', MIN: 0, MAX: 1},   # City/State/ZIP
    {ID: 'REF', MIN: 0, MAX: 12}, # IDs
    {ID: 'PER', MIN: 0, MAX: 3},  # Contacts
]},
```

**Date/Time References**
```python
{ID: 'DTM', MIN: 0, MAX: 10}  # Flexible date segment
```

**Extended References**
```python
{ID: 'N9', MIN: 0, MAX: 1000, LEVEL: [
    {ID: 'DTM', MIN: 0, MAX: 99999},
    {ID: 'MSG', MIN: 0, MAX: 1000},
]},
```

---

## 9. Testing and Validation Approach {#9-testing-validation}

### Obtaining Sample X12 Files

**Sources:**
1. **Trading partners** - Request sample files
2. **EDI software vendors** - Often provide test files
3. **Online EDI validators** - May have examples
4. **X12 documentation** - Sometimes includes samples

### Validating Grammar Syntax

**Python syntax check:**
```bash
python -m py_compile env/default/usersys/grammars/x12/855004010.py
```

If no errors, the grammar has valid Python syntax.

### Testing with Bots Engine

From the `env/default/` directory:

```bash
# Test parsing an inbound file
bots-engine.py -c config -r

# Test with specific route
bots-engine.py -c config -r --route=test_route
```

### Validation Checklist

- [ ] Python syntax is valid (no compilation errors)
- [ ] All mandatory segments have MIN: 1 or higher
- [ ] SE segment is last in ST LEVEL
- [ ] LEVEL arrays are properly nested
- [ ] MAX values are reasonable
- [ ] Functional group code matches transaction type
- [ ] recorddefs import matches version

### Testing Strategy

1. **Start simple** - Test with minimal valid transaction
2. **Add complexity** - Gradually add optional segments
3. **Test loops** - Verify repeating segments work
4. **Test nesting** - Check hierarchical relationships
5. **Test edge cases** - Maximum occurrences, optional segments

---

## 10. Troubleshooting Common Grammar Errors {#10-troubleshooting}

### "Segment not found" Error

**Cause:** Segment ID in grammar doesn't exist in recorddefs

**Solution:**
- Check segment ID spelling
- Verify you're using correct recorddefs version
- Check if segment exists in `records004010.py`

### MIN/MAX Violations

**Error:** `Segment X appears Y times but MIN is Z`

**Solution:**
- Adjust MIN value if segment should be optional
- Check X12 spec to verify requirements
- Ensure test data matches grammar rules

### LEVEL Nesting Problems

**Symptom:** Segments appear in wrong order or not recognized

**Cause:** Incorrect LEVEL nesting

**Solution:**
```python
# Wrong - N2 outside N1's LEVEL
{ID: 'N1', MIN: 0, MAX: 200},
{ID: 'N2', MIN: 0, MAX: 2},

# Correct - N2 inside N1's LEVEL
{ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
    {ID: 'N2', MIN: 0, MAX: 2},
]},
```

### Missing Mandatory Segments

**Error:** `Mandatory segment X not found`

**Solution:**
- Add segment to grammar with MIN: 1
- Check X12 spec - segment may be mandatory
- Verify test file contains the segment

### Import Errors

**Error:** `ImportError: cannot import name 'recorddefs'`

**Solution:**
```python
# Wrong
from records004010 import recorddefs

# Correct - note the dot
from .records004010 import recorddefs
```

### RecordDefs Version Mismatch

**Symptom:** Some segments not recognized even though they exist

**Cause:** Using wrong recorddefs version

**Solution:**
- 004010 files should import from `records004010`
- 005010 files should import from `records005010`
- Match grammar version to recorddefs version

---

## 11. Appendix: Quick Reference for All 17 Retail Transaction Sets {#11-appendix}

| Transaction | Name | Functional Group | Status | Primary Use |
|-------------|------|------------------|--------|-------------|
| **850** | Purchase Order | PO | Production-Ready | Order products from supplier |
| **855** | PO Acknowledgment | PR | Production-Ready | Confirm receipt/acceptance of PO |
| **856** | Ship Notice/Manifest | SH | Production-Ready | Advance ship notice (ASN) |
| **810** | Invoice | IN | Production-Ready | Bill for products/services |
| **997** | Functional Acknowledgment | FA | Production-Ready | Confirm receipt of EDI transmission |
| **860** | Purchase Order Change | PC | Skeleton | Modify existing PO |
| **865** | PO Change Acknowledgment | PA | Skeleton | Confirm PO change |
| **820** | Payment Order/Remittance | RA | Skeleton | Payment advice |
| **846** | Inventory Inquiry/Advice | IB | Skeleton | Inventory levels/status |
| **852** | Product Activity Data | IB | Skeleton | Sales/inventory activity |
| **753** | Request for Routing Instructions | SM | Skeleton | Request shipping routing |
| **754** | Routing Instructions | SM | Skeleton | Provide shipping routing |
| **940** | Warehouse Shipping Order | WA | Skeleton | Instruction to ship from warehouse |
| **943** | Warehouse Stock Transfer Shipment | WA | Skeleton | Notify of warehouse transfer shipment |
| **944** | Warehouse Stock Transfer Receipt | WA | Skeleton | Notify of warehouse transfer receipt |
| **945** | Warehouse Shipping Advice | WA | Skeleton | Notify of warehouse shipment |
| **947** | Warehouse Inventory Adjustment | WA | Skeleton | Notify of inventory adjustments |

### Key Mandatory Segments by Transaction

**850 (Purchase Order)**
- ST, BEG, PO1, SE

**855 (PO Acknowledgment)**
- ST, BAK, ACK, SE

**856 (Ship Notice)**
- ST, BSN, HL, SE

**810 (Invoice)**
- ST, BIG, IT1, TDS, SE

**997 (Functional Acknowledgment)**
- ST, AK1, AK9, SE

---

## 12. Glossary {#12-glossary}

**ASN** - Advance Ship Notice (856 transaction)

**Bots** - Open-source EDI translator framework

**EDI** - Electronic Data Interchange

**Envelope** - ISA/IEA segments that wrap functional groups

**Functional Group** - GS/GE segments that group transaction sets

**Grammar** - Python file defining transaction set structure

**HL** - Hierarchical Level segment (used in 856)

**Implementation Guide** - Industry/company-specific subset of X12 standard

**Loop** - Repeating group of related segments

**LEVEL** - Python list containing child segments

**MAX** - Maximum occurrences of a segment

**MIN** - Minimum occurrences of a segment

**recorddefs** - Segment field definitions for a specific X12 version

**Segment** - Single line/record in an X12 document (e.g., N1, PO1)

**ST/SE** - Transaction Set Header/Trailer

**Transaction Set** - Complete business document (PO, Invoice, etc.)

**VICS** - Voluntary Interindustry Commerce Standards (retail-specific)

**X12** - ANSI ASC X12 EDI standard

---

## External Resources

### Specifications
- [X12.org](https://x12.org) - Official X12 standards
- [WPC-EDI.com](https://www.wpc-edi.com) - Implementation guides
- [GS1 US](https://www.gs1us.org) - VICS/retail standards

### Learning
- [EDI Academy](https://ediacademy.com) - EDI training
- [X12Parser.com](https://www.x12parser.com) - Free segment reference

### Tools
- [EDI Validator](https://www.edival idator.com) - Online validation
- [Sublime Text](https://www.sublimetext.com) with X12 syntax highlighting
- [Visual Studio Code](https://code.visualstudio.com) with EDI extensions

---

## Next Steps

### For Skeleton Files
1. Review X12 004010 documentation for specific transaction
2. Identify all segments from specification
3. Determine MIN/MAX values
4. Map hierarchical relationships (loops)
5. Add segments to skeleton structure
6. Test with sample EDI files
7. Refine based on validation results

### Recommended Priority Order
1. **860** (PO Change) - Complements 850
2. **865** (PO Change Ack) - Complements 855
3. **846** (Inventory) - Common retail need
4. **940** (Warehouse Shipping Order) - High-volume warehouse operations
5. **945** (Warehouse Shipping Advice) - Pairs with 940
6. **820** (Payment/Remittance) - Financial transactions
7. **852** (Product Activity) - Sales reporting
8. **753/754** (Routing) - Shipping coordination
9. **943/944/947** (Warehouse transfers/adjustments) - Advanced warehouse operations

---

*Document Version: 1.0*  
*Created: 2025-11-06*  
*For: Bots EDI Framework X12 004010 Retail Transaction Sets*
