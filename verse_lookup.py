import json

from models import ChapterInfo


_DATA: dict[str, dict[str, int]] | None = None


def load_verse_counts() -> dict:
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


def add_verse_counts(
    chapters: list[ChapterInfo]
) -> list[ChapterInfo]:
    """
    Adds verse counts to each chapter.
    """

    database = load_verse_counts()

    for chapter in chapters:

        try:

            chapter.verse_count = database[
                chapter.book
            ][
                str(chapter.chapter)
            ]

        except KeyError:

            raise Exception(
                f"No verse count found for "
                f"{chapter.book} {chapter.chapter}."
            )

    return chapters