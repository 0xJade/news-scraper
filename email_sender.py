import os
import emails
from typing import Optional, List, Union
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    """
    A secure email sender class that uses environment variables for credentials.
    
    Required environment variables:
    - EMAIL_HOST: SMTP server (e.g., 'smtp.gmail.com')
    - EMAIL_PORT: SMTP port (e.g., 587 for TLS, 465 for SSL)
    - EMAIL_USER: Your email address
    - EMAIL_PASSWORD: Your email password or app-specific password
    - EMAIL_USE_TLS: 'true' or 'false' (optional, defaults to True)
    """
    
    def __init__(self):
        """Initialize the EmailSender with credentials from environment variables."""
        try:
            self.host = os.getenv('EMAIL_HOST')

            if not self.host:
                raise ValueError("EMAIL_HOST environment variable is not set")
            
            port_str = os.getenv('EMAIL_PORT', '587')
            try:
                self.port = int(port_str)
                if self.port <= 0 or self.port > 65535:
                    raise ValueError(f"Invalid port number: {self.port}")
            except ValueError:
                raise ValueError(f"EMAIL_PORT must be a valid integer, got: {port_str}")
            
            self.username = os.getenv('EMAIL_USER')

            if not self.username:
                raise ValueError("EMAIL_USER environment variable is not set")
            
            self.password = os.getenv('EMAIL_PASSWORD')
            if not self.password:
                raise ValueError("EMAIL_PASSWORD environment variable is not set")
            
            tls_str = os.getenv('EMAIL_USE_TLS', 'true')
            if tls_str.lower() not in ['true', 'false']:
                print(f"Warning: EMAIL_USE_TLS should be 'true' or 'false', got: {tls_str}. Defaulting to True.")
                self.use_tls = True
            else:
                self.use_tls = tls_str.lower() == 'true'
                
        except Exception as e:
            raise ValueError(f"Failed to initialize EmailSender: {str(e)}")
    
    def send_email(
        self, 
        to: Union[str, List[str]], 
        subject: str, 
        message: str,
        is_html: bool = False,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        from_name: Optional[str] = None,
        attachments: Optional[Union[str, List[str]]] = None
    ) -> bool:
        """
        Send an email to the specified recipient(s).
        
        Args:
            to: Recipient email address(es) - string or list of strings
            subject: Email subject line
            message: Email body content
            is_html: Whether the message is HTML (default: False for plain text)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            from_name: Custom sender name (optional)
            attachments: File path(s) to attach - string or list of strings (optional)
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Input validation
            if not to:
                raise ValueError("Recipient email address is required")
            if not subject or not subject.strip():
                raise ValueError("Email subject is required")
            if not message or not message.strip():
                raise ValueError("Email message content is required")
            
            # Validate email format (basic check)
            if isinstance(to, str):
                if '@' not in to or '.' not in to:
                    raise ValueError(f"Invalid email format: {to}")
            elif isinstance(to, list):
                for email in to:
                    if not email or '@' not in email or '.' not in email:
                        raise ValueError(f"Invalid email format in list: {email}")
            
            # Determine sender address
            from_addr = f"{from_name} <{self.username}>" if from_name else self.username
            
            # Create the email message
            if is_html:
                email_message = emails.html(
                    subject=subject,
                    html=message,
                    mail_from=from_addr
                )
            else:
                email_message = emails.html(
                    subject=subject,
                    text=message,
                    mail_from=from_addr
                )
            
            # Add CC and BCC if provided
            if cc:
                email_message['Cc'] = cc
            if bcc:
                email_message['Bcc'] = bcc
            
            # Add attachments if provided
            if attachments:
                # Convert single attachment to list for consistent handling
                if isinstance(attachments, str):
                    attachments = [attachments]
                
                for attachment_path in attachments:
                    try:
                        if not attachment_path:
                            print(f"Warning: Empty attachment path provided")
                            continue
                            
                        if not os.path.exists(attachment_path):
                            print(f"Warning: Attachment file not found: {attachment_path}")
                            continue
                        
                        # Read file content and attach properly
                        with open(attachment_path, 'rb') as file:
                            file_content = file.read()
                            if file_content is None:
                                print(f"Warning: Could not read file content from: {attachment_path}")
                                continue
                            
                            # Get filename from path
                            filename = os.path.basename(attachment_path)
                            email_message.attach(filename=filename, data=file_content)
                            
                    except (IOError, OSError) as e:
                        print(f"Warning: Error reading attachment {attachment_path}: {e}")
                        continue
                    except Exception as e:
                        print(f"Warning: Unexpected error with attachment {attachment_path}: {e}")
                        continue
            
            # Configure SMTP settings
            smtp_config = {
                'host': self.host,
                'port': self.port,
                'user': self.username,
                'password': self.password,
                'tls': self.use_tls
            }
            
            # Send the email
            try:
                response = email_message.send(to=to, smtp=smtp_config)
                
                if response is None:
                    print("Warning: No response received from email server")
                    return False
                
                # Check if email was sent successfully
                if hasattr(response, 'status_code'):
                    if response.status_code == 250:
                        print(f"✅ Email sent successfully to {to}")
                        return True
                    else:
                        print(f"❌ Email server returned status code: {response.status_code}")
                        print(f"response: {response}")
                        return False
                else:
                    print(f"Warning: Unexpected response format from email server: {type(response)}")
                    return False
                    
            except ConnectionError as e:
                print(f"❌ Connection error: Could not connect to SMTP server {self.host}:{self.port}")
                print(f"   Error details: {str(e)}")
                return False
            except TimeoutError as e:
                print(f"❌ Timeout error: SMTP server {self.host}:{self.port} did not respond in time")
                print(f"   Error details: {str(e)}")
                return False
            except Exception as e:
                print(f"❌ SMTP error: {str(e)}")
                return False
            
        except ValueError as e:
            print(f"❌ Validation error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            return False
    
    def send_simple_email(self, to: str, subject: str, message: str, attachments: Optional[Union[str, List[str]]] = None) -> bool:
        """
        Simplified method to send a plain text email to a single recipient.
        
        Args:
            to: Recipient email address
            subject: Email subject line
            message: Plain text message body
            attachments: File path(s) to attach - string or list of strings (optional)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        return self.send_email(to=to, subject=subject, message=message, is_html=False, attachments=attachments)
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection without sending an email.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            import smtplib
            
            print(f"🔍 Testing SMTP connection to {self.host}:{self.port}...")
            
            if self.use_tls:
                server = smtplib.SMTP(self.host, self.port, timeout=10)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.host, self.port, timeout=10)
            server.login(self.username, self.password)
            server.quit()
            
            print(f"✅ SMTP connection test successful!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"❌ Authentication failed: Check your EMAIL_USER and EMAIL_PASSWORD")
            return False
        except smtplib.SMTPConnectError:
            print(f"❌ Connection failed: Could not connect to {self.host}:{self.port}")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Connection test failed: {str(e)}")
            return False
    
    def get_config_summary(self) -> str:
        """
        Get a summary of the current email configuration.
        
        Returns:
            str: Configuration summary
        """
        return f"""
📧 Email Configuration Summary:
   Host: {self.host}
   Port: {self.port}
   Username: {self.username}
   Use TLS: {self.use_tls}
   Password: {'*' * len(self.password) if self.password else 'Not set'}
        """.strip()


# Example usage with enhanced error handling:
if __name__ == "__main__":
    try:
        # First, set your environment variables:
        # export EMAIL_HOST="smtp.gmail.com"
        # export EMAIL_PORT="587"
        # export EMAIL_USER="your_email@gmail.com"
        # export EMAIL_PASSWORD="your_app_password"
        # export EMAIL_USE_TLS="true"
        
        # Create sender instance with error handling
        sender = EmailSender()
        
        # Show configuration summary
        print(sender.get_config_summary())
        
        # Test connection before sending
        if not sender.test_connection():
            print("❌ Connection test failed. Please check your configuration.")
            exit(1)
        
        # Send a simple text email with PDF attachment
        success = sender.send_simple_email(
            to="recipient@example.com",
            subject="Test Email with PDF",
            message="Hello! Please find the attached PDF.",
            attachments="path/to/document.pdf"
        )
        
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email.")
        
        # Example with error handling for attachments
        try:
            success = sender.send_simple_email(
                to="recipient@example.com",
                subject="Multiple Attachments",
                message="Hello! Multiple files attached.",
                attachments=["document1.pdf", "image.jpg", "data.xlsx"]
            )
        except Exception as e:
            print(f"❌ Error sending email with attachments: {e}")
        
        # Send an HTML email with CC
        success = sender.send_email(
            to=["recipient1@example.com", "recipient2@example.com"],
            subject="HTML Test Email",
            message="<h1>Hello!</h1><p>This is an <b>HTML</b> message.</p>",
            is_html=True,
            cc="cc_recipient@example.com",
            from_name="Your Name"
        )
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your environment variables:")
        print("  - EMAIL_HOST")
        print("  - EMAIL_PORT") 
        print("  - EMAIL_USER")
        print("  - EMAIL_PASSWORD")
        print("  - EMAIL_USE_TLS (optional)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")