from lesson_finder import find_current_lesson


def main():

    lesson = find_current_lesson()

    print()

    print(f"Lesson     : {lesson.lesson_number}")
    print(f"Year       : {lesson.year}")
    print(f"Week       : {lesson.week.display}")
    print(f"Start Date : {lesson.week.start}")
    print(f"End Date   : {lesson.week.end}")
    print(f"Title      : {lesson.title}")
    print(f"Assignment : {lesson.scripture_assignment}")


if __name__ == "__main__":
    main()