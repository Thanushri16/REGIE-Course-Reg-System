class Department:
    def __init__(self, dept_id, dept_name, division_id, division_name):
        self.__dept_id = dept_id
        self.__dept_name = dept_name
        self.__division_id = division_id
        self.__division_name = division_name

    def get_dept_id(self):
        return self.__dept_id

    def get_dept_name(self):
        return self.__dept_name

    def get_divison_name(self):
        return self.__division_name

    def get_division_id(self):
        return self.__division_id

    def set_dept_id(self, val):
        self.__dept_id = val

    def set_dept_name(self, val):
        self.__dept_name = val

    def set_division_id(self, val):
        self.__division_id = val

    def set_division_name(self, val):
        self.__division_name = val
        