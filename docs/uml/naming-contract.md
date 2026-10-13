# Naming Contract

Classes used by more than one slice. Only the owner writes the code stub for that class. Everyone else uses it with these exact names.

| Class           | Owner   | Used By                      |
|-----------------|---------|------------------------------|
| Exam            | Rory    | Rory, Ubay, Deandre, Gabe    |
| Student         | Gabe    | Rory, Ubay, Deandre, Gabe    |
| GoogleCalendarService | Rory | Rory, Deandre             |

## Exam attributes
- exam_id: int
- course: str
- title: str
- date: date
- get_date(): date
- get_details(): dict
- update_details(title: str, date: date): bool
- delete(): bool

## Student attributes
- student_id: int
- email: str
- get_exams(): list

## GoogleCalendarService attributes
- calendar_id: str
- access_token: str
- email: str
- authorize_user()
- add_exam(exam: Exam)
- sync_exam(exam: Exam): bool
- remove_exam(exam: Exam): bool

## Rules
- If you need a shared class that is not on this list, add it here and tell the team the same day.
