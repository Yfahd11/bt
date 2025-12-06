# tests/test_models.py
"""Small tests for the Student and StudySession classes."""

import unittest

from src.models import Student, StudySession


class TestStudent(unittest.TestCase):
    def test_rating_average_is_updated_correctly(self) -> None:
        student = Student(1, "Test Student")
        student.add_rating(5)
        student.add_rating(3)
        self.assertEqual(student.rating_count, 2)
        self.assertAlmostEqual(student.rating_avg, 4.0)

    def test_invalid_rating_raises_value_error(self) -> None:
        student = Student(1, "Test Student")
        with self.assertRaises(ValueError):
            student.add_rating(0)


class TestStudySession(unittest.TestCase):
    def test_set_rating_stores_value(self) -> None:
        session = StudySession(1, 2, "Algebra review")
        session.set_rating(4)
        self.assertEqual(session.rating, 4)

    def test_invalid_session_rating_raises(self) -> None:
        session = StudySession(1, 2, "Algebra review")
        with self.assertRaises(ValueError):
            session.set_rating(10)


if __name__ == "__main__":
    unittest.main()
