from collections import UserDict, OrderedDict
from datetime import datetime
from typing import Union
import re


def _now():
    return datetime.today().date()


def _create_date(*, year, month, day):
    return datetime(year=year, month=month, day=day).date()


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # @classmethod
    # def create_field(cls, value):
    #     field = cls(value=value)
    #     return str(field)


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, num):
        # self._value = num
        number = ''
        for n in num:
            try:
                n = int(n)
                number += str(n)

            except ValueError:
                None
        if len(number) == 12 and number[0:3] == '380':
            self._value = number
        elif len(number) == 10 and number[0] == '0':
            self._value = f'38{number}'
        elif len(number) == 11 and number[0:2] == '80':
            self._value = f'3{number}'
        else:
            print('Number is not validate')
            self._value = ''


class Birthday(Field):

    @property
    def value(self) -> datetime.date:
        return self._value

    @value.setter
    def value(self, value):

        if value is None:
            return None
        else:
            try:
                self._value = datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                print('Birthday format must be 00-00-000')
                return None

    def __repr__(self):
        return datetime.strftime(self._value, "%d-%m-%Y")


class AddressBook(UserDict):

    limit = 5
    offset = 0

    def __next__(self):
        self.addresses = list(self.data.items())
        end_value = self.offset + self.limit
        page = self.addresses[self.offset:end_value]
        self.offset = end_value
        if self.offset > len(self.addresses):
            page = self.addresses[end_value -
                                  self.limit:len(self.addresses)+1]

        if page == []:
            print('No more addresses')

        return page

    def __repr__(self):
        string = ''
        for name, other_data in self.data.items():
            string = string + f"{name} : {other_data}\n"
        return string

    def add_contact(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        contact = Record(name=name, phone=phone, birthday=birthday)
        self.data[name.value] = contact

    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    # def find_by_name(self, name):
    #     try:
    #         return self.data[name]
    #     except KeyError:
    #         return None

    # def find_by_phone(self, phone: str):
    #     for record in self.data.values():  # type:Record
    #         if phone in [number.value for number in record.phones]:
    #             return record
    #         return None


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def __repr__(self):
        if self.birthday == None or self.birthday.value == None:
            return f'{self.name.value.capitalize()} : {" ".join(phone.value for phone in self.phones)}'
        return f'{self.name.value.capitalize()}: {" ".join(phone.value for phone in self.phones)} : {self.birthday.value.date()}'

    def days_to_birthday(self):
        now = _now()
        if self.birthday is not None:
            birthday: datetime = self.birthday.value.date()
            next_birthday = _create_date(
                year=now.year, month=birthday.month, day=birthday.day)
            if now > next_birthday:
                next_birthday = _create_date(
                    year=next_birthday.year + 1, month=next_birthday.month, day=next_birthday.day)
            print(f'{(next_birthday-now).days} days')
            return (next_birthday-now).days
        return None

    def add_phone(self, phone_number: Phone):
        self.phones.append(phone_number)

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def change_phone(self, old_number: str, new_number: Phone):
        try:
            # self.phones.append(old_number)
            # self.phones.append(new_number)
            for ph in self.phones:
                if ph.value == old_number:
                    self.phones.remove(ph)
                else:
                    print(f'Phone {old_number} does not exists')
                self.phones.append(new_number)
        except ValueError:
            print(f'{old_number} does not exists')

    def delete_phone(self, phone: Phone):

        # try:
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
            else:
                print(f'Number {phone} does not exists')

        # except ValueError:
        #     print(f'{phone} does not exists')
