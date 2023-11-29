from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
        
    @property    
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
        
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Invalid phone number")
        self.__value = value
           
class Birthday(Field):  
    @Field.value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date")
       
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None
        
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        now = datetime.now()
        next_birthday = datetime(now.year, self.birthday.value.month, self.birthday.value.day)
        if now > next_birthday:
            next_birthday = datetime(now.year + 1, self.birthday.value.month, self.birthday.value.day)
        print((next_birthday - now).days)
        return (next_birthday - now).days
    
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        phone = self.find_phone(old_phone_number)
        if phone is not None:
            phone.value = new_phone_number
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone_number):
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict): 
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)
    
    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += '---\nRecord {0}:\nName: {1}\n{2}\n'.format(counter+1, item, record)
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ""
                