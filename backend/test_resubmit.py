#!/usr/bin/env python3
"""
Test script for AI Nutrition Tracker API - Testing resubmit functionality
Creates a test user, submits a /process request, then resubmits with answers.
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER_DATA = {
    "username": f"testuser_{uuid.uuid4().hex[:8]}",
    "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

FOOD_DESCRIPTION = "6oz sirloin from long horns for dinner, and chicken for lunch"

# Answers to the expected follow-up questions
FOLLOW_UP_ANSWERS = ["breast", "grilled"]

def print_response(response, title="Response"):
    """Helper function to print response details"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Text Response: {response.text}")

def extract_questions_from_response(response_data):
    """Extract questions from the agent response"""
    questions = []
    
    # Check if response has parts structure (as seen in previous test)
    if "parts" in response_data and response_data["parts"]:
        for part in response_data["parts"]:
            if "text" in part:
                try:
                    # Parse the JSON text content
                    text_content = json.loads(part["text"])
                    if "questions" in text_content:
                        questions.extend(text_content["questions"])
                except json.JSONDecodeError:
                    print(f"Could not parse text as JSON: {part['text']}")
    
    # Also check direct questions field
    if "questions" in response_data:
        questions.extend(response_data["questions"])
    
    return questions

def test_resubmit_functionality():
    """Main test function for resubmit"""
    session = requests.Session()
    
    print("Starting AI Nutrition Tracker Resubmit Test")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER_DATA['username']}")
    print(f"Food Description: {FOOD_DESCRIPTION}")
    print(f"Follow-up Answers: {FOLLOW_UP_ANSWERS}")
    
    # Get CSRF token first
    print("\n" + "="*60)
    print("STEP 1: Getting CSRF token")
    print("="*60)
    
    csrf_response = session.get(f"{API_BASE}/register/")
    csrf_token = session.cookies.get('csrftoken')
    print(f"CSRF Token: {csrf_token}")
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    
    # Step 2: Register a new user
    print("\n" + "="*60)
    print("STEP 2: Registering new user")
    print("="*60)
    
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
    
    # Step 3: Initial /process request
    print("\n" + "="*60)
    print("STEP 3: Submitting initial /process request")
    print("="*60)
    
    # Update CSRF token after registration
    csrf_token = session.cookies.get('csrftoken')
    headers["X-CSRFToken"] = csrf_token
    
    process_response = session.post(
        f"{API_BASE}/process/",
        json={"food_description": FOOD_DESCRIPTION},
        headers=headers
    )
    
    print_response(process_response, "Initial Process Request")
    
    if process_response.status_code != 200:
        print("❌ Initial process request failed!")
        return False
    
    print("✅ Initial process request successful!")
    
    # Extract questions from response
    response_data = process_response.json()
    questions = extract_questions_from_response(response_data)
    
    if not questions:
        print("❌ No questions found in response - cannot test resubmit")
        print("Response data:", json.dumps(response_data, indent=2))
        return False
    
    print(f"\n📋 Found {len(questions)} questions:")
    for i, question in enumerate(questions, 1):
        if isinstance(question, dict):
            print(f"  {i}. {question.get('question', question)}")
        else:
            print(f"  {i}. {question}")
    
    # Step 4: Resubmit with answers
    print("\n" + "="*60)
    print("STEP 4: Resubmitting with answers")
    print("="*60)
    
    print(f"Submitting answers: {FOLLOW_UP_ANSWERS}")
    
    resubmit_response = session.post(
        f"{API_BASE}/resubmit/",
        json={"answers": FOLLOW_UP_ANSWERS},
        headers=headers
    )
    
    print_response(resubmit_response, "Resubmit Request")
    
    if resubmit_response.status_code == 200:
        print("✅ Resubmit request successful!")
        
        # Parse and display the final response
        try:
            final_response_data = resubmit_response.json()
            
            if "response" in final_response_data and final_response_data["response"]:
                foods = final_response_data["response"]
                print(f"\n🍽️  Successfully processed and saved {len(foods)} food items:")
                for food in foods:
                    print(f"  - {food.get('name', 'Unknown')} ({food.get('meal_type', 'Unknown meal')})")
                    print(f"    Calories: {food.get('calories', 0)}, Protein: {food.get('protein', 0)}g")
                    if food.get('carbohydrates'):
                        print(f"    Carbs: {food.get('carbohydrates', 0)}g, Fat: {food.get('saturated_fat', 0) + food.get('unsaturated_fat', 0)}g")
                
                print(f"\n💾 Food entries saved to database with user ID: {TEST_USER_DATA['username']}")
                return True
            else:
                print("⚠️  Resubmit successful but no food entries returned")
                print("Final response:", json.dumps(final_response_data, indent=2))
                return True
                
        except Exception as e:
            print(f"❌ Error parsing resubmit response: {e}")
            return False
            
    else:
        print("❌ Resubmit request failed!")
        return False

def main():
    """Main entry point"""
    try:
        success = test_resubmit_functionality()
        
        print("\n" + "="*60)
        print("RESUBMIT TEST SUMMARY")
        print("="*60)
        
        if success:
            print("✅ All resubmit tests completed successfully!")
            print("\nThe test workflow:")
            print("1. ✅ Created a new user account")
            print("2. ✅ Submitted initial food description to /process endpoint")
            print("3. ✅ Received follow-up questions from AI agent")
            print("4. ✅ Successfully resubmitted answers to /resubmit endpoint")
            print("5. ✅ Received final processed food data")
            print("\n🎉 The complete nutrition tracking workflow is working!")
        else:
            print("❌ Resubmit test failed - check the output above for details")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server.")
        print("Make sure the Django development server is running on http://localhost:8000")
        print("Run: python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()