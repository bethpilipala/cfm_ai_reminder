from datetime import date, timedelta

MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def week_start(day: date) -> date:
    """
    Returns the Monday of the week containing the given date.
    """

    return day - timedelta(days=day.weekday())

def build_lesson_url(base_url: str, lesson_number: int) -> str:
    """
    Builds the URL for a lesson.

    Example:
    https://.../28?lang=eng
    """

    return f"{base_url}/{lesson_number:02}?lang=eng"

def parse_date_range(date_range: str, year: int) -> tuple[date, date]:
    """
    Converts a Come, Follow Me date range into two date objects.
    Supported formats:
        July 6–12
        December 29–January 4
    """

    left, right = [part.strip() for part in date_range.split("–", maxsplit=1)]

    # Example:
    # left  = "July 6"
    # right = "12"
    #
    # or
    #
    # left  = "December 29"
    # right = "January 4"

    left_parts = left.split()

    start_month_name = left_parts[0]
    start_day = int(left_parts[1])

    # Does the right side contain another month?
    if " " in right:

        right_parts = right.split()

        end_month_name = right_parts[0]
        end_day = int(right_parts[1])

    else:

        end_month_name = start_month_name
        end_day = int(right)

    start_month = MONTHS[start_month_name]
    end_month = MONTHS[end_month_name]

    # Handle lessons that cross into the next calendar year.
    start_year = year
    end_year = year

    if end_month < start_month:
        end_year += 1

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    return start_date, end_date

if __name__ == "__main__":

    print(parse_date_range("July 6–12", 2026))

    print(parse_date_range("December 29–January 4", 2026))