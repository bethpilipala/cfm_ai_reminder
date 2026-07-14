from bs4 import BeautifulSoup
import re

from models import Lesson, LessonWeek
from utils import parse_date_range


def parse_lesson(
    html: str,
    lesson_number: int,
    lesson_url: str,
    year: int
) -> Lesson:
    """
    Parses a Come, Follow Me lesson page.

    Parameters
    ----------
    html : str
        HTML contents of the lesson page.
    lesson_number : int
        Lesson number (1-52).
    lesson_url : str
        Full lesson URL.
    year : int
        Year of the Come, Follow Me manual.

    Returns
    -------
    Lesson
        Parsed lesson information.

    Raises
    ------
    Exception
        If the page cannot be parsed.
    """

    try:
        soup = BeautifulSoup(html, "html.parser")

        if soup.title is None or soup.title.string is None:
            raise Exception("No <title> element found.")

        page_title = soup.title.string.strip()

        # Expected format:
        # July 6–12. “There Is a Prophet in Israel”: 2 Kings 2–7

        # Split into date range and the remainder.
        parts = page_title.split(". ", maxsplit=1)

        if len(parts) != 2:
            raise Exception(f"Unexpected page title format: {page_title}")

        date_range = parts[0]
        remainder = parts[1]

        # Split the remainder into title and scripture assignment.
        parts = remainder.rsplit(": ", maxsplit=1)

        if len(parts) != 2:
            raise Exception(f"Unexpected page title format: {page_title}")

        title = parts[0].strip("“”\"")
        scripture_assignment = parts[1]

        start_date, end_date = parse_date_range(date_range, year)

        week = LessonWeek(
            display=date_range,
            start=start_date,
            end=end_date
        )

        return Lesson(
            lesson_number=lesson_number,
            year=year,
            week=week,
            title=title,
            scripture_assignment=scripture_assignment,
            lesson_url=lesson_url
        )

    except Exception as e:
        raise Exception(f"Unable to parse lesson page.\n{e}")