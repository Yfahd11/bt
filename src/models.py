# src/models.py
"""
Core data models used by the StudyLink program.

The file defines:
  * Profile  – a simple base class for user profiles
  * Student  – extends Profile, adds strengths/needs and ratings
  * StudySession – represents one session between two students
  * Availability – simple time slot container (optional / future use)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class Profile:
    """Base profile class used mainly to show inheritance and reuse."""

    def __init__(self, profile_id: int, name: str) -> None:
        self._id = profile_id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def profile_summary(self) -> str:
        """Return a short text description of the profile."""
        return f"{self._id}: {self._name}"


class Student(Profile):
    """Student profile with subjects and feedback rating."""

    def __init__(
        self,
        student_id: int,
        name: str,
        major: Optional[str] = None,
        strengths: Optional[List[str]] = None,
        needs: Optional[List[str]] = None,
    ) -> None:
        super().__init__(student_id, name)
        self.major = major or ""
        self.strengths: List[str] = strengths or []
        self.needs: List[str] = needs or []
        self.rating_avg: float = 0.0
        self.rating_count: int = 0

    # --- simple helper checks ---

    def can_help(self, topic: str) -> bool:
        """Return True if this student lists the topic as a strength."""
        topic = topic.strip().lower()
        return any(topic == s.lower() for s in self.strengths)

    def needs_help(self, topic: str) -> bool:
        """Return True if this student lists the topic as a need."""
        topic = topic.strip().lower()
        return any(topic == n.lower() for n in self.needs)

    # --- rating logic ---

    def add_rating(self, score: int) -> None:
        """Update the rolling average rating for this student.

        The rating is expected to be an integer from 1 to 5 inclusive.
        """
        if not 1 <= score <= 5:
            raise ValueError("Rating must be an integer between 1 and 5.")

        total_before = self.rating_avg * self.rating_count
        total_after = total_before + score
        self.rating_count += 1
        self.rating_avg = total_after / self.rating_count

    def profile_summary(self) -> str:  # type: ignore[override]
        """Extend the summary with major, strengths, needs and rating."""
        strengths_text = ", ".join(self.strengths) if self.strengths else "None"
        needs_text = ", ".join(self.needs) if self.needs else "None"
        rating_text = f"{self.rating_avg:.2f}" if self.rating_count else "N/A"

        return (
            f"Student #{self.id} - {self.name} "
            f"(Major: {self.major or 'N/A'}, "
            f"Rating: {rating_text}, "
            f"Strengths: {strengths_text}, "
            f"Needs: {needs_text})"
        )


@dataclass
class StudySession:
    """Representation of one study session between two students."""

    s1_id: int
    s2_id: int
    topic: str
    note: str = ""
    rating: Optional[int] = None  # rating of the helper

    def add_note(self, text: str) -> None:
        """Append a note about how the session went."""
        text = text.strip()
        if not text:
            return
        if self.note:
            self.note += "\n"
        self.note += text

    def set_rating(self, score: int) -> None:
        """Store a 1–5 rating for this session."""
        if not 1 <= score <= 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = score

    def summarize(self) -> str:
        """Return a one‑line description of the session."""
        if self.rating is None:
            rating_text = "Not rated yet"
        else:
            rating_text = str(self.rating)
        return (
            f"Session between {self.s1_id} and {self.s2_id} "
            f"about '{self.topic}' (rating: {rating_text})"
        )


@dataclass
class Availability:
    """Very simple availability representation using string slots.

    Example slots: "Mon 3‑5", "Tue 10‑12".
    In a future version this could be replaced by real date/time objects.
    """

    student_id: int
    slots: List[str] = field(default_factory=list)

    def is_compatible(self, other: "Availability") -> bool:
        """Return True if there is at least one common slot."""
        return any(slot in other.slots for slot in self.slots)
