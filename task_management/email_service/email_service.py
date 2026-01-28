from django.core.mail import send_mail
from django.conf import settings

from task_management.interactors.email_service_interface.email_service_interface import \
    EmailServiceInterface


class EmailService(EmailServiceInterface):
    """
    Email service using Django's built-in email system.
    This respects EMAIL_BACKEND setting (console or smtp).
    """

    def send_password_reset_email(self, email: str, reset_link: str) -> bool:
        try:
            subject = "Password Reset Request"

            # Plain text message
            message = f"""
Hi,

You requested to reset your password. Click the link below to reset it:

{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Task Management Team
            """

            # HTML message
            html_message = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #333;">Password Reset Request</h2>
    <p>Hi,</p>
    <p>You requested to reset your password.</p>
    <p style="margin: 30px 0;">
        <a href="{reset_link}" 
           style="display: inline-block; 
                  padding: 12px 24px; 
                  background-color: #007bff; 
                  color: white; 
                  text-decoration: none; 
                  border-radius: 5px;">
            Reset Password
        </a>
    </p>
    <p>Or copy and paste this link:</p>
    <p style="word-break: break-all; color: #007bff;">{reset_link}</p>
    <p><strong>This link will expire in 1 hour.</strong></p>
    <p>If you didn't request this, please ignore this email.</p>
    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666;">Best regards,<br>Task Management Team</p>
</body>
</html>
            """

            # Send email using Django's system
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )

            # print(f"✅ Email sent successfully to {email}")
            return result > 0

        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False

