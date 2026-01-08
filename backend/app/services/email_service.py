"""
SendGrid Email Service
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from typing import Dict, Optional
from datetime import datetime

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "SG...")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@phonicslearn.com")
SENDER_NAME = os.getenv("SENDER_NAME", "PhonicsLearn")

sg = SendGridAPIClient(SENDGRID_API_KEY)

# Email templates
EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to PhonicsLearn! 🎉",
        "template_id": os.getenv("SENDGRID_TEMPLATE_WELCOME"),
    },
    "license_key": {
        "subject": "Your PhonicsLearn License Key",
        "template_id": os.getenv("SENDGRID_TEMPLATE_LICENSE"),
    },
    "trial_reminder": {
        "subject": "Your PhonicsLearn Trial Ends Soon",
        "template_id": os.getenv("SENDGRID_TEMPLATE_TRIAL_REMINDER"),
    },
    "expiration": {
        "subject": "Your PhonicsLearn License Has Expired",
        "template_id": os.getenv("SENDGRID_TEMPLATE_EXPIRATION"),
    },
    "payment_success": {
        "subject": "Payment Successful - PhonicsLearn",
        "template_id": os.getenv("SENDGRID_TEMPLATE_PAYMENT_SUCCESS"),
    },
}

async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    template_data: Optional[Dict] = None
) -> Dict:
    """
    Send a basic email using SendGrid
    """
    try:
        message = Mail(
            from_email=Email(SENDER_EMAIL, SENDER_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        response = sg.send(message)
        
        return {
            "success": True,
            "status_code": response.status_code,
            "message_id": response.headers.get("X-Message-Id")
        }
    except Exception as e:
        print(f"Error sending email: {e}")
        return {
            "success": False,
            "error": str(e)
        }

async def send_welcome_email(to_email: str, user_name: str) -> Dict:
    """
    Send welcome email to new user
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Welcome to PhonicsLearn!</h1>
            </div>
            <div class="content">
                <h2>Hi {user_name}!</h2>
                <p>Thank you for joining PhonicsLearn. We're excited to help your children master phonics!</p>
                <p><strong>Here's what you can do next:</strong></p>
                <ul>
                    <li>Explore our 81+ interactive lessons</li>
                    <li>Track your child's progress in real-time</li>
                    <li>Access personalized learning recommendations</li>
                </ul>
                <a href="http://localhost:3000/license-activation.html" class="button">Get Started →</a>
                <p>If you have any questions, feel free to reach out to our support team.</p>
            </div>
            <div class="footer">
                <p>© 2025 PhonicsLearn. All rights reserved.</p>
                <p>Questions? Email us at support@phonicslearn.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, "Welcome to PhonicsLearn! 🎉", html_content)

async def send_license_key_email(to_email: str, license_key: str, license_type: str, days_valid: int) -> Dict:
    """
    Send license key to user
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .license-box {{ background: white; border: 2px dashed #667eea; padding: 20px;
                           text-align: center; margin: 20px 0; border-radius: 8px; }}
            .license-key {{ font-size: 20px; font-weight: bold; color: #667eea; 
                           letter-spacing: 2px; margin: 10px 0; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔑 Your PhonicsLearn License Key</h1>
            </div>
            <div class="content">
                <h2>Congratulations!</h2>
                <p>Your <strong>{license_type}</strong> license is ready.</p>
                
                <div class="license-box">
                    <p>Your License Key:</p>
                    <div class="license-key">{license_key}</div>
                    <p style="font-size: 12px; color: #666;">Valid for {days_valid} days</p>
                </div>
                
                <p><strong>How to activate:</strong></p>
                <ol>
                    <li>Click the button below</li>
                    <li>Enter your license key</li>
                    <li>Start learning immediately!</li>
                </ol>
                
                <a href="http://localhost:3000/license-activation.html" class="button">Activate License →</a>
                
                <p style="margin-top: 30px; font-size: 14px; color: #666;">
                    <strong>Important:</strong> Save this email! You'll need your license key to access the app.
                </p>
            </div>
            <div class="footer">
                <p>© 2025 PhonicsLearn. All rights reserved.</p>
                <p>Need help? Contact support@phonicslearn.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, "Your PhonicsLearn License Key 🔑", html_content)

async def send_trial_reminder_email(to_email: str, days_remaining: int, license_key: str) -> Dict:
    """
    Send reminder that trial is ending soon
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #ff9800 0%, #ff5722 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .alert {{ background: #fff3cd; border: 2px solid #ffc107; padding: 15px;
                     border-radius: 8px; margin: 20px 0; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⏰ Your Trial Ends in {days_remaining} Days</h1>
            </div>
            <div class="content">
                <div class="alert">
                    <strong>Don't lose access!</strong> Your free trial is ending soon.
                </div>
                
                <p>We hope you've enjoyed exploring PhonicsLearn with your children!</p>
                
                <p><strong>What happens next?</strong></p>
                <ul>
                    <li>Your trial expires in {days_remaining} days</li>
                    <li>Upgrade now to keep all your progress</li>
                    <li>Choose from flexible monthly or yearly plans</li>
                </ul>
                
                <a href="http://localhost:3000/landing.html#pricing" class="button">View Plans & Upgrade →</a>
                
                <p style="margin-top: 30px;">
                    <strong>Questions?</strong> Our team is here to help you choose the right plan.
                </p>
            </div>
            <div class="footer">
                <p>© 2025 PhonicsLearn. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, f"Your Trial Ends in {days_remaining} Days ⏰", html_content)

async def send_expiration_email(to_email: str, license_type: str) -> Dict:
    """
    Send notification that license has expired
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #f44336; color: white; padding: 30px; text-align: center; 
                       border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your License Has Expired</h1>
            </div>
            <div class="content">
                <p>Your <strong>{license_type}</strong> license has expired.</p>
                
                <p><strong>Don't worry - your progress is saved!</strong></p>
                <p>Renew your license to continue where you left off.</p>
                
                <a href="http://localhost:3000/landing.html#pricing" class="button">Renew License →</a>
                
                <p>We'd love to have you back. Contact us if you have any questions.</p>
            </div>
            <div class="footer">
                <p>© 2025 PhonicsLearn. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, "Your PhonicsLearn License Has Expired", html_content)

async def send_payment_success_email(to_email: str, amount: float, plan_type: str, license_key: str) -> Dict:
    """
    Send payment confirmation email
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .success-box {{ background: #e8f5e9; border: 2px solid #4caf50; padding: 20px;
                           border-radius: 8px; margin: 20px 0; }}
            .license-key {{ font-size: 18px; font-weight: bold; color: #667eea; 
                           letter-spacing: 2px; margin: 10px 0; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Payment Successful!</h1>
            </div>
            <div class="content">
                <div class="success-box">
                    <h2 style="margin-top: 0; color: #4caf50;">Thank You!</h2>
                    <p>Your payment of <strong>${amount}</strong> for <strong>{plan_type}</strong> has been processed.</p>
                </div>
                
                <p><strong>Your License Key:</strong></p>
                <div class="license-key">{license_key}</div>
                
                <p><strong>What's Next?</strong></p>
                <ul>
                    <li>Your license is now active</li>
                    <li>Access all features immediately</li>
                    <li>Receipt sent to this email</li>
                </ul>
                
                <a href="http://localhost:3000/index.html" class="button">Start Learning →</a>
            </div>
            <div class="footer">
                <p>© 2025 PhonicsLearn. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, "Payment Successful - PhonicsLearn ✅", html_content)
