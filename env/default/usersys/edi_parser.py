"""
EDI Parser Utilities
Parse and generate EDI files with metadata extraction
"""

import os
import re
from datetime import datetime
from django.core.exceptions import ValidationError


class EDIParser:
    """Utility class for parsing EDI files"""
    
    # Common EDI document types
    DOCUMENT_TYPES = {
        '850': 'Purchase Order',
        '810': 'Invoice',
        '856': 'Advance Ship Notice',
        '997': 'Functional Acknowledgment',
        '855': 'Purchase Order Acknowledgment',
        '860': 'Purchase Order Change',
        'ORDERS': 'Purchase Order (EDIFACT)',
        'INVOIC': 'Invoice (EDIFACT)',
        'DESADV': 'Despatch Advice (EDIFACT)',
        'CONTRL': 'Control (EDIFACT)',
    }
    
    def __init__(self):
        """Initialize the EDI parser"""
        pass
    
    def detect_format(self, content):
        """
        Detect EDI format from content
        
        Args:
            content: EDI file content (string)
        
        Returns:
            Format name ('X12', 'EDIFACT', 'XML', 'JSON', 'CSV', 'UNKNOWN')
        """
        if not content or not isinstance(content, str):
            return 'UNKNOWN'
        
        # Remove leading/trailing whitespace
        content = content.strip()
        
        # Check for X12 format (starts with ISA)
        if content.startswith('ISA'):
            return 'X12'
        
        # Check for EDIFACT format (starts with UNB or UNA)
        if content.startswith('UNB') or content.startswith('UNA'):
            return 'EDIFACT'
        
        # Check for XML format
        if content.startswith('<?xml') or content.startswith('<'):
            return 'XML'
        
        # Check for JSON format
        if content.startswith('{') or content.startswith('['):
            return 'JSON'
        
        # Check for CSV format (simple heuristic)
        lines = content.split('\n')
        if len(lines) > 1 and ',' in lines[0]:
            return 'CSV'
        
        return 'UNKNOWN'
    
    def parse_x12(self, content):
        """
        Parse X12 EDI format
        
        Args:
            content: X12 EDI content
        
        Returns:
            Dictionary with parsed metadata
        """
        metadata = {
            'format': 'X12',
            'parsed_at': datetime.now().isoformat(),
            'segments': []
        }
        
        try:
            # X12 uses specific delimiters
            # ISA segment defines the delimiters
            if not content.startswith('ISA'):
                raise ValidationError("Invalid X12 format: missing ISA segment")
            
            # Extract element separator (position 3 in ISA)
            element_sep = content[3] if len(content) > 3 else '*'
            
            # Extract segment terminator (usually ~)
            segment_term = '~'
            if '~' in content:
                segment_term = '~'
            elif '\n' in content:
                segment_term = '\n'
            
            # Split into segments
            segments = content.split(segment_term)
            
            for segment in segments:
                if not segment.strip():
                    continue
                
                # Split segment into elements
                elements = segment.split(element_sep)
                segment_id = elements[0] if elements else ''
                
                # Parse ISA (Interchange Control Header)
                if segment_id == 'ISA':
                    if len(elements) >= 16:
                        metadata['sender_id'] = elements[6].strip()
                        metadata['receiver_id'] = elements[8].strip()
                        metadata['interchange_date'] = elements[9].strip()
                        metadata['interchange_time'] = elements[10].strip()
                        metadata['control_number'] = elements[13].strip()
                
                # Parse GS (Functional Group Header)
                elif segment_id == 'GS':
                    if len(elements) >= 8:
                        metadata['functional_id'] = elements[1].strip()
                        metadata['sender_code'] = elements[2].strip()
                        metadata['receiver_code'] = elements[3].strip()
                        metadata['group_date'] = elements[4].strip()
                        metadata['group_time'] = elements[5].strip()
                
                # Parse ST (Transaction Set Header)
                elif segment_id == 'ST':
                    if len(elements) >= 2:
                        doc_type_code = elements[1].strip()
                        metadata['document_type_code'] = doc_type_code
                        metadata['document_type'] = self.DOCUMENT_TYPES.get(
                            doc_type_code, 
                            f'Unknown ({doc_type_code})'
                        )
                        if len(elements) >= 3:
                            metadata['transaction_control'] = elements[2].strip()
                
                # Parse BEG (Beginning Segment for PO)
                elif segment_id == 'BEG':
                    if len(elements) >= 4:
                        metadata['po_number'] = elements[3].strip()
                        if len(elements) >= 5:
                            metadata['po_date'] = elements[4].strip()
                
                # Parse N1 (Name segment for partner info)
                elif segment_id == 'N1':
                    if len(elements) >= 3:
                        qualifier = elements[1].strip()
                        name = elements[2].strip()
                        if qualifier == 'BY':  # Buying Party
                            metadata['buyer_name'] = name
                        elif qualifier == 'SE':  # Selling Party
                            metadata['seller_name'] = name
                        elif qualifier == 'ST':  # Ship To
                            metadata['ship_to_name'] = name
                
                metadata['segments'].append(segment_id)
            
            # Determine partner name (prefer buyer, then seller)
            if 'buyer_name' in metadata:
                metadata['partner_name'] = metadata['buyer_name']
            elif 'seller_name' in metadata:
                metadata['partner_name'] = metadata['seller_name']
            elif 'sender_id' in metadata:
                metadata['partner_name'] = metadata['sender_id']
            
        except Exception as e:
            metadata['parse_error'] = str(e)
        
        return metadata
    
    def parse_edifact(self, content):
        """
        Parse EDIFACT EDI format
        
        Args:
            content: EDIFACT EDI content
        
        Returns:
            Dictionary with parsed metadata
        """
        metadata = {
            'format': 'EDIFACT',
            'parsed_at': datetime.now().isoformat(),
            'segments': []
        }
        
        try:
            # EDIFACT uses specific delimiters defined in UNA or defaults
            # UNA:+.? ' (component:+, element:, decimal:., release:?, segment:')
            
            # Default delimiters
            component_sep = ':'
            element_sep = '+'
            decimal_sep = '.'
            release_char = '?'
            segment_term = "'"
            
            # Check for UNA segment
            if content.startswith('UNA'):
                # Extract delimiters from UNA
                if len(content) >= 9:
                    component_sep = content[3]
                    element_sep = content[4]
                    decimal_sep = content[5]
                    release_char = content[6]
                    segment_term = content[8]
                # Remove UNA from content
                content = content[9:]
            
            # Split into segments
            segments = content.split(segment_term)
            
            for segment in segments:
                if not segment.strip():
                    continue
                
                # Split segment into elements
                elements = segment.split(element_sep)
                segment_id = elements[0] if elements else ''
                
                # Parse UNB (Interchange Header)
                if segment_id == 'UNB':
                    if len(elements) >= 5:
                        # Sender identification
                        sender_parts = elements[2].split(component_sep)
                        metadata['sender_id'] = sender_parts[0] if sender_parts else ''
                        
                        # Receiver identification
                        receiver_parts = elements[3].split(component_sep)
                        metadata['receiver_id'] = receiver_parts[0] if receiver_parts else ''
                        
                        # Date/time
                        datetime_parts = elements[4].split(component_sep)
                        if len(datetime_parts) >= 2:
                            metadata['interchange_date'] = datetime_parts[0]
                            metadata['interchange_time'] = datetime_parts[1]
                
                # Parse UNH (Message Header)
                elif segment_id == 'UNH':
                    if len(elements) >= 3:
                        metadata['message_ref'] = elements[1]
                        
                        # Message type
                        msg_type_parts = elements[2].split(component_sep)
                        if msg_type_parts:
                            doc_type_code = msg_type_parts[0]
                            metadata['document_type_code'] = doc_type_code
                            metadata['document_type'] = self.DOCUMENT_TYPES.get(
                                doc_type_code,
                                f'Unknown ({doc_type_code})'
                            )
                
                # Parse BGM (Beginning of Message)
                elif segment_id == 'BGM':
                    if len(elements) >= 3:
                        metadata['document_number'] = elements[2]
                        # For orders, this is often the PO number
                        if metadata.get('document_type_code') == 'ORDERS':
                            metadata['po_number'] = elements[2]
                
                # Parse DTM (Date/Time/Period)
                elif segment_id == 'DTM':
                    if len(elements) >= 2:
                        dtm_parts = elements[1].split(component_sep)
                        if len(dtm_parts) >= 2:
                            qualifier = dtm_parts[0]
                            date_value = dtm_parts[1]
                            if qualifier == '137':  # Document date
                                metadata['document_date'] = date_value
                
                # Parse NAD (Name and Address)
                elif segment_id == 'NAD':
                    if len(elements) >= 3:
                        qualifier = elements[1]
                        # Party name is in element 3 or 4
                        name_parts = elements[3].split(component_sep) if len(elements) > 3 else []
                        name = name_parts[0] if name_parts else ''
                        
                        if qualifier == 'BY':  # Buyer
                            metadata['buyer_name'] = name
                        elif qualifier == 'SU':  # Supplier
                            metadata['supplier_name'] = name
                        elif qualifier == 'DP':  # Delivery party
                            metadata['delivery_name'] = name
                
                metadata['segments'].append(segment_id)
            
            # Determine partner name
            if 'buyer_name' in metadata:
                metadata['partner_name'] = metadata['buyer_name']
            elif 'supplier_name' in metadata:
                metadata['partner_name'] = metadata['supplier_name']
            elif 'sender_id' in metadata:
                metadata['partner_name'] = metadata['sender_id']
            
        except Exception as e:
            metadata['parse_error'] = str(e)
        
        return metadata
    
    def parse_edi_file(self, file_path):
        """
        Parse EDI file and extract metadata
        
        Args:
            file_path: Path to EDI file
        
        Returns:
            Dictionary with parsed metadata
        """
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            raise ValidationError(f"Failed to read file: {str(e)}")
        
        # Detect format
        format_type = self.detect_format(content)
        
        # Parse based on format
        if format_type == 'X12':
            metadata = self.parse_x12(content)
        elif format_type == 'EDIFACT':
            metadata = self.parse_edifact(content)
        else:
            # For other formats, return basic metadata
            metadata = {
                'format': format_type,
                'parsed_at': datetime.now().isoformat(),
                'file_size': os.path.getsize(file_path),
                'line_count': len(content.split('\n'))
            }
        
        # Add file information
        metadata['file_path'] = file_path
        metadata['file_name'] = os.path.basename(file_path)
        metadata['file_size'] = os.path.getsize(file_path)
        
        return metadata
    
    def generate_edi_file(self, transaction_data, format_type='X12'):
        """
        Generate EDI file from transaction data
        
        Args:
            transaction_data: Dictionary with transaction information
            format_type: EDI format ('X12', 'EDIFACT', etc.)
        
        Returns:
            EDI content as string
        """
        if format_type == 'X12':
            return self._generate_x12(transaction_data)
        elif format_type == 'EDIFACT':
            return self._generate_edifact(transaction_data)
        else:
            raise ValidationError(f"Unsupported format: {format_type}")
    
    def _generate_x12(self, data):
        """Generate X12 EDI content"""
        # This is a simplified example - production would use proper X12 generation
        
        now = datetime.now()
        date_str = now.strftime('%y%m%d')
        time_str = now.strftime('%H%M')
        
        # ISA segment
        isa = f"ISA*00*          *00*          *ZZ*{data.get('sender_id', 'SENDER'):<15}*ZZ*{data.get('receiver_id', 'RECEIVER'):<15}*{date_str}*{time_str}*U*00401*000000001*0*P*>~"
        
        # GS segment
        gs = f"GS*PO*{data.get('sender_code', 'SENDER')}*{data.get('receiver_code', 'RECEIVER')}*{date_str}*{time_str}*1*X*004010~"
        
        # ST segment
        st = f"ST*850*0001~"
        
        # BEG segment
        beg = f"BEG*00*NE*{data.get('po_number', 'PO123')}**{date_str}~"
        
        # N1 segments (parties)
        n1_by = f"N1*BY*{data.get('buyer_name', 'Buyer Company')}~"
        n1_se = f"N1*SE*{data.get('seller_name', 'Seller Company')}~"
        
        # SE segment (transaction set trailer)
        se = "SE*6*0001~"
        
        # GE segment (functional group trailer)
        ge = "GE*1*1~"
        
        # IEA segment (interchange trailer)
        iea = "IEA*1*000000001~"
        
        # Combine all segments
        edi_content = isa + gs + st + beg + n1_by + n1_se + se + ge + iea
        
        return edi_content
    
    def _generate_edifact(self, data):
        """Generate EDIFACT EDI content"""
        # This is a simplified example - production would use proper EDIFACT generation
        
        now = datetime.now()
        date_str = now.strftime('%y%m%d')
        time_str = now.strftime('%H%M')
        
        # UNB segment
        unb = f"UNB+UNOC:3+{data.get('sender_id', 'SENDER')}:14+{data.get('receiver_id', 'RECEIVER')}:14+{date_str}:{time_str}+1'"
        
        # UNH segment
        unh = f"UNH+1+ORDERS:D:96A:UN'"
        
        # BGM segment
        bgm = f"BGM+220+{data.get('po_number', 'PO123')}+9'"
        
        # DTM segment
        dtm = f"DTM+137:{date_str}:102'"
        
        # NAD segments (parties)
        nad_by = f"NAD+BY+{data.get('buyer_id', 'BUYER')}::9+{data.get('buyer_name', 'Buyer Company')}'"
        nad_su = f"NAD+SU+{data.get('supplier_id', 'SUPPLIER')}::9+{data.get('supplier_name', 'Supplier Company')}'"
        
        # UNT segment (message trailer)
        unt = "UNT+6+1'"
        
        # UNZ segment (interchange trailer)
        unz = "UNZ+1+1'"
        
        # Combine all segments
        edi_content = unb + unh + bgm + dtm + nad_by + nad_su + unt + unz
        
        return edi_content
    
    def validate_edi_content(self, content, format_type=None):
        """
        Validate EDI content
        
        Args:
            content: EDI content string
            format_type: Expected format (optional, will auto-detect if not provided)
        
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'format': None,
            'errors': [],
            'warnings': []
        }
        
        if not content:
            result['errors'].append("Content is empty")
            return result
        
        # Detect format if not provided
        if not format_type:
            format_type = self.detect_format(content)
        
        result['format'] = format_type
        
        # Validate based on format
        if format_type == 'X12':
            if not content.startswith('ISA'):
                result['errors'].append("X12 must start with ISA segment")
            if not content.endswith('~'):
                result['warnings'].append("X12 should end with segment terminator (~)")
            
            # Check for required segments
            if 'GS' not in content:
                result['errors'].append("Missing GS (Functional Group Header) segment")
            if 'ST' not in content:
                result['errors'].append("Missing ST (Transaction Set Header) segment")
            
        elif format_type == 'EDIFACT':
            if not (content.startswith('UNA') or content.startswith('UNB')):
                result['errors'].append("EDIFACT must start with UNA or UNB segment")
            if not content.endswith("'"):
                result['warnings'].append("EDIFACT should end with segment terminator (')")
            
            # Check for required segments
            if 'UNH' not in content:
                result['errors'].append("Missing UNH (Message Header) segment")
        
        elif format_type == 'UNKNOWN':
            result['errors'].append("Unable to detect EDI format")
        
        # Set valid flag
        result['valid'] = len(result['errors']) == 0
        
        return result
