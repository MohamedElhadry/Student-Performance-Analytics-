
import unittest
import numpy as np

from src.analytics import (
    calculate_statistics,
    calculate_student_averages,
    calculate_subject_averages,
    rank_students,
    calculate_pass_fail,
    get_student_status,
    detect_outliers
)


class TestStudentAnalytics(unittest.TestCase):

    def setUp(self):
        self.names = ["Ahmed", "Sara", "Omar"]

        self.scores = np.array([
            [80, 90, 85, 75],
            [95, 92, 98, 90],
            [40, 45, 50, 35]
        ], dtype=float)

    def test_statistics(self):
        stats = calculate_statistics(self.scores)

        self.assertAlmostEqual(stats["average"], np.mean(self.scores))
        self.assertAlmostEqual(stats["median"], np.median(self.scores))
        self.assertEqual(stats["highest"], 98)
        self.assertEqual(stats["lowest"], 35)

    def test_student_averages(self):
        averages = calculate_student_averages(self.scores)

        expected = np.array([82.5, 93.75, 42.5])
        np.testing.assert_array_almost_equal(averages, expected)

    def test_subject_averages(self):
        averages = calculate_subject_averages(self.scores)

        expected = np.array([71.67, 75.67, 77.67, 66.67])
        np.testing.assert_array_almost_equal(
            averages, expected, decimal=2
        )

    def test_ranking(self):
        ranking = rank_students(self.names, self.scores)

        self.assertEqual(ranking[0][0], "Sara")
        self.assertEqual(ranking[1][0], "Ahmed")
        self.assertEqual(ranking[2][0], "Omar")

    def test_pass_fail(self):
        passed, failed = calculate_pass_fail(self.scores)

        self.assertEqual(passed, 9)
        self.assertEqual(failed, 3)

    def test_student_status(self):
        self.assertEqual(get_student_status(75), "PASS")
        self.assertEqual(get_student_status(40), "FAIL")

    def test_outlier_detection(self):
        scores = np.array([10, 12, 13, 14, 15, 16, 100])

        outliers, lower, upper = detect_outliers(scores)

        self.assertIn(100, outliers)

    def test_outlier_boundaries(self):
        scores = np.array([10, 20, 30, 40, 50])

        outliers, lower, upper = detect_outliers(scores)

        self.assertEqual(len(outliers), 0)


if __name__ == "__main__":
    unittest.main()
