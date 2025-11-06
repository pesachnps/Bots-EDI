#!/usr/bin/env python
"""
Bots EDI API Testing Script
Test API endpoints and functionality
"""

import requests
import json
import os
import sys
from datetime import datetime

# Configuration
API_KEY = ""  # Set your API key here
BASE_URL = "http://localhost:8080/api"

def test_api_status():
    """Test API status endpoint"""
    print("\n🔍 Testing API Status...")
    
    headers = {"X-API-Key": API_KEY}
    
    try:
        response = requests.get(f"{BASE_URL}/v1/status", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Status Retrieved Successfully!")
            print(f"   API Key Name: {data['api_key']['name']}")
            print(f"   User: {data['api_key']['user']}")
            print(f"   Active: {data['api_key']['is_active']}")
            print(f"   Rate Limit: {data['api_key']['current_usage']}/{data['api_key']['rate_limit']}")
            print(f"   Permissions: {', '.join(data['api_key']['permissions'])}")
            return True
        else:
            print(f"❌ Failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_list_files():
    """Test file listing endpoint"""
    print("\n🔍 Testing File List...")
    
    headers = {"X-API-Key": API_KEY}
    
    try:
        response = requests.get(f"{BASE_URL}/v1/files/list?type=outfile", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File List Retrieved Successfully!")
            print(f"   Total Files: {data['count']}")
            if data['count'] > 0:
                print(f"   First File: {data['files'][0]['name']}")
            return True
        else:
            print(f"❌ Failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_file_upload(file_path):
    """Test file upload endpoint"""
    print(f"\n🔍 Testing File Upload: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    headers = {"X-API-Key": API_KEY}
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'route': 'test_route',
                'partner': 'TEST_PARTNER'
            }
            response = requests.post(
                f"{BASE_URL}/v1/files/upload",
                headers=headers,
                files=files,
                data=data
            )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ File Uploaded Successfully!")
            print(f"   File Name: {result['file']['name']}")
            print(f"   File Size: {result['file']['size']} bytes")
            print(f"   Route: {result['file']['route']}")
            return True
        else:
            print(f"❌ Failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_reports():
    """Test reports endpoint"""
    print("\n🔍 Testing Reports...")
    
    headers = {"X-API-Key": API_KEY}
    
    try:
        response = requests.get(f"{BASE_URL}/v1/reports?limit=10", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reports Retrieved Successfully!")
            print(f"   Total Reports: {data['count']}")
            if data['count'] > 0:
                print(f"   Latest Report: {data['reports'][0]}")
            return True
        else:
            print(f"❌ Failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_invalid_api_key():
    """Test with invalid API key"""
    print("\n🔍 Testing Invalid API Key...")
    
    headers = {"X-API-Key": "INVALID_KEY_12345"}
    
    try:
        response = requests.get(f"{BASE_URL}/v1/status", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Invalid API Key Correctly Rejected!")
            return True
        else:
            print(f"❌ Unexpected response: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_rate_limiting():
    """Test rate limiting (optional - makes many requests)"""
    print("\n🔍 Testing Rate Limiting...")
    print("⚠️  This test makes many rapid requests to test rate limiting.")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Skipped.")
        return None
    
    headers = {"X-API-Key": API_KEY}
    rate_limited = False
    
    try:
        for i in range(1100):  # Attempt to exceed default rate limit
            response = requests.get(f"{BASE_URL}/v1/status", headers=headers)
            
            if response.status_code == 429:
                print(f"✅ Rate Limiting Enforced at Request #{i+1}!")
                print(f"   Response: {response.json()}")
                rate_limited = True
                break
            
            if (i + 1) % 100 == 0:
                print(f"   Completed {i+1} requests...")
        
        if not rate_limited:
            print("⚠️  Rate limit not reached within test range")
        
        return rate_limited
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_all_tests(test_file_path=None):
    """Run all API tests"""
    print("=" * 60)
    print("🚀 Bots EDI API Test Suite")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY[:16]}..." if API_KEY else "API Key: NOT SET")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    if not API_KEY:
        print("\n❌ ERROR: API_KEY not set!")
        print("Please set your API key in this script or as an environment variable:")
        print("  export BOTS_API_KEY=your-api-key-here")
        sys.exit(1)
    
    results = {}
    
    # Run tests
    results['API Status'] = test_api_status()
    results['List Files'] = test_list_files()
    results['Get Reports'] = test_get_reports()
    results['Invalid API Key'] = test_invalid_api_key()
    
    if test_file_path:
        results['File Upload'] = test_file_upload(test_file_path)
    
    # Optional rate limiting test
    # results['Rate Limiting'] = test_rate_limiting()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for test_name, result in results.items():
        icon = "✅" if result is True else "❌" if result is False else "⏭️ "
        print(f"{icon} {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    print("=" * 60)
    
    return failed == 0


def main():
    """Main function"""
    global API_KEY
    
    # Check for API key in environment variable
    if not API_KEY:
        API_KEY = os.environ.get('BOTS_API_KEY', '')
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Bots EDI API Testing Script")
            print("\nUsage:")
            print("  python test_api.py                    - Run all tests")
            print("  python test_api.py <file_path>        - Run tests with file upload")
            print("  python test_api.py status             - Test API status only")
            print("  python test_api.py upload <file>      - Test file upload only")
            print("\nEnvironment Variables:")
            print("  BOTS_API_KEY - Your API key (or set in script)")
            return
        
        elif sys.argv[1] == 'status':
            test_api_status()
            return
        
        elif sys.argv[1] == 'upload' and len(sys.argv) > 2:
            test_file_upload(sys.argv[2])
            return
        
        else:
            # Treat as file path for upload test
            run_all_tests(sys.argv[1])
            return
    
    # Run all tests
    success = run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
