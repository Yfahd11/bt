# src/matching.py
"""
Matching logic and simple strategy pattern implementation for StudyLink.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from .models import Student, StudySession


class MatchStrategy(ABC):
    """Interface for scoring how well two students match."""

    @abstractmethod
    def score_pair(self, seeker: Student, candidate: Student) -> int:
        """Return a non‑negative integer score for (seeker, candidate)."""
        raise NotImplementedError


class NeedsStrengthsOverlapStrategy(MatchStrategy):
    """
    Simple strategy that counts overlapping topics between
    the seeker's needs and the candidate's strengths.
    """

    def score_pair(self, seeker: Student, candidate: Student) -> int:
        needs = {n.lower() for n in seeker.needs}
        strengths = {s.lower() for s in candidate.strengths}
        return len(needs & strengths)


class MatchEngine:
    """Coordinates student profiles, matching, and session history."""

    def __init__(self, strategy: Optional[MatchStrategy] = None) -> None:
        self._students: Dict[int, Student] = {}
        self._sessions: List[StudySession] = []
        self._next_student_id: int = 1
        self.strategy: MatchStrategy = strategy or NeedsStrengthsOverlapStrategy()

    # --- student management ---

    def create_or_update_student(
        self,
        student_id: Optional[int],
        name: str,
        major: str,
        strengths: List[str],
        needs: List[str],
    ) -> Student:
        """Create a new student or update an existing one and return it."""
        cleaned_strengths = [s.strip() for s in strengths if s.strip()]
        cleaned_needs = [n.strip() for n in needs if n.strip()]

        if student_id is None:
            # create a new entry
            new_id = self._next_student_id
            self._next_student_id += 1
            student = Student(
                student_id=new_id,
                name=name.strip(),
                major=major.strip(),
                strengths=cleaned_strengths,
                needs=cleaned_needs,
            )
            self._students[new_id] = student
        else:
            # update existing
            if student_id not in self._students:
                raise KeyError(f"No student with id {student_id}")
            student = self._students[student_id]
            student._name = name.strip()
            student.major = major.strip()
            student.strengths = cleaned_strengths
            student.needs = cleaned_needs

        return student

    def get_student(self, student_id: int) -> Student:
        """Return the Student with the given id or raise KeyError."""
        if student_id not in self._students:
            raise KeyError(f"No student with id {student_id}")
        return self._students[student_id]

    def all_students(self) -> List[Student]:
        """Return a list of all stored Student objects."""
        return list(self._students.values())

    # --- matching ---

    def _score_candidates(self, seeker: Student) -> List[Tuple[Student, int]]:
        """Internal helper: score all candidates for a given seeker."""
        scored: List[Tuple[Student, int]] = []
        for candidate in self._students.values():
            if candidate.id == seeker.id:
                continue
            score = self.strategy.score_pair(seeker, candidate)
            if score > 0:
                scored.append((candidate, score))
        return scored

    def recommend_for(self, student_id: int, limit: int = 5) -> List[Student]:
        """Return up to 'limit' recommended partners for the given student."""
        seeker = self.get_student(student_id)
        scored = self._score_candidates(seeker)

        def _key(item: Tuple[Student, int]) -> Tuple[int, float]:
            candidate, score = item
            return (score, candidate.rating_avg)

        scored.sort(key=_key, reverse=True)
        if limit < 0:
            limit = 0
        return [c for c, _ in scored[:limit]]

    # --- sessions ---

    def record_session(self, s1_id: int, s2_id: int, topic: str) -> StudySession:
        """Create a new StudySession and store it."""
        # Make sure both ids exist
        self.get_student(s1_id)
        self.get_student(s2_id)

        session = StudySession(s1_id=s1_id, s2_id=s2_id, topic=topic.strip())
        self._sessions.append(session)
        return session

    def list_sessions(self) -> List[StudySession]:
        """Return a copy of the session list."""
        return list(self._sessions)

    def get_session(self, index: int) -> StudySession:
        """Return a specific session by index or raise IndexError."""
        if not 0 <= index < len(self._sessions):
            raise IndexError("Invalid session index.")
        return self._sessions[index]
