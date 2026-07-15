from lesson_finder import find_current_lesson
from scripture_parser import parse_scripture_assignment
from verse_lookup import add_verse_counts
from plan_storage import current_plan_exists, save_plan
from reading_divider import divide_reading


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

    print(f"Lesson     : {lesson.lesson_number}")
    print(f"Year       : {lesson.year}")
    print(f"Week       : {lesson.week.display}")
    print(f"Start Date : {lesson.week.start}")
    print(f"End Date   : {lesson.week.end}")
    print(f"Title      : {lesson.title}")
    print(f"Assignment : {lesson.scripture_assignment}")

    print()

    print("Chapters:")

    if not chapters:
        print("  No scripture chapters.")
    else:
        for chapter in chapters:
            print(
                f"{chapter.book} "
                f"{chapter.chapter} "
                f"({chapter.verse_count} verses)"
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
        print(f"Error generating reading plan: {error}")
        return

    save_plan(weekly_plan)

    print()
    print("Weekly plan saved.")

    print()
    print("Weekly Plan:")

    for reading in weekly_plan.readings:
        print(f"Day {reading.day}:")

        if not reading.passages:
            print("  No passages.")
        else:
            for passage in reading.passages:
                print(
                    f"  {passage.book} "
                    f"{passage.chapter}:"
                    f"{passage.start_verse}-"
                    f"{passage.end_verse}"
                )


if __name__ == "__main__":
    main()