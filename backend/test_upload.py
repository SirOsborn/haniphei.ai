#!/usr/bin/env python3
"""
Test script for document upload endpoint
"""
import requests
import sys

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{API_BASE_URL}/api/documents"

def test_upload_without_auth():
    """Test 1: Upload without authentication (should fail)"""
    print("\n=== Test 1: Upload without authentication ===")

    # Create a dummy PDF file
    files = {'file': ('test.pdf', b'%PDF-1.4 dummy content', 'application/pdf')}

    response = requests.post(ENDPOINT, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 401 or response.status_code == 403:
        print("✓ Correctly rejected unauthenticated request")
    else:
        print("✗ Unexpected response for unauthenticated request")

def test_upload_with_wrong_field_name():
    """Test 2: Upload with wrong field name"""
    print("\n=== Test 2: Upload with wrong field name ===")

    # Wrong field name: 'document' instead of 'file'
    files = {'document': ('test.pdf', b'%PDF-1.4 dummy content', 'application/pdf')}

    response = requests.post(ENDPOINT, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 422:
        print("✓ Got 422 error (expected - wrong field name)")
    else:
        print("✗ Unexpected response")

def test_upload_with_json():
    """Test 3: Upload as JSON instead of multipart/form-data"""
    print("\n=== Test 3: Upload as JSON (wrong content type) ===")

    headers = {'Content-Type': 'application/json'}
    data = {'file': 'some data'}

    response = requests.post(ENDPOINT, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 422:
        print("✓ Got 422 error (expected - wrong content type)")
    else:
        print("✗ Unexpected response")

def test_upload_correct_format():
    """Test 4: Upload with correct format (needs auth)"""
    print("\n=== Test 4: Upload with correct format ===")
    print("Note: This will fail without valid authentication")

    # Correct format
    files = {'file': ('test.pdf', b'%PDF-1.4 dummy content', 'application/pdf')}

    # Add session cookie if you have one
    # cookies = {'session': 'your-session-token'}
    # response = requests.post(ENDPOINT, files=files, cookies=cookies)

    response = requests.post(ENDPOINT, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    print("Testing Document Upload Endpoint")
    print(f"Target: {ENDPOINT}")

    try:
        # Check if server is running
        health_check = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_check.status_code != 200:
            print("❌ Server is not responding correctly")
            sys.exit(1)
        print("✓ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print(f"   Expected URL: {API_BASE_URL}")
        sys.exit(1)

    # Run tests
    test_upload_without_auth()
    test_upload_with_wrong_field_name()
    test_upload_with_json()
    test_upload_correct_format()

    print("\n" + "="*50)
    print("DIAGNOSIS:")
    print("="*50)
    print("If your client is getting 422 errors, check:")
    print("1. Using multipart/form-data content type")
    print("2. Field name is 'file' (not 'document' or anything else)")
    print("3. Authentication is properly set (session cookie or bearer token)")
    print("4. File type is allowed: PDF, DOCX, JPG, JPEG, PNG")
    print("5. File size is under 10MB")

if __name__ == "__main__":
    main()
