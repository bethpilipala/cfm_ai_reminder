import re

from config_loader import get_manual_base_url
from lesson_fetcher import download_lesson
from lesson_parser import parse_lesson


def main():

    base_url = get_manual_base_url()

    # Extract the manual year from the URL.
    match = re.search(r"(\d{4})$", base_url)

    if match is None:
        raise Exception("Unable to determine manual year from the base URL.")

    year = int(match.group(1))

    lesson_number = 28

    lesson_url = f"{base_url}/{lesson_number:02}?lang=eng"

    print(f"Downloading:\n{lesson_url}\n")

    html = download_lesson(lesson_url)

    lesson = parse_lesson(
        html,
        lesson_number,
        lesson_url,
        year
    )

    print(lesson)
    print()

    print(f"Lesson     : {lesson.lesson_number}")
    print(f"Year       : {lesson.year}")
    print(f"Week       : {lesson.week.display}")
    print(f"Start Date : {lesson.week.start}")
    print(f"End Date   : {lesson.week.end}")
    print(f"Title      : {lesson.title}")
    print(f"Assignment : {lesson.scripture_assignment}")


if __name__ == "__main__":
    main()