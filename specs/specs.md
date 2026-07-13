# Automated Come, Follow Me Daily Reading Reminder
## Project Specification

# Project Goal

Create a fully automated system that generates **seven daily Come, Follow Me reading reminders** each week using only official Church resources for factual information.

The system should:

- Run automatically once each week.
- Determine the current week's Come, Follow Me lesson.
- Extract the assigned scripture reading.
- Use a verified scripture database to determine verse counts.
- Use AI to intelligently divide the reading into seven daily assignments.
- Use AI to write engaging daily reminders.
- Store the completed week.
- Send one reminder each day.

The system should require no manual intervention after initial setup.

---

# Core Design Philosophy

This project intentionally separates **objective facts** from **subjective decisions**.

Large Language Models excel at:

- understanding narratives
- identifying natural story breaks
- writing engaging content
- balancing readability

However, they should **never** be trusted as the source of factual scripture information.

Instead, the project follows this rule:

> **Code determines truth. AI determines presentation.**

---

# Responsibilities

## Code is responsible for

- Current date
- Current Come, Follow Me lesson
- Scripture assignment
- Parsing scripture references
- Verse counts
- Official scripture URLs
- Verifying AI output
- Sending notifications
- Storing generated reminders

Everything that has a single correct answer is handled by code.

---

## AI is responsible for

- Finding natural story breaks
- Balancing daily readings
- Writing engaging hooks
- Writing introductions
- Writing invitations to read

Everything involving judgment or creativity is handled by AI.

---

# Data Source

Verse counts are stored locally.

Example:

```json
{
  "Genesis": {
    "1": 31,
    "2": 25,
    "3": 24
  },
  "Exodus": {
    "1": 22
  }
}
```

This is considered the authoritative source for verse counts.

The AI never estimates verse counts.

---

# Overall Workflow

```
Weekly Scheduler

↓

Determine today's date

↓

Retrieve current Come, Follow Me lesson

↓

Extract scripture assignment

↓

Load verse-count JSON

↓

Create verified chapter information

↓

Send verified information to AI

↓

AI creates seven balanced readings

↓

Code verifies AI schedule

↓

AI writes seven reminders

↓

Store reminders

↓

Daily Scheduler

↓

Load today's reminder

↓

Send notification
```

---

# Weekly Lesson Retrieval

The purpose of this step is to determine the **current week's Come, Follow Me lesson** and extract the **official scripture assignment**.

This process should rely on deterministic parsing whenever possible. AI should only be used as a fallback if deterministic parsing cannot extract the required information.

---

## Manual URL

Each Come, Follow Me manual follows a predictable URL pattern.

Examples:

2026 Old Testament

https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026

2025 Doctrine and Covenants

https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025

Each weekly lesson is located by appending the lesson number.

Examples:

```
.../01?lang=eng
.../02?lang=eng
...
.../52?lang=eng
```

---

## Manual Base URL

The application should support two methods for determining the base manual URL.

### Method 1 (Preferred)

Allow the base URL to be specified in a configuration file.

Example:

```json
{
    "manualBaseUrl": "https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026"
}
```

If this value is present, always use it.

---

### Method 2 (Automatic)

If no base URL is configured, predict it using the known Come, Follow Me rotation.

Rotation:

Old Testament

↓

New Testament

↓

Book of Mormon

↓

Doctrine and Covenants

↓

(repeat)

Construct the expected URL for the current year.

If the predicted URL does not exist, report the failure rather than guessing another URL.

---

## Lesson Discovery

Loop through lesson numbers 01–52.

For each lesson:

1. Construct the lesson URL.
2. Download the HTML.
3. Parse the page.
4. Extract:
   - Date range
   - Lesson title
   - Scripture assignment
5. Compare today's date with the lesson's date range.
6. If today's date falls within that range, stop searching and use that lesson.

---

## Primary Parsing Method

The application should first attempt deterministic parsing.

It should extract information from the HTML, preferably from the `<title>` element.

Example:

```html
<title>
August 17–23. “The Lord Is My Shepherd”: Psalms 1–2; 8; 19–33; 40; 46
</title>
```

Extract:

- Date Range
- Lesson Title
- Scripture Assignment

---

## AI Parsing Fallback

If the webpage downloads successfully but deterministic parsing cannot extract the required information, the application should invoke AI as a fallback parser.

The AI should receive:

- the lesson URL
- the page title (if available)
- the page HTML (or relevant visible text)

The AI should **only** extract structured information already present on the page.

Example prompt:

```
The following HTML was downloaded from the official Church Come, Follow Me website.

Extract ONLY the following fields.

- Date Range
- Lesson Title
- Scripture Assignment

Do not summarize.
Do not interpret.
Do not guess.
If a field cannot be found, return null.

Return valid JSON only.
```

Example output:

```json
{
    "dateRange": "August 17–23",
    "lessonTitle": "The Lord Is My Shepherd",
    "scriptureAssignment": "Psalms 1–2; 8; 19–33; 40; 46"
}
```

The returned information should then be validated exactly as if it had been produced by the deterministic parser.

---

## Validation

Regardless of whether the information came from deterministic parsing or AI parsing, the application must validate:

- Date range exists.
- Scripture assignment exists.
- Lesson title exists.
- Today's date falls within the extracted date range.

If validation fails, continue searching the remaining lesson pages.

---

## Failure Conditions

If all 52 lessons are searched and no valid lesson is found, the application should report that it could not determine the current week's Come, Follow Me lesson.

