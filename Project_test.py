import json
import os
import re
from datetime import datetime, timedelta

DATA_FILE = 'personal_assistant_data.json'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
else:
    data = {
        'contacts': [],
        'notes': []
    }

def save_data():
    
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


def add_contact(name, address, phone, email, birthday):
    contact = {
        'name': name,
        'address': address,
        'phone': phone,
        'email': email,
        'birthday': birthday
    }
    data['contacts'].append(contact)
    save_data()


def find_contacts_by_name(name):
    results = [contact for contact in data['contacts'] if name.lower() in contact['name'].lower()]
    return results


def upcoming_birthdays(days):
    today = datetime.now()
    upcoming_date = today + timedelta(days=days)
    upcoming_birthdays = [contact for contact in data['contacts'] if contact['birthday'].date() == upcoming_date.date()]
    return upcoming_birthdays

import re

def validate_phone_number(phone):
    
    pattern = r'^\+380\d{9}$'
    
    if re.match(pattern, phone):
        return True
    else:
        print("Неправильний формат введення номера телефону. Правильний формат: +380XXXXXXXXX")
        return False

def validate_email(email):
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        print("Неправильний формат введення email-адреси. Правильний формат: example@email.com")
        return False


def edit_contact(contact_idx, new_data):
    if 0 <= contact_idx < len(data['contacts']):
        data['contacts'][contact_idx].update(new_data)
        save_data()


def delete_contact(contact_idx):
    if 0 <= contact_idx < len(data['contacts']):
        del data['contacts'][contact_idx]
        save_data()


def add_note(text):
    note = {'text': text, 'tags': []}
    data['notes'].append(note)
    save_data()


def find_notes_by_tag(tag):
    results = [note for note in data['notes'] if tag in note['tags']]
    return results


def edit_note(note_idx, new_data):
    if 0 <= note_idx < len(data['notes']):
        data['notes'][note_idx].update(new_data)
        save_data()


def delete_note(note_idx):
    if 0 <= note_idx < len(data['notes']):
        del data['notes'][note_idx]
        save_data()

if __name__ == '__main__':
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
            if validate_phone_number(phone) and validate_email(email):
                add_contact(name, address, phone, email, datetime.strptime(birthday, '%Y-%m-%d'))
                print("Контакт додано.")
            else:
                print("Некоректний номер телефону або email.")
        
        elif choice == '2':
            name = input("Пошук за іменем: ")
            results = find_contacts_by_name(name)
            if results:
                for idx, contact in enumerate(results):
                    print(f"{idx+1}. {contact['name']} - {contact['phone']} - {contact['email']}")
            else:
                print("Контактів не знайдено.")
        
        elif choice == '3':
            days = int(input("Введіть кількість днів: "))
            upcoming = upcoming_birthdays(days)
            if upcoming:
                for contact in upcoming:
                    print(f"{contact['name']} - {contact['birthday'].strftime('%Y-%m-%d')}")
            else:
                print("Немає контактів з найближчими днями народження.")
        
        elif choice == '4':
            note = input("Текст нотатки: ")
            add_note(note)
            print("Нотатку додано.")
        
        elif choice == '5':
            tag = input("Пошук за тегом: ")
            results = find_notes_by_tag(tag)
            if results:
                for idx, note in enumerate(results):
                    print(f"{idx+1}. {note['text']}")
            else:
                print("Нотаток з вказаним тегом не знайдено.")
        
        elif choice == '6':
            break
