import boto3 # type: ignore
from dotenv import load_dotenv

load_dotenv()

sns = boto3.client(
    "sns",
    region_name="us-east-1",
)

response = sns.publish(
    PhoneNumber="+15555555555",
    Message="Testing Come Follow Me AI Reminder 🎉",
)

print(response)