import smtplib
from email.message import EmailMessage

from app.config import get_settings


def send_otp_email(to_email: str, otp: str):
    settings = get_settings()

    message = EmailMessage()
    message["Subject"] = "Your Login OTP"
    message["From"] = settings.smtp_username
    message["To"] = to_email

    message.set_content(
        f"Your OTP for login is: {otp}\n\n"
        f"This OTP will expire in {settings.otp_expiry_minutes} minutes."
    )

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)