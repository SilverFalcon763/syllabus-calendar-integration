class Exam:
    """Represents an exam extracted from a syllabus."""

    def __init__(self, exam_id: int | None, course: str, title: str, date: str):
        self.exam_id = exam_id
        self.course = course
        self.title = title
        self.date = date

    def get_date(self) -> str:
        """Return the exam date in ISO format, such as 2026-11-01."""
        return self.date

    def get_details(self) -> str:
        """Return a readable description of the exam."""
        return f"Exam {self.exam_id}: {self.course} - {self.title} on {self.date}"

    def to_dict(self) -> dict:
        """Return the exam in the format already used by the Flask API."""
        return {
            "course": self.course,
            "title": self.title,
            "date": self.date,
        }
