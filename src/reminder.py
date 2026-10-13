from datetime import date

# Reminder for only one exam
class Reminder:
  
  def __init__(self, reminder_id: int, exam_id: int, days_before: int, sent: bool = False):
     self._reminder_id = reminder_id
     self._exam_id = exam_id
     self._days_before = days_before # How many days before the student wants the reminder
     self._sent = sent

  # Checks if today is the day to send reminder
  def is_due(self, today: date) -> bool:
    pass # Empty for now

  # Marks the reminder as sent so it doesnt send twice
  def mark_sent(self) -> None:
    pass # Empty for now
