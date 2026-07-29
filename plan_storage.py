import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from config_loader import load_config
from models import (
    ChapterInfo,
    DailyReading,
    Lesson,
    LessonWeek,
    Passage,
    Reminder,
    WeeklyPlan,
)
from secret_manager import running_in_lambda
from utils import week_start


PLAN_DIRECTORY = Path("plans")

_s3 = None #type: ignore


def get_s3():
    """
    Returns a cached S3 client.
    """

    global _s3

    if _s3 is None:
        _s3 = boto3.client("s3")

    return _s3


def get_bucket_name() -> str:
    """
    Returns the configured S3 bucket.
    """

    config = load_config()

    return config["plan_bucket"]


def plan_filename(week: date) -> Path:
    """
    Returns the local filename for a weekly plan.
    """

    return PLAN_DIRECTORY / f"{week.isoformat()}.json"


def plan_key(week: date) -> str:
    """
    Returns the filename/key used in S3.
    """

    return f"{week.isoformat()}.json"


def current_plan_filename() -> Path:
    """
    Returns the current week's local filename.
    """

    return plan_filename(
        week_start(date.today())
    )


def current_plan_exists() -> bool:
    """
    Returns True if the current week's plan exists.
    """

    week = week_start(date.today())

    if running_in_lambda():

        try:

            get_s3().head_object(
                Bucket=get_bucket_name(),
                Key=plan_key(week),
            )

            return True

        except ClientError:

            return False

    return current_plan_filename().exists()


def save_plan(plan: WeeklyPlan) -> None:
    """
    Saves a weekly reading plan.
    """

    data = json.dumps(
        asdict(plan),
        indent=4,
        ensure_ascii=False,
        default=str,
    )

    week = plan.lesson.week.start

    if running_in_lambda():

        get_s3().put_object(
            Bucket=get_bucket_name(),
            Key=plan_key(week),
            Body=data,
            ContentType="application/json",
        )

    else:

        PLAN_DIRECTORY.mkdir(
            exist_ok=True
        )

        filepath = plan_filename(week)

        with filepath.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write(data)


def load_plan(
    week: date,
) -> WeeklyPlan:
    """
    Loads a weekly reading plan.
    """

    if running_in_lambda():

        try:

            response = get_s3().get_object(
                Bucket=get_bucket_name(),
                Key=plan_key(week),
            )

        except ClientError:

            raise FileNotFoundError(
                f"No plan found for {week}."
            )

        data = json.loads(
            response["Body"].read().decode("utf-8")
        )

    else:

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