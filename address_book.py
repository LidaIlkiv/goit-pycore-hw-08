from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
         super().__init__(value)

class Phone(Field):    
    def __init__(self, value):
        super().__init__(value)        
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError('Value error.It`s not a phone number.')

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
         self.phones.append(Phone(phone_number))
    
    def remove_phone(self, phone_number):
         for phone in self.phones:
              if str(phone) == phone_number:
                   self.phones.remove(phone)
              
    def edit_phone(self, phone_number, new_phone_number):
         for phone in self.phones:
              if str(phone) == phone_number:
                   self.phones[self.phones.index(phone)] = Phone(new_phone_number)
        

    def find_phone(self, phone_number):
         for phone in self.phones:
              if str(phone) == phone_number:
                   return phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)         
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
    
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthday = []
        now = datetime.today().date()        
        
        for record in self.data.values():
            if record.birthday and record.birthday.value:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()           
                next_birthday = birthday_date.replace(year=now.year)
                if 0 <= (next_birthday- now).days <= 7:                    
                    upcoming_birthday.append(record)                   
        return upcoming_birthday   
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:            
            return "Enter the correct arguments for the command"
        except KeyError:
            return "Key error"
        except IndexError:
            return "Index error"     

    return inner    


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    i = 0
    for arg in args:
        arg = arg.strip().lower()
        args[i] = arg
        i+=1
        
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)        
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact`s phone updated."
    if record is None:
        message = "Contact is not exist."       
    else:
        record.edit_phone(phone, new_phone)        
    return message

@input_error
def show_phone(args, book: AddressBook):
    
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact is not exist."  
    else:
        return f"Phones: {'; '.join(p.value for p in record.phones)}"

        

def show_all(book: AddressBook):
    return book



@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Contact`s birthday updated."
    if record is None:
        return "Contact is not exist."
    else:
        record.add_birthday(birthday)       
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact is not exist."  
    else:
        return f"Birthday: {record.birthday.value}"

    

@input_error
def birthdays(book:AddressBook):
    return book.get_upcoming_birthdays()

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


        

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
            
        elif command == "change":
            print(change_contact(args, book))
            
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")
    

if __name__ == "__main__":
    main()
    

    





     