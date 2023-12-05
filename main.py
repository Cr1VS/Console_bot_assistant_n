from collections import UserDict
from datetime import datetime
import json

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
        self._Field__value = value
           
class Birthday(Field):  
    @Field.value.setter
    def value(self, value):
        try:
            self._Field__value = datetime.strptime(value, '%Y-%m-%d')
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
        phones_str = '\n'.join([f'    {p}' for p in self.phones])
        birthday_str = f"\n🎂 Birthday: {self.birthday.value.strftime('%Y-%m-%d')}" if self.birthday else ""
        return "👤 Contact name: {}\n📞 Phones:\n{}{}".format(self.name.value, phones_str, birthday_str)

    

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
                
    @staticmethod
    def serialize_record(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d')
        return obj.__dict__ if hasattr(obj, '__dict__') else obj
    
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            data = self.data.copy()
            for name, record in data.items():
                if record.birthday:
                    record.birthday = record.birthday.value.strftime('%Y-%m-%d')
                record.phones = [phone.value for phone in record.phones]
            json.dump(data, file, default=self.serialize_record, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for name, record_data in data.items():
                    birthday_data = record_data.get('birthday')
                    if birthday_data and isinstance(birthday_data, str):
                        birthday = birthday_data
                    else:
                        birthday = None
                    record = Record(name, birthday)
                    for phone_data in record_data.get('phones', []):
                        record.add_phone(phone_data)
                    self.add_record(record)
        except FileNotFoundError:
            print("Файл не найден.")

    def search(self, query):
        results = []
        for name, record in self.data.items():
            if query.lower() in name.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query in phone.value:
                        results.append(record)
                        break
        return results
    
def main():
    book = AddressBook()
    book.load_from_file("data.json")
    
    query = input("Enter search query: ")   
    search_results = book.search(query)

    if search_results:
        print("Search results:")
        for result in search_results:
            print(result)
    else:
        print("No matching records found.")
        
        
if __name__ == "__main__":
    main()










