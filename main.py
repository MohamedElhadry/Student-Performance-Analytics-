
from pathlib import Path
import csv

from src.analytics import (
    SUBJECTS,
    load_data,
    calculate_statistics,
    calculate_student_averages,
    calculate_subject_averages,
    rank_students,
    calculate_pass_fail,
    get_student_status,
    detect_outliers
)


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = PROJECT_DIR / "Data"

if not DATA_DIR.exists():
    DATA_DIR = PROJECT_DIR / "data"

CSV_FILE = DATA_DIR / "students.csv"


def create_sample_data():
    """Create a sample student dataset."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    students = [
        [1, "Ahmed", 85, 90, 95, 80],
        [2, "Sara", 92, 88, 96, 91],
        [3, "Omar", 65, 70, 75, 68],
        [4, "Mona", 78, 82, 85, 90],
        [5, "Ali", 45, 55, 60, 50],
        [6, "Nour", 98, 95, 99, 97],
        [7, "Youssef", 72, 68, 80, 75],
        [8, "Salma", 88, 92, 90, 94],
        [9, "Khaled", 55, 60, 58, 62],
        [10, "Farah", 81, 85, 89, 88],
        [11, "Amr", 67, 73, 70, 65],
        [12, "Laila", 94, 97, 93, 96]
    ]

    headers = ["student_id", "name"] + SUBJECTS

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(students)

    print("\nSample dataset created successfully!")


def print_section(title):
    print("\n" + "-" * 55)
    print(title)
    print("-" * 55)


def main():

    print("=" * 55)
    print("          STUDENT PERFORMANCE ANALYTICS")
    print("=" * 55)

    # Check dataset
    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
        print("\nDataset is missing or empty.")
        create_sample_data()

    # Load dataset
    try:
        names, scores = load_data(CSV_FILE)

    except ValueError as error:
        print(f"\nInvalid dataset: {error}")
        print("Replacing it with sample data...")

        # This replaces the existing CSV with sample data.
        create_sample_data()
        names, scores = load_data(CSV_FILE)

    print(f"\nDataset: {CSV_FILE}")
    print(f"Total Students: {len(names)}")
    print(f"Total Subjects: {len(SUBJECTS)}")

    # General statistics
    statistics = calculate_statistics(scores)

    print_section("GENERAL STATISTICS")

    for key, value in statistics.items():
        print(f"{key.replace('_', ' ').title():25}: {value:.2f}")

    # Student results
    averages = calculate_student_averages(scores)

    print_section("STUDENT RESULTS")

    for name, average in zip(names, averages):
        status = get_student_status(average)
        print(f"{name:15} Average: {average:6.2f} | {status}")

    # Student ranking
    ranking = rank_students(names, scores)

    print_section("STUDENT RANKING")

    for position, (name, average) in enumerate(ranking, start=1):
        print(f"{position:2}. {name:15} Average: {average:.2f}")

    # Subject analysis
    subject_averages = calculate_subject_averages(scores)

    print_section("SUBJECT ANALYSIS")

    for subject, average in zip(SUBJECTS, subject_averages):
        print(f"{subject:22}: {average:.2f}")

    # Pass and fail
    passed, failed = calculate_pass_fail(scores)

    print_section("PASS / FAIL ANALYSIS")

    print(f"Passed subject results: {passed}")
    print(f"Failed subject results: {failed}")

    # Outlier detection
    outliers, lower, upper = detect_outliers(scores)

    print_section("OUTLIER DETECTION")

    print(f"Lower Bound: {lower:.2f}")
    print(f"Upper Bound: {upper:.2f}")
    print(f"Detected Outliers: {outliers}")

    # Completion
    print("\n" + "=" * 55)
    print("             ANALYSIS COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        print(f"\nERROR: {error}")
