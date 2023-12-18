from abc import ABC, abstractmethod
from AddressBook import AddressBook, Record


class UserInteraction(ABC):
    @abstractmethod
    def get_input(self, prompt):
        pass

    @abstractmethod
    def display_output(self, output):
        pass


class ConsoleInteraction(UserInteraction):
    def get_input(self, prompt):
        return input(prompt)

    def display_output(self, output):
        print(output)


class Bot:
    def __init__(self, interaction):
        self.book = AddressBook()
        self.interaction = interaction

    def handle(self, action):
        if action == "add":
            name = self.interaction.get_input("Name: ").strip()
            phones = self.interaction.get_input("Phones: ")
            birth = self.interaction.get_input("Birthday (dd/mm/YYYY): ")
            email = self.interaction.get_input("Email: ").strip()
            status = self.interaction.get_input(
                "Status (family, friend, work): "
            ).strip()
            note = self.interaction.get_input("Note: ")
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)
        elif action == "search":
            self.interaction.display_output(
                "There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote"
            )
            category = self.interaction.get_input("search category: ")
            pattern = self.interaction.get_input("Search pattern: ")
            result = self.book.search(pattern, category)
            for account in result:
                if account["birthday"]:
                    birth = account["birthday"].strftime("%d/%m/%Y")
                    result_output = (
                        "_" * 50
                        + "\n"
                        + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"
                        + "_" * 50
                    )
                    self.interaction.display_output(result_output)
        elif action == "edit":
            contact_name = self.interaction.get_input("Contact name: ")
            parameter = self.interaction.get_input(
                "Which parameter to edit(name, phones, birthday, status, email, note): "
            ).strip()
            new_value = self.interaction.get_input("New Value: ")
            return self.book.edit(contact_name, parameter, new_value)
        elif action == "remove":
            pattern = self.interaction.get_input("Remove (contact name or phone): ")
            return self.book.remove(pattern)
        elif action == "save":
            file_name = self.interaction.get_input("File name: ")
            return self.book.save(file_name)
        elif action == "load":
            file_name = self.interaction.get_input("File name: ")
            return self.book.load(file_name)
        elif action == "congratulate":
            self.interaction.display_output(self.book.congratulate())
        elif action == "view":
            self.interaction.display_output(str(self.book))
        elif action == "exit":
            pass
        else:
            self.interaction.display_output("There is no such command!")


console_interaction = ConsoleInteraction()
