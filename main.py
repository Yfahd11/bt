# main.py
"""
Simple command-line interface for the StudyLink project.

This script lets a student:
  * create or edit their profile
  * get recommended study partners
  * log study sessions
  * rate a partner and update their rating
  * search for helpers by subject
"""

from __future__ import annotations

from typing import List

from src.matching import MatchEngine
from src.models import Student


def _ask_list(prompt: str) -> List[str]:
    """Ask for a comma‑separated list and return the cleaned items."""
    text = input(prompt + " (comma‑separated, leave blank for none): ").strip()
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


def create_or_edit_profile(engine: MatchEngine) -> None:
    """Create a new profile or update an existing one."""
    raw_id = input("Your student id (leave blank to create a new profile): ").strip()
    student_id = int(raw_id) if raw_id else None

    name = input("Name: ").strip()
    major = input("Major (optional): ").strip()
    strengths = _ask_list("What subjects are you strong in")
    needs = _ask_list("What subjects do you want help with")

    try:
        student = engine.create_or_update_student(
            student_id=student_id,
            name=name,
            major=major,
            strengths=strengths,
            needs=needs,
        )
    except KeyError as exc:
        print(f"Error: {exc}")
        return

    print("\nProfile saved:")
    print(student.profile_summary())
    print()


def show_matches(engine: MatchEngine) -> None:
    """Show recommended study partners for a given student id."""
    try:
        student_id = int(input("Enter your student id: ").strip())
    except ValueError:
        print("Please enter a valid number for the id.")
        return

    limit_text = input("How many matches should I list? (default 5): ").strip()
    try:
        limit = int(limit_text) if limit_text else 5
    except ValueError:
        limit = 5

    try:
        matches = engine.recommend_for(student_id, limit=limit)
    except KeyError as exc:
        print(f"Error: {exc}")
        return

    if not matches:
        print("No compatible matches found yet. Try adding more students first.")
        return

    print("\nRecommended study partners:")
    for student in matches:
        print(" •", student.profile_summary())
    print()


def start_session(engine: MatchEngine) -> None:
    """Create a new StudySession between two students."""
    try:
        s1 = int(input("Your student id: ").strip())
        s2 = int(input("Partner's student id: ").strip())
    except ValueError:
        print("Ids must be whole numbers.")
        return

    topic = input("What are you planning to study together? ").strip()
    if not topic:
        print("Session topic cannot be empty.")
        return

    try:
        session = engine.record_session(s1_id=s1, s2_id=s2, topic=topic)
    except KeyError as exc:
        print(f"Error: {exc}")
        return

    idx = engine.list_sessions().index(session)
    print(f"Session saved with index {idx}.")
    print(session.summarize())
    print()


def rate_session(engine: MatchEngine) -> None:
    """Rate a partner for a given session index and add a note."""
    from src.models import Student  # imported here to avoid circular feel

    try:
        index = int(input("Which session index do you want to rate? ").strip())
    except ValueError:
        print("Session index must be a whole number.")
        return

    try:
        session = engine.get_session(index)
    except IndexError as exc:
        print(f"Error: {exc}")
        return

    print("Current session:")
    print(" ", session.summarize())
    print()

    note_text = input("Add a short note about the session (optional): ").strip()
    rating_text = input("Give your partner a rating from 1 to 5: ").strip()

    try:
        rating_value = int(rating_text)
    except ValueError:
        print("Rating must be a whole number from 1 to 5.")
        return

    try:
        if note_text:
            session.add_note(note_text)
        session.set_rating(rating_value)

        # For this simple version, student 2 is treated as the helper.
        helper_id = session.s2_id
        helper: Student = engine.get_student(helper_id)
        helper.add_rating(rating_value)
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}")
        return

    print("Thank you, your feedback has been recorded.")
    print("Updated helper info:")
    print(helper.profile_summary())
    print()


def search_helpers(engine: MatchEngine) -> None:
    """Search for helpers by subject name and minimum rating."""
    subject = input("Subject to search for (for example: Algebra): ").strip()
    rating_text = input("Minimum rating (0 for no filter): ").strip()

    try:
        min_rating = float(rating_text) if rating_text else 0.0
    except ValueError:
        min_rating = 0.0

    matches_found = False
    print("\nPossible helpers:")
    for student in engine.all_students():
        if student.can_help(subject) and student.rating_avg >= min_rating:
            print(" •", student.profile_summary())
            matches_found = True

    if not matches_found:
        print("No helpers match that filter yet.")
    print()


def list_students(engine: MatchEngine) -> None:
    """Print all student profiles currently in the system."""
    students = engine.all_students()
    if not students:
        print("No student profiles created yet.")
        return

    print("\nStudents:")
    for s in students:
        print(" •", s.profile_summary())
    print()


def list_sessions(engine: MatchEngine) -> None:
    """Print all recorded study sessions."""
    sessions = engine.list_sessions()
    if not sessions:
        print("No sessions have been recorded yet.")
        return

    print("\nStudy sessions:")
    for index, session in enumerate(sessions):
        print(f"[{index}] {session.summarize()}")
    print()


def main() -> None:
    """Run the basic text menu for the StudyLink program."""
    engine = MatchEngine()

    menu = """
StudyLink – Peer Study Matcher
-------------------------------
1) Create or edit my profile
2) See recommended partners
3) Log a new study session
4) Rate a partner for a session
5) Search for helpers by subject
6) List all students
7) List all sessions
0) Exit
"""

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_or_edit_profile(engine)
        elif choice == "2":
            show_matches(engine)
        elif choice == "3":
            start_session(engine)
        elif choice == "4":
            rate_session(engine)
        elif choice == "5":
            search_helpers(engine)
        elif choice == "6":
            list_students(engine)
        elif choice == "7":
            list_sessions(engine)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("That was not one of the options. Please try again.\n")


if __name__ == "__main__":
    main()
