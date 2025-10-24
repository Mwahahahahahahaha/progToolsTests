import json
import re
import os
import phonenumbers # pip install phonenumbers

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    input("Press Enter to continue...")

def is_valid_number(number):
    try:
        parsed_number = phonenumbers.parse(number, "PH")
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False

def is_valid_name(name):
    return bool(re.match(r"^[a-zA-Z\s'-]+$", name)) and len(name) >= 2

def is_valid_address(address):
    return bool(re.match(r'^[a-zA-Z0-9\s,.\'-]+$', address)) and len(address) >= 2

def format_phone_number(number):
    return number.replace(" ", "").replace("-", "")

class PhoneBookRecord:
    def __init__(self, id, name, number, address):
        self.id = id
        self.name = name
        self.number = format_phone_number(number)
        self.address = address

    def to_dict(self):
        return {"id": self.id, "name": self.name, "number": self.number, "address": self.address}

    @staticmethod
    def from_dict(data):
        return PhoneBookRecord(
            id=data["id"],
            name=data["name"],
            number=data["number"],
            address=data["address"]
        )

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Number: {self.number}, Address: {self.address}"

class FileIO:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as f:
                json.dump([], f)

    def load(self):
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
                return [PhoneBookRecord.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            print("Continuing with an empty phone book.")
            return []

    def save(self, data):
        try:
            with open(self.file_name, 'w') as f:
                json.dump([item.to_dict() for item in data], f)
        except IOError as e:
            print(f"Error saving data: {e}")

class DataManager:
    def __init__(self):
        self.record_list = []
        self.highest_id = 0

    def populate(self, data):
        global highest_id
        self.record_list = data
        highest_id = max(log.id for log in self.record_list) if self.record_list else 0

    def add_record(self, name, number, address):
        record = PhoneBookRecord(self.highest_id + 1, name, number, address)
        self.record_list.append(record)
        self.highest_id += 1

    def delete_record(self, record):
        self.record_list.remove(record)

    def print_all_records(self):
        if not self.record_list:
            print("No records found.")
        else:
            for record in self.record_list:
                print(record)

    def is_number_duplicate(self, number):
        return any(record.number == number for record in self.record_list)


def main():
    file_io = FileIO('database.json')
    data_manager = DataManager()
    is_running = True
    data_manager.populate(file_io.load())

    def search_record():
        print("[1] - ID")
        print("[2] - Number")
        choice = input("Search by: ")
        match choice:
            case "1":
                field = "id"
            case "2":
                field = "number"
            case _:
                print("Invalid choice")
                return None

        value = input(f"Enter {field}: ").strip()
        if field == "id":
            try:
                value = int(value)
            except ValueError:
                print("Invalid ID. Please enter a numeric value")
                return None
        else:
            value = format_phone_number(value)

        for record in data_manager.record_list:
            if getattr(record, field) == value:
                return record
        return None

    while is_running:
        try:
            clear_console()
            print("========PHONEBOOK========")
            print("[1] - Create")
            print("[2] - Search")
            print("[3] - Update")
            print("[4] - Delete")
            print("[5] - Print All")
            print("[6] - Exit")
            choice = input("Enter your choice: ")

            match choice:
                case "1":
                    clear_console()
                    print("========CREATE RECORD========")
                    name = input("Name: ").strip()
                    if not is_valid_name(name):
                        print("Invalid name")
                        pause()
                        continue

                    number = input("Number: ").strip()
                    if not is_valid_number(number) or data_manager.is_number_duplicate(format_phone_number(number)):
                        print("Invalid number")
                        pause()
                        continue

                    address = input("Address: ").strip()
                    if not is_valid_address(address):
                        print("Invalid address")
                        pause()
                        continue

                    data_manager.add_record(name, format_phone_number(number), address)
                    print("Record created successfully!")
                    pause()
                case "2":
                    clear_console()
                    print("========SEARCH RECORD========")
                    record = search_record()
                    print("=============================")
                    if record:
                        print(record)
                    else:
                        print("Record not found")
                    pause()
                    continue
                case "3":
                    clear_console()
                    print("========UPDATE RECORD========")
                    record = search_record()
                    if record:
                        print("[1] - Name")
                        print("[2] - Number")
                        print("[3] - Address")
                        update_choice = input("Enter: ")
                        match update_choice:
                            case "1":
                                name = input("New Name: ").strip()
                                is_valid = is_valid_name(name)
                                if is_valid:
                                    record.name = name
                                    print("Name updated successfully")
                                else:
                                    print("Invalid name")
                                    pause()
                            case "2":
                                number = input("New Number: ").strip()
                                is_valid = is_valid_number(number) and not data_manager.is_number_duplicate(number)
                                if is_valid:
                                    record.number = format_phone_number(number)
                                    print("Number updated successfully")
                                else:
                                    print("Invalid number")
                                    pause()
                            case "3":
                                address = input("New Address: ").strip()
                                is_valid = is_valid_address(address)
                                if is_valid:
                                    record.address = address
                                    print("Address updated successfully")
                                else:
                                    print("Invalid address")
                                    pause()
                    else:
                        print("Record not found.")
                        pause()
                        continue
                case "4":
                    clear_console()
                    print("========DELETE RECORD========")
                    record = search_record()
                    if record:
                        print("Are you sure you want to delete this record?")
                        print(record)
                        print("=============================")
                        confirmation = input("Enter 'y' to confirm: ").strip().lower()
                        if confirmation == "y":
                            data_manager.record_list.remove(record)
                            print("=============================")
                            print("Record deleted.")
                        else:
                            print("Deletion cancelled.")
                        pause()
                    else:
                        print("=============================")
                        print("Record not found.")
                        pause()
                        continue
                case "5":
                    clear_console()
                    print("========ALL RECORDS========")
                    data_manager.print_all_records()
                    pause()
                case "6":
                    print("Exiting the program...")
                    is_running = False
                case _:
                    print("Invalid choice. Please try again.")
                    pause()
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            is_running = False
    file_io.save(data_manager.record_list)

main()
