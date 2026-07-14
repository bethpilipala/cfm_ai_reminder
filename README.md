# Come, Follow Me AI Reminder

An automated system that generates and sends daily Come, Follow Me reading reminders.

The project combines deterministic code with AI:

- Code determines factual information.
- AI makes subjective decisions such as dividing readings and writing reminders.

---

# Current Project Structure

config.json
        │
        ▼
config_loader.py
        │
        ▼
lesson_finder.py
        │
        ├───────────────┐
        ▼               │
lesson_fetcher.py       │
        ▼               │
lesson_parser.py        │
        ▼               │
     Lesson ◄───────────┘

## main.py

Application entry point.

Currently used to test the various modules while the project is under development.

Eventually, this will start the weekly reminder generation pipeline.

---

## config.json

Stores user-editable configuration.

Currently includes:

- Come, Follow Me manual URLs
- Time zone
- Notification time

---

## config_loader.py

Loads configuration information.

Responsibilities:

- Read `config.json`
- Determine the correct manual URL
- Predict future manual URLs if the current year is not configured
- Verify predicted URLs exist

---

## models.py

Contains all project data models using Python dataclasses.

Current models:

- Lesson
- ChapterInfo
- DailyReading
- Reminder
- WeeklyPlan

These objects are passed between modules instead of using dictionaries.

---

## lesson_fetcher.py

Downloads lesson pages from the official Church website.

Responsibilities:

- Download HTML
- Report download failures

Does **not** parse any HTML.

---

## lesson_parser.py

Parses downloaded HTML into a `Lesson` object.

Current responsibilities:

- Read the page title
- Extract:
  - Date range
  - Lesson title
  - Scripture assignment

Future responsibilities:

- AI fallback parsing if deterministic parsing fails.

---

## lesson_finder.py

(Not yet implemented)

Will determine the current week's lesson.

Responsibilities:

- Loop through lessons 01–52
- Download each lesson
- Parse each lesson
- Compare lesson dates with today's date
- Return the current lesson

---

## scripture_parser.py

(Not yet implemented)

Will convert scripture references into structured data.

Example:

Genesis 37–41

↓

Genesis 37

Genesis 38

Genesis 39

Genesis 40

Genesis 41

---

## utils.py

General helper functions used throughout the project.

Examples:

- Date parsing
- Miscellaneous reusable utilities

These functions are intentionally kept small and independent.

---

## verse_lookup.py

(Not yet implemented)

Loads and queries the local verse-count database.

The verse-count JSON is considered the authoritative source.

---

## reading_divider.py

(Not yet implemented)

Uses AI to divide the week's reading into seven balanced daily assignments.

---

## reading_validator.py

(Not yet implemented)

Verifies AI-generated reading schedules.

Checks include:

- Exactly seven days
- No skipped verses
- No duplicate verses
- No invalid verses
- All verses accounted for

---

## reminder_generator.py

(Not yet implemented)

Uses AI to generate daily reading reminders.

---

## storage.py

(Not yet implemented)

Saves and loads generated weekly reading plans.

---

## notification.py

(Not yet implemented)

Sends the daily reminder using the selected notification service.

---

# Design Philosophy

The project follows one guiding principle:

> Objective truth comes from code. Subjective judgment comes from AI.

The code is responsible for:

- Current lesson
- Scripture assignments
- Verse counts
- Validation
- URLs
- Notifications

AI is responsible for:

- Dividing readings
- Writing reminders
- Natural language generation

AI is never treated as the source of factual scripture information.