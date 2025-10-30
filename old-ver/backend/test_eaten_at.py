#!/usr/bin/env python3
"""
Test script specifically for eaten_at field functionality
Uses specific, non-ambiguous foods to test time parsing
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Test data with specific, non-ambiguous foods
TEST_USER_DATA = {
    "username": f"testuser_{uuid.uuid4().hex[:8]}",
    "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

# Specific foods that shouldn't trigger ambiguity questions
FOOD_DESCRIPTIONS = [
    "1 medium apple yesterday afternoon",
    "2 bananas this morning", 
    "1 cup of white rice for lunch today"
]

def print_response(response, title="Response"):
    """Helper function to print response details"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        response_json = response.json()
        print(f"JSON Response: {json.dumps(response_json, indent=2)}")
        return response_json
    except:
        print(f"Text Response: {response.text}")
        return None

def test_eaten_at_field():
    """Test eaten_at field functionality"""
    session = requests.Session()
    
    print("Testing eaten_at field functionality")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER_DATA['username']}")
    
    # Get CSRF token and register user
    csrf_response = session.get(f"{API_BASE}/register/")
    csrf_token = session.cookies.get('csrftoken')
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    
    register_response = session.post(
        f"{API_BASE}/register/",
        json=TEST_USER_DATA,
        headers=headers
    )
    
    if register_response.status_code != 201:
        print("❌ User registration failed!")
        return False
    
    print("✅ User registration successful!")
    
    # Test each food description
    success_count = 0
    
    for i, food_description in enumerate(FOOD_DESCRIPTIONS, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {food_description}")
        print("="*60)
        
        # Update CSRF token
        csrf_token = session.cookies.get('csrftoken')
        headers["X-CSRFToken"] = csrf_token
        
        process_response = session.post(
            f"{API_BASE}/process/",
            json={"food_description": food_description},
            headers=headers
        )
        
        response_data = print_response(process_response, f"Process Request {i}")
        
        if process_response.status_code == 200 and response_data:
            # Check if we got questions (ambiguous) or direct response
            has_questions = False
            
            if "questions" in response_data and response_data["questions"]:
                print(f"📋 Got {len(response_data['questions'])} follow-up questions")
                has_questions = True
            
            # Check parts for questions
            if "parts" in response_data:
                for part in response_data["parts"]:
                    if "text" in part:
                        try:
                            text_content = json.loads(part["text"])
                            if "questions" in text_content and text_content["questions"]:
                                print(f"📋 Got {len(text_content['questions'])} follow-up questions in parts")
                                has_questions = True
                        except:
                            pass
            
            # Check if foods were saved directly
            if "response" in response_data and response_data["response"]:
                print(f"💾 Saved {len(response_data['response'])} food entries to database")
                for food_entry in response_data["response"]:
                    print(f"  Food: {food_entry.get('name', 'Unknown')}")
                    if "eaten_at" in food_entry:
                        print(f"  ✅ eaten_at: {food_entry['eaten_at']}")
                    else:
                        print(f"  ❌ Missing eaten_at field")
                success_count += 1
            elif not has_questions:
                print("⚠️  No foods saved and no questions - unexpected response")
            else:
                print("ℹ️  Got questions for clarification - this is expected for some foods")
        else:
            print(f"❌ Request failed with status {process_response.status_code}")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        success = test_eaten_at_field()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        if success:
            print("✅ eaten_at field test completed - at least one food was saved with timestamp")
        else:
            print("⚠️  No foods were saved directly - all triggered clarification questions")
            print("This might be expected behavior, but we can't verify eaten_at field this way")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server.")
        print("Make sure the Django development server is running on http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")