#!/usr/bin/env python3
"""
Test script for multiple email recipients functionality
"""

from email_sender import EmailSender

def test_multiple_recipients():
    """Test the multiple recipients functionality"""
    
    print("🧪 Testing Multiple Recipients Functionality")
    print("=" * 50)
    
    try:
        # Initialize the email sender
        sender = EmailSender()
        
        # Show configuration summary
        print("📧 Email Configuration:")
        print(f"   Default Recipients: {sender.default_recipients}")
        print()
        
        if not sender.default_recipients:
            print("⚠️  No default recipients configured in .env file")
            print("💡 Add EMAIL_RECIPIENTS to your .env file like:")
            print("   EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com")
            return
        
        # Test sending to default recipients
        print(f"📧 Sending test email to {len(sender.default_recipients)} recipient(s)...")
        success = sender.send_to_default_recipients(
            subject="Test Email - Multiple Recipients",
            message="This is a test email sent to multiple recipients configured in your .env file.",
        )
        
        if success:
            print("✅ Test email sent successfully!")
        else:
            print("❌ Failed to send test email")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multiple_recipients()