It should not guess.
It should not continue with incomplete data.

---

## Design Principle

Deterministic parsing is always preferred because it is faster and more reliable.

AI serves as an intelligent fallback when the webpage structure changes but the required information is still present.

The AI is never asked to determine the week's reading independently; it may only extract information that already exists on the official Church webpage.

# Scripture Parsing

The extracted assignment is parsed into a structured format.

Example:

```
Genesis 37–41
```

becomes

```json
{
    "book": "Genesis",
    "chapters": [
        37,
        38,
        39,
        40,
        41
    ]
}
```

If verse ranges are already provided by the lesson, preserve them.

---

# Verse Count Lookup

The program loads the local verse-count JSON.

Example:

```
Genesis

37 → 36 verses

38 → 30 verses

39 → 23 verses

40 → 23 verses

41 → 57 verses
```

This information is considered authoritative.

The AI is never asked to determine verse counts.

---

# Reading Division

This is the first AI task.

The AI receives only verified information.

Example input:

```text
Lesson:
July 13–19

Scripture Assignment:
Genesis 37–41

Verified Verse Counts

Genesis 37 = 36

Genesis 38 = 30

Genesis 39 = 23

Genesis 40 = 23

Genesis 41 = 57

Total verses = 169

Target ≈ 24 verses/day
```

The AI is instructed to:

- divide the reading into exactly seven days
- keep each day's reading approximately equal in length
- prefer ending at natural story, sermon, vision, or topic boundaries
- keep stories together whenever practical
- combine short chapters when appropriate
- split long chapters when necessary

The AI **must not** invent verse numbers.

---

# Reading Division Prompt

```
You are creating a seven-day scripture reading schedule.

The following information has already been verified.

Lesson:
{{LESSON}}

Scripture Assignment:
{{ASSIGNMENT}}

Verified Verse Counts

{{VERSE_COUNTS}}

Total verses:
{{TOTAL}}

Target verses per day:
{{TARGET}}

Create exactly seven daily readings.

Requirements

- Every verse must appear exactly once.
- No verse may be skipped.
- No verse may appear twice.
- Never exceed the verified verse count for any chapter.
- Prefer natural story, sermon, vision, or topic boundaries.
- Keep daily reading lengths as balanced as practical.
- Combine short chapters when appropriate.
- Split long chapters when necessary.

Return only the seven-day reading schedule.
```

---

# Reading Verification

The code verifies the AI output before continuing.

Checks include:

- exactly seven days
- every chapter exists
- every verse number exists
- no duplicated verses
- no skipped verses
- all verses included
- no verse exceeds the verified chapter length

If verification fails:

- reject the schedule
- send the validation errors back to the AI
- ask for a corrected schedule

This repeats until the schedule passes validation.

---

# Reminder Generation

Once the schedule is verified, AI generates one reminder for each day.

Input:

```
Lesson:
July 13–19

Today's Reading:
Genesis 37:1–24

Official URL:
https://...

(Optional)
Short description of where today's reading fits within the week's lesson.
```

---

# Reminder Prompt

```
You are writing a daily Come, Follow Me reading reminder.

The following information has already been verified.

Lesson:
{{LESSON}}

Today's Reading:
{{READING}}

Official Scripture URL:
{{URL}}

Write a reminder using this structure.

1.

Begin with a compelling hook.

Examples

- Why did...
- What would happen if...
- Can one decision...
- Have you ever wondered...
- One unexpected event...

The hook should spark curiosity without spoiling future events.

2.

Write 2–4 sentences introducing today's reading.

Encourage the reader to discover the answers for themselves.

Do not reveal important events that occur after today's reading.

3.

Write

Today's Reading

{{READING}}

4.

Write

Read here

{{URL}}

Requirements

Maximum 150 words.

Use an uplifting, inviting tone.

Do not invent scripture references.

Do not reference verses outside today's reading.

Avoid repeating hooks used earlier in the week.
```

---

# Example Reminder

```
🌟 One dream changed an entire family's future.

Joseph's dreams seemed impossible, yet they stirred powerful emotions among those closest to him. As you read today, look for what these early experiences teach about faith, family, and God's purposes—even when His plan isn't immediately clear.

Today's Reading

Genesis 37:1–24

Read here

https://www.churchofjesuschrist.org/study/scriptures/ot/gen/37
```

---

# Weekly Storage

Once all reminders are generated, they are saved locally.

Example:

```json
{
  "lesson": "July 13–19",
  "days": [
    {
      "day": 1,
      "reading": "Genesis 37:1–24",
      "url": "...",
      "message": "..."
    }
  ]
}
```

The daily notification system only reads from this file.

No AI calls occur during the week.

---

# Daily Notification

Each morning:

```
Determine current day

↓

Load stored week

↓

Retrieve today's reminder

↓

Send notification
```

---

# Future Improvements

Potential enhancements include:

- Reflection questions
- Daily challenges
- Prayer invitations
- Alternate writing styles
- Emoji themes
- Multiple hook options ranked by AI
- Different reminder lengths
- Multiple languages
- Support for future Come, Follow Me manuals
- Mobile app with native notifications
- SMS support if a practical free option becomes available

---

# Guiding Principle

The project follows one simple rule:

> **Objective truth comes from code. Subjective judgment comes from AI.**

Code provides verified scripture data and validates every reading assignment.

AI uses that verified information to make thoughtful reading divisions and create engaging, uplifting reminders without ever inventing factual information.