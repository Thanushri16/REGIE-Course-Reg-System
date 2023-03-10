# This file is used to check if two schedules are compatible with one another
# If they are, then student can register for both the classes
# Else, student would have a timetable clash. 
from datetime import datetime, time

class Check_Compatibility:
    def __init__(self) -> None:
        self.result = False

    # Schedule 1 is already existing schedule and Schedule 2 is incoming schedule
    def execute(self, schedule1, schedule2):
        self.result = False
        if schedule1[0].lower() == schedule2[0].lower():  # Same day
            start_time1 = datetime.strptime(str(schedule1[1]), '%H:%M:%S').time()
            end_time1 = datetime.strptime(str(schedule1[2]), '%H:%M:%S').time()
            start_time2 = datetime.strptime(str(schedule2[1]), '%H:%M:%S').time()
            end_time2 = datetime.strptime(str(schedule2[2]), '%H:%M:%S').time()

            if start_time1 <= end_time2 and start_time2 <= end_time1:
                print("Schedules overlap!")
                self.result = True
            else: 
                self.result = False
        return self.result

