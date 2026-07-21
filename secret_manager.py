import os

import boto3  # type: ignore
from dotenv import load_dotenv

from config_loader import load_config


load_dotenv()

config = load_config()


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
) -> str:
    """
    Retrieves a secret.

    Local:
        Reads from .env

    AWS Lambda:
        Reads from AWS Parameter Store.
    """

    if running_in_lambda():

        parameter_name = (
            config["aws_parameter_store"]
                  [env_name]
        )

        ssm = boto3.client(
            "ssm",
            region_name=config["aws_region"],
        )

        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True,
        )

        return response["Parameter"]["Value"]

    value = os.getenv(env_name)

    if value is None:
        raise RuntimeError(
            f"Missing environment variable: {env_name}"
        )

    return value