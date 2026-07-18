from config_loader import load_config
from email_sender import send_email
from sns_sender import send_sms


def send_notification(
    subject: str,
    message: str,
) -> None:
    """
    Sends a notification using all configured methods.
    """

    config = load_config()

    methods = config["notification_methods"]

    for method in methods:

        if method == "email":
            send_email(subject, message)

        elif method == "sms":
            send_sms(subject, message)

        else:
            print(
                f"Unknown notification method: {method}"
            )