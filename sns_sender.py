import os

import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore
from dotenv import load_dotenv

from config_loader import load_config


load_dotenv()


def send_sms(title: str, message: str) -> None:
    """
    Sends an SMS message using AWS SNS.
    """

    config = load_config()

    phone_number = os.getenv(
        "PHONE_NUMBER"
    )

    if phone_number is None:
        raise RuntimeError(
            "PHONE_NUMBER was not found in environment variables."
        )
    
    if os.getenv("AWS_ACCESS_KEY_ID") is None:
        raise RuntimeError(
            "AWS credentials were not found. "
            "Check your .env file."
        )

    sns = boto3.client(
        "sns",
        region_name=config["aws_region"],
    )

    sms_message = (
        f"{title}\n\n"
        f"{message}"
    )

    try:
        response = sns.publish(
            PhoneNumber=phone_number,
            Message=sms_message,
        )

    except ClientError as error:
        raise RuntimeError(
            "Failed to send SMS notification."
        ) from error

    print(
        "SMS sent successfully."
    )

    print(
        f"Message ID: {response['MessageId']}"
    )