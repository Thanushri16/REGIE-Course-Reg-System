# This file lets the faculty add or remove features from course sections
# This file also involves the Observer class that observes if the feature is "Instructor Approval Required" and 
# makes changes accordingly to the Course Section database

from observer import *
from course_section import *

class Modify_Features: 
    def __init__(self, con, quarter, course_section_id, feature) -> None:
        self.con = con
        self._quarter = quarter
        self._course_section_id = course_section_id
        self._feature = feature
        self.observer = Permission_Modifying_Observer(self._course_section_id, self.con)


    def add_features(self, con, quarter = '', course_section_id = '', features = []):
        # This function adds a feature to the course section
        course_section = CourseSection()
        results = course_section.retrieve_course_section(con, quarter, course_section_id)
        if results:
            for feature in features:
                if feature in course_section.get_course_features():
                    print(f"Feature {feature} is already present in {course_section.get_course_id()}")
                    continue
                course_section.add_course_feature(feature)
                cursor = con.con.cursor()
                query = "insert into CourseFeatures (course_section_id, feature) values(%s,%s)"
                values = (course_section.get_course_section_id(), feature)
                cursor.execute(query, values)
                con.con.commit()
                if feature.lower() == "instructor approval required":
                    if self.observer.update(1):
                        print("Observer updated!")
                    else: 
                        print("Error in modifying permissions by observer!")
                print(f"Feature {feature} added to course section {course_section.get_course_section_id()}")
            return True

        else: 
            print("Course section does not exist!")
            return False
        

    def remove_features(self, con, quarter = '', course_section_id = '', features = []):
        # This function removes a feature from the course section
        course_section = CourseSection()
        results = course_section.retrieve_course_section(con, quarter, course_section_id)
        if results:
            for feature in features:
                if not feature in course_section.get_course_features():
                    print(f"Feature {feature} is not already present in {course_section.get_course_id()}")
                    continue
                course_section.delete_course_feature(feature)
                cursor = con.con.cursor()
                query = "delete from CourseFeatures where course_section_id = %s and feature = %s"
                values = (course_section.get_course_section_id(), feature)
                cursor.execute(query, values)
                con.con.commit()
                if feature.lower() == "instructor approval required":
                    if self.observer.update(0):
                        print("Observer updated!")
                    else: 
                        print("Error in modifying permissions by observer!")
                print(f"Feature {feature} deleted from course section {course_section.get_course_section_id()}")
            return True

        else: 
            print("Course section does not exist!")
            return False