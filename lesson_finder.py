from datetime import date
import re

from config_loader import get_manual_base_url
from lesson_fetcher import download_lesson
from lesson_parser import parse_lesson
from models import Lesson
from utils import build_lesson_url


def get_manual_year(base_url: str) -> int:
    """
    Extracts the manual year from the base URL.
    """

    match = re.search(r"(\d{4})$", base_url)

    if match is None:
        raise Exception("Unable to determine manual year from the base URL.")

    return int(match.group(1))


def find_lesson(lesson_number: int) -> Lesson:
    """
    Downloads and parses a specific lesson.
    """

    base_url = get_manual_base_url()

    year = get_manual_year(base_url)

    lesson_url = build_lesson_url(base_url, lesson_number)

    html = download_lesson(lesson_url)

    return parse_lesson(
        html,
        lesson_number,
        lesson_url,
        year
    )


def find_current_lesson() -> Lesson:
    """
    Finds the current week's lesson.
    """

    today = date.today()

    for lesson_number in range(1, 53):

        print(f"Checking lesson {lesson_number}...")

        lesson = find_lesson(lesson_number)

        if lesson.week.start <= today <= lesson.week.end:
            return lesson

    raise Exception("Unable to determine the current lesson.")