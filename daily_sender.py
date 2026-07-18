from datetime import date

from plan_storage import load_current_plan
from utils import week_start


def get_day_number() -> int:
    """
    Returns today's position in the Come, Follow Me week.
    Monday = 1
    Sunday = 7
    """

    monday = week_start(date.today())

    return (
        date.today() - monday
    ).days + 1


def send_daily_reminder():

    plan = load_current_plan()

    day = get_day_number()

    reading = plan.get_reading(day)
    reminder = plan.get_reminder(day)

    print()
    print("Today's Come, Follow Me Reminder")
    print("--------------------------------")
    print()

    print(reminder.title)
    print()

    print(reminder.body)
    print()

    print("Today's Reading:")

    for passage in reading.passages:
        print(
            f"{passage.book} "
            f"{passage.chapter}:"
            f"{passage.start_verse}-"
            f"{passage.end_verse}"
        )


if __name__ == "__main__":
    send_daily_reminder()