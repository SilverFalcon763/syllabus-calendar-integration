# Syncs exam changes to the student's Google Calendar
class GoogleCalendarService:

    def __init__(self, calendar_id: str, email: str):
        self._calendar_id = calendar_id
        self._email = email

    # Updates the calendar event for an edited exam
    def sync_exam(self, exam: "Exam") -> bool:
        pass

    # Removes the calendar event for a deleted exam
    def remove_exam(self, exam: "Exam") -> bool:
        pass