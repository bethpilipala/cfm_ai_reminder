from dataclasses import dataclass, field
from datetime import date

@dataclass(slots=True)
class LessonWeek:
    display: str
    start: date
    end: date
@dataclass(slots=True)
class Lesson:
    """
    Represents one Come, Follow Me lesson.
    """
    lesson_number: int
    week: LessonWeek
    title: str
    scripture_assignment: str
    lesson_url: str
    year: int
@dataclass(slots=True)
class ChapterInfo:
    """
    Represents one chapter and its verified verse count.
    """

    book: str
    chapter: int
    verse_count: int | None = None

@dataclass(slots=True)
class Passage:
    book: str
    chapter: int
    start_verse: int
    end_verse: int


@dataclass(slots=True)
class DailyReading:
    """
    Represents one day's assigned reading.
    """

    day: int
    passages: list[Passage]
    scripture_url: str = "" # This will give a link to the first chapter of the reading, if available.


@dataclass(slots=True)
class Reminder:
    """
    Represents one generated reminder.
    """

    day: int
    reading: DailyReading
    title: str
    body: str


@dataclass(slots=True)
class WeeklyPlan:
    """
    Represents the completed weekly reading plan.
    """

    lesson: Lesson
    chapters: list[ChapterInfo] = field(default_factory=list)
    readings: list[DailyReading] = field(default_factory=list)
    reminders: list[Reminder] = field(default_factory=list)