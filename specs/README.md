# Come, Follow Me AI Daily Reading Reminder

## Overview

The **Come, Follow Me AI Daily Reading Reminder** is an automated system that generates engaging daily scripture reading reminders based on the current week's official *Come, Follow Me* lesson from The Church of Jesus Christ of Latter-day Saints.

The project combines deterministic programming with AI to create an experience that is both **factually reliable** and **engaging to read**.

Every week, the application automatically:

1. Determines the current week's Come, Follow Me lesson.
2. Retrieves the official scripture assignment.
3. Determines the verse count for every chapter using a verified local database.
4. Uses AI to divide the reading into seven balanced daily assignments while respecting natural story boundaries.
5. Uses AI to write seven engaging reading reminders.
6. Stores the reminders.
7. Sends one reminder each day.

After the initial setup, the entire process is fully automated.

---

# Primary Design Philosophy

This project intentionally separates **objective truth** from **creative judgment**.

Large Language Models are excellent writers, but they should not be treated as authoritative sources for scripture references or structured data.

Instead, the application follows one guiding principle:

> **Objective truth comes from deterministic code. Subjective judgment comes from AI.**

This philosophy dramatically reduces the chance of hallucinated scripture references while still benefiting from AI's ability to understand narrative flow and write engaging content.

---

# Responsibilities

## Code is responsible for

- Determining today's date
- Finding the correct Come, Follow Me lesson
- Downloading and parsing official Church webpages
- Extracting scripture assignments
- Loading verified verse counts
- Generating official scripture URLs
- Validating every AI-generated reading assignment
- Saving weekly reminder data
- Scheduling reminders
- Sending notifications

Anything with a single objectively correct answer is handled by code.

---

## AI is responsible for

- Finding natural reading breaks
- Balancing daily reading assignments
- Writing engaging hooks
- Writing introductions
- Encouraging scripture study

Anything requiring creativity or subjective judgment is handled by AI.

---

# Design Goals

The project should be:

- Fully automated
- Deterministic whenever possible
- Easy to maintain
- Modular
- Easy to extend
- Easy to debug
- Easy to adapt for future Come, Follow Me manuals

---

# High-Level Workflow

```text
Weekly Scheduler
        │
        ▼
Determine today's date
        │
        ▼
Retrieve current Come, Follow Me lesson
        │
        ▼
Extract scripture assignment
        │
        ▼
Load verified verse-count database
        │
        ▼
Generate verified chapter information
        │
        ▼
AI creates seven balanced readings
        │
        ▼
Code validates the schedule
        │
        ▼
AI generates seven reminders
        │
        ▼
Store weekly reminder data
        │
        ▼
Daily Scheduler
        │
        ▼
Load today's reminder
        │
        ▼
Send notification
```

---

# AI Philosophy

AI should never be asked to answer questions that code can answer with certainty.

### Good AI Tasks

- Where is the best place to end today's reading?
- Does this split preserve the narrative well?
- Write a compelling introduction.
- Create curiosity without spoilers.

### Bad AI Tasks

- How many verses are in Genesis 37?
- What is this week's reading?
- Does Alma 32 have 43 or 44 verses?
- Generate a scripture URL.

Those are deterministic problems and should always be solved by code.

---

# Reliability Strategy

The application is designed with multiple layers of validation.

For example:

1. Code retrieves the scripture assignment.
2. Code verifies chapter and verse counts.
3. AI proposes a reading schedule.
4. Code validates every verse reference.
5. If validation fails, AI is asked to correct the schedule.
6. Only validated schedules are used to generate reminders.

This approach allows AI to make creative decisions while preventing factual errors.

---

# Error Recovery Philosophy

Whenever possible, deterministic methods should be attempted first.

If deterministic parsing fails because the Church website structure has changed, AI may be used as an intelligent parser.

However, AI is only allowed to extract information that already exists on the downloaded webpage.

AI must never guess missing information.

Preferred order:

1. Deterministic HTML parsing
2. Deterministic regex parsing
3. AI extraction from downloaded HTML
4. Report an error

Not:

1. Ask AI to guess this week's lesson

---

# Project Architecture

```text
/specs
    README.md
    configuration.md
    workflow.md
    lesson-retrieval.md
    scripture-parsing.md
    reading-division.md
    reminder-generation.md
    notifications.md
    prompts.md

/src
    main.py
    config.py
    scheduler.py
    lesson_retrieval.py
    scripture_parser.py
    reading_divider.py
    reminder_generator.py
    validator.py
    notifier.py
    storage.py

/data
    verse_counts.json
    weekly_readings.json

/prompts
    reading_division.txt
    reminder_generation.txt
    html_parsing.txt
```

The exact language or project structure may evolve over time, but responsibilities should remain separated by module.

---

# Weekly Workflow

Every week the application performs the following sequence:

1. Determine the current date.
2. Retrieve the correct Come, Follow Me lesson.
3. Extract the scripture assignment.
4. Parse the scripture assignment into chapters.
5. Load verified verse counts.
6. Send verified information to AI.
7. Receive a proposed seven-day reading schedule.
8. Validate the schedule.
9. Request corrections if necessary.
10. Generate seven daily reminders.
11. Save the completed week's reminders.

After this process completes successfully, no additional AI calls are required until the following week.

---

# Daily Workflow

Each day:

1. Determine today's day of the week.
2. Load the stored weekly reminder file.
3. Retrieve today's reminder.
4. Send the notification.

Daily notifications should never require another AI request.

---

# Configuration

The application should be configurable.

Examples include:

- Manual base URL
- OpenAI model
- API keys
- Notification provider
- Notification time
- Time zone
- Storage location
- Logging options
- Debug mode

Configuration details are documented separately in `configuration.md`.

---

# Data Files

The project maintains two primary data files.

## `verse_counts.json`

Contains the verified verse count for every chapter.

Example:

```json
{
    "Genesis": {
        "1": 31,
        "2": 25,
        "3": 24
    }
}
```

This file is considered the authoritative source for verse counts.

---

## `weekly_readings.json`

Contains the generated reminders for the current week.

Example:

```json
{
    "lesson": "...",
    "days": [
        {
            "day": 1,
            "reading": "...",
            "message": "...",
            "url": "..."
        }
    ]
}
```

---

# Future Features

Potential future enhancements include:

- Native Android application
- iOS application
- SMS support
- Multiple notification providers
- Reflection questions
- Daily challenges
- Prayer invitations
- Multiple writing styles
- Theme customization
- Language localization
- Support for additional study manuals
- Synchronization across devices

---

# Guiding Principle

Whenever a design decision is unclear, follow this rule:

> **If something has one objectively correct answer, code should determine it. If something benefits from creativity or interpretation, AI should determine it.**

This philosophy keeps the application reliable, maintainable, and resilient while allowing AI to enhance the daily scripture study experience without becoming a source of factual error.