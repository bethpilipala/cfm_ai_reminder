# Come, Follow Me AI Reminder Service

An automated Python application that generates personalized daily **Come, Follow Me** study reminders using AI and delivers them through email and/or SMS. The project is designed to run locally for development or as a scheduled AWS Lambda function in production with the same codebase.

---

## Overview

Each week the application:

- Determines the current Come, Follow Me lesson
- Downloads and parses the official lesson from ChurchofJesusChrist.org
- Extracts the scripture assignment
- Calculates verse counts
- Divides the weekly reading into balanced daily assignments
- Uses AI to generate personalized daily reminders
- Saves the completed weekly plan

Each day it:

- Loads the current week's plan (or generates one if none exists)
- Selects today's reading
- Builds the daily reminder
- Sends notifications using the configured delivery methods

---

## Features

- Automatic weekly Come, Follow Me lesson detection
- Scripture parsing and reading assignment generation
- Balanced daily reading schedule creation
- AI-generated personalized daily reminders
- Weekly plan caching to avoid unnecessary regeneration
- Email notifications (Gmail SMTP)
- SMS notifications (Amazon SNS)
- Configurable notification methods
- Local development using `.env`
- Production deployment on AWS Lambda
- Secure secret management through AWS Systems Manager Parameter Store

---

## Example Message


Lost & Found: The Best Book! 📖✨

Imagine cleaning out your house and finding something incredibly valuable you totally forgot you had, something that changes everything! That's kind of what happens during King Josiah's reign when the Book of the Law is rediscovered. It sparks a massive spiritual revival and a kingdom-wide clean-up. Don't miss this inspiring read today!

📖 Today's Reading:\
2 Kings 22:1-20\
2 Kings 23:1-37

🔗 https://www.churchofjesuschrist.org/study/scriptures/ot/2-kgs/22?lang=eng


---

## Architecture

```
Church Website
       │
       ▼
Lesson Fetcher
       │
       ▼
Scripture Parser
       │
       ▼
Verse Counter
       │
       ▼
Reading Divider
       │
       ▼
Gemini AI
       │
       ▼
Weekly Plan
       │
       ▼
Daily Reminder
       │
       ├────────► Email (SMTP)
       │
       └────────► SMS (AWS SNS)
```

---

## Technology Stack

### Languages

- Python 3.12

### AI

- Google Gemini

### AWS

- AWS Lambda
- AWS SAM
- Amazon EventBridge
- Amazon SNS
- AWS Systems Manager Parameter Store
- Amazon CloudFormation

### Libraries

- requests
- beautifulsoup4
- python-dateutil
- boto3
- google-genai
- python-dotenv

---

## Project Structure

```
.
├── ai_client.py              # AI interface
├── config_loader.py          # Configuration loading
├── daily_sender.py           # Daily reminder workflow
├── email_sender.py           # Email notifications
├── lambda_handler.py         # AWS Lambda entry point
├── lesson_fetcher.py         # Lesson downloader
├── lesson_finder.py          # Current lesson detection
├── lesson_parser.py          # Lesson parsing
├── main.py                   # Local entry point
├── models.py                 # Shared models
├── notification.py           # Notification dispatcher
├── plan_storage.py           # Weekly plan persistence
├── prompt_loader.py          # AI prompt loading
├── reading_divider.py        # Daily reading generation
├── reading_validator.py      # Reading validation
├── reminder_generator.py     # AI reminder generation
├── scripture_parser.py       # Scripture parsing
├── scripture_url.py          # Scripture URL generation
├── secret_manager.py         # Secret loading
├── sns_sender.py             # SMS notifications
├── template.yaml             # AWS SAM template
├── utils.py                  # Shared utilities
├── verse_lookup.py           # Verse counting
├── weekly_pipeline.py        # Weekly generation pipeline
│
├── plans/                    # Cached weekly plans
├── prompts/                  # AI prompt templates
├── data/                     # Supporting data
├── tests/                    # Unit tests
└── config.json               # Application configuration
```

---

## Weekly Pipeline

1. Locate the current Come, Follow Me lesson
2. Download and parse the lesson
3. Extract scripture assignments
4. Determine verse counts
5. Divide readings into daily portions
6. Generate AI reminders
7. Save the weekly plan

Each generated plan is stored as a separate file (one per week), using the week's start date as the filename (for example: `2026-07-20`).

---

## Notification Pipeline

Every day the application:

- Loads the current week's plan
- Determines today's reading assignment
- Retrieves today's AI-generated reminder
- Builds the notification message
- Includes a scripture URL for quick access
- Sends notifications using the configured delivery methods

Notification methods are configurable and currently support:

- Email (SMTP)
- SMS (Amazon SNS)

---

## Configuration

Application behavior is controlled through `config.json`, including:

- Supported Come, Follow Me manuals
- Time zone
- Notification time
- AWS region
- AWS Parameter Store paths
- Enabled notification methods

Secrets are **never** stored in the configuration file.

---

## Secret Management

The project uses a single abstraction for secrets.

### Local Development

Secrets are loaded from a `.env` file.

### AWS Deployment

Secrets are loaded from AWS Systems Manager Parameter Store.

The rest of the application is unaware of where secrets originate, allowing the same code to run locally and in AWS without modification.

---

## AWS Deployment

The production deployment consists of:

- AWS Lambda
- Amazon EventBridge scheduled trigger
- Amazon SNS
- AWS Systems Manager Parameter Store
- AWS SAM / CloudFormation

The Lambda function executes once per day to generate and send that day's reminder.

---

## Design Goals

- Clean modular architecture
- Environment-independent business logic
- Secure secret management
- Minimal duplication between local and cloud execution
- Easily extensible notification system
- Reusable weekly plan generation
- Strong separation of responsibilities between modules