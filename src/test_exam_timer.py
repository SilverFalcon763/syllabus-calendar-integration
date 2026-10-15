# Use pytest to test the exam countdown calculations

# Import datetime to set the current time for testing
from datetime import datetime

# Import the Exam and CreateExamTimer classes
from exam import Exam
from create_exam_timer import CreateExamTimer

# Test that the timer correctly calculates two days remaining
def test_two_days_remaining():
    
    # Create an object of the CreateExamTimer class
    timer = CreateExamTimer()

    #Set the current time
    now = datetime.fromisoformat("2026-11-01T09:00:00")

    # Create an exam scheduled two days later
    exam = Exam(
    exam_id=1,
    course="CS 210",
    title="Data Structures Midterm",
    date="2026-11-03T09:00:00",)

    #Calculate the time remaining until the exam
    result = timer.createTimer(exam, now)

    # Check that the result is exactly two days
    assert result == {
        "days": 2,
        "hours": 0,
        "minutes": 0,
        "seconds": 0
    }

# Test that the timer correctly calculates two days remaining
def test_hours_minutes_seconds():
    
    # Create an object of the CreateExamTimer class
    timer = CreateExamTimer()

    #Set the current time
    now = datetime.fromisoformat("2026-11-01T09:00:00")

     # Create an exam scheduled 2 hours, 30 minutes, and 45 seconds later
    exam = Exam(
    exam_id=1,
    course="CS 210",
    title="Data Structures Midterm",
    date="2026-11-01T11:30:45",)

    #Calculate the time remaining until the exam
    result = timer.createTimer(exam, now)

    # Check that the result is exactly two days
    assert result == {
        "days": 0,
        "hours": 2,
        "minutes": 30,
        "seconds": 45
    }

# Test that the timer correctly calculates two days remaining
def test_exam_in_past():
    
    # Create an object of the CreateExamTimer class
    timer = CreateExamTimer()

    #Set the current time
    now = datetime.fromisoformat("2026-11-01T09:00:00")

     # Create an exam scheduled for the previous day
    exam = Exam(
    exam_id=1,
    course="CS 210",
    title="Data Structures Midterm",
    date="2026-10-31T09:00:00",)

    #Calculate the time remaining until the exam
    result = timer.createTimer(exam, now)

    # Check that the result is exactly two days
    assert result is None