import json
from datetime import date
from dataclasses import asdict
from pathlib import Path

from models import (
    Lesson,
    LessonWeek,
    ChapterInfo,
    Passage,
    DailyReading,
    Reminder,
    WeeklyPlan,
)
from utils import week_start


PLAN_DIRECTORY = Path("plans")


def plan_filename(week: date) -> Path:
    """
    Returns the filename for the weekly plan.
    """

    return PLAN_DIRECTORY / f"{week.isoformat()}.json"


def current_plan_filename() -> Path:
    """
    Returns the filename for the current week's plan.
    """

    return plan_filename(
        week_start(date.today())
    )


def current_plan_exists() -> bool:
    """
    Returns True if a plan already exists for the current week.
    """

    return current_plan_filename().exists()


def save_plan(plan: WeeklyPlan) -> None:
    """
    Saves a weekly reading plan as a JSON file.
    """

    PLAN_DIRECTORY.mkdir(
        exist_ok=True
    )

    filepath = plan_filename(
        plan.lesson.week.start
    )

    with filepath.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            asdict(plan),
            file,
            indent=4,
            ensure_ascii=False,
            default=str,
        )


def load_plan(
    week: date,
) -> WeeklyPlan:
    """
    Loads a weekly reading plan from JSON.
    """

    filepath = plan_filename(week)

    if not filepath.exists():
        raise FileNotFoundError(
            f"No plan found for {week}."
        )

    with filepath.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)


    # Rebuild LessonWeek

    lesson_week = LessonWeek(
        display=data["lesson"]["week"]["display"],
        start=date.fromisoformat(
            data["lesson"]["week"]["start"]
        ),
        end=date.fromisoformat(
            data["lesson"]["week"]["end"]
        ),
    )


    # Rebuild Lesson

    lesson = Lesson(
        lesson_number=data["lesson"]["lesson_number"],
        week=lesson_week,
        title=data["lesson"]["title"],
        scripture_assignment=data["lesson"]["scripture_assignment"],
        lesson_url=data["lesson"]["lesson_url"],
        year=data["lesson"]["year"],
    )


    # Rebuild chapters

    chapters = []

    for chapter in data["chapters"]:

        chapters.append(
            ChapterInfo(
                book=chapter["book"],
                chapter=chapter["chapter"],
                verse_count=chapter["verse_count"],
            )
        )


    # Rebuild readings

    readings = []

    for reading in data["readings"]:

        passages = []

        for passage in reading["passages"]:

            passages.append(
                Passage(
                    book=passage["book"],
                    chapter=passage["chapter"],
                    start_verse=passage["start_verse"],
                    end_verse=passage["end_verse"],
                )
            )

        readings.append(
            DailyReading(
                day=reading["day"],
                passages=passages,
                scripture_url=reading.get(
                    "scripture_url",
                    "",
                ),
            )
        )


    # Rebuild reminders

    reading_lookup = {
        reading.day: reading
        for reading in readings
    }

    reminders = []

    for reminder in data["reminders"]:

        reminders.append(
            Reminder(
                day=reminder["day"],
                reading=reading_lookup[
                    reminder["day"]
                ],
                title=reminder["title"],
                body=reminder["body"],
            )
        )


    return WeeklyPlan(
        lesson=lesson,
        chapters=chapters,
        readings=readings,
        reminders=reminders,
    )


def load_current_plan() -> WeeklyPlan:
    """
    Loads the current week's plan.
    """

    return load_plan(
        week_start(date.today())
    )