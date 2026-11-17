
import csv
import numpy as np


SUBJECTS = ["math", "physics", "computer_science", "english"]
PASS_MARK = 50


def load_data(file_path):
    """Load and validate student data from a CSV file."""

    names = []
    scores = []

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:

        sample = file.read(4096)
        file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(file, dialect=dialect)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")

        # Normalize column names
        reader.fieldnames = [
            column.strip().lower() for column in reader.fieldnames
        ]

        required_columns = ["name"] + SUBJECTS

        missing_columns = [
            column for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}. "
                f"Found columns: {reader.fieldnames}"
            )

        for row_number, row in enumerate(reader, start=2):

            name = (row.get("name") or "").strip()

            if not name:
                raise ValueError(
                    f"Missing student name at row {row_number}."
                )

            student_scores = []

            for subject in SUBJECTS:

                value = (row.get(subject) or "").strip()

                if not value:
                    raise ValueError(
                        f"Missing {subject} score for {name}."
                    )

                try:
                    score = float(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid {subject} score for {name}: {value}"
                    )

                if not 0 <= score <= 100:
                    raise ValueError(
                        f"{subject} score for {name} must be between 0 and 100."
                    )

                student_scores.append(score)

            names.append(name)
            scores.append(student_scores)

    if not scores:
        raise ValueError("No student records found in CSV file.")

    return names, np.array(scores, dtype=float)


def calculate_statistics(scores):
    """Calculate general statistics."""

    return {
        "average": np.mean(scores),
        "median": np.median(scores),
        "highest": np.max(scores),
        "lowest": np.min(scores),
        "standard_deviation": np.std(scores)
    }


def calculate_student_averages(scores):
    """Calculate each student's average."""

    return np.mean(scores, axis=1)


def calculate_subject_averages(scores):
    """Calculate each subject's average."""

    return np.mean(scores, axis=0)


def rank_students(names, scores):
    """Rank students from highest to lowest."""

    averages = calculate_student_averages(scores)
    indices = np.argsort(averages)[::-1]

    return [
        (names[i], averages[i])
        for i in indices
    ]


def calculate_pass_fail(scores):
    """Count passed and failed subject results."""

    passed = np.sum(scores >= PASS_MARK)
    failed = scores.size - passed

    return int(passed), int(failed)


def get_student_status(average):
    """Determine student status."""

    return "PASS" if average >= PASS_MARK else "FAIL"


def detect_outliers(scores):
    """Detect outliers using the IQR method."""

    q1 = np.percentile(scores, 25)
    q3 = np.percentile(scores, 75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = scores[
        (scores < lower_bound) | (scores > upper_bound)
    ]

    return outliers, lower_bound, upper_bound
