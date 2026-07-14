import re

from models import ChapterInfo


BOOK_PATTERN = re.compile(r"^(.*?)\s+(\d+(?:–\d+)?)$")
RANGE_PATTERN = re.compile(r"^(\d+)–(\d+)$")
SINGLE_PATTERN = re.compile(r"^\d+$")


def parse_scripture_assignment(scripture_assignment: str) -> list[ChapterInfo]:
    """
    Parses a Come, Follow, Me scripture assignment into
    a list of ChapterInfo objects.

    Returns an empty list if the assignment does not appear
    to reference scripture.
    """

    segments = [
        segment.strip()
        for segment in scripture_assignment.split(";")
    ]

    chapters = []

    current_book = None

    for segment in segments:

        #
        # Does this segment introduce a new book?
        #
        match = BOOK_PATTERN.match(segment)

        if match:

            current_book = match.group(1)
            chapter_text = match.group(2)

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