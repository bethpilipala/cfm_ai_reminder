import json
import time

from google import genai
from google.genai import types, errors
from secret_manager import get_secret
from dotenv import load_dotenv

load_dotenv()

api_key = get_secret(
    "GEMINI_API_KEY"
)

if api_key is None:
    raise RuntimeError(
        "GEMINI_API_KEY was not found in the environment."
    )

_client = genai.Client(api_key=api_key)


def generate_json(
    prompt: str,
    request: dict,
) -> dict:
    """
    Sends a request to Gemini and returns the JSON response.
    """

    full_prompt = (
        f"{prompt}\n\n"
        "Input JSON:\n"
        f"{json.dumps(request, indent=2, ensure_ascii=False)}"
    )

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):

        try:
            response = _client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )

            break

        except errors.ServerError as error:

            if attempt == max_attempts:
                raise RuntimeError(
                    "Gemini server unavailable after "
                    f"{max_attempts} attempts."
                ) from error

            wait_time = attempt * 2

            print(
                f"Gemini unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


        except errors.ClientError as error:

            if error.code == 400:
                raise RuntimeError(
                    "Gemini API rejected the request. "
                    "Check that your API key is valid."
                ) from error

            raise RuntimeError(
                "Gemini API request failed."
            ) from error

    print("\nGemini Response:")
    print(response.text)

    if response.text is None:
        raise ValueError(
            "Gemini returned an empty response."
        )

    try:
        return json.loads(response.text)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned invalid JSON."
        ) from error