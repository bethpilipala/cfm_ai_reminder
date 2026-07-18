from plan_storage import load_current_plan


def main():

    plan = load_current_plan()

    print("Loaded successfully!")

    print()
    print("Lesson:")
    print(plan.lesson.title)

    print()
    print("Readings:")
    print(len(plan.readings))

    for reading in plan.readings:
        print(
            f"Day {reading.day}: "
            f"{len(reading.passages)} passages"
        )

    print()
    print("Reminders:")
    print(len(plan.reminders))

    for reminder in plan.reminders:
        print(
            f"Day {reminder.day}: "
            f"{reminder.title}"
        )


if __name__ == "__main__":
    main()