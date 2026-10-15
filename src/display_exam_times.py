class DisplayExamTimes:

    def displayTimes(self, countdown):
        if countdown is None: 
            return "Exam has started or passed"
        
        return (
            f"{countdown['days']} days, "
            f"{countdown['hours']} hours, "
            f"{countdown['minutes']} minutes, "
            f"{countdown['seconds']} seconds remaining"
        )