import smtplib
from email.message import EmailMessage

from app.config import get_settings

def send_email(
    to_email: str,
    subject: str,
    body: str
):
    settings = get_settings()

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_username
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port
    ) as server:
        server.starttls()
        server.login(
            settings.smtp_username,
            settings.smtp_password
        )
        server.send_message(message)

def send_otp_email(to_email: str, otp: str):
    settings = get_settings()

    subject = "Your Login OTP"
    body = (
        f"Your OTP for login is: {otp}\n\n"
        f"This OTP will expire in "
        f"{settings.otp_expiry_minutes} minutes."
    )

    send_email(to_email, subject, body)

def send_invoice_status_email(
    to_email: str,
    invoice_number: str,
    status: str,
    message_text: str
):
    subject = f"Invoice {invoice_number}"

    body = (
        f"Invoice Number: {invoice_number}\n\n"
        f"{message_text}"
    )

    send_email(to_email, subject, body)