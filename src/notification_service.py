from datetime import date

# Checks reminders and sends them to the student
class NotificationService:

  # Runs when the service gets made
  def __init__(self, enabled: bool = True, last_checked: date = None):
    self._enabled = enabled
    self._last_checked = last_checked

  # Checks which reminders are due today
  def check_reminders(self, today: date) -> None:
    pass

  # Sends reminder message and returns True if sent, False if it didn't
  def send_notification(self, message: str) -> bool:
    pass
