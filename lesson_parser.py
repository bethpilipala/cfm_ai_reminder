from bs4 import BeautifulSoup

from models import Lesson


def parse_lesson(
    html: str,
    lesson_number: int,
    lesson_url: str
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
        Full URL of the lesson.

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

        # -------------------------
        # Extract the page title
        # -------------------------
        if soup.title is None or soup.title.string is None:
            raise Exception("No <title> element found.")

        page_title = soup.title.string.strip()

        # Example:
        # "July 6–12. “There Is a Prophet in Israel”"

        if ". " not in page_title:
            raise Exception("Unexpected page title format.")

        date_range, title = page_title.split(". ", maxsplit=1)

        # Remove smart quotes if present
        title = title.strip("“”\"")

        # -------------------------
        # Scripture assignment
        #
        # We'll implement this next after
        # inspecting the page structure.
        # -------------------------
        scripture_assignment = ""

        return Lesson(
            lesson_number=lesson_number,
            date_range=date_range,
            title=title,
            scripture_assignment=scripture_assignment,
            lesson_url=lesson_url
        )

    except Exception as e:
        raise Exception(f"Unable to parse lesson page.\n{e}")