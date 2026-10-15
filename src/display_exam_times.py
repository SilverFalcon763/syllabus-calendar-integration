# Create a class to format and display exam countdown times
class DisplayExamTimes:

      # Check if the countdown is unavailable because the exam has started or passed
    def displayTimes(self, countdown):
        if countdown is None: 
            return "Exam has started or passed"
        
        # Return the remaining days, hours, minutes, and seconds as a message
        return (
            f"{countdown['days']} days, "
            f"{countdown['hours']} hours, "
            f"{countdown['minutes']} minutes, "
            f"{countdown['seconds']} seconds remaining"
        )