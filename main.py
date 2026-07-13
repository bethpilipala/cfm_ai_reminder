from config_loader import get_manual_base_url
from lesson_fetcher import download_lesson


def main():

    base_url = get_manual_base_url()

    lesson_number = 28

    lesson_url = f"{base_url}/{lesson_number:02}?lang=eng"

    print(f"Downloading:\n{lesson_url}\n")

    html = download_lesson(lesson_url)

    print(html[:1000])


if __name__ == "__main__":
    main()