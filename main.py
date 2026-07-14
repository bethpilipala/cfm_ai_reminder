from config_loader import get_manual_base_url
from lesson_fetcher import download_lesson
from lesson_parser import parse_lesson


def main():

    base_url = get_manual_base_url()

    lesson_number = 28

    lesson_url = f"{base_url}/{lesson_number:02}?lang=eng"

    print(f"Downloading:\n{lesson_url}\n")

    html = download_lesson(lesson_url)

    lesson = parse_lesson(
        html,
        lesson_number,
        lesson_url
    )

    print(lesson)
    print()

    print(f"Date Range : {lesson.date_range}")
    print(f"Title      : {lesson.title}")
    print(f"Assignment : {lesson.scripture_assignment}")

if __name__ == "__main__":
    main()