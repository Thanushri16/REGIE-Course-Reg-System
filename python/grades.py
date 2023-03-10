# Simple Grade class that contains the allowed grades
class Grades:
    def __init__(self) -> None:
        self.__grades = ["A","B","C","D","F","P","I"," "]
        self.__gpa_point_scale = {
            "A": 4,
            "B": 3.5,
            "C": 3,
            "D": 2.5,
            "F": 2,
            "P": 1.5,
            "I": 1,
            " ": 0
        }

    def get_gpa_point_scale(self):
        return self.__gpa_point_scale

    def get_acceptable_grades(self):
        return self.__grades