from lesson_finder import find_current_lesson
from scripture_parser import parse_scripture_assignment
from verse_lookup import add_verse_counts
from plan_storage import save_plan
from reading_divider import divide_reading
from reminder_generator import generate_reminders


def generate_weekly_plan():
    """
    Creates and saves the current week's Come Follow Me plan.
    """

    print("Generating weekly plan...")

    lesson = find_current_lesson()

    chapters = parse_scripture_assignment(
        lesson.scripture_assignment
    )

    chapters = add_verse_counts(chapters)

    weekly_plan = divide_reading(
        lesson,
        chapters,
    )

    weekly_plan = generate_reminders(
        weekly_plan
    )

    save_plan(weekly_plan)

    return weekly_plan