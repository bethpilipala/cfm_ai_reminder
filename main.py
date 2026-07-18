from lesson_finder import find_current_lesson
from scripture_parser import parse_scripture_assignment
from verse_lookup import add_verse_counts
from plan_storage import current_plan_exists, save_plan
from reading_divider import divide_reading
from reminder_generator import generate_reminders

def main():

    if current_plan_exists():
        print("Weekly plan already exists.")
        return

    print("Generating weekly plan...")

    lesson = find_current_lesson()

    chapters = parse_scripture_assignment(
        lesson.scripture_assignment
    )

    chapters = add_verse_counts(chapters)

    print()

    print(
        f"Lesson {lesson.lesson_number} "
        f"({lesson.week.display}, {lesson.year})"
    )
    print(lesson.title)
    print(lesson.scripture_assignment)

    total_verses = sum(
        chapter.verse_count or 0
        for chapter in chapters
    )

    print()
    print(
        f"Parsed {len(chapters)} chapters "
        f"({total_verses} verses)"
    )

    print()
    print("Generating reading plan...")

    try:
        weekly_plan = divide_reading(
            lesson,
            chapters,
        )

    except RuntimeError as error:
        print()
        print(
            f"Error generating reading plan:\n{error}"
        )
        return

    print()
    print("Generating reminders...")

    try:
        weekly_plan = generate_reminders(
            weekly_plan
        )

    except RuntimeError as error:
        print()
        print(
            f"Error generating reminders:\n{error}"
        )
        return

    save_plan(weekly_plan)

    print()
    print("✓ Weekly plan saved.")

    print()
    print("Reading Schedule:")

    for reading in weekly_plan.readings:

        if not reading.passages:
            summary = "No reading"

        else:

            first = reading.passages[0]
            last = reading.passages[-1]

            if (
                first.book == last.book
                and first.chapter == last.chapter
            ):
                summary = (
                    f"{first.book} "
                    f"{first.chapter}"
                )

            elif first.book == last.book:
                summary = (
                    f"{first.book} "
                    f"{first.chapter}–{last.chapter}"
                )

            else:
                summary = (
                    f"{first.book} {first.chapter}"
                    f" → "
                    f"{last.book} {last.chapter}"
                )

        print(
            f"  Day {reading.day}: {summary}"
        )

    print()
    print("Reminder Titles:")

    for reminder in weekly_plan.reminders:

        print(
            f"  Day {reminder.day}: "
            f"{reminder.title}"
        )


if __name__ == "__main__":
    main()