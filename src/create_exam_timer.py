from datetime import datetime

class CreateExamTimer:

    def createTimer(self, exam, now=None):
        # Get the exam date
        exam_date = datetime.fromisoformat(exam.get_date())

        # Get the current date and time if one wasn't provided
        if now is None: 
            now = datetime.now()

        #Calculate the time remaining 
        time_remaining = exam_date - now

        # Get total seconds 
        total_seconds = int(time_remaining.total_seconds())

        # Checks if the exam has arrived or passed
        if total_seconds <= 0: 
            return None 
        
        # Convert the total seconds into days, hours, minutes, and seconds
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Return the countdown values in a dictionary
        return {
            "days": days,
            "hours": hours, 
            "minutes": minutes, 
            "seconds": seconds
        }