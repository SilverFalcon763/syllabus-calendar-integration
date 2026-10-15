# Import the Exam, CreateExamTimer, and DisplayExamTimes classes
from exam import Exam
from create_exam_timer import CreateExamTimer
from display_exam_times import DisplayExamTimes

# Create an exam
exam = Exam(
    exam_id=1,
    course="CS 210",
    title="Data Structures Midterm",
    date="2026-11-01T09:00:00"
)

# Create the timer and display objects
timer = CreateExamTimer()
display = DisplayExamTimes()

# Calculate and display the countdown
countdown = timer.createTimer(exam)
result = display.displayTimes(countdown)

# Check that the display returns a string
assert isinstance(result, str)

# Check that the display returns a string
print("Test passed!")

print(result)