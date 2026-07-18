from datetime import date

from notification import send_notification
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


def create_daily_message() -> tuple[str, str]:
    """
    Creates the subject and body for today's notification.
    """

    plan = load_current_plan()

    day = get_day_number()

    reading = plan.get_reading(day)
    reminder = plan.get_reminder(day)

    passages = []

    for passage in reading.passages:
        passages.append(
            f"{passage.book} "
            f"{passage.chapter}:"
            f"{passage.start_verse}-"
            f"{passage.end_verse}"
        )

    reading_text = "\n".join(passages)

    message = (
        f"{reminder.title}\n\n"
        f"{reminder.body}\n\n"
        f"📖 Today's Reading:\n"
        f"{reading_text}"
    )

    if reading.scripture_url:
        message += (
            "\n\n"
            f"🔗 {reading.scripture_url}"
        )

    return reminder.title, message


def send_daily_reminder():
    """
    Creates and sends today's reminder.
    """

    subject, message = create_daily_message()

    print()
    print("Message:")
    print("----------------")
    print(message)
    print("----------------")
    print()

    send_notification(
        subject,
        message,
    )


if __name__ == "__main__":
    send_daily_reminder()