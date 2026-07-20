import os

import boto3 #type: ignore
from dotenv import load_dotenv


load_dotenv()


def running_in_lambda() -> bool:
    """
    Determines whether the application is running in AWS Lambda.
    """

    return bool(
        os.getenv(
            "AWS_LAMBDA_FUNCTION_NAME"
        )
    )


def get_secret(
    env_name: str,
    parameter_name: str,
) -> str:
    """
    Retrieves a secret.

    Local:
        Reads from .env

    AWS Lambda:
        Reads from AWS Parameter Store
    """

    if running_in_lambda():

        ssm = boto3.client(
            "ssm"
        )

        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True,
        )

        return response["Parameter"]["Value"]

    else:

        value = os.getenv(
            env_name
        )

        if value is None:
            raise RuntimeError(
                f"Missing environment variable: {env_name}"
            )

        return value