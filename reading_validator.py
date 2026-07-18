from models import WeeklyPlan


def validate_reading_plan(
    plan: WeeklyPlan
) -> list[str]:
    """
    Validates a WeeklyPlan.

    Returns
    -------
    list[str]
        A list of validation errors.
        An empty list indicates the plan is valid.
    """

    errors: list[str] = []

    # --------------------------------------------------
    # Must have exactly seven readings
    # --------------------------------------------------

    if len(plan.readings) != 7:
        errors.append(
            f"Expected 7 readings but found {len(plan.readings)}."
        )

    # --------------------------------------------------
    # Build chapter lookup
    # --------------------------------------------------

    chapter_lookup: dict[tuple[str, int], int] = {}

    for chapter in plan.chapters:

        if chapter.verse_count is None:
            continue

        chapter_lookup[
            (chapter.book, chapter.chapter)
        ] = chapter.verse_count

    # --------------------------------------------------
    # Check every passage
    # --------------------------------------------------

    seen: set[tuple[str, int, int]] = set()

    for reading in plan.readings:

        for passage in reading.passages:

            chapter_key = (
                passage.book,
                passage.chapter,
            )

            if chapter_key not in chapter_lookup:

                errors.append(
                    f"Unknown chapter: {passage.book} {passage.chapter}"
                )

                continue

            verse_count = chapter_lookup[chapter_key]

            if passage.start_verse < 1:

                errors.append(
                    f"{passage.book} {passage.chapter}: "
                    "starts before verse 1."
                )

            if passage.end_verse > verse_count:

                errors.append(
                    f"{passage.book} {passage.chapter}: "
                    f"ends after verse {verse_count}."
                )

            if passage.start_verse > passage.end_verse:

                errors.append(
                    f"{passage.book} {passage.chapter}: "
                    "start verse is after end verse."
                )

            for verse in range(
                passage.start_verse,
                passage.end_verse + 1,
            ):

                verse_key = (
                    passage.book,
                    passage.chapter,
                    verse,
                )

                if verse_key in seen:

                    errors.append(
                        f"Duplicate verse: "
                        f"{passage.book} "
                        f"{passage.chapter}:{verse}"
                    )

                else:

                    seen.add(verse_key)

    # --------------------------------------------------
    # Verify every verse exists exactly once
    # --------------------------------------------------

    for chapter in plan.chapters:

        if chapter.verse_count is None:
            continue

        for verse in range(
            1,
            chapter.verse_count + 1,
        ):

            verse_key = (
                chapter.book,
                chapter.chapter,
                verse,
            )

            if verse_key not in seen:

                errors.append(
                    f"Missing verse: "
                    f"{chapter.book} "
                    f"{chapter.chapter}:{verse}"
                )

    return errors