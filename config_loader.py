import json
from datetime import datetime
import requests


ROTATION = [
    "old-testament",
    "new-testament",
    "book-of-mormon",
    "doctrine-and-covenants"
]

BASE_URL = (
    "https://www.churchofjesuschrist.org/study/manual/"
    "come-follow-me-for-home-and-church-"
)


def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)


def predict_manual_url(year: int) -> str:
    """
    Predicts the Come, Follow Me manual URL using the known rotation.

    2026 = Old Testament
    """

    start_year = 2026

    index = (year - start_year) % len(ROTATION)

    manual = ROTATION[index]

    return f"{BASE_URL}{manual}-{year}"


def url_exists(url: str) -> bool:
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)

        if response.status_code == 405:
            response = requests.get(url, timeout=10)

        return response.status_code == 200

    except requests.RequestException:
        return False


def get_manual_base_url() -> str:
    config = load_config()

    year = str(datetime.now().year)

    manuals = config.get("manuals", {})

    if year in manuals:
        return manuals[year]["url"]

    predicted = predict_manual_url(int(year))

    if url_exists(predicted):
        return predicted

    raise Exception(f"No Come, Follow Me manual found for {year}.")