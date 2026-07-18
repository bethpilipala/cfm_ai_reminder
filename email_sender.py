import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()


def send_email(
    subject: str,
    body: str,
) -> None:
    """
    Sends an email notification.
    """

    sender = os.getenv(
        "EMAIL_ADDRESS"
    )

    password = os.getenv(
        "EMAIL_APP_PASSWORD"
    )

    recipient = os.getenv(
        "EMAIL_RECIPIENT"
    )

    if not sender or not password or not recipient:
        raise RuntimeError(
            "Email environment variables are missing."
        )

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    message.set_content(body)

    with smtplib.SMTP(
        "smtp.gmail.com",
        587,
    ) as smtp:

        smtp.starttls()

        smtp.login(
            sender,
            password,
        )

        smtp.send_message(message)

    print("Email sent successfully.")