#!/usr/bin/env python3
"""
Test script for Gemma 2B integration
Tests both direct API and LangChain methods
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_status():
    """Test the status endpoint"""
    print("🔍 Testing status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            if 'model' in data:
                print(f"📦 Model: {data['model']}")
            return data['status'] == 'ready'
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def test_direct_api():
    """Test the direct API endpoint"""
    print("\n🔍 Testing direct API endpoint (/generate)...")
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json={"prompt": "Hello, what is your name?"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Direct API Response: {data.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Direct API failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Direct API error: {e}")
        return False

def test_langchain_api():
    """Test the LangChain endpoint"""
    print("\n🔍 Testing LangChain endpoint (/chat)...")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Hello, what model are you?",
                "use_langchain": True
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LangChain Response: {data.get('response', 'No response')[:100]}...")
            print(f"📊 Method: {data.get('method')}")
            print(f"📦 Model: {data.get('model')}")
            return True
        else:
            print(f"❌ LangChain API failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ LangChain API error: {e}")
        return False

def main():
    print("🚀 Testing Gemma 2B Integration")
    print("=" * 50)
    
    # Test status
    if not test_status():
        print("\n⏳ Model not ready yet. Waiting 10 seconds...")
        time.sleep(10)
        if not test_status():
            print("❌ Model still not ready. Please check your setup.")
            return
    
    # Test both endpoints
    direct_success = test_direct_api()
    langchain_success = test_langchain_api()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Direct API: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"LangChain:  {'✅ PASS' if langchain_success else '❌ FAIL'}")
    
    if direct_success and langchain_success:
        print("\n🎉 All tests passed! Gemma 2B is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()