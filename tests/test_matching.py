# tests/test_matching.py
"""Tests for the matching engine and strategy logic."""

import unittest

from src.matching import MatchEngine
from src.models import Student


class TestMatching(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MatchEngine()

        # Alice needs Math help and is strong in Python
        self.alice = self.engine.create_or_update_student(
            student_id=None,
            name="Alice",
            major="Computer Science",
            strengths=["Python"],
            needs=["Math"],
        )

        # Bob is strong in Math and needs Python help
        self.bob = self.engine.create_or_update_student(
            student_id=None,
            name="Bob",
            major="Mathematics",
            strengths=["Math"],
            needs=["Python"],
        )

        # Charlie is unrelated to Alice's needs
        self.charlie = self.engine.create_or_update_student(
            student_id=None,
            name="Charlie",
            major="Biology",
            strengths=["Biology"],
            needs=[],
        )

    def test_recommend_for_finds_bob(self) -> None:
        matches = self.engine.recommend_for(self.alice.id, limit=5)
        self.assertIn(self.bob, matches)
        self.assertNotIn(self.charlie, matches)

    def test_record_and_get_session(self) -> None:
        session = self.engine.record_session(self.alice.id, self.bob.id, "Limits")
        sessions = self.engine.list_sessions()
        self.assertIn(session, sessions)
        idx = sessions.index(session)
        fetched = self.engine.get_session(idx)
        self.assertEqual(fetched.topic, "Limits")


if __name__ == "__main__":
    unittest.main()
