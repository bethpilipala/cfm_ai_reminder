from ai_client import generate_json
from prompt_loader import load_prompt

from models import (
    DailyReading,
    Lesson,
    Reminder,
    WeeklyPlan,
)


def build_request(
    lesson: Lesson,
    readings: list[DailyReading],
) -> dict:
    """
    Builds the AI request for generating all weekly reminders.
    """

    request: dict = {
        "lesson": {
            "title": lesson.title,
            "scripture_assignment": lesson.scripture_assignment,
        },
        "readings": [],
    }

    for reading in readings:

        request["readings"].append(
            {
                "day": reading.day,
                "scripture_url": reading.scripture_url,
                "passages": [
                    {
                        "book": passage.book,
                        "chapter": passage.chapter,
                        "start_verse": passage.start_verse,
                        "end_verse": passage.end_verse,
                    }
                    for passage in reading.passages
                ],
            }
        )

    return request


def parse_response(
    weekly_plan: WeeklyPlan,
    response: dict,
) -> list[Reminder]:
    """
    Converts Gemini response JSON into Reminder objects.
    """

    reminders = []

    try:
        generated_reminders = response["reminders"]

    except KeyError:
        raise RuntimeError(
            "AI response did not contain a 'reminders' field."
        )

    for reminder_data in generated_reminders:

        day = reminder_data["day"]

        matching_reading = next(
            (
                reading
                for reading in weekly_plan.readings
                if reading.day == day
            ),
            None,
        )

        if matching_reading is None:
            raise RuntimeError(
                f"AI generated reminder for invalid day {day}."
            )

        reminders.append(
            Reminder(
                day=day,
                reading=matching_reading,
                title=reminder_data["title"],
                body=reminder_data["body"],
            )
        )

    return reminders


def generate_reminders(
    weekly_plan: WeeklyPlan,
) -> WeeklyPlan:
    """
    Uses AI to generate reminders for the week's readings.
    """

    prompt = load_prompt(
        "generate_reminders"
    )

    request = build_request(
        weekly_plan.lesson,
        weekly_plan.readings,
    )

    response = generate_json(
        prompt,
        request,
    )

    reminders = parse_response(
        weekly_plan,
        response,
    )

    weekly_plan.reminders.extend(
        reminders
    )

    return weekly_plan