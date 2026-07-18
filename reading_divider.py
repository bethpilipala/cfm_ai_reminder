import json

from ai_client import generate_json
from prompt_loader import load_prompt
from reading_validator import validate_reading_plan

from models import (
    ChapterInfo,
    DailyReading,
    Lesson,
    Passage,
    WeeklyPlan,
)

MAX_ATTEMPTS = 3

MOCK_AI_RESPONSE = {
    "days": [
        {
            "passages": [
                {
                    "book": "Genesis",
                    "chapter": 37,
                    "start_verse": 1,
                    "end_verse": 24,
                }
            ]
        },
        {
            "passages": []
        },
        {
            "passages": []
        },
        {
            "passages": []
        },
        {
            "passages": []
        },
        {
            "passages": []
        },
        {
            "passages": []
        },
    ]
}


def build_request(
    lesson: Lesson,
    chapters: list[ChapterInfo],
) -> dict:
    """
    Builds the JSON request that will be sent to the AI.
    """

    total_verses = sum(
        chapter.verse_count or 0
        for chapter in chapters
    )

    request: dict = {
        "lesson": {
            "title": lesson.title,
            "scripture_assignment": lesson.scripture_assignment,
            "total_verses": total_verses,
        },
        "chapters": [],
    }

    for chapter in chapters:
        request["chapters"].append(
            {
                "book": chapter.book,
                "chapter": chapter.chapter,
                "verses": chapter.verse_count,
            }
        )

    return request


def print_request(request: dict) -> None:
    """
    Prints the AI request in a readable format.
    """

    print(
        json.dumps(
            request,
            indent=4,
            ensure_ascii=False,
        )
    )


def parse_response(
    lesson: Lesson,
    chapters: list[ChapterInfo],
    response: dict,
) -> WeeklyPlan:
    """
    Converts the AI response JSON into a WeeklyPlan object.
    """

    weekly_plan = WeeklyPlan(
        lesson=lesson,
        chapters=chapters,
    )

    try:
        days = response["days"]
    except KeyError:
        raise RuntimeError(
            "AI response did not contain a 'days' field."
        )

    for day_number, day in enumerate(
        days,
        start=1,
    ):
        passages = []

        for passage in day["passages"]:
            passages.append(
                Passage(
                    book=passage["book"],
                    chapter=passage["chapter"],
                    start_verse=passage["start_verse"],
                    end_verse=passage["end_verse"],
                )
            )

        weekly_plan.readings.append(
            DailyReading(
                day=day_number,
                passages=passages,
            )
        )

    return weekly_plan


def divide_reading(
    lesson: Lesson,
    chapters: list[ChapterInfo],
) -> WeeklyPlan:
    """
    Uses AI to divide the week's reading into seven daily readings.
    Retries up to MAX_ATTEMPTS if validation fails.
    """

    request = build_request(
        lesson,
        chapters,
    )

    prompt = load_prompt("divide_reading")

    last_errors: list[str] = []

    for attempt in range(
        1,
        MAX_ATTEMPTS + 1,
    ):

        print(f"\nAI Attempt {attempt}/{MAX_ATTEMPTS}")

        response = generate_json(
            prompt,
            request,
        )

        plan = parse_response(
            lesson,
            chapters,
            response,
        )

        errors = validate_reading_plan(plan)

        if not errors:

            print("✓ Reading plan validated successfully.")

            return plan

        last_errors = errors

        print("Validation failed:")

        for error in errors:
            print(f"  • {error}")

    raise RuntimeError(
        "Unable to generate a valid reading plan after "
        f"{MAX_ATTEMPTS} attempts.\n\n"
        + "\n".join(last_errors)
    )