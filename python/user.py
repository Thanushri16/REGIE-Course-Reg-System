from abc import ABC, abstractmethod

# Abstract User Interface
class User(ABC):
    @abstractmethod
    def get_type(self):
        # Get the type of the user
        pass

    def __init__(self, id, name, address, mobile, email, password) -> None:
        self._id = id
        self._name = name
        self._address = address
        self._mobile = mobile
        self._email = email
        self._password = password

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_address(self) -> str:
        return self._address

    def get_mobile(self) -> int:
        return self._mobile

    def get_email(self) -> str:
        return self._email
    
    def modify_profile(self, name='', address='', mobile='', email='', password='', repassword = '') -> bool:
        # Function that lets the user to modify their profile
        flag = 0
        d = {}
        if len(name) > 0 and self._name != name:
            # No changes are to be made unless the new value is different from the old value and the new value is not empty
            self._name = name
            flag = 1
            d["name"] = name
        if len(address) > 0 and self._address != address:
            self._address = address
            flag = 1
            d["address"] = address
        if mobile and self._mobile != mobile:
            self._mobile = mobile
            flag = 1
            d["mobile"] = mobile
        if len(email) > 0 and self._email != email:
            self._email = email
            flag = 1
            d["email"] = email
        if len(password) > 0 and len(repassword) > 0:
            if password == repassword and self._password != password:
                self._password = password
                flag = 1
                d["password"] = password
            else:
                print("Passwords do not match")
                
        if flag: 
            print("Changes made to user profile")
        return d
