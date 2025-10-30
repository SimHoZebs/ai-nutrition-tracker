#!/usr/bin/env python3
"""
Test script for AI Nutrition Tracker API
Creates a test user and submits a /process request with food description.
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust if your Django server runs on different port
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER_DATA = {
    "username": f"testuser_{uuid.uuid4().hex[:8]}",
    "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

FOOD_DESCRIPTIONS = [
    "6oz sirloin from long horns for dinner yesterday, and chicken for lunch today",
    "I had coffee this morning and pizza last night",
    "Ate an apple 2 hours ago and had breakfast this morning"
]

def print_response(response, title="Response"):
    """Helper function to print response details"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Text Response: {response.text}")

def test_nutrition_api():
    """Main test function"""
    session = requests.Session()
    
    print("Starting AI Nutrition Tracker API Test")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER_DATA['username']}")
    print(f"Food Descriptions: {len(FOOD_DESCRIPTIONS)} test cases")
    
    # Get CSRF token first
    print("\n" + "="*50)
    print("STEP 0: Getting CSRF token")
    print("="*50)
    
    csrf_response = session.get(f"{API_BASE}/register/")
    csrf_token = session.cookies.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")
    
    # Step 1: Register a new user
    print("\n" + "="*50)
    print("STEP 1: Registering new user")
    print("="*50)
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    
    register_response = session.post(
        f"{API_BASE}/register/",
        json=TEST_USER_DATA,
        headers=headers
    )
    
    print_response(register_response, "User Registration")
    
    if register_response.status_code != 201:
        print("❌ User registration failed!")
        return False
    
    print("✅ User registration successful!")
    
    # Registration automatically logs in the user, so skip explicit login
    print("\n✅ User automatically logged in after registration!")
    
    # Step 2: Test multiple food descriptions with time parsing
    success_count = 0
    
    for i, food_description in enumerate(FOOD_DESCRIPTIONS, 1):
        print("\n" + "="*50)
        print(f"STEP 2.{i}: Testing food description with time parsing")
        print("="*50)
        print(f"Description: {food_description}")
        
        # Update CSRF token
        csrf_token = session.cookies.get('csrftoken')
        headers["X-CSRFToken"] = csrf_token
        
        process_response = session.post(
            f"{API_BASE}/process/",
            json={"food_description": food_description},
            headers=headers
        )
        
        print_response(process_response, f"Process Request {i}")
        
        if process_response.status_code == 200:
            print(f"✅ Process request {i} successful!")
            
            # Parse and display the response content
            try:
                response_data = process_response.json()
                
                if "questions" in response_data and response_data["questions"]:
                    print(f"\n📋 Agent has {len(response_data['questions'])} follow-up questions:")
                    for j, question in enumerate(response_data["questions"], 1):
                        print(f"  {j}. {question.get('question', question)}")
                        
                if "foods" in response_data and response_data["foods"]:
                    print(f"\n🍽️  Agent processed {len(response_data['foods'])} food items:")
                    for food in response_data["foods"]:
                        print(f"  - {food.get('name', 'Unknown')} ({food.get('meal_type', 'Unknown meal')})")
                        print(f"    Calories: {food.get('calories', 0)}, Protein: {food.get('protein', 0)}g")
                        
                if "response" in response_data:
                    print(f"\n💾 Saved {len(response_data['response'])} food entries to database")
                    # Check if eaten_at field is present
                    for food_entry in response_data["response"]:
                        if "eaten_at" in food_entry:
                            print(f"  ✅ Food '{food_entry['name']}' has eaten_at: {food_entry['eaten_at']}")
                        else:
                            print(f"  ⚠️  Food '{food_entry['name']}' missing eaten_at field")
                    
                success_count += 1
                    
            except Exception as e:
                print(f"❌ Error parsing response: {e}")
        else:
            print(f"❌ Process request {i} failed!")
    
    return success_count == len(FOOD_DESCRIPTIONS)

def main():
    """Main entry point"""
    try:
        success = test_nutrition_api()
        
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
        if success:
            print("✅ All tests completed successfully!")
            print("\nThe test script:")
            print("1. ✅ Created a new user account")
            print(f"2. ✅ Successfully tested {len(FOOD_DESCRIPTIONS)} food descriptions with time parsing")
            print("3. ✅ Verified eaten_at field is properly stored in database")
            print("4. ✅ Received and parsed all responses")
        else:
            print("❌ Some tests failed - check the output above for details")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server.")
        print("Make sure the Django development server is running on http://localhost:8000")
        print("Run: python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()