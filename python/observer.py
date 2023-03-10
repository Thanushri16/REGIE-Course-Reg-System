# This file contains the interface and the implementations of the observer class methods.
# The concrete observer implements the interface observer. It is called the Permission_Modifying_Observer
# that modifies the permission required variable in course sections based on the features variable. 
# When the feature is "Instructor Approval Required", then the observer gets updated and it keeps track of the permission
# variable. 

from abc import ABCMeta, abstractmethod

class Observer(metaclass = ABCMeta):
    @abstractmethod
    def update(self, statuscode):  
        # This is the status code upon which the update of the course section to faculty permission required depends on
        # If its 1, then the observer must update the course section to faculty permission required
        # If its 0, then the observer sets the course section to faculty permission not required
        pass

class Permission_Modifying_Observer(Observer):
    def __init__(self, course_section_id, con) -> None:
        self.course_section_id = course_section_id
        self.con = con  # The database connection is got as input

    def update(self, statuscode):
        try: 
            if statuscode:  # Course section requires Instructor Approval
                cursor = self.con.con.cursor()
                query = "update CourseSection set permission_required = 1 where course_section_id = %s"
                values = (self.course_section_id, )
                cursor.execute(query, values)
                self.con.con.commit()

            else:   # Course section does not require Instructor Approval
                cursor = self.con.con.cursor()
                query = "update CourseSection set permission_required = 0 where course_section_id = %s"
                values = (self.course_section_id, )
                cursor.execute(query, values)
                self.con.con.commit()

        except Exception as e:
            print(f"Error in the Permission Modifying Observer: {e}")
            return False

        return True