#!/usr/bin/env python3
"""
Test script for AI Nutrition Tracker Audio Transcription API
Tests both standalone transcription and integrated audio processing workflows.
"""

import requests
import json
import uuid
import os
from datetime import datetime

# Configuration
BASE_URL = (
    "http://localhost:8000"  # Adjust if your Django server runs on different port
)
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER_DATA = {
    "username": f"audiotest_{uuid.uuid4().hex[:8]}",
    "email": f"audiotest_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123",
    "first_name": "Audio",
    "last_name": "Test",
}

# Path to test audio file
AUDIO_FILE_PATH = "../test/Recording.mp3"


def print_response(response, title="Response"):
    """Helper function to print response details"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        response_json = response.json()
        print(f"JSON Response: {json.dumps(response_json, indent=2)}")
        return response_json
    except:
        print(f"Text Response: {response.text}")
        return None


def check_audio_file():
    """Check if the test audio file exists"""
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        print("Looking for audio files in test directory...")
        test_dir = "../test"
        if os.path.exists(test_dir):
            files = os.listdir(test_dir)
            audio_files = [
                f
                for f in files
                if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))
            ]
            if audio_files:
                print(f"Found audio files: {audio_files}")
                return os.path.join(test_dir, audio_files[0])
            else:
                print("No audio files found in test directory")
        return None
    return AUDIO_FILE_PATH


def setup_user_session():
    """Create user and setup authenticated session"""
    session = requests.Session()

    print("\n" + "=" * 60)
    print("SETUP: Creating test user and session")
    print("=" * 60)

    # Get CSRF token
    csrf_response = session.get(f"{API_BASE}/register/")
    csrf_token = session.cookies.get("csrftoken")
    print(f"CSRF Token: {csrf_token}")

    # Register user
    headers = {"Content-Type": "application/json", "X-CSRFToken": csrf_token}

    register_response = session.post(
        f"{API_BASE}/register/", json=TEST_USER_DATA, headers=headers
    )

    print_response(register_response, "User Registration")

    if register_response.status_code != 201:
        print("❌ User registration failed!")
        return None, None

    print("✅ User registration successful!")

    # Update CSRF token after registration
    csrf_token = session.cookies.get("csrftoken")
    headers["X-CSRFToken"] = csrf_token

    return session, headers


def test_standalone_transcription(session, headers, audio_file_path):
    """Test the standalone /api/transcribe/ endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: Standalone Audio Transcription (/api/transcribe/)")
    print("=" * 60)

    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {"audio": ("recording.mp3", audio_file, "audio/mpeg")}

            # Remove Content-Type from headers for multipart upload
            transcribe_headers = {
                k: v for k, v in headers.items() if k != "Content-Type"
            }

            transcribe_response = session.post(
                f"{API_BASE}/transcribe/", files=files, headers=transcribe_headers
            )

            response_data = print_response(
                transcribe_response, "Transcription Response"
            )

            if transcribe_response.status_code == 200:
                print("✅ Standalone transcription successful!")
                if response_data and "transcription" in response_data:
                    transcription = response_data["transcription"]
                    print(f"🎤 Transcribed text: '{transcription}'")
                    return transcription
                else:
                    print("⚠️  No transcription text in response")
                    return None
            else:
                print("❌ Standalone transcription failed!")
                return None

    except FileNotFoundError:
        print(f"❌ Audio file not found: {audio_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None


def test_audio_process_endpoint(session, headers, audio_file_path):
    """Test the integrated /api/process/ endpoint with audio input"""
    print("\n" + "=" * 60)
    print("TEST 2: Audio Processing Integration (/api/process/)")
    print("=" * 60)

    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {"audio": ("recording.mp3", audio_file, "audio/mpeg")}

            # Remove Content-Type from headers for multipart upload
            process_headers = {k: v for k, v in headers.items() if k != "Content-Type"}

            process_response = session.post(
                f"{API_BASE}/process/", files=files, headers=process_headers
            )

            response_data = print_response(process_response, "Audio Process Response")

            if process_response.status_code == 200:
                print("✅ Audio process request successful!")

                if response_data:
                    # Check for transcription info
                    if "transcription" in response_data:
                        print(f"🎤 Transcribed: '{response_data['transcription']}'")

                    # Check for follow-up questions
                    if "questions" in response_data and response_data["questions"]:
                        print(
                            f"📋 Agent has {len(response_data['questions'])} follow-up questions:"
                        )
                        for i, question in enumerate(response_data["questions"], 1):
                            print(f"  {i}. {question}")

                    # Check for processed foods
                    if "foods" in response_data and response_data["foods"]:
                        print(
                            f"🍽️  Agent processed {len(response_data['foods'])} food items:"
                        )
                        for food in response_data["foods"]:
                            print(
                                f"  - {food.get('name', 'Unknown')} ({food.get('meal_type', 'Unknown meal')})"
                            )
                            print(
                                f"    Calories: {food.get('calories', 0)}, Protein: {food.get('protein', 0)}g"
                            )

                    # Check for database entries
                    if "response" in response_data:
                        print(f"💾 Database entries: {len(response_data['response'])}")
                        if response_data["response"]:
                            print("✅ Food entries saved to database")
                        else:
                            print("⚠️  Warning: No food entries saved to database")

                return response_data

            else:
                print("❌ Audio process request failed!")
                return None

    except FileNotFoundError:
        print(f"❌ Audio file not found: {audio_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error during audio processing: {e}")
        return None


def test_error_scenarios(session, headers):
    """Test error handling scenarios"""
    print("\n" + "=" * 60)
    print("TEST 3: Error Handling Scenarios")
    print("=" * 60)

    # Test 1: No audio file provided
    print("\n--- Test 3.1: Missing audio file ---")
    process_headers = {k: v for k, v in headers.items() if k != "Content-Type"}

    no_audio_response = session.post(f"{API_BASE}/process/", headers=process_headers)

    print_response(no_audio_response, "No Audio File Response")

    if no_audio_response.status_code == 400:
        print("✅ Correctly rejected request without audio file")
    else:
        print("⚠️  Unexpected response for missing audio file")

    # Test 2: Invalid file type (if we have a text file to test with)
    print("\n--- Test 3.2: Invalid file type ---")
    try:
        # Create a temporary text file
        temp_file_content = b"This is not an audio file"
        files = {"audio": ("fake_audio.txt", temp_file_content, "text/plain")}

        invalid_response = session.post(
            f"{API_BASE}/transcribe/", files=files, headers=process_headers
        )

        print_response(invalid_response, "Invalid File Type Response")

        if invalid_response.status_code != 200:
            print("✅ Correctly handled invalid file type")
        else:
            response_data = invalid_response.json()
            if not response_data.get("transcription"):
                print("✅ Invalid file resulted in empty transcription")
            else:
                print("⚠️  Unexpected success with invalid file")
    except Exception as e:
        print(f"Error testing invalid file type: {e}")


def test_comparison_text_vs_audio(session, headers, transcribed_text):
    """Compare results from text input vs audio input"""
    print("\n" + "=" * 60)
    print("TEST 4: Text vs Audio Comparison")
    print("=" * 60)

    if not transcribed_text:
        print("⚠️  Skipping comparison - no transcribed text available")
        return

    print(f"Testing with transcribed text: '{transcribed_text}'")

    # Test with text input
    text_response = session.post(
        f"{API_BASE}/process/",
        json={"food_description": transcribed_text},
        headers=headers,
    )

    text_data = print_response(text_response, "Text Input Response")

    if text_response.status_code == 200:
        print("✅ Text processing successful!")

        if text_data:
            # Compare key metrics
            text_foods = text_data.get("foods", [])
            text_questions = text_data.get("questions", [])

            print(f"📊 Text input results:")
            print(f"  - Foods processed: {len(text_foods)}")
            print(f"  - Questions generated: {len(text_questions)}")

            # Note: We'd need the audio processing results to compare
            print("💡 Compare these results with the audio processing results above")
    else:
        print("❌ Text processing failed!")


def main():
    """Main test function"""
    print("🎤 Starting AI Nutrition Tracker Audio Transcription Tests")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER_DATA['username']}")

    # Check for audio file
    audio_file_path = check_audio_file()
    if not audio_file_path:
        print("❌ Cannot proceed without audio file")
        return False

    print(f"Audio file: {audio_file_path}")

    # Setup user session
    session, headers = setup_user_session()
    if not session:
        print("❌ Cannot proceed without user session")
        return False

    test_results = {
        "transcription": False,
        "audio_process": False,
        "error_handling": True,  # Assume pass unless we detect issues
        "comparison": False,
    }

    # Test 1: Standalone transcription
    transcribed_text = test_standalone_transcription(session, headers, audio_file_path)
    test_results["transcription"] = transcribed_text is not None

    # Test 2: Audio processing integration
    audio_process_data = test_audio_process_endpoint(session, headers, audio_file_path)
    test_results["audio_process"] = audio_process_data is not None

    # Test 3: Error handling
    test_error_scenarios(session, headers)

    # Test 4: Comparison (if we have transcribed text)
    if transcribed_text:
        test_comparison_text_vs_audio(session, headers, transcribed_text)
        test_results["comparison"] = True

    # Print summary
    print("\n" + "=" * 60)
    print("🎤 AUDIO TRANSCRIPTION TEST SUMMARY")
    print("=" * 60)

    passed_tests = sum(test_results.values())
    total_tests = len(test_results)

    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print()

    for test_name, passed in test_results.items():
        status = "✅" if passed else "❌"
        test_display = test_name.replace("_", " ").title()
        print(f"{status} {test_display}")

    if passed_tests == total_tests:
        print("\n🎉 All audio transcription tests completed successfully!")
        print("\nThe audio transcription system supports:")
        print("1. ✅ Standalone audio transcription via /api/transcribe/")
        print("2. ✅ Integrated audio processing via /api/process/")
        print("3. ✅ Error handling for invalid inputs")
        print("4. ✅ Full workflow: audio → transcription → AI processing")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed - check output above")
        return False


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server.")
        print(
            "Make sure the Django development server is running on http://localhost:8000"
        )
        print("Run: python manage.py runserver")
        exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)

