import json
import re

from models import ChapterInfo


BOOK_PATTERN = re.compile(r"^(.*?)\s+(\d+(?:–\d+)?)$")
RANGE_PATTERN = re.compile(r"^(\d+)–(\d+)$")
SINGLE_PATTERN = re.compile(r"^\d+$")

_DATA: dict[str, dict[str, int]] | None = None


def load_verse_counts() -> dict[str, dict[str, int]]:
    """
    Loads the verse-count database.

    The file is loaded only once.
    """

    global _DATA

    if _DATA is None:

        with open(
            "data/verse_counts.json",
            encoding="utf-8"
        ) as file:

            _DATA = json.load(file)

    return _DATA


def is_book_name(text: str) -> bool:
    """
    Returns True if the text exactly matches a book
    in the verse-count database.
    """

    return text in load_verse_counts()


def parse_scripture_assignment(scripture_assignment: str) -> list[ChapterInfo]:
    """
    Parses a Come, Follow, Me scripture assignment into
    a list of ChapterInfo objects.

    Supports:
        Genesis 37–41
        Proverbs 1–4; 15–16; 22
        Esther
        Nehemiah 11–13; Esther

    Returns an empty list if the assignment does not appear
    to reference scripture.
    """

    segments = [
        segment.strip()
        for segment in scripture_assignment.split(";")
    ]

    chapters: list[ChapterInfo] = []

    current_book = None

    verse_database = load_verse_counts()

    for segment in segments:

        #
        # Does this segment introduce a new book with
        # explicit chapter numbers?
        #
        match = BOOK_PATTERN.match(segment)

        if match:

            current_book = match.group(1)
            chapter_text = match.group(2)

        #
        # Is this segment simply an entire book?
        #
        elif is_book_name(segment):

            current_book = segment

            for chapter_number in sorted(
                verse_database[current_book].keys(),
                key=int
            ):

                chapters.append(
                    ChapterInfo(
                        book=current_book,
                        chapter=int(chapter_number)
                    )
                )

            continue

        #
        # Otherwise, assume it continues the previous book.
        #
        else:

            if current_book is None:
                # Not a scripture assignment.
                return []

            chapter_text = segment

        #
        # Single chapter
        #
        if SINGLE_PATTERN.fullmatch(chapter_text):

            chapters.append(
                ChapterInfo(
                    book=current_book,
                    chapter=int(chapter_text)
                )
            )

            continue

        #
        # Chapter range
        #
        match = RANGE_PATTERN.fullmatch(chapter_text)

        if match:

            start = int(match.group(1))
            end = int(match.group(2))

            for chapter in range(start, end + 1):

                chapters.append(
                    ChapterInfo(
                        book=current_book,
                        chapter=chapter
                    )
                )

            continue

        #
        # Unknown format.
        #
        raise ValueError(
            f"Unsupported chapter format: '{segment}'"
        )

    return chapters


if __name__ == "__main__":

    test_cases = [
        "Genesis 37–41",
        "2 Kings 2–7",
        "Doctrine and Covenants 1–5",
        "1 Nephi 1–5",
        "Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12",
        "Esther",
        "Nehemiah 11–13; Esther",
        "Ruth; 1 Samuel 1–3",
        "Introduction to the Old Testament",
    ]

    for assignment in test_cases:

        print("=" * 60)
        print(assignment)

        chapters = parse_scripture_assignment(assignment)

        if not chapters:
            print("No scripture chapters.")
            continue

        for chapter in chapters:
            print(chapter)