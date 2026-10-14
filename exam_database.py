import sqlite3

from .exam import Exam


class ExamDatabase:
    """Stores and retrieves Exam objects using SQLite."""

    def __init__(self, database_name: str = "events.db"):
        self.database_name = database_name
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)

    def _create_table(self) -> None:
        """Create the existing three-column table if it does not exist."""
        with self._connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    course TEXT NOT NULL,
                    title TEXT NOT NULL,
                    date TEXT NOT NULL
                )
                """
            )

    def save_exam(self, exam: Exam) -> Exam:
        """Save an exam and return it with its database id assigned."""
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO events (course, title, date) VALUES (?, ?, ?)",
                (exam.course, exam.title, exam.date),
            )
            exam.exam_id = cursor.lastrowid
        return exam

    def get_exams(self) -> list[Exam]:
        """Return every stored exam."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT rowid, course, title, date FROM events ORDER BY rowid"
            ).fetchall()

        return [
            Exam(exam_id=row[0], course=row[1], title=row[2], date=row[3])
            for row in rows
        ]
