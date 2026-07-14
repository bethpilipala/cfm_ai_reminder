from models import ChapterInfo, Lesson, WeeklyPlan


def divide_reading(
    lesson: Lesson,
    chapters: list[ChapterInfo]
) -> WeeklyPlan:
    """
    Uses AI to divide the week's reading into seven daily readings.
    """

    raise NotImplementedError