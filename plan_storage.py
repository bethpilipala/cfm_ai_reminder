import json
from datetime import date
from dataclasses import asdict
from pathlib import Path

from models import Lesson, WeeklyPlan
from utils import week_start


PLAN_DIRECTORY = Path("plans")


def plan_filename(week: date) -> Path:
    """
    Returns the filename for a weekly plan.
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

    monday = week_start(date.today())

    return plan_filename(monday).exists()


def save_plan(plan: WeeklyPlan) -> None:
    """
    Saves a weekly reading plan as a JSON file.
    """

    filename = (
        f"{plan.lesson.week.start}.json"
    )

    filepath = PLAN_DIRECTORY / filename

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


def load_plan(lesson: Lesson) -> WeeklyPlan:
    """
    Loads a previously saved weekly plan.
    """

    raise NotImplementedError