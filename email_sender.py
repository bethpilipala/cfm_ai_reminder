import smtplib

from email.message import EmailMessage
from secret_manager import get_secret

from dotenv import load_dotenv


load_dotenv()


def send_email(
    subject: str,
    body: str,
) -> None:
    """
    Sends an email notification.
    """

    sender = get_secret(
        "EMAIL_ADDRESS"
    )

    password = get_secret(
        "EMAIL_APP_PASSWORD"
    )

    recipients = get_secret(
        "EMAIL_RECIPIENTS"
    ).split(",")

    recipients = [
        email.strip()
        for email in recipients
        if email.strip()
    ]

    if not sender or not password or not recipients:
        raise RuntimeError(
            "Email environment variables are missing."
        )

    email_message = EmailMessage()

    email_message["Subject"] = subject
    email_message["From"] = sender
    email_message["Bcc"] = ", ".join(recipients)

    email_message.set_content(body)

    with smtplib.SMTP(
        "smtp.gmail.com",
        587,
    ) as smtp:

        smtp.starttls()

        smtp.login(
            sender,
            password,
        )

        smtp.send_message(email_message)

    print("Email sent successfully.")