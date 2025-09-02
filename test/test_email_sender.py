#!/usr/bin/env python3
"""
Test script for EmailSender with enhanced error handling
"""

import os
from email_sender import EmailSender
from dotenv import load_dotenv

load_dotenv()

def test_email_sender():
    """Test the EmailSender class with various scenarios"""
    
    print("🧪 Testing EmailSender with enhanced error handling...\n")
    
    # Test 1: Missing environment variables
    print("1️⃣ Testing with missing environment variables...")
    try:
        # Clear environment variables temporarily
        original_env = {}
        for key in ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USER', 'EMAIL_PASSWORD']:
            if key in os.environ:
                original_env[key] = os.environ[key]
                del os.environ[key]
        
        sender = EmailSender()
        print("❌ Should have failed - environment variables missing")
        
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")
    finally:
        # Restore environment variables
        for key, value in original_env.items():
            os.environ[key] = value
    
    # Test 2: Invalid port number
    print("\n2️⃣ Testing with invalid port number...")
    try:
        os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
        os.environ['EMAIL_PORT'] = '99999'  # Invalid port
        os.environ['EMAIL_USER'] = 'test@example.com'
        os.environ['EMAIL_PASSWORD'] = 'password123'
        
        sender = EmailSender()
        print("❌ Should have failed - invalid port")
        
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")
    
    # Test 3: Valid configuration
    print("\n3️⃣ Testing with valid configuration...")
    try:
        os.environ['EMAIL_PORT'] = '587'  # Valid port
        
        sender = EmailSender()
        print("✅ Configuration loaded successfully")
        print(sender.get_config_summary())
        
        # Test 4: Input validation
        print("\n4️⃣ Testing input validation...")
        
        # Test empty recipient
        success = sender.send_email(to="", subject="Test", message="Test")
        print(f"Empty recipient test: {'❌ Failed as expected' if not success else '✅ Should have failed'}")
        
        # Test empty subject
        success = sender.send_email(to="test@example.com", subject="", message="Test")
        print(f"Empty subject test: {'❌ Failed as expected' if not success else '✅ Should have failed'}")
        
        # Test empty message
        success = sender.send_email(to="test@example.com", subject="Test", message="")
        print(f"Empty message test: {'❌ Failed as expected' if not success else '✅ Should have failed'}")
        
        # Test invalid email format
        success = sender.send_email(to="invalid-email", subject="Test", message="Test")
        print(f"Invalid email test: {'❌ Failed as expected' if not success else '✅ Should have failed'}")
        
        # Test 5: Connection test (will likely fail without real credentials)
        print("\n5️⃣ Testing SMTP connection...")
        try:
            connection_success = sender.test_connection()
            if connection_success:
                print("✅ Connection test successful!")
            else:
                print("❌ Connection test failed (expected without real credentials)")
        except Exception as e:
            print(f"❌ Connection test error: {e}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    print("\n🎉 Error handling tests completed!")
    print("\n💡 Key improvements made:")
    print("   • Input validation for email addresses, subjects, and messages")
    print("   • Better attachment handling with file content reading")
    print("   • Specific error types (ConnectionError, TimeoutError, etc.)")
    print("   • Connection testing before sending emails")
    print("   • Detailed error messages with emojis for clarity")
    print("   • Graceful handling of missing or invalid attachments")

if __name__ == "__main__":
    test_email_sender()
