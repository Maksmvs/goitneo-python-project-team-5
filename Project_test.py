import json
import os
import re
from datetime import datetime, timedelta

DATA_FILE = 'personal_assistant_data.json'

class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

class PersonalAssistant:
    def __init__(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {
                'contacts': [],
                'notes': []
            }

    def save_data(self):
        with open(DATA_FILE, 'w') as file:
            json.dump(self.data, file)

    def add_contact(self, name, address, phone, email, birthday):
        contact = {
            'name': name,
            'address': address,
            'phone': phone,
            'email': email,
            'birthday': birthday.strftime('%Y-%m-%d')
        }
        self.data['contacts'].append(contact)
        self.save_data()

    def find_contacts_by_name(self, name):
        results = [contact for contact in self.data['contacts'] if name.lower() in contact['name'].lower()]
        return results

    def upcoming_birthdays(self, days):
        today = datetime.now()
        upcoming_date = today + timedelta(days=days)
        upcoming_birthdays = [contact for contact in self.data['contacts'] if datetime.strptime(contact['birthday'], '%Y-%m-%d').date() == upcoming_date.date()]
        return upcoming_birthdays

    @staticmethod
    def validate_phone_number(phone):
        pattern = r'^\+380\d{9}$'
        if re.match(pattern, phone):
            return True
        else:
            print("Неправильний формат введення номера телефону. Правильний формат: +380XXXXXXXXX")
            return False

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            print("Неправильний формат введення email-адреси. Правильний формат: example@email.com")
            return False

    def edit_contact(self, contact_idx, new_data):
        if 0 <= contact_idx < len(self.data['contacts']):
            self.data['contacts'][contact_idx].update(new_data)
            self.save_data()

    def delete_contact(self, contact_idx):
        if 0 <= contact_idx < len(self.data['contacts']):
            del self.data['contacts'][contact_idx]
            self.save_data()

    def add_note(self, text, tags):
        note = {'text': text, 'tags': tags}
        self.data['notes'].append(note)
        self.save_data()

    def find_notes_by_tag(self, tag):
        results = [note for note in self.data['notes'] if tag in note['tags']]
        return results

    def edit_note(self, note_idx, new_data):
        if 0 <= note_idx < len(self.data['notes']):
            self.data['notes'][note_idx].update(new_data)
            self.save_data()

    def delete_note(self, note_idx):
        if 0 <= note_idx < len(self.data['notes']):
            del self.data['notes'][note_idx]
            self.save_data()

if __name__ == '__main__':
    personal_assistant = PersonalAssistant()

    while True:
        print("1. Додати контакт")
        print("2. Пошук контактів за іменем")
        print("3. Вивести контакти з найближчими днями народження")
        print("4. Додати нотатку")
        print("5. Пошук нотаток за тегом")
        print("6. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == '1':
            name = input("Ім'я: ")
            address = input("Адреса: ")
            phone = input("Номер телефону: ")
            email = input("Email: ")
            birthday = input("Дата народження (рррр-мм-дд): ")
            if personal_assistant.validate_phone_number(phone) and personal_assistant.validate_email(email):
                personal_assistant.add_contact(name, address, phone, email, datetime.strptime(birthday, '%Y-%m-%d'))
                print("Контакт додано.")
            else:
                print("Некоректний номер телефону або email.")
        
        elif choice == '2':
            name = input("Пошук за іменем: ")
            results = personal_assistant.find_contacts_by_name(name)
            if results:
                for idx, contact in enumerate(results):
                    print(f"{idx+1}. {contact['name']} - {contact['phone']} - {contact['email']}")
            else:
                print("Контактів не знайдено.")
        
        elif choice == '3':
            days = int(input("Введіть кількість днів: "))
            upcoming = personal_assistant.upcoming_birthdays(days)
            if upcoming:
                for contact in upcoming:
                    print(f"{contact['name']} - {contact['birthday'].strftime('%Y-%m-%d')}")
            else:
                print("Немає контактів з найближчими днями народження.")
        
        elif choice == '4':
            note = input("Текст нотатки: ")
            tags = input("Теги (розділені комами): ").split(',')
            personal_assistant.add_note(note, tags)
            print("Нотатку додано.")
        
        elif choice == '5':
            tag = input("Пошук за тегом: ")
            results = personal_assistant.find_notes_by_tag(tag)
            if results:
                for idx, note in enumerate(results):
                    print(f"{idx+1}. {note['text']}")
            else:
                print("Нотаток з вказаним тегом не знайдено.")
        
        elif choice == '6':
            break
