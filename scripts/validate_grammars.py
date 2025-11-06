#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
X12 Grammar Validation Script
Validates all X12 grammar files for Python syntax and structural correctness
"""

import os
import sys
import py_compile
import json
from pathlib import Path
from datetime import datetime

class GrammarValidator:
    def __init__(self, grammars_dir):
        self.grammars_dir = Path(grammars_dir)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'files': {}
        }
    
    def validate_python_syntax(self, filepath):
        """Validate Python syntax by attempting to compile"""
        try:
            py_compile.compile(str(filepath), doraise=True)
            return True, "Valid Python syntax"
        except py_compile.PyCompileError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Compilation error: {str(e)}"
    
    def validate_structure(self, filepath):
        """Validate grammar file structure"""
        issues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required imports
            if 'from bots.botsconfig import *' not in content and 'from botsconfig import *' not in content:
                issues.append("Missing 'from bots.botsconfig import *'")
            
            if 'from .records004010 import recorddefs' not in content and 'records004010' not in content:
                issues.append("Missing recorddefs import")
            
            # Check for syntax dictionary
            if 'syntax = {' not in content:
                issues.append("Missing syntax dictionary")
            
            # Check for structure array
            if 'structure = [' not in content:
                issues.append("Missing structure array")
            
            # Check for ST and SE segments
            if "ID: 'ST'" not in content:
                issues.append("Missing ST (Transaction Set Header) segment")
            
            if "ID: 'SE'" not in content:
                issues.append("Missing SE (Transaction Set Trailer) segment")
            
            # Check for proper functional group
            if 'functionalgroup' not in content:
                issues.append("Missing 'functionalgroup' in syntax dictionary")
            
            # Check for version
            if 'version' not in content:
                issues.append("Missing 'version' in syntax dictionary")
            
            return len(issues) == 0, issues if issues else ["Valid structure"]
            
        except Exception as e:
            return False, [f"Structure validation error: {str(e)}"]
    
    def validate_file(self, filepath):
        """Validate a single grammar file"""
        filename = filepath.name
        file_results = {
            'filename': filename,
            'path': str(filepath),
            'status': 'unknown',
            'tests': {}
        }
        
        # Test 1: Python syntax
        syntax_valid, syntax_msg = self.validate_python_syntax(filepath)
        file_results['tests']['python_syntax'] = {
            'passed': syntax_valid,
            'message': syntax_msg
        }
        
        # Test 2: Structure validation
        if syntax_valid:
            structure_valid, structure_msgs = self.validate_structure(filepath)
            file_results['tests']['structure'] = {
                'passed': structure_valid,
                'messages': structure_msgs
            }
        else:
            file_results['tests']['structure'] = {
                'passed': False,
                'messages': ["Skipped due to syntax errors"]
            }
            structure_valid = False
        
        # Overall status
        if syntax_valid and structure_valid:
            file_results['status'] = 'passed'
            self.results['passed'] += 1
        else:
            file_results['status'] = 'failed'
            self.results['failed'] += 1
        
        return file_results
    
    def validate_all(self, pattern='*004010.py'):
        """Validate all grammar files matching pattern"""
        grammar_files = sorted(self.grammars_dir.glob(pattern))
        
        if not grammar_files:
            print(f"No grammar files found matching pattern '{pattern}' in {self.grammars_dir}")
            return self.results
        
        self.results['total_files'] = len(grammar_files)
        
        print(f"\nValidating {len(grammar_files)} X12 grammar files...")
        print("=" * 70)
        
        for filepath in grammar_files:
            print(f"\nChecking: {filepath.name}")
            file_results = self.validate_file(filepath)
            self.results['files'][filepath.name] = file_results
            
            # Print results
            if file_results['status'] == 'passed':
                print(f"  ✓ PASSED")
            else:
                print(f"  ✗ FAILED")
                for test_name, test_result in file_results['tests'].items():
                    if not test_result['passed']:
                        print(f"    {test_name}:")
                        if isinstance(test_result.get('messages'), list):
                            for msg in test_result['messages']:
                                print(f"      - {msg}")
                        else:
                            print(f"      - {test_result.get('message', 'Unknown error')}")
        
        return self.results
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Total files:  {self.results['total_files']}")
        print(f"Passed:       {self.results['passed']} ({self.results['passed']/max(self.results['total_files'], 1)*100:.1f}%)")
        print(f"Failed:       {self.results['failed']}")
        print(f"Skipped:      {self.results['skipped']}")
        print()
        
        if self.results['failed'] > 0:
            print("Failed files:")
            for filename, file_result in self.results['files'].items():
                if file_result['status'] == 'failed':
                    print(f"  - {filename}")
        else:
            print("✓ All grammar files passed validation!")
        
        print("=" * 70)
    
    def save_results(self, output_file='validation_results.json'):
        """Save validation results to JSON file"""
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to: {output_path}")


def main():
    """Main validation function"""
    # Determine grammars directory
    script_dir = Path(__file__).parent
    grammars_dir = script_dir / 'env' / 'default' / 'usersys' / 'grammars' / 'x12'
    
    if not grammars_dir.exists():
        print(f"Error: Grammars directory not found: {grammars_dir}")
        print("Please run this script from the bots project root directory.")
        sys.exit(1)
    
    # Create validator
    validator = GrammarValidator(grammars_dir)
    
    # Run validation
    results = validator.validate_all()
    
    # Print summary
    validator.print_summary()
    
    # Save results
    validator.save_results()
    
    # Exit with error code if any validations failed
    sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
